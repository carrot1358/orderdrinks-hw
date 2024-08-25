import logging
import serial
import time
import string
import pynmea2
import threading
import json
from config import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GPS:
    def __init__(self, ws_handler):
        self.ws_handler = ws_handler
        self.lat = 0
        self.lng = 0
        self.running = False
        self.thread = None
        logging.info("GPS initialized")

    def start(self):
        logging.info("Starting GPS")
        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()
        logging.info("GPS thread started")

    def stop(self):
        logging.info("Stopping GPS")
        self.running = False
        if self.thread:
            self.thread.join()

    def run(self):
        try:
            port = "/dev/ttyAMA0"
            ser = serial.Serial(port, baudrate=9600, timeout=0.5)
            dataout = pynmea2.NMEAStreamReader()

            last_send_time = 0

            while self.running:
                newdata = ser.readline()
                newdata = newdata.decode('ascii', errors='ignore').strip()

                if newdata.startswith("$GPRMC"):
                    try:
                        newmsg = pynmea2.parse(newdata)
                        self.lat = newmsg.latitude
                        self.lng = newmsg.longitude
                        gps = f"Latitude={self.lat} and Longitude={self.lng}"
                        print(gps)

                        current_time = time.time()
                        if current_time - last_send_time >= 10:
                            self.send_gps_data("ready")
                            last_send_time = current_time

                    except pynmea2.ParseError as e:
                        print(f"Failed to parse NMEA sentence: {e}")
                else:
                    self.send_gps_data("not_ready")
                    print("Non-GPRMC data received or noise")

                time.sleep(10)  # เพิ่มการหน่วงเวลาเล็กน้อยเพื่อลดการใช้ CPU

        except Exception as e:
            logging.error(f"An error occurred in the GPS thread: {e}")

    def send_gps_data(self,status):
        message = {
            "sendto": "backend",
            "body": {
                "gpsStatus" : status,
                "latitude": self.lat,
                "longitude": self.lng,
                "deviceId": config.device_id
            }
        }
        self.ws_handler.send_message(json.dumps(message))