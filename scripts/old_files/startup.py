import os
import sys
import time

# All pads are at logic 0V
# This just resets FPGA internal logic
os.system('poke 0x43c00000 0x00000001')
print ('Asserting master logic reset')
time.sleep(0.5)
os.system('poke 0x43c00000 0x00000000')
