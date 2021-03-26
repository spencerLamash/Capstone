# This script was utilized to collect ppg data for acceptance testing verification

import time
from max30105 import MAX30105, HeartRate

file = open("Test.txt", "w")
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
time.sleep(10)

for i in range(0, 6000):
    secs = str(time.perf_counter())
    file.write(secs)
    file.write(" , ")
    samples = max30105.get_samples()
    if samples is not None:
        for k in range(0, len(samples), 2):
            # Process the least significant byte, where most wiggling is
            ir = samples[k + 1] & 0xff
            d = hr.low_pass_fir(ir)
            result = d[1]/2

    else:
        result = "none"
    file.write(str(result))
    file.write("\n")
    time.sleep(0.01)
file.close()
print("Data Collected!")
