# Written by PURM Students Summer 2024
# Meant to run the scripts involved in the Magic Sequence
# Gets the system up and running in a simple mode
# python3 runMagicSequence.py

import os
import sys
import time

print('Running the Magic Sequence: ')

# Set reset width
#os.system('poke 0x43c00020 0x3e8')

# Set calibration widths
os.system('poke 0x43c00020 0x000500FA')

os.system('python3 set_Thresholds.py TP 2 0.800')

os.system('python3 set_Thresholds.py VCOMP 1 0.780')

os.system('python3 set_Thresholds.py VCOMP 2 0.950')

# Calibration mode,DBL_bar, ring osc on, one channel enabled
os.system('python3 Serial_Interface.py  1  0x55B680CE')
#os.system('python3 Serial_Interface.py  2  0x55B680CE')

os.system('python3 Integrator_rst_fix.py 1')
#os.system('python3 Integrator_rst_fix.py 2')

os.system('python3 Calibrate.py')

# Calibration mode, ring osc on slow, ALL channel enabled (decimal 17)
os.system('python3 Serial_Interface.py  1  0x55B6FFC6')
os.system('python3 Serial_Interface.py  2  0x55B6FFC6')

print('Magic Sequence Completed!')



