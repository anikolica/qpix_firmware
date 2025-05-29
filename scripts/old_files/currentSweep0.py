# Written by PURM Students Summer 2024
# Meant to run get_samples.py multiple times for each current setting and provide basic data on the results
# Uses "samplesCollection.py"
# curReplen bits are at [0,0,0] (high)
# python3 currentSweep0.py [# of runs]

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
print(f'Running DECIMAL {decimalNum} :')
decimalNum -= 1

# Programming the serial interface to a replenCur bit (this one is 31)
os.system('python3 Serial_Interface.py  1  0xF1B6FFC6')
os.system('python3 Serial_Interface.py  2  0xF1B6FFC6')

os.system(f'python3 samplesCollection.py {testNum}')

time.sleep(5)

# DECIMAL 30
print(f'Running DECIMAL {decimalNum} :')
decimalNum -= 1

os.system('python3 Serial_Interface.py  1  0xF1B6FF46')
os.system('python3 Serial_Interface.py  2  0xF1B6FF46')

os.system(f'python3 samplesCollection.py {testNum}')

time.sleep(5)

# DECIMAL 29
print(f'Running DECIMAL {decimalNum} :')
decimalNum -= 1

os.system('python3 Serial_Interface.py  1  0x71B6FFC6')
os.system('python3 Serial_Interface.py  2  0x71B6FFC6')

os.system(f'python3 samplesCollection.py {testNum}')

time.sleep(5)

# DECIMAL 28
print(f'Running DECIMAL {decimalNum} :')
decimalNum -= 1

os.system('python3 Serial_Interface.py  1  0x71B6FF46')
os.system('python3 Serial_Interface.py  2  0x71B6FF46')

os.system(f'python3 samplesCollection.py {testNum}')

time.sleep(5)

# DECIMAL 27
print(f'Running DECIMAL {decimalNum} :')
decimalNum -= 1

os.system('python3 Serial_Interface.py  1  0xB1B6FFC6')
os.system('python3 Serial_Interface.py  2  0xB1B6FFC6')

os.system(f'python3 samplesCollection.py {testNum}')

time.sleep(5)

# DECIMAL 26
print(f'Running DECIMAL {decimalNum} :')
decimalNum -= 1

os.system('python3 Serial_Interface.py  1  0xB1B6FF46')
os.system('python3 Serial_Interface.py  2  0xB1B6FF46')

os.system(f'python3 samplesCollection.py {testNum}')

time.sleep(5)

# DECIMAL 25
print(f'Running DECIMAL {decimalNum} :')
decimalNum -= 1

os.system('python3 Serial_Interface.py  1  0x31B6FFC6')
os.system('python3 Serial_Interface.py  2  0x31B6FFC6')

os.system(f'python3 samplesCollection.py {testNum}')

time.sleep(5)

# DECIMAL 24
print(f'Running DECIMAL {decimalNum} :')
decimalNum -= 1

os.system('python3 Serial_Interface.py  1  0x31B6FF46')
os.system('python3 Serial_Interface.py  2  0x31B6FF46')

os.system(f'python3 samplesCollection.py {testNum}')

time.sleep(5)

# DECIMAL 23
print(f'Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0xD1B6FFC6')
os.system('python3 Serial_Interface.py  2  0xD1B6FFC6')

os.system(f'python3 samplesCollection.py {testNum}')

time.sleep(5)

# DECIMAL 22
print(f'Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0xD1B6FF46')
os.system('python3 Serial_Interface.py  2  0xD1B6FF46')

os.system(f'python3 samplesCollection.py {testNum}')

time.sleep(5)

# DECIMAL 21
print(f'Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0x51B6FFC6')
os.system('python3 Serial_Interface.py  2  0x51B6FFC6')

os.system(f'python3 samplesCollection.py {testNum}')

time.sleep(5)

# DECIMAL 20
print(f'Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0x51B6FF46')
os.system('python3 Serial_Interface.py  2  0x51B6FF46')

os.system(f'python3 samplesCollection.py {testNum}')

time.sleep(5)

# DECIMAL 19
print(f'Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0x91B6FFC6')
os.system('python3 Serial_Interface.py  2  0x91B6FFC6')

os.system(f'python3 samplesCollection.py {testNum}')

time.sleep(5)

# DECIMAL 18
print(f'Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0x91B6FF46')
os.system('python3 Serial_Interface.py  2  0x91B6FF46')

os.system(f'python3 samplesCollection.py {testNum}')

time.sleep(5)

# DECIMAL 17
print(f'Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0x11B6FFC6')
os.system('python3 Serial_Interface.py  2  0x11B6FFC6')

os.system(f'python3 samplesCollection.py {testNum}')

time.sleep(5)

# DECIMAL 16
print(f'Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0x11B6FF46')
os.system('python3 Serial_Interface.py  2  0x11B6FF46')

os.system(f'python3 samplesCollection.py {testNum}')

time.sleep(5)

# DECIMAL 15
print(f'Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0xE1B6FFC6')
os.system('python3 Serial_Interface.py  2  0xE1B6FFC6')

os.system(f'python3 samplesCollection.py {testNum}')

time.sleep(5)

# DECIMAL 14
print(f'Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0xE1B6FF46')
os.system('python3 Serial_Interface.py  2  0xE1B6FF46')

os.system(f'python3 samplesCollection.py {testNum}')

time.sleep(5)

# DECIMAL 13
print(f'Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0x61B6FFC6')
os.system('python3 Serial_Interface.py  2  0x61B6FFC6')

os.system(f'python3 samplesCollection.py {testNum}')

time.sleep(5)

# DECIMAL 12
print(f'Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0x61B6FF46')
os.system('python3 Serial_Interface.py  2  0x61B6FF46')

os.system(f'python3 samplesCollection.py {testNum}')

time.sleep(5)

# DECIMAL 11
print(f'Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0xA1B6FFC6')
os.system('python3 Serial_Interface.py  2  0xA1B6FFC6')

os.system(f'python3 samplesCollection.py {testNum}')

time.sleep(5)

# DECIMAL 10
print(f'Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0xA1B6FF46')
os.system('python3 Serial_Interface.py  2  0xA1B6FF46')

os.system(f'python3 samplesCollection.py {testNum}')

time.sleep(5)

# DECIMAL 9
print(f'Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0x21B6FFC6')
os.system('python3 Serial_Interface.py  2  0x21B6FFC6')

os.system(f'python3 samplesCollection.py {testNum}')

time.sleep(5)

# DECIMAL 8
print(f'Running DECIMAL {decimalNum} :')
decimalNum -= 1
os.system('python3 Serial_Interface.py  1  0x21B6FF46')
os.system('python3 Serial_Interface.py  2  0x21B6FF46')

os.system(f'python3 samplesCollection.py {testNum}')

time.sleep(5)
