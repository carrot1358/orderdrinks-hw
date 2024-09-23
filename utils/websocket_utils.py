import json
import threading
import time
from datetime import datetime
import websocket
from config import config
import logging

class WebSocketHandler:
    def __init__(self, detection_handler, gps):
        self.url = f"{config.websocket_url}/{config.device_id}"
        self.ws = None
        self.detection_handler = detection_handler
        self.gps = gps
        self.reconnect_interval = 10
        self.is_connected = False
        self.should_run = True
        self.connect()

    def connect(self):
        self.ws = websocket.WebSocketApp(
            self.url,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            on_open=self._on_open
        )

    def _on_message(self, ws, message):
        logging.info(f"ได้รับข้อความ: {message}")
        self.handle_message(message)

    def _on_error(self, ws, error):
        logging.info(f"เกิดข้อผิดพลาด: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        logging.info("การเชื่อมต่อถูกปิด")
        self.is_connected = False

    def _on_open(self, ws):
        logging.warning("การเชื่อมต่อเปิดแล้ว")
        self.is_connected = True

    def reconnect(self):
        while not self.is_connected and self.should_run:
            logging.warning(f"กำลังพยายามเชื่อมต่อใหม่ในอีก {self.reconnect_interval} วินาที...")
            time.sleep(self.reconnect_interval)
            self.connect()
            self.ws.run_forever(reconnect=5)  # จะลองเชื่อมต่อใหม่ทุก 5 วินาทีโดยอัตโนมัติ

    def send_message(self, message):
        if self.ws and self.is_connected:
            self.ws.send(message)
        else:
            logging.info("ไม่สามารถส่งข้อความได้: WebSocket ไม่ได้เชื่อมต่อ")

    def start(self):
        def run_websocket():
            while self.should_run:
                try:
                    self.ws.run_forever(reconnect=5)
                except Exception as e:
                    logging.info(f"เกิดข้อผิดพลาดในการเชื่อมต่อ WebSocket: {e}")
                if not self.is_connected:
                    self.reconnect()

        self.websocket_thread = threading.Thread(target=run_websocket)
        self.websocket_thread.daemon = True
        self.websocket_thread.start()

    def stop(self):
        self.should_run = False
        if self.ws:
            self.ws.close()
        if self.websocket_thread:
            self.websocket_thread.join()

    def send_bottle_result(self, detection_result, sendto):
        payload = {
            "sendto": sendto,
            "body": {
                "bottle_count": detection_result["bottle_count"],
                "has_water": detection_result["has_water"],
                "no_water": detection_result["no_water"],
                "time_completed": datetime.now().isoformat(),
                "image": detection_result["image"]
            }
        }
        if "order_id" in detection_result:
            payload["body"]["order_id"] = detection_result["order_id"]
        
        self.send_message(json.dumps(payload))
        
    def send_gps_result(self, gps_result):
        payload = {
            "sendto": "both",
            "body": {
                "gpsStatus": gps_result.get("status", "not_ready"),
                "latitude": gps_result.get("latitude", 0),
                "longitude": gps_result.get("longitude", 0),
                "deviceId": config.device_id
            }
        }
        self.send_message(json.dumps(payload))

    def handle_message(self, message):
        try:
            data = json.loads(message)
            logging.info(f"ได้รับข้อความ: {data}")
            if data.get("sendto") == "device" and "body" in data:
                body = data["body"]
                logging.info(f"ได้รับ Data: {body}")
                if body.get("topic") == "need_bottle_image":
                    order_id = body.get("orderId")
                    result = self.detection_handler.perform_detection(order_id)
                    if result:
                        sendto = "backend" if order_id else "both"
                        self.send_bottle_result(result, sendto)
                    # ส่งข้อมูล GPS ทุกครั้งที่มีการตรวจจับ
                    gps_result = self.get_gps_data()
                    self.send_gps_result(gps_result)

        except json.JSONDecodeError:
            logging.info("ไม่สามารถแปลงข้อความเป็น JSON ได้")
        except Exception as e:
            logging.info(f"เกิดข้อผิดพลาดในการจัดการข้อความ WebSocket: {e}")

    def get_gps_data(self):
        return {
            "status": "ready" if self.gps.lat != 0 and self.gps.lng != 0 else "not_ready",
            "latitude": self.gps.lat,
            "longitude": self.gps.lng
        }

def create_websocket_handler(detection_handler, gps):
    return WebSocketHandler(detection_handler, gps)