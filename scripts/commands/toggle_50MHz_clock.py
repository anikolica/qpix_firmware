#### TOGGLE 50MHz CLOCK ##############################
# Authors: NCD, AN, ACG
# Usage: python3 commands/toggle_50MHz_clock.py [on or off or 1 or 0]
# Notes: 
################################################

import os
import sys
import time
from string import *
from helper_functions import *

if len(sys.argv) < 2: 
    print("Error: Please specify 1 or 0")
    sys.exit()

# Replenishment clock opad_CLK and opad2_CLK
if sys.argv[1].isalpha():
    print ('Invalid selection! Options are 1 or 0')
    sys.exit()
elif int(sys.argv[1]) == 1:
    set_ext_clock(1)
elif int(sys.argv[1]) == 0:
    set_ext_clock(0)
else:
    print ('Invalid selection! Options are 1 or 0')
    sys.exit()

