import os
import sys
import time

# Keep beta-multiplier startup pads high for all time
os.system('poke 0x43c00000 0x03000000') # bits 25,24
print ('Asserting opad_startup, opad2_startup')
