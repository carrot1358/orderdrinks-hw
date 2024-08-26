#!/usr/bin/python3
import logging
import cv2
import time
from config import config
from utils.detection_utils import create_detection_handler
from utils.websocket_utils import create_websocket_handler
from utils.gps_utils import GPS
import requests
import numpy as np
import json

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

def test_detection(detection_handler, ws_handler):
    # ตรวจจับด้วยรูปภาพทดสอบ
    image_path = "./image/test_image/Test_image.jpg"
    image = cv2.imread(image_path)
    detection_handler.Detect_test(image)

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
        test_detection(detection_handler, ws_handler)
    else:
        logging.info("เริ่ม GPS")
        gps.start()
        time.sleep(3)
        logging.info("เริ่มทำงานโปรแกรมหลัก")
        run_detection_loop(detection_handler, ws_handler)
           
if __name__ == "__main__":
    main()