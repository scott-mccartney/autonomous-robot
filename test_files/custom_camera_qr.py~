#!/usr/bin/python
import cv2
import cv2.cv as cv
import numpy
import zbar
import time
import picamera
import picamera.array
import threading
import smbus
import math

camera = picamera.PiCamera()
LOOP_INTERVAL_TIME = 0.25

# Room numbers are first 6 binary digits of QR code
def roomBinaryLookup(roomInt):
    if roomInt == 271:
        return '000001'
    elif roomInt == 273:
        return '000010'
    elif roomInt == 277:
        return '000011'
    else:
        return '000001'     # Default room is 271

class QRScanner(threading.Thread):
    def __init__(self, r):
        threading.Thread.__init__(self)
        self.roomNum = r
        # camera.start_preview()
        time.sleep(2)

    def scan(self, img):   
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        raw = str(imgray.data)
        
        scanner = zbar.ImageScanner()
        scanner.parse_config('enable')

        imageZbar = zbar.Image(1920, 1080, 'Y800', raw)
        scanner.scan(imageZbar)

        for symbol in imageZbar:
            if symbol.data[:6] in self.roomNum:
                print 'Room Binary num: ', symbol.data[:6]
                print 'Room characteristics: ', symbol.data[6:]
                return True
            else:
                return False

    def run(self):
        #while True:
        for i in range(0,10):
            stream = picamera.array.PiRGBArray(camera)
            camera.capture(stream, format='bgr')

            img1 = stream.array
            right_door = self.scan(img1)

            if right_door:
                break

        # camera.stop_preview()

roomNum = roomBinaryLookup(271)
scanner = QRScanner(roomNum)
scanner.start()
