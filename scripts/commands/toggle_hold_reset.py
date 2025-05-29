#### TOGGLE HOLD RESET ##############################
# Authors: NCD, AN, ACG
# Usage: python3 commands/toggle_hold_reset.py [1|2] [1|0|'on'|'off']
# Notes: asserts reset pads
################################################

import os
import sys
import time

if len(sys.argv) < 3:
    print("Error. Please run: python3 toggle_hold_reset.py [1|2] ['on'|'off']")
    sys.exit()

if sys.argv[2] == 'on' or sys.argv[2] == '1':
	if sys.argv[1] == '1':
    		data = '0x00000020'
	if sys.argv[1] == '2':
    		data = '0x00000040'
elif sys.argv[2] == 'off' or sys.argv[2] == '0':
    data = '0x00000000'
else:
    print ('Invalid selection!')

os.system('poke 0x43c00000 ' + data)
print ('Setting opad_RST' + sys.argv[1] + ' ' + sys.argv[2])
