#!/usr/bin/python
import cv2
import cv2.cv as cv
import numpy
import zbar
import time
import threading
#import smbus
#import math

# Power management registers
#power_mgmt_1 = 0x6b
#power_mgmt_2 = 0x6c
'''
# MPU6050 sensor methods
def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)
'''
# Gyroscope class
'''
class Gyro(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # Do stuff

    def run(self):
         gyro_xout = read_word_2c(0x43)
         gyro_yout = read_word_2c(0x45)
         gyro_zout = read_word_2c(0x47)
         accel_xout = read_word_2c(0x3b)
         accel_yout = read_word_2c(0x3d)
         accel_zout = read_word_2c(0x3f)
         axs = accel_xout / 16384.0
         ays = accel_yout / 16384.0
         azs = accel_zout / 16384.0

         print("x_rot, y_rot: " , '{0:.2f}'.format(get_x_rotation(axs, ays, azs)), '{0:.2f}'.format(get_y_rotation(axs, ays, azs)))
'''

# QR Reader class
class QRScanner(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.WINDOW_NAME = 'Camera'
        self.CV_SYSTEM_CACHE_CNT = 5 # Cv has 5-frame cache
        self.LOOP_INTERVAL_TIME = 0.5

        cv.NamedWindow(self.WINDOW_NAME, cv.CV_WINDOW_NORMAL)
        self.cam = cv2.VideoCapture(-1)

    def scan(self, aframe):
        print aframe.shape    # If throws error 'NoneType' ==> img loaded improperly
        imgray = cv2.cvtColor(aframe, cv2.COLOR_BGR2GRAY)
        raw = str(imgray.data)

        scanner = zbar.ImageScanner()
        scanner.parse_config('enable')          

        width = int(self.cam.get(cv.CV_CAP_PROP_FRAME_WIDTH))
        height = int(self.cam.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
        imageZbar = zbar.Image(width, height,'Y800', raw)
        scanner.scan(imageZbar)

        for symbol in imageZbar:
            print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data

    def run(self):
        while True:      
            for i in range(0,self.CV_SYSTEM_CACHE_CNT):
                self.cam.read()
            img = self.cam.read()
            self.scan(img[1])
            # If the QR code is correct, exit while loop and release cam
            cv2.imshow(self.WINDOW_NAME, img[1])
            cv.WaitKey(1)
            time.sleep(self.LOOP_INTERVAL_TIME)
            
        cam.release()

scanner = QRScanner()
scanner.start()
