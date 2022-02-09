import sys
import urllib.request
import urllib.parse
import json
import ast
import struct
import base64
import os
import time
import threading
import math
import subprocess
import logging
import picamera
import smbus
import schedule
import time
from datetime import datetime as dt


url = "https://smartghsip.belajarobot.com/sensor/insert/1"
# url = "https://smartghsip.belajarobot.com/sensor/insert/2"


hostname = "8.8.8.8"


def realtime():
    readLux()
    readSHT()
    takePicture()
    with open("example.jpg", "rb") as img_file:
        Image = base64.b64encode(img_file.read())

    headers = {}
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    files = urllib.parse.urlencode({
        'lumen': int(lux),
        'temp': int(cTemp),
        'humid': int(humidity),
        'image': Image
    }).encode('ascii')
    try:
        send_image = urllib.request.urlopen(url, data=files)
        print(send_image.read())
    except:
        print("post image bermasalah!")


def takePicture():
    try:
        camera = picamera.PiCamera()
        time.sleep(0.5)
        camera.resolution = (320, 240)
        camera.rotation = 180
        camera.start_preview()
        time.sleep(0.5)
        camera.capture('example.jpg')
        camera.stop_preview()
        camera.close()
    except:
        print("Camera Error")


def readLux():
    global lux
    try:
        bus = smbus.SMBus(1)
        bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)
        bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)
        time.sleep(0.5)
        data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2)
        lux = data[1] * 256 + data[0]

        # print("Lux Meter: {} Lumen".format(lux))

    except Exception as error:
        print("Lux data error")


def readSHT():
    global cTemp, fTemp, humidity
    try:
        # Get I2C bus
        bus = smbus.SMBus(1)
        bus.write_i2c_block_data(0x44, 0x2C, [0x06])  # Address 0x44
        time.sleep(0.5)
        data = bus.read_i2c_block_data(0x44, 0x00, 6)

        # Convert the data
        temp = data[0] * 256 + data[1]
        cTemp = -45 + (175 * temp / 65535.0)
        fTemp = -49 + (315 * temp / 65535.0)
        humidity = 100 * (data[3] * 256 + data[4]) / 65535.0

        # print("Temperature in Celsius is : %.2f C" % cTemp)
        # print("Temperature in Fahrenheit is : %.2f F" % fTemp)
        # print("Relative Humidity is : %.2f %%RH" % humidity)

    except:
        print("SHT error")


def mainloop():
    schedule.run_pending()
    time.sleep(1)


# Inisialisasi
schedule.every(3).minutes.do(realtime)

while True:
    response = os.system("ping -c3 " + hostname)
    if response == 0:
        mainloop()
    else:
        print("Device not connected to Internet")
