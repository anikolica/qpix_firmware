#### SET DAC_7578 ############################
# Authors: NCD, AN, ACG
# Usage: python3 commands/set_DAC7578.py
# Notes: sets vref and vset for DAC7578
##############################################

import sys
import os
import time
import math

### USER INPUTS ####
vref = 1.6
vset = 0.8
####################

dac_addr = "0x48"

# 12-bit DAC
steps = vref/4096
if (vset <= 0):
	counts = 0x000
	print ("Invalid voltage specified! Value should be 0 - " + str(vset) + " V")
elif (vset >= vref):
	counts = 0xfff
	print ("Invalid voltage specified! Value should be 0 - " + str(vset) + " V")
else:
	counts = math.floor(vset/steps)

# Set all 8 channels
counts_formatted = str.format('{:04X}', counts << 4)
msn = counts_formatted[0:2] 
lsn = counts_formatted[2:4]

for channel in range(0, 8):
	command = 'i2cset -y 1 ' + dac_addr + ' 0x0' + str(channel) + ' 0x' + msn + ' 0x' + lsn + ' i'
	print ("Sending command: " + command)
	i2c_raw = os.popen(command).read()

