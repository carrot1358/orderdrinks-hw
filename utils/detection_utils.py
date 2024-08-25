import logging
import cv2
import base64
import os
from picamera2 import Picamera2
from roboflow import Roboflow
from config import config

class DetectionHandler:
    def __init__(self):
        self.picam2 = self.setup_camera()
        self.model = self.initialize_model()

    def setup_camera(self):
        picam2 = Picamera2()
        camera_config = picam2.create_still_configuration(main={"size": (4056, 3040)})
        picam2.configure(camera_config)
        picam2.start()
        return picam2

    def initialize_model(self):
        rf = Roboflow(api_key=config.Roboflow_api_key)
        project = rf.workspace(config.Roboflow_workspace).project(config.Roboflow_project)
        return project.version(config.Roboflow_version, local=f"http://{config.inference_ip}:{config.inference_port}/").model

    def Detect(self, debug=False):
        image = self.picam2.capture_array()
        prediction = self.model.predict(image, confidence=config.confidence_threshold)
        if debug:
            self.save_debug_image(image, prediction)
        return prediction

    def save_debug_image(self, image, prediction):
        for pred in prediction:
            x, y, w, h = pred['x'], pred['y'], pred['width'], pred['height']
            cv2.rectangle(image, (int(x - w/2), int(y - h/2)), (int(x + w/2), int(y + h/2)), (0, 255, 0), 2)
        cv2.imwrite('output/output_marked.png', image)

    def count_water(self, prediction):
        has_water = sum(1 for pred in prediction if pred['class'] == 'has_water')
        no_water = sum(1 for pred in prediction if pred['class'] == 'no_water')
        return has_water, no_water

    def perform_detection(self, order_id):
        logging.info(f"กำลังทำการตรวจจับสำหรับ order_id: {order_id}")
        data = self.Detect(config.debug)
        has_water, no_water = self.count_water(data)
        
        image_base64 = ""
        output_image_path = 'output/output_marked.png'
        if os.path.exists(output_image_path):
            with open(output_image_path, 'rb') as image_file:
                image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        else:
            logging.error(f"ไม่พบไฟล์ภาพที่ {output_image_path}")

        bottle_count = has_water + no_water 
        logging.info(f"จำนวนขวด: {bottle_count}")

        return {
            "order_id": order_id,
            "bottle_count": bottle_count,
            "image": image_base64
        }

def create_detection_handler():
    return DetectionHandler()
