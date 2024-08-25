import json
import threading
from datetime import datetime
import websocket
from config import config

class WebSocketHandler:
    def __init__(self):
        self.url = f"ws://{config.backEnd_ip}:{config.backEnd_Port}/ws/device/{config.device_id}"
        self.ws = None
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

    def handle_message(self, message, detection_callback):
        try:
            data = json.loads(message)
            if data.get("sendto") == "device" and "message" in data:
                order_id = data["message"].get("orderId")
                if order_id:
                    return detection_callback(order_id)
        except json.JSONDecodeError:
            print("ไม่สามารถแปลงข้อความเป็น JSON ได้")
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการจัดการข้อความ WebSocket: {e}")
        return None

def create_websocket_handler():
    return WebSocketHandler()