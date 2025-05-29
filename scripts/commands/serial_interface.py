#### SERIAL INTERFACE ############################
# Authors: AN, ACG
# Usage: python3 serial_interface.py [1 or 2] [data in 32-bit hex]
# Notes: reset serial interfaces first
##################################################

import os
import sys
import time

# serial interface 1 or 2
if sys.argv[1] == '1':
    interface = sys.argv[1]
    ctrl_addr = '0x43c00004 '
    data_addr = '0x43c00008 '
elif sys.argv[1] == '2':
    interface = sys.argv[1]
    ctrl_addr = '0x43c0000c '
    data_addr = '0x43c00010 '
else:
    print ('Invalid serial interface!')

# Input data in 32-bit hext, e.g. 0x12345678
data = sys.argv[2]

print ('Programming QPix interface ' + interface + ' with data: ' + data)
os.system('poke ' + data_addr + data) # write data into internal reg
print ('Loading internal reg')
time.sleep(0.5)

os.system('poke ' + ctrl_addr + '0x00000002') # bit 1
print ('Loading data into FGPA shift register')
time.sleep(0.5)
os.system('poke ' + ctrl_addr + '0x00000000') # de-assert bit 1
time.sleep(0.5)

os.system('poke ' + ctrl_addr + '0x00000004') # bit 2
print ('Shift out to QPix with gated clock')
time.sleep(0.01)

os.system('poke ' + ctrl_addr + '0x00000100') # bit 8
print ('Shift out to QPix with gated clock')
time.sleep(0.5)
os.system('poke ' + ctrl_addr + '0x00000000') # de-assert bits 2,8
