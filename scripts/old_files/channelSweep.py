# Written by PURM Students Summer 2024
# Meant to run get_samples.py multiple times for each current setting and provide basic data on the results
# python3 currentSweep.py [# of runs]

import os
import sys
import time
import math 

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
print('Running DECIMAL {decimalNum} :')
decimalNum -= 1

os.system('python3 Serial_Interface.py  1  0xF5B6FFC6')
os.system('python3 Serial_Interface.py  2  0xF5B6FFC6')

os.system('python3 channelRunsJuly1.py {testNum}')

# DECIMAL 30
print('Running DECIMAL {decimalNum} :')
decimalNum -= 1

os.system('python3 Serial_Interface.py  1  0xF5B6FF46')
os.system('python3 Serial_Interface.py  2  0xF5B6FF46')

os.system('python3 channelRunsJuly1.py {testNum}')

# DECIMAL 29
print('Running DECIMAL {decimalNum} :')
decimalNum -= 1

os.system('python3 Serial_Interface.py  1  0x75B6FFC6')
os.system('python3 Serial_Interface.py  2  0x75B6FFC6')

os.system('python3 channelRunsJuly1.py {testNum}')

# DECIMAL 28
print('Running DECIMAL {decimalNum} :')
decimalNum -= 1

os.system('python3 Serial_Interface.py  1  0x75B6FF46')
os.system('python3 Serial_Interface.py  2  0x75B6FF46')

os.system('python3 channelRunsJuly1.py {testNum}')

# DECIMAL 27
print('Running DECIMAL {decimalNum} :')
decimalNum -= 1

os.system('python3 Serial_Interface.py  1  0xB5B6FFC6')
os.system('python3 Serial_Interface.py  2  0xB5B6FFC6')

os.system('python3 channelRunsJuly1.py {testNum}')

# DECIMAL 26
print('Running DECIMAL {decimalNum} :')
decimalNum -= 1

os.system('python3 Serial_Interface.py  1  0xB5B6FF46')
os.system('python3 Serial_Interface.py  2  0xB5B6FF46')

os.system('python3 channelRunsJuly1.py {testNum}')

# DECIMAL 25
print('Running DECIMAL {decimalNum} :')
decimalNum -= 1

os.system('python3 Serial_Interface.py  1  0x35B6FFC6')
os.system('python3 Serial_Interface.py  2  0x35B6FFC6')

os.system('python3 channelRunsJuly1.py {testNum}')

# DECIMAL 24
print('Running DECIMAL {decimalNum} :')
decimalNum -= 1

os.system('python3 Serial_Interface.py  1  0x35B6FF46')
os.system('python3 Serial_Interface.py  2  0x35B6FF46')

os.system('python3 channelRunsJuly1.py {testNum}')

# DECIMAL 23
print('Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0xD5B6FFC6')
os.system('python3 Serial_Interface.py  2  0xD5B6FFC6')

os.system('python3 channelRunsJuly1.py {testNum}')

# DECIMAL 22
print('Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0xD5B6FF46')
os.system('python3 Serial_Interface.py  2  0xD5B6FF46')

os.system('python3 channelRunsJuly1.py {testNum}')

# DECIMAL 21
print('Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0x55B6FFC6')
os.system('python3 Serial_Interface.py  2  0x55B6FFC6')

os.system('python3 channelRunsJuly1.py {testNum}')

# DECIMAL 20
print('Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0x55B6FF46')
os.system('python3 Serial_Interface.py  2  0x55B6FF46')

os.system('python3 channelRunsJuly1.py {testNum}')

# DECIMAL 19
print('Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0x95B6FFC6')
os.system('python3 Serial_Interface.py  2  0x95B6FFC6')

os.system('python3 channelRunsJuly1.py {testNum}')

# DECIMAL 18
print('Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0x95B6FF46')
os.system('python3 Serial_Interface.py  2  0x95B6FF46')

os.system('python3 channelRunsJuly1.py {testNum}')

# DECIMAL 17
print('Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0x15B6FFC6')
os.system('python3 Serial_Interface.py  2  0x15B6FFC6')

os.system('python3 channelRunsJuly1.py {testNum}')

# DECIMAL 16
print('Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0x15B6FF46')
os.system('python3 Serial_Interface.py  2  0x15B6FF46')

os.system('python3 channelRunsJuly1.py {testNum}')

# DECIMAL 15
print('Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0xE5B6FFC6')
os.system('python3 Serial_Interface.py  2  0xE5B6FFC6')

os.system('python3 channelRunsJuly1.py {testNum}')

# DECIMAL 14
print('Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0xE5B6FF46')
os.system('python3 Serial_Interface.py  2  0xE5B6FF46')

os.system('python3 channelRunsJuly1.py {testNum}')

# DECIMAL 13
print('Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0x65B6FFC6')
os.system('python3 Serial_Interface.py  2  0x65B6FFC6')

os.system('python3 channelRunsJuly1.py {testNum}')

# DECIMAL 12
print('Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0x65B6FF46')
os.system('python3 Serial_Interface.py  2  0x65B6FF46')

os.system('python3 channelRunsJuly1.py {testNum}')

# DECIMAL 11
print('Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0xA5B6FFC6')
os.system('python3 Serial_Interface.py  2  0xA5B6FFC6')

os.system('python3 channelRunsJuly1.py {testNum}')

# DECIMAL 10
print('Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0xA5B6FF46')
os.system('python3 Serial_Interface.py  2  0xA5B6FF46')

os.system('python3 channelRunsJuly1.py {testNum}')

# DECIMAL 9
print('Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0x25B6FFC6')
os.system('python3 Serial_Interface.py  2  0x25B6FFC6')

os.system('python3 channelRunsJuly1.py {testNum}')

# DECIMAL 8
print('Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0x25B6FF46')
os.system('python3 Serial_Interface.py  2  0x25B6FF46')

os.system('python3 channelRunsJuly1.py {testNum}')

