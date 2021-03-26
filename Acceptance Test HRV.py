# This script is used for acceptance tests to detect peaks and calculate HRV
# to then output to a text file for further analysis
# importing required libraries
import csv
import math

# reading in data set
with open('PyData2.csv') as data:
    dataRead = csv.reader(data, delimiter=',')
    time = []
    ppg = []

    for row in dataRead:
        time.append(row[0])
        ppg.append(row[1])

# Splitting data into 0.5s intervals to detect peaks, normal human HR is 60-100 bpm so every
# second can contain ~1.5 beats, therefore choose 0.25 sample intervals for peak detection
# sampling rate is ~50Hz therefore 12 samples~0.25s

divWidth = 12
divNum = int(math.ceil(len(ppg)/divWidth))
peakTimes = []
highest = 0.0
highSpot = 0

# splitting data into sections containing peaks & finding max point in each
for i in range(0, divNum-1):
    for k in range(0, divWidth):
        index = (i*divWidth)+k
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
    timePeak.append(time[peakTimes[k]])

# determining peaks
RPeakI = []
RPeakT = []
RPeakM = []
past = 0
# var to define 'close' position to border of cells, kept outside for fine tuning during dev
b = 6
for i in range(0, len(peakTimes)):
    lowBound = 12*i
    highBound = lowBound+12
    current = int(peakTimes[i])
    if (i+1) < len(peakTimes):
        future = int(peakTimes[i+1])
    if i > 0:
        past = int(peakTimes[i-1])
    # if point is within 0.25s bin
    if (current > lowBound) and (current < highBound):
        # and if point is sufficiently far from bins border
        if ((current-b) >= lowBound) and ((current + b) <= highBound):
            RPeakI.append(current)
        # if point is close to low border & not in first bin
        if ((current-b) < lowBound) and (i != 0):
            # and current is bigger than last bin
            if float(ppg[current]) > float(ppg[past]):
                RPeakI.append(current)
            elif (current-past) > 12:
                RPeakI.append(current)
        # if point is close to low border & in first bin
        if ((current - b) < lowBound) and (i == 0):
            RPeakI.append(current)
        # if point is close to high border & not in last bin
        if ((current+b) > highBound) and (i != len(ppgPeak)):
            # and if current is higher than next
            if float(ppg[current]) > float(ppg[future]):
                RPeakI.append(current)
            # if smaller but sufficiently far
            elif (future-current) > 12:
                RPeakI.append(current)
        # if point is close to high border & in last bin
        if ((current+b) > highBound) and (i == (len(ppgPeak)-1)):
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
        if (future-b) > highBound:
            RPeakI.append(current)
        elif ((future-b) <= highBound) and (float(ppg[future]) > float(ppg[current])):
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
        if (past+b) < lowBound:
            RPeakI.append(current)
        elif ((past+b) >= lowBound) and (float(ppg[past]) > float(ppg[current])):
            continue
        elif ((past+b) >= lowBound) & (float(ppg[past]) < float(ppg[current])):
            RPeakI.append(current)
for k in range(0, len(RPeakI)):
    RPeakT.append(time[RPeakI[k]])
    RPeakM.append(ppg[RPeakI[k]])

# Calculating HRV & RRMSSD
HRV =[]
RRMSSD = []
file = open("results.txt","w")
for j in range(0, len(RPeakT)):
    if (j+1) < len(RPeakT):
        diff = float(RPeakT[j+1])-float(RPeakT[j])
        HRV.append(diff)
        file.write(str(diff))
        file.write("\n")
