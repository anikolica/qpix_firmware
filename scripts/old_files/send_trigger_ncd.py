import os
import sys
import time

os.system('poke 0x43c00020 0x000509c4') # Reset width 50us
#os.system('poke 0x43c00020 0x000501F4') # Reset width 10us
#os.system('poke 0x43c00020 0x00051388') # Reset width 100us

# Set bit for calibration routine
print ('Sending 5us pulse on RST_EXT1,2, followed by TRIGGER')
#os.system('poke 0x43c00000 0x00030080') # bit 7, Enable External CLOCKS bit 17,16 -ncd
os.system('poke 0x43c00000 0x00000080') # bit 7, Disable external CLOCKS bit 17,16 -ncd

#os.system('poke 0x43c00000 0x00030000')  # Keep External clock on
os.system('poke 0x43c00000 0x00000000')   # Keep External Clock disabled
time.sleep(0.5)
