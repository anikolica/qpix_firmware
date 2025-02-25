## My modules
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


def channelSimulation(c, i, channelCounts):
#        This function takes inputs c and i where c is the channel (list) and i is the number of the channel (int) and; 
#        1) Counts the number of calibration counts/resets in c
#        2) Appends the number of counts to channelCounts for c

#        channelCounts = []
        


        ch = c[0]
        fifo_status_reg = c[1]
        ts_hi_reg = c[2]
        ts_lo_reg = c[3]
        data = []
        counter = 0
        ch_wr_rst_busy, ch_almost_full, ch_full, ch_rd_rst_busy, ch_almost_empty, ch_empty = read_ch_status(fifo_status_reg)
        while (ch_empty != 1):
            current_ts = read_ch_fifo(ch, ts_hi_reg, ts_lo_reg)
            data.append(current_ts)
            ch_wr_rst_busy, ch_almost_full, ch_full, ch_rd_rst_busy, ch_almost_empty, ch_empty = read_ch_status(fifo_status_reg)
            counter = counter+1;
        channelCounts[i].append(counter)

        print('Channel ' + str(ch) + ' calibration counts are: ' + str(counter))
        return channelCounts.append(counter)



