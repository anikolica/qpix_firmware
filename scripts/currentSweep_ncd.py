# Written by PURM Students Summer 2024
# Meant to run get_samples.py multiple times for each current setting and provide basic data on the results
# Uses "samplesCollection.py"
# curReplen bits are at [0,1,0] (default)
# python3 currentSweep.py [# of runs]

import os
import sys
import time
import math 
import sample_ncd as s

## USAGE: python3 currentSweep_ncd.py numTrials
## numTrials: repeat measurment 'numTrials' times
##  DECIMAL_replen: replenishment value (Decimal 1 - 31)
## -ncd

numTrials = 10


os.system('rm fch*')  # remove the 16 individual channel files -ncd


# DECIMAL 31
print("Running DECIMAL_replen: 31")
# Programming the serial interface to a replenCur bit (this one is 31)
os.system('python3 Serial_Interface.py  1  0xF5B6FFC6')
os.system('python3 Serial_Interface.py  2  0xF5B6FFC6')
s.sample(numTrials, 31)

# DECIMAL 30
print("Running DECIMAL_replen: 30")
os.system('python3 Serial_Interface.py  1  0xF5B6FF46')
os.system('python3 Serial_Interface.py  2  0xF5B6FF46')
s.sample(numTrials, 30)

# DECIMAL 29
print("Running DECIMAL_replen: 29")
os.system('python3 Serial_Interface.py  1  0x75B6FFC6')
os.system('python3 Serial_Interface.py  2  0x75B6FFC6')
s.sample(numTrials, 29)

# DECIMAL 28
print("Running DECIMAL_replen: 28")
os.system('python3 Serial_Interface.py  1  0x75B6FF46')
os.system('python3 Serial_Interface.py  2  0x75B6FF46')
s.sample(numTrials, 28)

# DECIMAL 27
print("Running DECIMAL_replen: 27")
os.system('python3 Serial_Interface.py  1  0xB5B6FFC6')
os.system('python3 Serial_Interface.py  2  0xB5B6FFC6')
s.sample(numTrials, 27)


# DECIMAL 26
print("Running DECIMAL_replen: 26")
os.system('python3 Serial_Interface.py  1  0xB5B6FF46')
os.system('python3 Serial_Interface.py  2  0xB5B6FF46')
s.sample(numTrials, 26)

# DECIMAL 25
print("Running DECIMAL_replen: 25")
os.system('python3 Serial_Interface.py  1  0x35B6FFC6')
os.system('python3 Serial_Interface.py  2  0x35B6FFC6')
s.sample(numTrials, 25)

# DECIMAL 24
print("Running DECIMAL_replen: 24")
os.system('python3 Serial_Interface.py  1  0x35B6FF46')
os.system('python3 Serial_Interface.py  2  0x35B6FF46')
s.sample(numTrials, 24)

# DECIMAL 23
print("Running DECIMAL_replen: 23")
os.system('python3 Serial_Interface.py  1  0xD5B6FFC6')
os.system('python3 Serial_Interface.py  2  0xD5B6FFC6')
s.sample(numTrials, 23)

# DECIMAL 22
print("Running DECIMAL_replen: 22")
os.system('python3 Serial_Interface.py  1  0xD5B6FF46')
os.system('python3 Serial_Interface.py  2  0xD5B6FF46')
s.sample(numTrials, 22)

# DECIMAL 21
print("Running DECIMAL_replen: 21")
os.system('python3 Serial_Interface.py  1  0x55B6FFC6')
os.system('python3 Serial_Interface.py  2  0x55B6FFC6')
s.sample(numTrials, 21)

# DECIMAL 20
print("Running DECIMAL_replen: 20")
os.system('python3 Serial_Interface.py  1  0x55B6FF46')
os.system('python3 Serial_Interface.py  2  0x55B6FF46')
s.sample(numTrials, 20)
"""
# DECIMAL 19
print("Running DECIMAL_replen: 19")
os.system('python3 Serial_Interface.py  1  0x95B6FFC6')
os.system('python3 Serial_Interface.py  2  0x95B6FFC6')
s.sample(numTrials, 19)

# DECIMAL 18
print("Running DECIMAL_replen: 18")
os.system('python3 Serial_Interface.py  1  0x95B6FF46')
os.system('python3 Serial_Interface.py  2  0x95B6FF46')
s.sample(numTrials, 18)

# DECIMAL 17
print("Running DECIMAL_replen: 17")
os.system('python3 Serial_Interface.py  1  0x15B6FFC6')
os.system('python3 Serial_Interface.py  2  0x15B6FFC6')
s.sample(numTrials, 17)

# DECIMAL 16
print("Running DECIMAL_replen: 16")
os.system('python3 Serial_Interface.py  1  0x15B6FF46')
os.system('python3 Serial_Interface.py  2  0x15B6FF46')
s.sample(numTrials, 16)

# DECIMAL 15
print("Running DECIMAL_replen: 15")
os.system('python3 Serial_Interface.py  1  0xE5B6FFC6')
os.system('python3 Serial_Interface.py  2  0xE5B6FFC6')
s.sample(numTrials, 15)

# DECIMAL 14
print("Running DECIMAL_replen: 14")
os.system('python3 Serial_Interface.py  1  0xE5B6FF46')
os.system('python3 Serial_Interface.py  2  0xE5B6FF46')
s.sample(numTrials, 14)

# DECIMAL 13
print("Running DECIMAL_replen: 13")
os.system('python3 Serial_Interface.py  1  0x65B6FFC6')
os.system('python3 Serial_Interface.py  2  0x65B6FFC6')
s.sample(numTrials, 13)

# DECIMAL 12
print("Running DECIMAL_replen: 12")
os.system('python3 Serial_Interface.py  1  0x65B6FF46')
os.system('python3 Serial_Interface.py  2  0x65B6FF46')
s.sample(numTrials, 12)

# DECIMAL 11
print("Running DECIMAL_replen: 11")
os.system('python3 Serial_Interface.py  1  0xA5B6FFC6')
os.system('python3 Serial_Interface.py  2  0xA5B6FFC6')
s.sample(numTrials, 11)

# DECIMAL 10
print("Running DECIMAL_replen: 10")
os.system('python3 Serial_Interface.py  1  0xA5B6FF46')
os.system('python3 Serial_Interface.py  2  0xA5B6FF46')
s.sample(numTrials, 10)

# DECIMAL 9
print("Running DECIMAL_replen: 9")
os.system('python3 Serial_Interface.py  1  0x25B6FFC6')
os.system('python3 Serial_Interface.py  2  0x25B6FFC6')
s.sample(numTrials, 9)

# DECIMAL 8
print("Running DECIMAL_replen: 8")
os.system('python3 Serial_Interface.py  1  0x25B6FF46')
os.system('python3 Serial_Interface.py  2  0x25B6FF46')
s.sample(numTrials, 8)
"""



