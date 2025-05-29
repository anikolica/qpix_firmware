import os
import sys
import time

# Set bit for calibration routine
print ('Sending 5us pulse on RST_EXT1,2, followed by TRIGGER')
os.system('poke 0x43c00000 0x00000080') # bit 7
time.sleep(0.5)
os.system('poke 0x43c00000 0x00000000')
