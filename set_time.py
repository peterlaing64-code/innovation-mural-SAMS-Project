import board
import displayio
import os
import time
import asyncio
import busio
import digitalio
import terminalio
from adafruit_matrixportal.matrix import Matrix
from adafruit_matrixportal.matrixportal import MatrixPortal
from digitalio import DigitalInOut, Pull
from adafruit_debouncer import Debouncer
from adafruit_pcf8523.pcf8523 import PCF8523
import adafruit_vl53l0x
import bitbangio
import sdcardio
import storage
import random

spi = busio.SPI(board.A1, MOSI=board.A2, MISO=board.A3)
sd = sdcardio.SDCard(spi, board.A4) # A4 is chip select
storage.mount(storage.VfsFat(sd),"/sd")
with open("/sd/logs/startupTest.txt","w") as f: # quick test: write a file
    f.write("it works - starup")

matrixportal = MatrixPortal(
    width=64,
    height=32,
    bit_depth=4,
    status_neopixel=None,
    debug=False
)

# Initialize the I2C bus
i2c = bitbangio.I2C(board.SCL, board.SDA, frequency=50000)  # USES SCL AND SDA FROM STEMMA QT PORT
time.sleep(0.2)
# Initialize the RTC
rtc = PCF8523(i2c)

# Initialize the TOF sensor
vl53 = adafruit_vl53l0x.VL53L0X(i2c)
vl53.measurement_timing_budget = 200000
days = ("Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun")
# SET TIME - ONLY PUT TO TRUE TO SET CURRENT TIME
if True:
    # (year, month, day, hour, minute, second, weekday(0-6), day of the year) !!! -1 means calculate it by its self!!!
    t = time.struct_time((2026, 11, 3, 21, 31, 0, 3, -1, -1))
    rtc.datetime = t
    print("Time has been set!")