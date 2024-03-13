import os
import sys
import time

# Set bit for calibration routine
print ('Assert RST_EXT1,2, followed by TRIGGER, then release RST_EXT1,2 and TRIGGER 15us later')
os.system('poke 0x43c00000 0x00004000') # bit 14
time.sleep(0.5)
os.system('poke 0x43c00000 0x00000000')
