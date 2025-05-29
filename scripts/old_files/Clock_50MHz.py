import os
import sys
import time

# Replenishment clock opad_CLK and opad2_CLK
if sys.argv[1] == 'on':
    state = sys.argv[1]
    data = '0x00030000'
elif sys.argv[1] == 'off':
    state = sys.argv[1]
    data = '0x00000000'
else:
    print ('Invalid selection!')

os.system('poke 0x43c00000 ' + data)
print ('Replenishment clocks ' + state)
