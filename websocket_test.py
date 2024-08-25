import websocket
import json
import base64
import io
from datetime import datetime
from picamera2 import Picamera2

import time


def capture_image():
    # ตั้งค่า PiCamera2
    picam2 = Picamera2()

    # กำหนดความละเอียดสูงสุดที่กล้องรองรับ
    # หมายเหตุ: ค่าเหล่านี้อาจต้องปรับตามรุ่นของ Raspberry Pi Camera ที่คุณใช้
    camera_config = picam2.create_still_configuration(main={"size": (4056, 3040)})
    picam2.configure(camera_config)

    picam2.start()

    # รอให้กล้องพร้อม
    time.sleep(2)

    # ถ่ายภาพและบันทึกลงใน memory เป็น PNG
    stream = io.BytesIO()
    picam2.capture_file(stream, format='jpeg')
    stream.seek(0)

    # หยุดการทำงานของกล้อง
    picam2.stop()

    return stream.getvalue()


def send_bottle_data(ws, order_id, bottle_count):
    # ถ่ายภาพ
    image_data = capture_image()

    # เข้ารหัสรูปภาพเป็น base64
    encoded_string = base64.b64encode(image_data).decode('utf-8')

    # สร้าง JSON object
    data = {
        "order_id": order_id,
        "bottle_count": bottle_count,
        "time_completed": datetime.now().isoformat(),
        "image": encoded_string
    }

    # ส่งข้อมูลผ่าน WebSocket
    ws.send(json.dumps(data))


# เชื่อมต่อ WebSocket
ws = websocket.WebSocket()
ws.connect("ws://orderdrinks.webhop.me:9000/ws/device/70cb8bfc-5b67-4115-8db6-d371e22b430b")

# ส่งข้อมูล
send_bottle_data(ws, "92621068-6888-435a-9945-bce98dc6ff25", 5)

# ปิดการเชื่อมต่อ
ws.close()
