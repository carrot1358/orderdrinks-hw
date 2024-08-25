import json
import threading
from datetime import datetime
import websocket
from config import config
import logging
class WebSocketHandler:
    def __init__(self, detection_handler, gps):
        self.url = f"ws://{config.backEnd_ip}:{config.backEnd_Port}/ws/device/{config.device_id}"
        self.ws = None
        self.detection_handler = detection_handler
        self.gps = gps
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
        print(f"ได้รับข้อความ: {message}")
        self.handle_message(message)

    def _on_error(self, ws, error):
        print(f"เกิดข้อผิดพลาด: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        print("การเชื่อมต่อถูกปิด")

    def _on_open(self, ws):
        print("การเชื่อมต่อเปิดแล้ว")

    def send_message(self, message):
        if self.ws:
            self.ws.send(message)
        else:
            print("ไม่สามารถส่งข้อความได้: WebSocket ไม่ได้เชื่อมต่อ")

    def start(self):
        threading.Thread(target=self.ws.run_forever, daemon=True).start()

    def send_bottle_result(self, detection_result):
        payload = {
            "sendto": "backend",
            "body": {
                "order_id": detection_result["order_id"],
                "bottle_count": detection_result["bottle_count"],
                "time_completed": datetime.now().isoformat(),
                "image": detection_result["image"]
            }
        }
        self.send_message(json.dumps(payload))
        
    def send_gps_result(self, gps_result):
        payload = {
            "sendto": "backend",
            "body": {
                "gpsStatus" : gps_result.status,
                "latitude": gps_result.latitude,
                "longitude": gps_result.longitude,
                "deviceId": config.device_id
            }
        }
        self.send_message(json.dumps(payload))

    def handle_message(self, message):
        try:
            data = json.loads(message)
            if data.get("sendto") == "device" and "body" in data:
                body = data["body"]
                logging.info(f"ได้รับ Data: {body}")
                if body.get("message") == "need_bottle" and "orderId" in body:
                    order_id = body["orderId"]
                    result = self.detection_handler.perform_detection(order_id)
                    if result:
                        self.send_bottle_result(result)
                    
                    # ส่งข้อมูล GPS ทุกครั้งที่มีการตรวจจับ
                    gps_result = self.get_gps_data()
                    self.send_gps_result(gps_result)
        except json.JSONDecodeError:
            print("ไม่สามารถแปลงข้อความเป็น JSON ได้")
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการจัดการข้อความ WebSocket: {e}")

    def get_gps_data(self):
        # สมมติว่าเรามีเมธอดใน GPS class ที่ให้ข้อมูล GPS ล่าสุด
        return {
            "status": "ready",  # หรือ "not_ready" ขึ้นอยู่กับสถานะจริง
            "latitude": self.gps.lat,
            "longitude": self.gps.lng
        }

def create_websocket_handler(detection_handler, gps):
    return WebSocketHandler(detection_handler, gps)