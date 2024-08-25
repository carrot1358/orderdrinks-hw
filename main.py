#!/usr/bin/python3
import logging
import cv2
import base64
from io import BytesIO
from config import config
import sys
import os
from utils.detection_utils import create_detection_handler
from utils.websocket_utils import create_websocket_handler
from utils.gps_utils import GPS
import json
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_detection_loop(detection_handler, ws_handler, detection_callback):
    """
    ทำงานในลูปหลักของการตรวจจับ

    Args:
        detection_handler: ออบเจ็กต์ DetectionHandler
        ws_handler: ตัวจัดการ WebSocket
        detection_callback: ฟังก์ชันสำหรับการตรวจจับ
    """
    while True:
        try:
            if ws_handler:
                message = ws_handler.handle_message(detection_callback)
                if message:
                    logging.info(f"Received message2: {message}")
                    try:
                        data = json.loads(message)
                        if data.get('message') == 'need_bottle' and 'orderId' in data:
                            order_id = data['orderId']
                            logging.info(f"Detection order_id: {order_id}")
                            result = detection_callback(order_id)
                            if result:
                                ws_handler.send_detection_result(result)
                    except json.JSONDecodeError:
                        logging.error("ไม่สามารถแปลงข้อความเป็น JSON ได้")
                    except Exception as e:
                        logging.error(f"เกิดข้อผิดพลาดในการประมวลผลข้อความ: {e}")
                else:
                    logging.info("ไม่ได้รับข้อความจาก WebSocket")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except Exception as e:
            logging.error(f"เกิดข้อผิดพลาดในลูปการตรวจจับ: {e}")

    cv2.destroyAllWindows()

def main():
    """
    ฟังก์ชันหลักสำหรับการทำงานของระบบตรวจจับและการสื่อสาร
    """
    detection_handler = create_detection_handler()
    ws_handler = create_websocket_handler()
    ws_handler.start()

    def detection_callback(order_id):
        return detection_handler.perform_detection(order_id)

    if config.test_model:
        pass
    else:
        gps = GPS(ws_handler)
        gps.start()
        time.sleep(5)
        logging.info("โปรแกรมหลักทำงานต่อหลังจากเริ่ม GPS")
        
        run_detection_loop(detection_handler, ws_handler, detection_callback)
           
if __name__ == "__main__":
    main()