import os
import sys
import time

# Set bit for calibration routine
print ('Sending calibration pulse sequence on cal_control1,2 and RST_EXT1,2')
os.system('poke 0x43c00000 0x00000010') # bit 4
time.sleep(0.5)
os.system('poke 0x43c00000 0x00000000')
