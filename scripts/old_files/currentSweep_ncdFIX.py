# Written by PURM Students Summer 2024
# Meant to run get_samples.py multiple times for each current setting and provide basic data on the results
# Uses "samplesCollection.py"
# curReplen bits are at [0,1,0] (default)
# python3 currentSweep.py [# of runs]

import os
import sys
import time
import math 
import csv
import sample_ncd as run




decimalNum = 31


# Take in user input
if len(sys.argv) < 2:
     testNum = 1
else:
     testNum = int(sys.argv[1])

# Edge case
if  (testNum == 0 or testNum == None):
    testNum = 1


# DECIMAL 31
print(f'Running DECIMAL {decimalNum} :')
decimalNum -= 1

# Programming the serial interface to a replenCur bit (this one is 31)

os.system('python3 Serial_Interface.py  1  0xF5B6FFC6')
os.system('python3 Serial_Interface.py  2  0xF5B6FFC6')
run.sample(testNum)

# DECIMAL 30
print(f'Running DECIMAL {decimalNum} :')
decimalNum -= 1

os.system('python3 Serial_Interface.py  1  0xF5B6FF46')
os.system('python3 Serial_Interface.py  2  0xF5B6FF46')
run.sample(testNum)



