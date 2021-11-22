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
import time
from datetime import datetime as dt
from time import time, sleep


# url_suhu = "https://gh1.rumahkuhidroponik.com/post_suhu.php"
# url_image = "https://gh1.rumahkuhidroponik.com/post_image.php"
# url_realtime = "https://rumahkuhidroponik.com/API/sensor/update-device3/"
url_baru = "https://smartghsip.belajarobot.com/sensor/insert/1"
# url_lux =  "https://rumahkuhidroponik.com/API/sensor/updatse-device1/"
# url_lux = "https://gh1.rumahkuhidroponik.com/post_ppm.php"
api_key = "a1ffqsVcx45IuG"


menit = 0
jam = 0
flag = 0
flag1 = 0

camera = picamera.PiCamera()
hostname = "8.8.8.8"
datenow = dt.now().strftime("%Y-%m-%d")


def realtime():
    camera.resolution = (320, 240)
    camera.rotation = 180
    camera.start_preview()
    time.sleep(0.5)
    camera.capture('example.jpg')
    camera.stop_preview()
    readSHT()
    readLux()
    with open("example.jpg", "rb") as img_file:
        Image = base64.b64encode(img_file.read())

    headers = {}
    # headers['Content-Type'] = 'application/json'
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    files = urllib.parse.urlencode({
        # 'api':api_key,
        # 'id':'0001',
        'lumen': int(lux),
        'temp': int(cTemp),
        'humid': int(humidity),
        'image': Image
    }).encode('ascii')
    try:
        send_image = urllib.request.urlopen(url_baru, data=files)
        print(send_image.read())
    except:
        print("post image bermasalah!")


def readLux():
    global lux
    try:
        bus = smbus.SMBus(1)
        bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)
        bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)
        sleep(0.5)
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
        sleep(0.5)
        data = bus.read_i2c_block_data(0x44, 0x00, 6)

        # Convert the data
        temp = data[0] * 256 + data[1]
        cTemp = -45 + (175 * temp / 65535.0)
        fTemp = -49 + (315 * temp / 65535.0)
        humidity = 100 * (data[3] * 256 + data[4]) / 65535.0

        # Output data to screen
        # print("Temperature in Celsius is : %.2f C" % cTemp)
        # print("Temperature in Fahrenheit is : %.2f F" % fTemp)
        # print("Relative Humidity is : %.2f %%RH" % humidity)

    except:
        print("SHT error")


def mainloop():
    global menit
    global flag1
    if menit != dt.now().minute:
        flag1 += 1
        if flag1 == 2:
            realtime()
        if flag1 > 2:
            flag1 = 0
        menit = dt.now().minute


while True:
    response = os.system("ping -c3 " + hostname)
    print("Response: {}".format(response))
    if response == 0:
        # maincode()
        mainloop()
    if response != 0:
        print("Device not connected to Internet")
