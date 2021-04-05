# This script is for normal operation of the stress monitoring device

# importing needed libraries
import time
from max30105 import MAX30105, HeartRate
import math
from ina219 import INA219
from ina219 import DeviceRangeError
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# initializing devices
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
# initializing current sensor
SHUNT_OHMS = 0.1
ina = INA219(SHUNT_OHMS)
ina.configure()
# initializing ppg sensor
timeZero = time.perf_counter()
max30105 = MAX30105()
max30105.setup(leds_enable=2)

max30105.set_led_pulse_amplitude(1, 0.2)
max30105.set_led_pulse_amplitude(2, 12.5)
max30105.set_led_pulse_amplitude(3, 0)

max30105.set_slot_mode(1, 'red')
max30105.set_slot_mode(2, 'ir')
max30105.set_slot_mode(3, 'off')
max30105.set_slot_mode(4, 'off')
hr = HeartRate(max30105)

# function for breathing exercise visual
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
# function to collect data in intervals defined by function arguments
def datacollect(runtime):
    collectTime = []
    collectPPG = []
    result = 0
    for i in range(0, runtime):
        collectTime.append(time.perf_counter())
        samples = max30105.get_samples()
        if samples is not None:
            for k in range(0, len(samples), 2):
                # Process the least significant byte, where most wiggling is
                ir = samples[k + 1] & 0xff
                d = hr.low_pass_fir(ir)
                result = d[1] / 2

        else:
            result = "none"
        collectPPG.append(result)
        time.sleep(0.01)
    return collectTime, collectPPG


# function to split data into peaks and calculate HRV
def hrv(sensordata):
    ppg = []
    senstime = []
    # splitting 2D array into 2, 1D arrays
    for i in range(0, len(sensordata)):
        ppg.append(sensordata[0][i])
        senstime.append(sensordata[1][i])
    divWidth = 12
    divNum = int(math.ceil(len(ppg) / divWidth))
    peakTimes = []
    highest = 0.0
    highSpot = 0
    # splitting data into sections containing peaks & finding max point in each
    for i in range(0, divNum - 1):
        for k in range(0, divWidth):
            index = (i * divWidth) + k
            if index < len(ppg):
                value = float(ppg[index])
                if value > highest:
                    highSpot = index
                    highest = float(ppg[index])
            else:
                continue
        peakTimes.append(highSpot)
        highest = 0
    # Getting magnitude of time and ppg at max time intervals
    ppgPeak = []
    timePeak = []
    for k in range(0, len(peakTimes)):
        ppgPeak.append(ppg[peakTimes[k]])
        timePeak.append(senstime[peakTimes[k]])

    # determining peaks
    RPeakI = []
    RPeakT = []
    RPeakM = []
    past = 0
    # var to define 'close' position to border of cells, kept outside for fine tuning during dev
    b = 6
    for i in range(0, len(peakTimes)):
        lowBound = 12 * i
        highBound = lowBound + 12
        current = int(peakTimes[i])
        if (i + 1) < len(peakTimes):
            future = int(peakTimes[i + 1])
        if i > 0:
            past = int(peakTimes[i - 1])
        # if point is within 0.25s bin
        if (current > lowBound) and (current < highBound):
            # and if point is sufficiently far from bins border
            if ((current - b) >= lowBound) and ((current + b) <= highBound):
                RPeakI.append(current)
            # if point is close to low border & not in first bin
            if ((current - b) < lowBound) and (i != 0):
                # and current is bigger than last bin
                if float(ppg[current]) > float(ppg[past]):
                    RPeakI.append(current)
                elif (current - past) > 12:
                    RPeakI.append(current)
            # if point is close to low border & in first bin
            if ((current - b) < lowBound) and (i == 0):
                RPeakI.append(current)
            # if point is close to high border & not in last bin
            if ((current + b) > highBound) and (i != len(ppgPeak)):
                # and if current is higher than next
                if float(ppg[current]) > float(ppg[future]):
                    RPeakI.append(current)
                # if smaller but sufficiently far
                elif (future - current) > 12:
                    RPeakI.append(current)
            # if point is close to high border & in last bin
            if ((current + b) > highBound) and (i == (len(ppgPeak) - 1)):
                RPeakI.append(current)
        # if point is on low end & not at 0 position
        if (current == lowBound) and (current != 0):
            # if magnitude of previous is higher, not a peak
            if float(ppg[past]) > float(ppg[current]):
                continue
            elif float(ppg[past]) < float(ppg[current]):
                RPeakI.append(current)
        # if point is on low end & at 0 position
        if (current == lowBound) and (current == 0):
            # check if next is close to bin border
            # if close and magnitude is higher, current is not a peak and vise versa
            if (future - b) > highBound:
                RPeakI.append(current)
            elif ((future - b) <= highBound) and (float(ppg[future]) > float(ppg[current])):
                continue
            elif ((future - b) <= highBound) and (float(ppg[future]) < float(ppg[current])):
                RPeakI.append(current)
        # if point is on high end & not last position
        if (current == highBound) and (current != len(ppg)):
            # if magnitude of next is higher, not a peak
            if float(ppg[future]) > float(ppg[current]):
                continue
            elif float(ppg[future]) < float(ppg[current]):
                RPeakI.append(current)
        # if point is on high end & last position
        if (current == highBound) and (current == len(ppg)):
            # check if past is close to bin border
            # if close and magnitude is higher, current is not a peak and vise versa
            if (past + b) < lowBound:
                RPeakI.append(current)
            elif ((past + b) >= lowBound) and (float(ppg[past]) > float(ppg[current])):
                continue
            elif ((past + b) >= lowBound) & (float(ppg[past]) < float(ppg[current])):
                RPeakI.append(current)
    for k in range(0, len(RPeakI)):
        RPeakT.append(senstime[RPeakI[k]])
        RPeakM.append(ppg[RPeakI[k]])

    # Calculating HRV
    HRV = []
    for j in range(0, len(RPeakT)):
        if (j + 1) < len(RPeakT):
            diff = float(RPeakT[j + 1]) - float(RPeakT[j])
            HRV.append(diff)
    return HRV


# function to see if battery is below 25%
def checkbatt(timezero):
    current = ina.current()
    present = time.perf_counter()
    presentNum = (present - timezero) / 60
    capacity = presentNum * current
    if capacity >= 0.375:
        return "False"
    else:
        return "True"


# function to output breathing algorithm to ppg sensor
def breathingalgo(ppg):
    calm = "False"
    delay = 0.5
    while calm == "False":
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
        bardraw(delay)
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        disp.display(0.5)
        disp.clear()
        draw.text((8, top), "hold...", font=font, fill=255)
        disp.image(image)
        disp.display()
        bardraw(delay)
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        disp.display()
        disp.clear()
        draw.text((8, top), "Breath Out...", font=font, fill=255)
        disp.image(image)
        disp.display()
        bardraw(delay)
        # collect 2s of new data to compare HRV
        newData = datacollect(200)
        variability = hrv(newData)
        RMSSD = (sum(variability)) / (len(variability))
        if (RMSSD < ppg) and (RMSSD < 0.65):
            calm = "True"
        else:
            calm = "False"
            delay = delay+0.1


# running of main code
charged = "True"
while charged == "True":
    charged = checkbatt(timeZero)
    # collect 3 min of data
    ppgCollect = datacollect(18000)
    filtered = hrv(ppgCollect)
    RMSSD = (sum(filtered)) / (len(filtered))
    if RMSSD < 0.65:
        breathingalgo(RMSSD)
    else:
        HR = (len(ppgCollect))/3
        draw.text((8, 32), "HR: {} BPM".format(HR), font=font, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(3)
        disp.clear()
