# Written by PURM Students Summer 2024
# Meant to run the scripts involved in the Magic Sequence
# Gets the system up and running in a simple mode
# python3 runMagicSequence.py
# Modified -ncd 8/20/2024

import os
import sys
import time

print('Running the Magic Sequence -ncd: ')

# Set calibration widths
os.system('poke 0x43c00020 0x000500FA') # Cal Delay: 100ns, Reset Width: 5us
os.system('python3 set_Thresholds.py TP 2 0.800')
os.system('python3 set_Thresholds.py VCOMP 1 0.780')
os.system('python3 set_Thresholds.py VCOMP 2 0.950')

os.system('python3 set_DAC7578_ncd.py')

# Calibration mode, ring osc on slow, ALL channel enabled (decimal 17)
print('All channels enabled, ring osc slow, replenishement: decimal 17')

os.system('python3 Serial_Interface.py  1  0x55B6FFC6')
os.system('python3 Serial_Interface.py  2  0x55B6FFC6')

os.system('python3 Integrator_rst_fix.py 1')
os.system('python3 Integrator_rst_fix.py 2')


print('Magic Sequence Completed!')


