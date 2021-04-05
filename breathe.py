# importing needed libraries
import time
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# set up vibrating motor
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)

# initializing Rpi pins
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
# initializing OLED
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
# Initialize library.
disp.begin()
# Clear display.
disp.clear()
disp.display()
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
padding = 2
top = padding
font = ImageFont.load_default()
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)


# function for breathing exercise
def bardraw(delay):
    draw.rectangle((24, 24, 10, 32), outline=255, fill=255)
    disp.image(image)
    disp.display()
    GPIO.output(4, GPIO.HIGH)
    time.sleep(delay)
    disp.clear()
    draw.rectangle((24, 24, 20, 32), outline=255, fill=255)
    disp.image(image)
    disp.display()
    GPIO.output(4, GPIO.LOW)
    time.sleep(delay)
    disp.clear()
    draw.rectangle((24, 24, 30, 32), outline=255, fill=255)
    disp.image(image)
    disp.display()
    GPIO.output(4, GPIO.HIGH)
    time.sleep(delay)
    disp.clear()
    draw.rectangle((24, 24, 40, 32), outline=255, fill=255)
    disp.image(image)
    disp.display()
    GPIO.output(4, GPIO.LOW)
    time.sleep(delay)
    disp.clear()
    draw.rectangle((24, 24, 50, 32), outline=255, fill=255)
    disp.image(image)
    disp.display()
    GPIO.output(4, GPIO.HIGH)
    time.sleep(delay)
    disp.clear()
    draw.rectangle((24, 24, 60, 32), outline=255, fill=255)
    disp.image(image)
    disp.display()
    GPIO.output(4, GPIO.LOW)
    time.sleep(delay)
    disp.clear()
    draw.rectangle((24, 24, 70, 32), outline=255, fill=255)
    disp.image(image)
    disp.display()
    GPIO.output(4, GPIO.HIGH)
    time.sleep(delay)
    disp.clear()
    draw.rectangle((24, 24, 80, 32), outline=255, fill=255)
    disp.image(image)
    disp.display()
    GPIO.output(4, GPIO.LOW)
    time.sleep(delay)
    disp.clear()
    draw.rectangle((24, 24, 90, 32), outline=255, fill=255)
    disp.image(image)
    disp.display()
    GPIO.output(4, GPIO.HIGH)
    time.sleep(delay)
    disp.clear()
    draw.rectangle((24, 24, 100, 32), outline=255, fill=255)
    disp.image(image)
    disp.display()
    GPIO.output(4, GPIO.LOW)
    time.sleep(delay)
    disp.clear()


# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)
disp.display()
disp.clear()

# begin breathing algo
draw.text((8, top), "You're ok,", font=font, fill=255)
draw.text((8, top + 8), "your stress device", font=font, fill=255)
draw.text((8, top + 16), "has your back!", font=font, fill=255)
disp.image(image)
disp.display()
time.sleep(2)
disp.clear()
draw.rectangle((0, 0, width, height), outline=0, fill=0)
disp.display()
disp.clear()

# breath in 5 sec
draw.text((8, top), "Breath in...", font=font, fill=255)
disp.image(image)
disp.display()
bardraw(0.5)
draw.rectangle((0, 0, width, height), outline=0, fill=0)
disp.display(0.5)
disp.clear()
draw.text((8, top), "hold...", font=font, fill=255)
disp.image(image)
disp.display()
bardraw(0.5)
draw.rectangle((0, 0, width, height), outline=0, fill=0)
disp.display()
disp.clear()
draw.text((8, top), "Breath Out...", font=font, fill=255)
disp.image(image)
disp.display()
bardraw(0.5)
print("done")
