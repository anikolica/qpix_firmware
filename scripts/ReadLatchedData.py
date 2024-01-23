import os
import sys
import time

# serial interface 1 or 2
if sys.argv[1] == '1':
    interface = sys.argv[1]
    ctrl_addr = '0x43c00004 '
elif sys.argv[1] == '2':
    interface = sys.argv[1]
    ctrl_addr = '0x43c0000c '
else:
    print ('Invalid serial interface!')

os.system('poke ' + ctrl_addr + '0x00000010') # bit 4
print ('Raising serialOutCnt' + interface)
time.sleep(0.1)
os.system('poke ' + ctrl_addr + '0x00000000') # de-assert bit 4
time.sleep(0.1)

os.system('poke ' + ctrl_addr + '0x00000020') # bit 5
print ('Pulse 5us on opad' + interface + '_CLKin2')
time.sleep(0.1)
os.system('poke ' + ctrl_addr + '0x00000000') # de-assert bit 5
time.sleep(0.1)

os.system('poke ' + ctrl_addr + '0x00000040') # bit 6
print ('Sending 32 pulses on opad' + interface + '_CLKin2')
time.sleep(0.5)
os.system('poke ' + ctrl_addr + '0x00000000') # de-assert bit 6
