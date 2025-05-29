### SAMPLE COLLECTION SCRIPT ##################################
# Authors: PURM Students Summer 2024, NCD, ACG
# Usage: python3 send_trigger.py
# Notes: send a trigger to the external wave generator
###############################################################

import os
import sys
import time
from commands.helper_functions import *

### USER INPUT ###
reset_width = 50e-6
external_clock_on = False
##################

set_reset_width(reset_width)

if external_clock_on:
    print(f'Sending {reset_width}s pulse on RST_EXT1,2, followed by TRIGGER, with external clock ON...', end='')
    os.system('poke 0x43c00000 0x00030080') # bit 7 sends trigger, Enable External CLOCKS bit 17,16 -ncd
    os.system('poke 0x43c00000 0x00030000')  # Keep External clock on
if not external_clock_on:
    print (f'Sending {reset_width}s pulse on RST_EXT1,2, followed by TRIGGER, with external clock OFF...', end='')
    os.system('poke 0x43c00000 0x00000080') # bit 7 sends trigger, Disable external CLOCKS bit 17,16 -ncd
    os.system('poke 0x43c00000 0x00000000')   # Keep External Clock disabled
time.sleep(0.5)
print(" done.")
