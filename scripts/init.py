### INITIALIZATION SCRIPT "Magic Sequence" ###
# Authors: PURM Students Summer 2024, NCD, ACG
# Usage: python3 init.py 
# Notes:
##############################################

import os
import sys
import time
from commands.helper_functions import *

### USER INPUTS ###
rst_cal_gap = 100e-9
reset_width = 5e-6
tp_threshold = 0.800
vcomp1_threshold = 0.780
vcomp2_threshold = 0.9
###################

print('Running the Magic Sequence: ')
# Set calibration widths
set_rst_cal_gap(rst_cal_gap)
set_reset_width(reset_width)
# SET DAC THRESHOLDS
os.system(f'python3 commands/set_DACs.py TP 2 {str(tp_threshold)}')
os.system(f'python3 commands/set_DACs.py VCOMP 1 {str(vcomp1_threshold)}')
os.system(f'python3 commands/set_DACs.py VCOMP 2 {str(vcomp2_threshold)}')


# ---- Testing VCM2 controls due to 10k and 5k resistors - SRAK
os.system('python3 old_files/set_DAC7578_ncd.py')
os.system('python3 old_files/set_DAC2.py')
# ----

# Calibration mode, DBL_bar, ring osc on, one channel enabled
os.system('python3 commands/serial_interface.py  1  0x55B680CE')
os.system('python3 commands/serial_interface.py  2  0x55B680CE')

os.system('python3 commands/integrator_rst.py 1')
os.system('python3 commands/integrator_rst.py 2')

calibration_pulse()

# Calibration mode, ring osc on slow, ALL channel enabled (decimal 17)
os.system('python3 commands/serial_interface.py  1  0x55B6FFC4')
os.system('python3 commands/serial_interface.py  2  0x55B6FFC4')

startup()
set_ext_clock(1)

print('Magic Sequence Completed!')
