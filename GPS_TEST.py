import serial
import time
import string
import pynmea2

while True:
	port = "/dev/ttyAMA0"
	ser = serial.Serial(port, baudrate=9600, timeout=0.5)
	dataout = pynmea2.NMEAStreamReader()
	newdata = ser.readline()
	newdata = newdata.decode('ascii', errors='ignore').strip()  # Decode to ASCII and ignore non-ASCII characters

	if newdata.startswith("$GPRMC"):  # Check if the data starts with $GPRMC
		try:
			newmsg = pynmea2.parse(newdata)
			lat = newmsg.latitude
			lng = newmsg.longitude
			gps = f"Latitude={lat} and Longitude={lng}"
			print(gps)
		except pynmea2.ParseError as e:
			print(f"Failed to parse NMEA sentence: {e}")
	else:
		print("Non-GPRMC data received or noise")
