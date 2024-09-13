import os
import sys
import time

# Set bit for calibration routine
##
# Set reset width & time past de-assert reset to de-assert cal_control
print ('setting reset width = 10us')
print ('setting de-assert cal_control from de-assert reset = 100ns')
os.system('poke 0x43c00020 0x000501F4') # reg8: cal=100ns, reset=10us 



print ('Sending calibration pulse sequence on cal_control1,2 and RST_EXT1,2')
os.system('poke 0x43c00000 0x00000010') # reg0[4]
time.sleep(0.5)
os.system('poke 0x43c00000 0x00000000')
