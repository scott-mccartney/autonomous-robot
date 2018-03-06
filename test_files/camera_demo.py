import picamera
from time import sleep
camera = picamera.PiCamera()

camera.start_preview()

camera.start_recording('video1.h264')
sleep(15)
camera.stop_recording()
