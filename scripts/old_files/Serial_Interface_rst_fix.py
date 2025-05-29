import os
import sys
import time

print ('Resetting serial interfaces')

os.system('poke 0x43c00004 0x00000200') # bit 8
print ('Asserting opad_selDefData')
time.sleep(0.5)

os.system('poke 0x43c00004 0x00000300') # bits 8,9
print ('Sending 100us pulse on opad_loadData')
time.sleep(0.5)

os.system('poke 0x43c00004 0x00000000')
print ('De-asserting opad_selDefData')
time.sleep(0.5)

os.system('poke 0x43c0000c 0x00000200') # repeat on interface #2
print ('Asserting opad2_selDefData')
time.sleep(0.5)

os.system('poke 0x43c0000c 0x00000300')
print ('Sending 100us pulse on opad2_loadData')
time.sleep(0.5)

os.system('poke 0x43c0000c 0x00000000')
print ('De-asserting opad2_selDefData')
