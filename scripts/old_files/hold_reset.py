import os
import sys
import time

# Simply assert reset pads
# python3 hold_reset.py [1|2] [on|off]
if sys.argv[2] == 'on':
	if sys.argv[1] == '1':
    		data = '0x00000020'
	if sys.argv[1] == '2':
    		data = '0x00000040'
elif sys.argv[2] == 'off':
    data = '0x00000000'
else:
    print ('Invalid selection!')

os.system('poke 0x43c00000 ' + data)
print ('Setting opad_RST' + sys.argv[1] + ' ' + sys.argv[2])
