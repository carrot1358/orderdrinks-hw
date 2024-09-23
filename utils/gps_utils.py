import logging
import serial
import time
import string
import pynmea2
import threading
from config import config

# ตั้งค่า logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GPS:
    def __init__(self):
        self.lat = 0
        self.lng = 0
        self.running = False
        self.thread = None
        logger.info("GPS initialized")

    def start(self):
        logger.info("Starting GPS")
        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()
        logger.info("GPS thread started")

    def stop(self):
        logger.info("Stopping GPS")
        self.running = False
        if self.thread:
            self.thread.join()

    def run(self):
        try:
            port = "/dev/ttyAMA0"
            ser = serial.Serial(port, baudrate=9600, timeout=0.5)
            dataout = pynmea2.NMEAStreamReader()

            while self.running:
                newdata = ser.readline()
                newdata = newdata.decode('ascii', errors='ignore').strip()

                if newdata.startswith("$GPRMC"):
                    try:
                        newmsg = pynmea2.parse(newdata)
                        self.lat = newmsg.latitude
                        self.lng = newmsg.longitude
                        gps = f"Latitude={self.lat} and Longitude={self.lng}"
                        if self.lat != 0 and self.lng != 0:
                            logger.info(gps)
                        else:
                            self.lat = 0
                            self.lng = 0
                            logger.info("Non-GPRMC data received or noise")
                    except pynmea2.ParseError as e:
                        logger.info(f"Failed to parse NMEA sentence: {e}")
                else:
                    logger.info("Non-GPRMC data received or noise")

                time.sleep(1)  # เพิ่มการหน่วงเวลาเล็กน้อยเพื่อลดการใช้ CPU

        except Exception as e:
            logger.info(f"An error occurred in the GPS thread: {e}")