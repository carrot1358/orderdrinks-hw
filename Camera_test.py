import cv2
from picamera2 import Picamera2
import numpy as np
import time


def start_video_preview():
    picam2 = Picamera2()
    picam2.start_preview()
    config = picam2.create_preview_configuration(main={"size": (1920, 1080)})
    picam2.configure(config)
    picam2.start()

    try:
        while True:
            # Capture the image into a NumPy array
            image = picam2.capture_array()
            # Convert the image to RGB
            RGB_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # Display the RGB image
            cv2.imshow("Grayscale Video Stream", RGB_image)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        picam2.stop_preview()
        picam2.close()
        cv2.destroyAllWindows()
        # Add a small delay to ensure the camera is properly released
        time.sleep(1)


if __name__ == "__main__":
    start_video_preview()