#!/usr/bin/python3
import logging
import cv2
import time
from config import config
from utils.detection_utils import create_detection_handler
from utils.websocket_utils import create_websocket_handler
from utils.gps_utils import GPS
from picamera2 import Picamera2
import requests
import numpy as np
import json
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_detection_loop(detection_handler, ws_handler):
    """
    ทำงานในลูปหลักของการตรวจจับ

    Args:
        detection_handler: ออบเจ็กต์ DetectionHandler
        ws_handler: ตัวจัดการ WebSocket
    """
    while True:
        try:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except Exception as e:
            logging.info(f"เกิดข้อผิดพลาดในลูปการตรวจจับ: {e}")

    cv2.destroyAllWindows()

def test_detection(detection_handler, ws_handler, capture_from_camera=False):
    if not capture_from_camera:
        image_path = "./image/test_image/Test_image.jpg"
        image = cv2.imread(image_path)
    else:
        image = detection_handler.get_image()
    
    # ทำการตรวจจับและรับผลลัพธ์
    result = detection_handler.perform_detection(image=image)
    if result:
        # ส่งข้อมูลไปยัง WebSocket
        ws_handler.send_bottle_result(result, sendto="both")
        
        # แสดงผลลัพธ์
        logging.info(f"ผลการตรวจจับ: จำนวนขวด {result['bottle_count']}")
        logging.info(f"ผลการตรวจจับ: จำนวนขวดที่มีน้ำ {result['has_water']}")
        logging.info(f"ผลการตรวจจับ: จำนวนขวดที่ไม่มีน้ำ {result['no_water']}")
    else:
        logging.error("ไม่สามารถทำการตรวจจับได้")

    # แสดงภาพผลลัพธ์ (ถ้ามี)
    output_image_path = 'image/output/output_marked.png'
    if os.path.exists(output_image_path):
        output_image = cv2.imread(output_image_path)
        cv2.imshow("ผลการตรวจจับ", output_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def main():
    """
    ฟังก์ชันหลักสำหรับการทำงานของระบบตรวจจับและการสื่อสาร
    """
    detection_handler = create_detection_handler()
    gps = GPS()
    ws_handler = create_websocket_handler(detection_handler, gps)
    ws_handler.start()

    if config.test_model:
        logging.info("ทำการตรวจจับด้วยรูปภาพทดสอบ")
        test_detection(detection_handler, ws_handler, config.test_camera)
    else:
        logging.info("เริ่ม GPS")
        gps.start()
        time.sleep(3)
        logging.info("เริ่มทำงานโปรแกรมหลัก")
        run_detection_loop(detection_handler, ws_handler)
           
if __name__ == "__main__":
    main()