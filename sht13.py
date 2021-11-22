
import smbus
from time import sleep, time


def readSHT():
    try:
        # Get I2C bus
        bus = smbus.SMBus(1)
        bus.write_i2c_block_data(0x44, 0x2C, [0x06])
        sleep(0.5)
        data = bus.read_i2c_block_data(0x44, 0x00, 6)

        # Convert the data
        temp = data[0] * 256 + data[1]
        cTemp = -45 + (175 * temp / 65535.0)
        fTemp = -49 + (315 * temp / 65535.0)
        humidity = 100 * (data[3] * 256 + data[4]) / 65535.0

        # Output data to screen
        print("Temperature in Celsius is : %.2f C" % cTemp)
        print("Temperature in Fahrenheit is : %.2f F" % fTemp)
        print("Relative Humidity is : %.2f %%RH" % humidity)

    except:
        print("SHT error")


while True:
    readSHT()
