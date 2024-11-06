import os
import sys
import time

# CALL this program from get_samples_ncd.py 
# Set bit for calibration routine

# Set reset width & time past de-assert reset to de-assert cal_control
print ('setting reset width = 10us')
print ('setting de-assert cal_control from de-assert reset = 100ns')
os.system('poke 0x43c00020 0x000501F4') # reg8: de-assert cal_control after 100ns; reset width=10us 

os.system('poke 0x43c00024 0x000001F4') # REG9[31]=0 to sample during deltaT; sample delay= 10us 
#os.system('poke 0x43c00024 0x800001F4') # REG9[31]=1 to sample during window_width active; sample delay= 10us 



print ('Sending calibration pulse sequence on cal_control1,2 and RST_EXT1,2')
os.system('poke 0x43c00000 0x00000010') # reg0[4] , Now must readout data with get_samples_ncd.py
time.sleep(0.5)
os.system('poke 0x43c00000 0x00000000')
