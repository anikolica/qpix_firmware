#### SET DACs ############################
# Authors: NCD, AN, ACG
# Usage: python3 commands/set_DACs.py [TP or VCOMP] [1 or 2] [voltage in V]
# Notes: sets voltages for 10-bit DACs
##############################################

import sys
import os
import time
import math

# U74
if sys.argv[1] == "TP":
	dac_addr = "0x0d"
elif sys.argv[1] == "VCOMP":
	dac_addr = "0x0c"
else:
	dac_addr = "0x00"
	print("Invalid DAC specified! Choices are TP or VCOMP")

# U65
if sys.argv[2] == "1":
	channel = "0x01"
elif sys.argv[2] == "2":
	channel = "0x02"
else:
	channel = "0x00"
	print("Invalid channel specified! Choices are 1 or 2")

# 10-bit DAC
steps = 1.2/1024
voltage = float(sys.argv[3])
if (voltage < 0):
	counts = 0
	print ("Invalid voltage specified! Value should be 0 - 1.2V")
elif (1.194 < voltage <= 1.2):
	counts = 0x3ff
elif (voltage > 1.2):
	counts = 0x3ff
	print ("Invalid voltage specified! Value should be 0 - 1.2V")
else:
	counts = math.floor(voltage/steps)

# Xilinx I2C commands are byte-swapped
counts_formatted = str.format('0x{:04X}', counts << 2)
msb = counts_formatted[3:4]
lsb = counts_formatted[4:6]
ctrl_bits = "2"
word = '0x' + lsb + ctrl_bits + msb

command = 'i2cset -y 0 ' + dac_addr + ' ' + channel + ' ' + word + ' w'
print ("Sending command: " + command)
i2c_raw = os.popen(command).read()

