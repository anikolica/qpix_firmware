import sys
import os
import time
import math

def dac_command(channel, vset, vref):  # returns a DAC command -mcd 

    #vref = 1.6
    #vset = 0.8
    #vref=1.584
    #vref = 0.800

    # Choose voltage -ncd
    #vset = 0.761

    dac_addr = "0x48"

    # 12-bit DAC
    steps = vref/4096
    if (vset <= 0):
        counts = 0x000
        print ("Invalid voltage specified! Value should be 0 - " + str(vset) + " V")
#    elif (vset >= vref):
#       counts = 0xfff
#	print ("Invalid voltage specified! Value should be 0 - " + str(vset) + " V")
    else:
        counts = math.floor(vset/steps)

    #print("setting leakage cancelation for all channels: vset = ", vset )
    print("**** DAC vref = " , vref , "****")
    print(" ")
    print("counts=  ", counts)

    # Generate DAC command
    counts_formatted = str.format('{:04X}', counts << 4)
    msn = counts_formatted[0:2] 
    lsn = counts_formatted[2:4]

    command = 'i2cset -y 1 ' + dac_addr + ' 0x0' + str(channel) + ' 0x' + msn + ' 0x' + lsn + ' i'
    print ("channel: ", channel, "vset= ", vset)
    print ("Sending command: " + command)
    return command


##   Program the DAC's -ncd
#dac_command(channel, vset, vref) 

command = dac_command(0, 0.7611, 0.800)   # 0.7611v (3896)
i2c_raw = os.popen(command).read()

command = dac_command(1, 0.7580, 0.800)   #0.7583 (3881)
i2c_raw = os.popen(command).read()

command = dac_command(2, 0.7599, 0.800)  # 0.7599 (3890) 
i2c_raw = os.popen(command).read()

command = dac_command(3, 0.7598, 0.800)   # 0.7600 (3891) 
i2c_raw = os.popen(command).read()

command = dac_command(4, 0.7600, 0.800)  # 0.7604 (3893) 
i2c_raw = os.popen(command).read()

command = dac_command(5, 0.7589, 0.800) # 0.7589 (3885)
i2c_raw = os.popen(command).read()

command = dac_command(6, 0.7580, 0.800)  # 0.7584 (3883) 
i2c_raw = os.popen(command).read()

command = dac_command(7, 0.7555, 0.800)  # 0.7560 (3870)  
i2c_raw = os.popen(command).read()



