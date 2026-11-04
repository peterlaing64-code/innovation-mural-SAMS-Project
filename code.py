import board
import displayio
import os
import time
import asyncio
import busio
import digitalio
import terminalio
from adafruit_display_text import label
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

  
#------------------------------------------------------
# DESIGNED & FABRICATED IN 2025-2027 SCHOOL YEARS BY PETER LAING
# WITH ANY QUESTIONS, PLEASE CONTACT MR. REAGLE OR MR. CASEY FIRST
# IF UNREACHABLE, PLEASE CONTACT PETER LAING AT peterlaing64@icloud.com
# BEFORE MODIFING, PLEASE CONTACT MR. CASEY.
# IF FOR SOME REASON, NEITHER OF THEM WORK THERE ANYMORE, CONATCT THE SCHOOL PRINCIPAL AND GET IN TOUCH WITH PETER LAING
# THANK YOU!
#------------------------------------------------------
spi = busio.SPI(board.A1, MOSI=board.A2, MISO=board.A3)
sd = sdcardio.SDCard(spi, board.A4) # A4 is chip select
storage.mount(storage.VfsFat(sd),"/sd")
with open("/sd/logs/startupTest.txt","w") as f: # quick test: write a file
    f.write("it works - starup")

#------------------------------------------------------
matrixportal = MatrixPortal(
    width=64,
    height=32,
    bit_depth=6,
    status_neopixel=None,
    debug=False
    
)

root_group = displayio.Group()

matrixportal.display.root_group = root_group

left_half_group = displayio.Group()
right_half_group = displayio.Group(x=32)



root_group.append(left_half_group)
root_group.append(right_half_group)


catanese_bmp = "/sd/images/img_Catanese_Christopher_83.bmp"
bitmap = displayio.OnDiskBitmap(open(catanese_bmp, "rb"))
catanese = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
right_half_group.append(catanese)
time.sleep(1)
right_half_group.pop()


#------------------------------------------------------
class imagesMode:
    def __init__(self, portal_instance):
        self.running = True
        
        self.matrixportal = portal_instance
        self.right_half_group = displayio.Group(x=32, y=0)
        matrixportal.display.root_group.append(self.right_half_group)
    async def chooseRandomImage(self):
        self.image_dir = "/sd/images/"
        self.displayImage = random.choice(os.listdir(self.image_dir))
        
        if (self.displayImage.endswith(".bmp") and not self.displayImage.startswith(".") and self.displayImage.startswith("img")): 
            self.displayImagePath = "sd/images/"+self.displayImage
            print(self.displayImagePath)
            return self.displayImagePath
        else:
            return None
        
    async def displayRandomImage(self):
        self.imageToDisplay = await self.chooseRandomImage()
        print(self.imageToDisplay)
        if self.imageToDisplay == None or "None":
            self.displayRandomImage()
        try:
            self.bitmap = displayio.OnDiskBitmap(open(self.imageToDisplay, "rb"))
            self.teacher = displayio.TileGrid(self.bitmap, pixel_shader=self.bitmap.pixel_shader)
            self.right_half_group.append(self.teacher)
            self.matrixportal.display.refresh()
            print("appended")
        except (TypeError, Exception) as e:
            print("Problem! Skipped Given Problem", e)
            await self.displayRandomImage()
            
    async def clearImage(self, delay):
        while self.running:
            await asyncio.sleep(delay)
            if self.right_half_group:
                self.right_half_group.pop() 
                print("popped")
            await self.displayRandomImage()
            print("finished")
            
    def stop(self):
        self.running = False
        if self.right_half_group:
            self.right_half_group.pop()
#------------------------------------------------------
global red_left
global yellow_count
global green_left
global blue_low
global red_high

#red_left = 0
red_left = label.Label(
    terminalio.FONT,
    text="",
    color=0xFF0000
)
red_left.x = 0
red_left.y = 15
left_half_group.append(red_left)
red_left.text=""
#blue_low = 1
blue_low = label.Label(
    terminalio.FONT,
    text="",
    color=0x0000FF
)
blue_low.x = 0
blue_low.y = 25
left_half_group.append(blue_low)
blue_low.text=""
# Set GREEN FONT = 2
green_left = label.Label(
    terminalio.FONT,
    text="",
    color=0x00FF00
)
green_left.x = 0
green_left.y = 15
left_half_group.append(green_left)
green_left.text=""

# Set COUNTING TEXTFEILD = 3

yellow_count = label.Label(
    terminalio.FONT,
    text="",
    color=0xFFFF00
)
yellow_count.x = 5
yellow_count.y = 15
left_half_group.append(yellow_count)
yellow_count.text=""
# Set RED FONT = 4
red_high = label.Label(
    terminalio.FONT,
    text="",
    color=0xFF0000
)
red_high.x = 0
red_high.y = 5
left_half_group.append(red_high)
red_high.text=""


# Initialize the I2C bus
i2c = bitbangio.I2C(board.SCL, board.SDA, frequency=50000)  # USES SCL AND SDA FROM STEMMA QT PORT
time.sleep(0.2)
# Initialize the RTC
rtc = PCF8523(i2c)

# Initialize the TOF sensor
vl53 = adafruit_vl53l0x.VL53L0X(i2c)
vl53.measurement_timing_budget = 200000
days = ("Sun", "Mon", "Tue", "Wed", "Thur", "Fri", "Sat")


#------------------------------------------------------
#------------------------------------------------------
class countingMode:
    def __init__(self, portal_instance):
        self.running = True
        self.test_running = True
        self.object_present = False
        self.matrixportal = portal_instance
        self.count = 0
        
    async def displayDistanceTest(self):
        while self.test_running:
            red_left.text = str("{} mm".format(vl53.range))
            print("display dist test cnt")
            await asyncio.sleep(0.01)

    async def stopTestDisplaying(self, delay):
        await asyncio.sleep(delay)
        print("stop test cnt")
        self.test_running = False
        red_left.text=""
        yellow_count.text=""
        green_left.text=""
        

    async def stopDisplaying(self, delay):
        await asyncio.sleep(delay)
        print("stop cnt")
        self.running = False
        red_left.text=""
        yellow_count.text=""
        green_left.text=""
        

    async def main(self):
        while self.running:
            try:
                current_range = vl53.range
                print("display cnt main")
                if current_range < 1400 and not self.object_present:
                    self.count += 1
                    print(f"{self.count}")
                    yellow_count.text=f"{self.count}"
                    self.object_present = True
                elif current_range >= 1400 and self.object_present:
                    self.object_present = False
                    
            except (OSError, RuntimeError, Exception) as e:
                print("Sensor read skipped due to noise:", e)
                
            
            await asyncio.sleep(0.05)

#------------------------------------------------------
class timeMode:
    def __init__(self, portal_instance):
        self.running = True
        self.test_running = True
        self.matrixportal = portal_instance
        
    async def displayTime(self):
        while self.running:
            print("displaying time")
            t = rtc.datetime
            hour = t.tm_hour % 12
            if hour == 0: hour = 12
            time_str = f"{hour:02}:{t.tm_min:02}"
            red_high.text = time_str
            blue_low.text=f"{days[t.tm_wday]}"
            print("display Time")
            await asyncio.sleep(60)

    async def displayTestTime(self):
        while self.test_running:
            t = rtc.datetime
            hour = t.tm_hour % 12
            if hour == 0: hour = 12
            time_str = f"{hour:02}:{t.tm_min:02}"
            red_left.text=time_str
            blue_low.text = f"{days[t.tm_wday]}"
            print("displayTest Time")
            await asyncio.sleep(1)

    async def stopDisplaying(self, delay):
        await asyncio.sleep(delay)
        self.running = False
        red_left.text=""
        blue_low.text=""
        green_left.text=""
        print("stop displayTest Time")
        

    async def stopTestDisplaying(self, delay):
        await asyncio.sleep(delay)
        self.test_running = False
        red_left.text=""
        blue_low.text=""
        green_left.text=""
        print("stop display Time")

#------------------------------------------------------

tm_mode = timeMode(matrixportal)
cnt_mode = countingMode(matrixportal)
images_mode = imagesMode(matrixportal)

async def bufferDisplay(delay):
    while True:
        await asyncio.sleep(delay)
        matrixportal.display.refresh()
#------------------------------------------------------
# MAIN FUNCTIONS AND LOOPS
async def main():
    # STARTUP TESTS
    await asyncio.gather(cnt_mode.displayDistanceTest(), cnt_mode.stopTestDisplaying(10))
    await asyncio.gather(tm_mode.displayTestTime(), tm_mode.stopTestDisplaying(10))
    #print(matrixportal.display.root_group)
    await images_mode.displayRandomImage()
    #RUNNING TASK
    await asyncio.gather(
        cnt_mode.main(),
        tm_mode.displayTime(),
        images_mode.clearImage(30),
        bufferDisplay(0.1),
        
    )

#------------------------------------------------------
# MAIN FUNCTION CALL
asyncio.run(main())
# images_mode.displayRandomImage()
# images_mode.clearImage(5)