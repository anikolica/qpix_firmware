import os
import sys
import time


# Choose time for ON
print ('Enter time for ON:')
time_on = float(input())

# Choose time for REPEAT
print ('Enter time for REPEAT:')
time_repeat = float(input())

# Loop to repeat the process indefinitely
while True:
    data = '0x00000040'

    
    # Assert reset pads
    # if sys.argv[2] == 'on':
        # if sys.argv[1] == '1':
            # data = '0x00000020'
        # if sys.argv[1] == '2':
            # data = '0x00000040'
    # elif sys.argv[2] == 'off':
        # data = '0x00000000'
    # else:
        # print ('Invalid selection for sys.argv[1]!')
        # sys.exit(1)
    

    # Perform the reset
    os.system('poke 0x43c00000 ' + '0x00000040')
    # print(f'Setting opad_RST {sys.argv[1]} {sys.argv[2]}')

    # Wait for ON time
    # print(f'Waiting for {time_on} seconds...')
    time.sleep(time_on)

    # Repeat
    os.system('poke 0x43c00000 0x00000000')
    # print('Repeating')

    # Wait for REPEAT time
    # print(f'Waiting for {time_off} seconds...')
    time.sleep(time_repeat)

