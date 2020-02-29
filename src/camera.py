# Note: picamera library is available only on Raspberry Pi

import os
import time
from picamera import PiCamera

camera = PiCamera()
MODES = [
    'auto',
    'sunlight',
    'cloudy',
    'shade',
    'tungsten',
    'fluorescent',
    'incandescent',
    'flash',
    'horizon'
]

def set_white_balance(mode):
    camera.awb_mode = mode

def take_picture():
    camera.start_preview()
    time.sleep(3)
    camera.capture(os.path.join(os.getcwd(), 'tmp', 'image.jpg'))
    camera.stop_preview()
    