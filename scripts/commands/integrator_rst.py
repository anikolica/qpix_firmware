### ALL HELPER FUNCTIONS ########################
# Authors: AN, ACG
# Usage: python3 commands/integrator_rst.py [1 or 2]
# Notes: performs integrator reset
#################################################

import os
import sys
import time
from helper_functions import *

# opad_RST_EXT 1 or 2
if sys.argv[1] == '1':
    interface = sys.argv[1]
    data = '0x00000004'
elif sys.argv[1] == '2':
    interface = sys.argv[1]
    data = '0x00000008'
else:
    print ('Invalid reset interface!')

print ('Pulsing opad_RST_EXT' + interface + "(integrator_rst.py)...", end='')
os.system('poke 0x43c00000 ' + data)
time.sleep(0.5)
print(" done.")
print("Enabling replenishment clocks on opad_CLK, separate from system clock (integrator_rst.py).")
set_ext_clock(1)
