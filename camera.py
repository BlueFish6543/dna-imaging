# Note: picamera library is available only on Raspberry Pi

import os
import time
from picamera import PiCamera

def take_picture():
    camera = PiCamera()
    camera.start_preview()
    time.sleep(3)
    camera.capture(os.path.join(os.getcwd(), 'tmp', 'image.jpg'))
    camera.stop_preview()
    