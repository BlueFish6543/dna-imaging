# Note: picamera library is available only on Raspberry Pi

import os
import time
from picamera import PiCamera

camera = PiCamera()

def take_picture():
    camera.start_preview()
    time.sleep(3)
    camera.capture(os.path.join(os.getcwd(), 'tmp', 'image.jpg'))
    camera.stop_preview()
    