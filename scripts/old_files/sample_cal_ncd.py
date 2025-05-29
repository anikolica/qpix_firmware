##################################################
## CALIBRATION
## based on sample_cal_ncd.py
## Authors: ncd, PURM students summer 2024, acg
## python3 samplesCollection.py [# of runs]

import os
import sys
import time
import math 
import csv
import myModules as my
import statistics as s


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




copy_channelCounts = channelCounts.copy() # Make a backup copy of this list -ncd
channelCounts = copy_channelCounts.copy() # Then revert to it!  -ncd

print(channelCounts)
print(copy_channelCounts)

def channelSimulation(c, i):
        """
        This function takes inputs c and i where c is the channel (list) and i is the number of the channel (int) and; 
        1) Counts the number of calibration counts/resets in c
        2) Appends the number of counts to channelCounts for c
       ***** Copied from samplesCollection.py, which works -ncd 2025 ****
        """
       
        ch = c[0]
        fifo_status_reg = c[1]
        ts_hi_reg = c[2]
        ts_lo_reg = c[3]
        data = []
        counter = 0
        # print("here1")
        ch_wr_rst_busy, ch_almost_full, ch_full, ch_rd_rst_busy, ch_almost_empty, ch_empty = my.read_ch_status(fifo_status_reg)
        while (ch_empty != 1):
            #print("here")
            current_ts = my.read_ch_fifo(ch, ts_hi_reg, ts_lo_reg)
            #print(current_ts)
            data.append(current_ts)
            ch_wr_rst_busy, ch_almost_full, ch_full, ch_rd_rst_busy, ch_almost_empty, ch_empty = my.read_ch_status(fifo_status_reg)
            counter = counter+1;
        #print('Channel ' + str(ch) + ' calibration counts are: ' + str(counter))
        channelCounts[i].append(counter)

        
def sample_cal(numTrials, DECIMAL_replen):
    print(DECIMAL_replen)
    ## Set the sampling window Width and Delay
    ## Set the Window Width in seconds
        # AWG decending staircase freq: 14KHz --> 65us
        #                               4KHz  --> 200us
        #                               2KHz --> 400us
    os.system('poke 0x43c00028 0x00000001') # New bit to only look at deltaT2 during calibration

    
    winWidth = 64e-6
    #winWidth = 400e-6
    #winWidth = 1.8e-3
  
    ## Set Window Delay in seconds
    delay = 10e-6
    #delay = 250e-6
    ########################################

    # If you don't want to check a channel, add to this list
    #notWorking = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14] 
    #notWorking = [0,1,2,3,4,5,6,7,8,9,11,12,13,14,15] 
    #notWorking = [0,8,9,10,11,12,13,14,15] 
    
    notWorking = [0,1,2,3,4,5,6,7] 
    #notWorking = [0,1,2,3,4,5,6,7,9,10,11,12,13,14,15] 
    
    #notWorking = []
    ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

   

    if  (numTrials == 0 or numTrials == None):
        numTrials = 1

    width_Hex = hex( int(winWidth/20e-9) ) #change to 20ns clicks
    #print("width_Hex = ", width_Hex)
    #print("winWidth = ", winWidth)
    #windowWidth = "poke 0x43c001c " + width_Hex
    #print("windowWidth = ", windowWidth ) 

    delay_Hex = hex( 2147483648 + int(delay/20e-9) ) #change to 20ns clicks & add 0x80000000 to set Reg9[31]
    #print("delay_Hex and Reg9[31] set = ", delay_Hex)
    #windowDelay = "poke 0x43c0000 " + delay_Hex
    #print("windowDelay: ", windowDelay )


    os.system('poke 0x43c00028 0x00000001') # New bit to only look at deltaT2 during calibration
    #os.system('poke 0x43c00028 0x00000001') # New bit to only look at deltaT1 during calibration

    # Run 'numTrials' trials 
    
    #channelCounts = copy_channelCounts.copy() # Try to revert channelCount to initial state !  -ncd
    #channelCounts = []  # attempt 2 -ncd this crashes out of range

    for j in range(numTrials):
 
        #os.system('poke 0x43c0001c 0x00000CB2') # set window widths 65us
        #os.system('poke 0x43c0001c 0x00002710') # set window widths 200us
        os.system('poke 0x43c0001c "' + width_Hex + '" ') # set window widths 

        os.system('poke 0x43c00024 0x000001F4') # REG9[31]=0 (use deltaT -ncd);  Set delays 10us 
        #os.system('poke 0x43c00024 0x800001F4') # REG9[31]=1 (Ignore detalT -ncd);  Set delays 10us 
        #os.system('poke 0x43c00024 "' + delay_Hex + '" ') # REG9[31]=1 (Ignore detalT -ncd);  Set delays x usec 
        
        print ('System Reset')
        #os.system('poke 0x43c00020 0x000509c4') # reset width 50us -ncd
        os.system('poke 0x43c00020 0x000500c4') # reset width 50us -ncd

        os.system('poke 0x43c00000 0x00000001') #system reset
        
        
        os.system('poke 0x43c00000 0x00000010') # REG0[4]=1     ** Start Calibration sequence, External Clock OFF -ncd 
        
        time.sleep(1.1)
        os.system('poke 0x43c00000 0x00000000') # REG0[4]=0 Reset the bit for next time; TURNS External Clock OFF -ncd 

        print( "   Window width = ", winWidth, [width_Hex] )
        print( "   Window delay = ", delay,    [delay_Hex] ) 

        print("Run: " , j+1 , " of " , numTrials  )
        # Runs readout for each channel
        for i in range(16):
            if i in notWorking: 
                channels[i] = 0
                print("skipping ch = ", i)
            else:
                cht = channels[i]
                #my.channelSimulationT(cht, i, channelCounts)  # This version of channelSimulation writes out timestamps -ncd
                #my.channelSimulation(cht, i)  # This version of channelSimulation doesnt writes out timestamps -ncd
                channelSimulation(cht, i)  # local version that works correctly -ncd
    # Commented lines below are used to write raw data values of the returned arrays into a file
    # if only interested in averages and standard deviations, you can ignore

    print("before", channelCounts)
    #channelCounts = copy_channelCounts.copy() # Then revert to it!  -ncd
    print("after", channelCounts)


    f = open("dataBasket1.txt", "w+")

    # fix up output formatting -ncd
    print("\nChannel, Count Array,     Avg    Stdev")

    # Alternative excel writer method -ncd
    #Write to an Excel csv file in append mode -ncd
    f2 = open("cumdata.csv", "a")
#    This works but cannot ever close the file unless using "with as" method. -ncd
#    f2 = csv.writer( open("my.csv","a"), delimiter = ',')   # open csv file handle "f2"
#    f2 = csv.writer( open(f2, delimiter = ',')   # open csv file handle "f2"
#    f2.writerow('applepie', "car")    # write data to file
#    f2.writerow( ['Channel', 'Counts', 'Ave', 'Stdev' ] )
#    f2.writer(f2, delimiter = ',')
#    f2.writerow("carcarpear")

    # write separate csv files for each channel -ncd
    fch0 = open("fch0.csv", "a")
    fch1 = open("fch1.csv", "a")
    fch2 = open("fch2.csv", "a")
    fch3 = open("fch3.csv", "a")
    fch4 = open("fch4.csv", "a")
    fch5 = open("fch5.csv", "a")
    fch6 = open("fch6.csv", "a")
    fch7 = open("fch7.csv", "a")
    fch8 = open("fch8.csv", "a")
    fch9 = open("fch9.csv", "a")
    fch10 = open("fch10.csv", "a")
    fch11 = open("fch11.csv", "a")
    fch12 = open("fch12.csv", "a")
    fch13 = open("fch13.csv", "a")
    fch14 = open("fch14.csv", "a")
    fch15 = open("fch15.csv", "a")

    for k in range(16):
        # skip certain channels
        if k == k in notWorking:
            nope = 0
        
        # Return data at end of all runs
        else:
            #  channelCounts = []  # First clear list -ncd
            use = ','.join(map(str,channelCounts[k]))
            f.write(use + '\n')
            print( "%-9s %-15s %-6.2f %-6.2f"%(str(k),channelCounts[k],my.avgArr(channelCounts[k]),my.stdDev(channelCounts[k]) ) )

            apple = ','.join( map(str, channelCounts[k] ) )
            #use2 = ','.join(map(str, (k, apple, my.avgArr(channelCounts[k]), my.stdDev(channelCounts[k] )) ) ) 
            
            #use2 = ','.join(map(str, (k, DECIMAL_replen, apple, s.mean(channelCounts[k]), s.pstdev(channelCounts[k] )) ) ) 
            use2 = ','.join(map(str, (k, DECIMAL_replen, channelCounts[k], s.mean(channelCounts[k]), s.pstdev(channelCounts[k] )) ) ) 
            

            #f2.write( str( [ str(k), channelCounts[k], my.avgArr(channelCounts[k]), my.stdDev(channelCounts[k])  ] ) + "\n" )  
            f2.write( use2 + '\n' )  
            # write to channel Matrix -ncd
            #chanMatrix[k] =  k, s.mean(channelCounts[k] 
            if (k == 0): fch0.write(use2 + '\n')  
            if (k == 1): fch1.write(use2 + '\n')  
            if (k == 2): fch2.write(use2 + '\n')  
            if (k == 3): fch3.write(use2 + '\n')  
            if (k == 4): fch4.write(use2 + '\n')  
            if (k == 5): fch5.write(use2 + '\n')  
            if (k == 6): fch6.write(use2 + '\n')  
            if (k == 7): fch7.write(use2 + '\n')  
            if (k == 8): fch8.write(use2 + '\n')  
            if (k == 9): fch9.write(use2 + '\n')  
            if (k == 10): fch10.write(use2 + '\n')  
            if (k == 11): fch11.write(use2 + '\n')  
            if (k == 12): fch12.write(use2 + '\n')  
            if (k == 13): fch13.write(use2 + '\n')  
            if (k == 14): fch14.write(use2 + '\n')  
            if (k == 15): fch15.write(use2 + '\n') 
    for m in range(16): 
        closing = "fch" +  str(m) + ".close()"
        print(closing)
        closing

    fch0.close()
    f2.close()
    f.close

    print("Done Writing")


## Run this module -ncd
#numTrials = 1
#DECIMAL_replen = 31  # THIS DOES NOT set Replenishment: only a marker! 
#sample_cal(numTrials, DECIMAL_replen)



