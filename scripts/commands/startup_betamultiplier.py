#### STARTUP BETA-MULTIPLIER #################
# Authors: NCD, AN, ACG
# Usage: python3 commands/set_DAC7578.py
# Notes: formerly Kickstart.py, keeps beta-multiplier 
#        startup pads high for all time
##############################################

import os

print ('Asserting opad_startup, opad2_startup...', end='')
os.system('poke 0x43c00000 0x03000000') # bits 25,24
print(" done.")
