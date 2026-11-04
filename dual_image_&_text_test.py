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

#bitmap = displayio.OnDiskBitmap(catanese_bmp)
#sprite = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
# left_half_group.append(sprite)
# time.sleep(5)
# left_half_group.pop()


catanese_bmp = "/sd/images/img_Catanese_Christopher_83.bmp"
bitmap = displayio.OnDiskBitmap(open(catanese_bmp, "rb"))
catanese = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
right_half_group.append(catanese)
time.sleep(5)
right_half_group.pop()




#red_left = 0
red_left = label.Label(
    terminalio.FONT,
    text="",
    color=0xFF0000
)
red_left.x = 3
red_left.y = 15
left_half_group.append(red_left)

#blue_low = 1
blue_low = label.Label(
    terminalio.FONT,
    text="",
    color=0x0000FF
)
blue_low.x = 0
blue_low.y = 25
left_half_group.append(blue_low)

# Set GREEN FONT = 2
green_left = label.Label(
    terminalio.FONT,
    text="",
    color=0x00FF00
)
green_left.x = 0
green_left.y = 15
left_half_group.append(green_left)


# Set COUNTING TEXTFEILD = 3

yellow_count = label.Label(
    terminalio.FONT,
    text="",
    color=0xFFFF00
)
yellow_count.x = 5
yellow_count.y = 15
left_half_group.append(yellow_count)

# Set RED FONT = 4
red_high = label.Label(
    terminalio.FONT,
    text="",
    color=0xFF0000
)
red_high.x = 0
red_high.y = 5
left_half_group.append(red_high)



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
            
class testClass():
    def __init__(self):
        pass
    
    async def displayRandomText(self):
        while True:
            red_left.text = str(random.randint(0,10))
            blue_low.text = str(random.randint(0,10))
            green_left.text = str(random.randint(0,10))
            yellow_count.text = str(random.randint(0,10))
            red_high.text = str(random.randint(0,10))
            await asyncio.sleep(1)
        
test_class = testClass()
images_mode = imagesMode(matrixportal)

async def bufferDisplay(delay):
    while True:
        await asyncio.sleep(delay)
        matrixportal.display.refresh()
        
        
        
async def main():
    
    await images_mode.displayRandomImage()
    #RUNNING TASK
    await asyncio.gather(
        #cnt_mode.main(),
        #tm_mode.displayTime(),
        test_class.displayRandomText(),
        images_mode.clearImage(5),
        bufferDisplay(0.1),
        
    )


asyncio.run(main())