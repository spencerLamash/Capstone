# This script is used to collect current and voltage data throughout a charging cycle
import time
from ina219 import INA219
from ina219 import DeviceRangeError

# creating file for data output
file = open("Charge.txt", "w")

# initializing current sensor
SHUNT_OHMS = 0.1
ina =INA219(SHUNT_OHMS)
ina.configure()

# Assuming 1hr charge time, outputting current & voltage every min
for i in range(0, 90):
    file.write(ina.current())
    file.write(", ")
    file.write(ina.voltage())
    file.write("\n")
    time.sleep(60)
file.close()
print("program complete!")


