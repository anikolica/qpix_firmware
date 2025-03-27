## My modules 2025 update
import os
import sys
import time
import math 
import csv
def avgArr(ch):
    """Averaging function 
    Input: List of no. of resets for channel "ch"  
    Output: Average no. of resets for a channel (int)
    """
    total = 0
    for i in range(0, len(ch)):
        total += ch[i]
   
   #edge case 
    if len(ch)==0:
        return 0
    else:
        total = total / len(ch)
   
        return total
    
def stdDev(ch): 
    """Standard deviation function 
    Input: List of no. of resets for channel (ch)
    """
    Squared = square(ch)
    Squared=avgArr(Squared)

    std = Squared-avgArr(ch)**2
    return math.sqrt(std)

def square(ch): 
    "Squares each indice of the array ch"""
    f = []
    for i in range(len(ch)): 
        f.append(ch[i]**2)
    return(f)

def read_ch_status(fifo_status_reg):
    #print ('FIFO status is: ') #FIFO: first-in, first-out which sends  
    ch_read = os.popen('peek ' + fifo_status_reg).read()
    ch_status = int(ch_read, 16)
    ch_empty = (ch_status & 0x00000001)
    ch_almost_empty = (ch_status & 0x00000002) >> 1
    ch_rd_rst_busy = (ch_status & 0x00000003) >> 2
    ch_full = (ch_status & 0x00000010) >> 8
    ch_almost_full = (ch_status & 0x00000020) >> 9
    ch_wr_rst_busy = (ch_status & 0x00000030) >> 10
    #print ('empty: ' + str(ch_empty) + ' almost empty: ' + str(ch_almost_empty) + ' read reset busy: ' + str(ch_rd_rst_busy))
    #print ('full: ' + str(ch_full) + ' almost full: ' + str(ch_almost_full) + ' write reset busy: ' + str(ch_wr_rst_busy))
    return ch_wr_rst_busy, ch_almost_full, ch_full, ch_rd_rst_busy, ch_almost_empty, ch_empty

def read_ch_fifo(read_bit, ts_hi_reg, ts_lo_reg):
    #print ('Reading FIFO')
    os.system('poke 0x43c00018 ' + str(hex(1 << read_bit)))
    os.system('poke 0x43c00018 0x00000000')
    fifo_ts_hi = os.popen('peek ' + ts_hi_reg).read()
    fifo_ts_lo = os.popen('peek ' + ts_lo_reg).read()
    fifo_ts = (int(fifo_ts_hi, 16) << 32) + int(fifo_ts_lo, 16)
    #print ('FIFO word (timestamp) is: ' + str(fifo_ts))
    return fifo_ts


def channelSimulationT(c, i, channelCounts): 
#        This function takes inputs c and i where c is the channel (list) and i is the number of the channel (int) and; 
#        1) Counts the number of calibration counts/resets in c
#        2) Appends the number of counts to channelCounts for c

#        channelCounts = []

        ##os.system('rm timestamps*.csv')  # remove any existing timestamp file -ncd
        fdata = open("timestamps.csv", "a")   # open new file to contain timestamps -ncd
        fdata0 = open("timestamps_ch0.csv", "a")   # open new file to contain timestamps -ncd
        fdata1 = open("timestamps_ch1.csv", "a")   # open new file to contain timestamps -ncd
        fdata2 = open("timestamps_ch2.csv", "a")   # open new file to contain timestamps -ncd
        fdata3 = open("timestamps_ch3.csv", "a")   # open new file to contain timestamps -ncd
        fdata4 = open("timestamps_ch4.csv", "a")   # open new file to contain timestamps -ncd
        fdata5 = open("timestamps_ch5.csv", "a")   # open new file to contain timestamps -ncd
        fdata6 = open("timestamps_ch6.csv", "a")   # open new file to contain timestamps -ncd
        fdata7 = open("timestamps_ch7.csv", "a")   # open new file to contain timestamps -ncd

        fdata8 = open("timestamps_ch8.csv", "a")   # open new file to contain timestamps -ncd
        fdata9 = open("timestamps_ch9.csv", "a")   # open new file to contain timestamps -ncd
        fdata10 = open("timestamps_ch10.csv", "a")   # open new file to contain timestamps -ncd
        fdata11 = open("timestamps_ch11.csv", "a")   # open new file to contain timestamps -ncd
        fdata12 = open("timestamps_ch12.csv", "a")   # open new file to contain timestamps -ncd
        fdata13 = open("timestamps_ch13.csv", "a")   # open new file to contain timestamps -ncd
        fdata14 = open("timestamps_ch14.csv", "a")   # open new file to contain timestamps -ncd
        fdata15 = open("timestamps_ch15.csv", "a")   # open new file to contain timestamps -ncd


        ch = c[0]
        fifo_status_reg = c[1]
        ts_hi_reg = c[2]
        ts_lo_reg = c[3]
        data = []
        counter = 0
        ch_wr_rst_busy, ch_almost_full, ch_full, ch_rd_rst_busy, ch_almost_empty, ch_empty = read_ch_status(fifo_status_reg)
        while (ch_empty != 1):
            current_ts = read_ch_fifo(ch, ts_hi_reg, ts_lo_reg)
            #print("current_ts= ", current_ts, "i= ", i)  # prints out time stamps (5ns counts)  -ncd
            fdata.write( str(current_ts) + "\n" )   # write timestamps to file -ncd
            if (i == 0 ): fdata0.write( str(current_ts) + "\n" )   # write timestamps to file -ncd
            if (i == 1 ): fdata1.write( str(current_ts) + "\n" )   # write timestamps to file -ncd
            if (i == 2 ): fdata2.write( str(current_ts) + "\n" )   # write timestamps to file -ncd
            if (i == 3 ): fdata3.write( str(current_ts) + "\n" )   # write timestamps to file -ncd
            if (i == 4 ): fdata4.write( str(current_ts) + "\n" )   # write timestamps to file -ncd
            if (i == 5 ): fdata5.write( str(current_ts) + "\n" )   # write timestamps to file -ncd
            if (i == 6 ): fdata6.write( str(current_ts) + "\n" )   # write timestamps to file -ncd
            if (i == 7 ): fdata7.write( str(current_ts) + "\n" )   # write timestamps to file -ncd

            if (i == 8 ): fdata8.write( str(current_ts) + "\n" )   # write timestamps to file -ncd
            if (i == 9 ): fdata9.write( str(current_ts) + "\n" )   # write timestamps to file -ncd
            if (i == 10 ): fdata10.write( str(current_ts) + "\n" )   # write timestamps to file -ncd
            if (i == 11 ): fdata11.write( str(current_ts) + "\n" )   # write timestamps to file -ncd
            if (i == 12 ): fdata12.write( str(current_ts) + "\n" )   # write timestamps to file -ncd
            if (i == 13 ): fdata13.write( str(current_ts) + "\n" )   # write timestamps to file -ncd
            if (i == 14 ): fdata14.write( str(current_ts) + "\n" )   # write timestamps to file -ncd
            if (i == 15 ): fdata15.write( str(current_ts) + "\n" )   # write timestamps to file -ncd

            data.append(current_ts)
            ch_wr_rst_busy, ch_almost_full, ch_full, ch_rd_rst_busy, ch_almost_empty, ch_empty = read_ch_status(fifo_status_reg)
            counter = counter+1;
        channelCounts[i].append(counter)

        print('Channel ' + str(ch) + ' calibration counts are: ' + str(counter))
        
        fdata.close()  # close file with timestamps  -ncd
        fdata0.close()  # close file with timestamps  -ncd
        fdata1.close()  # close file with timestamps  -ncd
        fdata2.close()  # close file with timestamps  -ncd
        fdata3.close()  # close file with timestamps  -ncd
        fdata4.close()  # close file with timestamps  -ncd
        fdata5.close()  # close file with timestamps  -ncd
        fdata6.close()  # close file with timestamps  -ncd
        fdata7.close()  # close file with timestamps  -ncd

        fdata8.close()  # close file with timestamps  -ncd
        fdata9.close()  # close file with timestamps  -ncd
        fdata10.close()  # close file with timestamps  -ncd
        fdata11.close()  # close file with timestamps  -ncd
        fdata12.close()  # close file with timestamps  -ncd
        fdata13.close()  # close file with timestamps  -ncd
        fdata14.close()  # close file with timestamps  -ncd
        fdata15.close()  # close file with timestamps  -ncd
        
        return channelCounts.append(counter)


#def channelSimulation(c, i, channelCounts ): # dont pass channelCounts because it is global! -ncd
def channelSimulation(c, i ): 
#        This function takes inputs c and i where c is the channel (list) and i is the number of the channel (int) and; 
#        1) Counts the number of calibration counts/resets in c
#        2) Appends the number of counts to channelCounts for c
## THIS is edit to only return channel counts, instead of timestamps -ncd 2025

        ##os.system('rm timestamps*.csv')  # remove any existing timestamp file -ncd
        global channelCounts
        channelCounts = []
        
        ch = c[0]
        fifo_status_reg = c[1]
        ts_hi_reg = c[2]
        ts_lo_reg = c[3]
        data = []
        counter = 0
        ch_wr_rst_busy, ch_almost_full, ch_full, ch_rd_rst_busy, ch_almost_empty, ch_empty = read_ch_status(fifo_status_reg)
        print('ch_empty= ', ch_empty)
        while (ch_empty != 1):
            current_ts = read_ch_fifo(ch, ts_hi_reg, ts_lo_reg)
            #print("current_ts= ", current_ts, "i= ", i)  # prints out time stamps (5ns counts)  -ncd
 
            data.append(current_ts)
            ch_wr_rst_busy, ch_almost_full, ch_full, ch_rd_rst_busy, ch_almost_empty, ch_empty = read_ch_status(fifo_status_reg)
            counter = counter+1;
            channelCounts[i].append(counter)
        #print('Channel ' + str(ch) + ' calibration counts are: ' + str(counter))
        #return channelCounts.append(counter) # this breaks things -ncd


