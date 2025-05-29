import os
import sys
import time

# The minimun needed to get Qpix running (3/21/2025 -ncd)
# 
# First set all voltages required for Qpix

#   VDD, DVDD = 1.6v (set with Voltage regulator in Penn setup)

#   Qpix VCM and VCM2 are baseline volages used for the Qpix Integrators
#   and are provided by voltage regulators in the Penn setup

#   Qpix 'VCOMP' and 'VCOMP2' set Comparator 'Threshold' voltages and
#   are set with DACs in the Penn setup

#   For the Standard Channels: VCM  = 760mV, VCOMP2= 725mV
#   For C-gain channels:       VCM2 = 800mV, VCOMP2 = 815mV

# Penn setup DACs 
os.system('python3 set_Thresholds.py TP 2 0.800')
os.system('python3 set_Thresholds.py VCOMP 1 0.780')
os.system('python3 set_Thresholds.py VCOMP 2 0.875')
os.system('python3 set_DAC7578_ncd.py')
os.system('python3 set_DAC2.py')  

# program Qpix serial interfaces with reasonable values
# Data must get serialized into Qpix little-end first
# See Excel file for programming values
os.system('python3 Serial_Interface.py  1  0x55B6FFC4')  # program Inteface 1 (standard Chan)
os.system('python3 Serial_Interface.py  2  0x55B6FFC4')  # progam Inteface 2 (C-gain Chan)

# Issue Integrator resets 
os.system('poke 0x43c00020 0x000500FA') # Cal Delay: 100ns, Reset Width: 5us
os.system('python3 Integrator_rst_fix.py 1')
os.system('python3 Integrator_rst_fix.py 2')

# Look at LVDS outputs from channels; should see signs of life



