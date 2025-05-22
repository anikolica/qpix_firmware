import os
import sys
import time

# opad_RST_EXT 1 or 2
if sys.argv[1] == '1':
    interface = sys.argv[1]
    data = '0x00000004'
elif sys.argv[1] == '2':
    interface = sys.argv[1]
    data = '0x00000008'
else:
    print ('Invalid reset interface!')

print ('Pulsing RST_EXT' + interface)
os.system('poke 0x43c00000 ' + data)
time.sleep(0.5)
os.system('poke 0x43c00000 0x00000000')

print ('Pulsing TRIGGER')
os.system('poke 0x43c00014 0x00000001')
time.sleep(0.5)
os.system('poke 0x43c00014 0x00000000')
