# Written by PURM Students Summer 2024
# Meant to run get_samples.py multiple times and provide basic data on the results
# python3 samplesCollection.py [# of runs]

import os
import sys
import time
import math 
import csv
import myModules as my

#Defines the information in each channel 
ch0 = [0, '0x43c001b4', '0x43c00108', '0x43c0010c']
ch1 = [1, '0x43c001b8', '0x43c00110', '0x43c00114']
ch2 = [2, '0x43c001bc', '0x43c00118', '0x43c0011c']
ch3 = [3, '0x43c001c0', '0x43c00120', '0x43c00124']
ch4 = [4, '0x43c001c4', '0x43c00128', '0x43c0012c']
ch5 = [5, '0x43c001c8', '0x43c00130', '0x43c00134']
ch6 = [6, '0x43c001cc', '0x43c00138', '0x43c0013c']
ch7 = [7, '0x43c001d0', '0x43c00140', '0x43c00144']
ch8 = [8, '0x43c001d4', '0x43c00148', '0x43c0014c']
ch9 = [9, '0x43c001d8', '0x43c00150', '0x43c00154']
ch10 = [10, '0x43c001dc', '0x43c00158', '0x43c0015c']
ch11 = [11, '0x43c001e0', '0x43c00160', '0x43c00164']
ch12 = [12, '0x43c001e4', '0x43c00168', '0x43c0016c']
ch13 = [13, '0x43c001e8', '0x43c00170', '0x43c00174']
ch14 = [14, '0x43c001ec', '0x43c00178', '0x43c0017c']
ch15 = [15, '0x43c001f0', '0x43c00180', '0x43c00184']

channels=[ch0, ch1, ch2, ch3, ch4, ch5, ch6, ch7, ch8, ch9, ch10, ch11, ch12, ch13, ch14, ch15]

ch0Counts = []
ch1Counts = []
ch2Counts = []
ch3Counts = []
ch4Counts = []
ch5Counts = []
ch6Counts = []
ch7Counts = []
ch8Counts = []
ch9Counts = []
ch10Counts = []
ch11Counts = []
ch12Counts = []
ch13Counts = []
ch14Counts = []
ch15Counts = []

#Define channelCounts which stores the number of resets in a given channel 
channelCounts=[ch0Counts, ch1Counts, ch2Counts, ch3Counts, ch4Counts, ch5Counts, ch6Counts, ch7Counts, ch8Counts, ch9Counts, ch10Counts, ch11Counts, ch12Counts, ch13Counts, ch14Counts, ch15Counts]
os.system('poke 0x43c00024 0x000001F4') # REG9[31]=0 to sample during deltaT; sample delay= 10us 



#def channelSimulation(c, i, channelCounts):
#        
#       # This function takes inputs c and i where c is the channel (list) and i is the number of the channel (int) and; 
#       # 1) Counts the number of calibration counts/resets in c
#       # 2) Appends the number of counts to channelCounts for c
#        
#       
#        ch = c[0]
#       fifo_status_reg = c[1]
#        ts_hi_reg = c[2]
#        ts_lo_reg = c[3]
#        data = []
#        counter = 0
#        ch_wr_rst_busy, ch_almost_full, ch_full, ch_rd_rst_busy, ch_almost_empty, ch_empty = read_ch_status(fifo_status_reg)
#        while (ch_empty != 1):
#            current_ts = read_ch_fifo(ch, ts_hi_reg, ts_lo_reg)
#            data.append(current_ts)
#            ch_wr_rst_busy, ch_almost_full, ch_full, ch_rd_rst_busy, ch_almost_empty, ch_empty = read_ch_status(fifo_status_reg)
#            counter = counter+1;
#        print('Channel ' + str(ch) + ' calibration counts are: ' + str(counter))
#        channelCounts[i].append(counter)




# Take in user input
if len(sys.argv) < 2:
     testNum = 1
else:
     testNum = int(sys.argv[1])

# Edge case
if  (testNum == 0 or testNum == None):
    testNum = 1

# If you don't want to check a channel, add to this list
#notWorking = [] #[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
notWorking = [0,1,2,3,4,5,6,7,8] #[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

winWidth = 64e-6
#winWidth = 1.8e-3
width_Hex = hex( int(winWidth/20e-9) )
print("width_Hex = ", width_Hex)
print("winWidth = ", winWidth)
 

# Set window delay and width, reset system, and simulate
for j in range(testNum):
    # AWG decending staircase freq: 14KHz --> 65us
    #                               4KHz  --> 200us
    #                               2KHz --> 400us
    #  etc...
#    os.system('poke 0x43c0001c 0x00000CB2') # set window widths 65us
#    os.system('poke 0x43c0001c 0x00002710') # set window widths 200us
#    os.system('poke 0x43c0001c 0x00004E20') # set window widths 400us
#    os.system('poke 0x43c0001c 0x001E8480') # set window widths 40ms
    os.system('poke 0x43c0001c "' + width_Hex + '" ') # set window widths 

    os.system('poke 0x43c00024 0x800001F4') # REG9[31]=1 (Ignore detalT -ncd);  Set delays 10us 
    print ('System Reset')
    os.system('poke 0x43c00000 0x00000001') #system reset
    os.system('poke 0x43c00000 0x00000000') #channel reset 
    os.system('poke 0x43c00000 0x00008000') # REG0[15]=1 Start sampling swquence
    time.sleep(0.1)
    os.system('poke 0x43c00000 0x00000000') # REG0[15]=0 Reset the bit for next time 

    print( "   Window width = ", winWidth, [width_Hex] )
    print("Run: " , j+1 , " of " , testNum  )
    # Runs readout for each channel
    for i in range(16):
        if i == i in notWorking: 
            channels[i] = 0
        else:
            cht = channels[i]
            my.channelSimulation(cht, i, channelCounts)

# Commented lines below are used to write raw data values of the returned arrays into a file
# if only interested in averages and standard deviations, you can ignore

f = open("dataBasket1.txt", "w+")

# fix up output formatting -ncd
print("\nChannel, Count Array,     Avg    Stdev")

# WRITE TO Excel file csv
with open('eggs.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',' )
                              
#    spamwriter.writerow(['Spam'] * 5 + ['baked Beans'])
#    spamwriter.writerow(['Spam', 'Lovely Spoam', 'Wonderful Spam'])
#    spamwriter.writerow(['Spam', 'Lovely Spoam', 'Wonderfulfff Spamfff'])

    spamwriter.writerow( ['Channel', 'Counts', 'Ave', 'Stdev' ] )

    for k in range(16):
        # skip certain channels
          if k == k in notWorking:
            nope = 0

         # Return data at end of all runs
          else:
       #    print("Count Array, Avg Count, Std Dev for: " + str(k))
       #    print(channelCounts[k], end =" ")
       #    print(avgArr(channelCounts[k]), end =" ")
       #    print(stdDev(channelCounts[k]))
            use = ','.join(map(str,channelCounts[k]))
            f.write(use + '\n')   
            print( "%-9s %-15s %-6.2f %-6.2f"%(str(k),channelCounts[k],my.avgArr(channelCounts[k]),my.stdDev(channelCounts[k]) ) )
            spamwriter.writerow( [ str(k), channelCounts[k], my.avgArr(channelCounts[k]), my.stdDev(channelCounts[k])  ] )  


f.close
print("Done Writing!")

