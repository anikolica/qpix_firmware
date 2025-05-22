# Program to run QPIX Calibration Sweep -srak 3/26/2025
# Written by Student
# Meant to run get_samples.py multiple times for each current setting and provide basic data on the results
# Uses "samplesCollection.py"
# curReplen bits are at [0,1,0] (default)
# 

import os
import sys
import time
import math 
import sample_cal_srak as s

## USAGE: python3 currentSweep_ncd.py numTrials
## numTrials: repeat measurment 'numTrials' times
##  DECIMAL_replen: replenishment value (Decimal 1 - 31)
## -ncd

numTrials = 5


os.system('rm fch*')  # remove the 16 individual channel files -ncd


ch0Counts = []
ch1Counts = []
ch2Counts = []
ch3Counts = []
ch4Counts = []
ch5Counts = []
ch6Counts = []
ch7Counts = []
ch8Counts = []
ch9Counts = []
ch10Counts = []

ch11Counts = []
ch12Counts = []

ch13Counts = []
ch14Counts = []
ch15Counts = []

#Define channelCounts which stores the number of resets in a given channel
channelCounts=[ch0Counts, ch1Counts, ch2Counts, ch3Counts, ch4Counts, ch5Counts, ch6Counts, ch7Counts, ch8Counts, ch9Counts, ch10Counts, ch11Counts, ch12Counts, ch13Counts, ch14Counts, ch15Counts]


copy_channelCounts = channelCounts.copy() # Make a backup copy of this list -ncd

channelCounts = copy_channelCounts.copy() # Then revert to it!  -ncd


# DECIMAL 31
print("Running DECIMAL_replen: 31")
# Programming the serial interface to a replenCur bit (this one is 31)
os.system('python3 Serial_Interface.py  2  0xF5B6FFC4')
s.sample_cal(numTrials, 31)

# DECIMAL 30
print("Running DECIMAL_replen: 30")
os.system('python3 Serial_Interface.py  2  0xF5B6FF44')
s.sample_cal(numTrials, 30)

# DECIMAL 29
print("Running DECIMAL_replen: 29")
os.system('python3 Serial_Interface.py  2  0x75B6FFC4')
s.sample_cal(numTrials, 29)

# DECIMAL 28
print("Running DECIMAL_replen: 28")
os.system('python3 Serial_Interface.py  2  0x75B6FF44')
s.sample_cal(numTrials, 28)

# DECIMAL 27
print("Running DECIMAL_replen: 27")
os.system('python3 Serial_Interface.py  2  0xB5B6FFC4')
s.sample_cal(numTrials, 27)


# DECIMAL 26
print("Running DECIMAL_replen: 26")
os.system('python3 Serial_Interface.py  2  0xB5B6FF44')
s.sample_cal(numTrials, 26)

# DECIMAL 25
print("Running DECIMAL_replen: 25")
os.system('python3 Serial_Interface.py  2  0x35B6FFC4')
s.sample_cal(numTrials, 25)

# DECIMAL 24
print("Running DECIMAL_replen: 24")
os.system('python3 Serial_Interface.py  2  0x35B6FF44')
s.sample_cal(numTrials, 24)

# DECIMAL 23
print("Running DECIMAL_replen: 23")
os.system('python3 Serial_Interface.py  2  0xD5B6FFC4')
s.sample_cal(numTrials, 23)

#channelCounts = copy_channelCounts.copy() # Then revert to it!  -ncd
# DECIMAL 22
print("Running DECIMAL_replen: 22")
os.system('python3 Serial_Interface.py  2  0xD5B6FF44')
s.sample_cal(numTrials, 22)

#channelCounts = copy_channelCounts.copy() # Then revert to it!  -ncd
# DECIMAL 21
print("Running DECIMAL_replen: 21")
os.system('python3 Serial_Interface.py  2  0x55B6FFC4')
s.sample_cal(numTrials, 21)

# DECIMAL 20
print("Running DECIMAL_replen: 20")
os.system('python3 Serial_Interface.py  2  0x55B6FF44')
s.sample_cal(numTrials, 20)

# DECIMAL 19
print("Running DECIMAL_replen: 19")
os.system('python3 Serial_Interface.py  2  0x95B6FFC4')
s.sample_cal(numTrials, 19)

# DECIMAL 18
print("Running DECIMAL_replen: 18")
os.system('python3 Serial_Interface.py  2  0x95B6FF44')
s.sample_cal(numTrials, 18)

# DECIMAL 17
print("Running DECIMAL_replen: 17")
os.system('python3 Serial_Interface.py  2  0x15B6FFC4')
s.sample_cal(numTrials, 17)

# DECIMAL 16
print("Running DECIMAL_replen: 16")
os.system('python3 Serial_Interface.py  2  0x15B6FF44')
s.sample_cal(numTrials, 16)


# DECIMAL 15
print("Running DECIMAL_replen: 15")
os.system('python3 Serial_Interface.py  2  0xE5B6FFC4')
s.sample_cal(numTrials, 15)


# DECIMAL 14
print("Running DECIMAL_replen: 14")
os.system('python3 Serial_Interface.py  1  0xE5B6FF44')
s.sample_cal(numTrials, 14)

# DECIMAL 13
print("Running DECIMAL_replen: 13")
os.system('python3 Serial_Interface.py  1  0x65B6FFC4')
s.sample_cal(numTrials, 13)

# DECIMAL 12
print("Running DECIMAL_replen: 12")
os.system('python3 Serial_Interface.py  1  0x65B6FF44')
s.sample_cal(numTrials, 12)

# DECIMAL 11
print("Running DECIMAL_replen: 11")
os.system('python3 Serial_Interface.py  1  0xA5B6FFC4')
s.sample_cal(numTrials, 11)

# DECIMAL 10
print("Running DECIMAL_replen: 10")
os.system('python3 Serial_Interface.py  1  0xA5B6FF44')
s.sample_cal(numTrials, 10)

# DECIMAL 9
print("Running DECIMAL_replen: 9")
os.system('python3 Serial_Interface.py  1  0x25B6FFC4')
s.sample_cal(numTrials, 9)

# DECIMAL 8
print("Running DECIMAL_replen: 8")
os.system('python3 Serial_Interface.py  1  0x25B6FF44')
s.sample_cal(numTrials, 8)

"""
25B6FF44   8
25B6FFC4   9
A5B6FF44   10
A5B6FFC4   11
65B6FF44   12
65B6FFC4   13
E5B6FF44   14
E5B6FFC4   15
15B6FF44   16
15B6FFC4   17
95B6FF44   18
95B6FFC4   19
55B6FF44   20
55B6FFC4   21
D5B6FF44   22
D5B6FFC4   23
35B6FF44   24
35B6FFC4   25
B5B6FF44   26
B5B6FFC4   27
75B6FF44   28
75B6FFC4   29
F5B6FF44   30
F5B6FFC4   31
"""


command = dac_command(0, 0.7590, 1.000)   # 0.7611v (3896)
i2c_raw = os.popen(command).read()


