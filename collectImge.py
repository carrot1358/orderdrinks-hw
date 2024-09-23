from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
import time
import os
from libcamera import Transform

# เปลี่ยนตำแหน่งที่จะบันทึกวิดีโอเป็นโฟลเดอร์ในพื้นที่ของผู้ใช้
save_path = os.path.expanduser("~/video/collect")
os.makedirs(save_path, exist_ok=True)

# ตั้งค่ากล้อง
picam2 = Picamera2()
video_config = picam2.create_video_configuration()

# หมุนกล้องตามเข็มนาฬิกา 90 องศา
video_config["transform"] = Transform(rotation=90)

picam2.configure(video_config)

encoder = H264Encoder(bitrate=10000000)

while True:
    try:
        duration = int(input("ใส่ระยะเวลาบันทึกวิดีโอ (วินาที) หรือใส่ค่าติดลบเพื่อออกจากโปรแกรม: "))
        
        if duration < 0:
            print("จบการทำงานของโปรแกรม")
            break
        
        # สร้างชื่อไฟล์วิดีโอ
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        video_name = f"video_{timestamp}_{duration}s.h264"
        video_path = os.path.join(save_path, video_name)

        output = FileOutput(video_path)

        picam2.start_recording(encoder, output)

        print(f"กำลังบันทึกวิดีโอที่: {video_path}")
        print(f"บันทึกวิดีโอเป็นเวลา {duration} วินาที...")

        # บันทึกวิดีโอตามเวลาที่กำหนด
        time.sleep(duration)

        # หยุดการบันทึก
        picam2.stop_recording()

        print(f"เสร็จสิ้นการบันทึกวิดีโอ {duration} วินาที")
        
    except ValueError:
        print("กรุณาใส่ตัวเลขเท่านั้น")

# ปิดกล้อง
picam2.close()

print("ปิดกล้องและจบการทำงานของโปรแกรม")
