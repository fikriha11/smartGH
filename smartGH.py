import board
import smbus
import adafruit_dht
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from time import sleep, time


# millis
dhtTime = time()
luxTime = time()
SoundTime = time()
dhtDevice = adafruit_dht.DHT22(board.D23, use_pulseio=False)
Count = 0


def soundOutput():
    try:
        phrase = f"Selamat datang, Kondisi Suhu ruangan sekarang adalah {temperature_c} derajat Celcius, dan Kelembapan Sebesar {humidity} Persen."
        + f"Untuk Keterangan Cahaya, adalah Sebesar {readLux()} Lumen, Terima Kasih"

        language = 'id'
        output = gTTS(text=phrase, lang=language, slow=False)
        output.save('temp.wav')

        song = AudioSegment.from_mp3('temp.wav')
        play(song)
        return True
    except Exception as error:
        print(error)


def readLux():
    global lux
    try:
        bus = smbus.SMBus(1)
        bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)
        bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)
        sleep(0.5)
        data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2)
        lux = data[1] * 256 + data[0]
        return True
    except Exception as error:
        print(error)


def readDHT():
    global temperature_c, temperature_f, humidity
    try:
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        return True
    except Exception as error:
        print(error)


def ReadSensor():
    readDHT()
    readLux()
    print(
        "Temp: {:.1f} F / {:.1f} C    Humidity: {}% Count: {}".format(
            temperature_f, temperature_c, humidity, Count
        )
    )
    print(f"Lux Meter : {lux} lux")
    return True


def mainLoop():
    while True:
        ReadSensor()
        if(time() - SoundTime) > 30:
            soundOutput()
            SoundTime = time()


if __name__ == "__main__":
    mainLoop()
