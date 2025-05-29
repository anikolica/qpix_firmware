import os
import sys
import time

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

channelCounts=[ch0Counts, ch1Counts, ch2Counts, ch3Counts, ch4Counts, ch5Counts, ch6Counts, ch7Counts, ch8Counts, ch9Counts, ch10Counts, ch11Counts, ch12Counts, ch13Counts, ch14Counts, ch15Counts]

def avgArr(ch):
	total = 0
	for i in range(0, len(ch)):
		total += ch[i]
	
	if len(ch)==0:
		return 0
	else:
		total = total / len(ch)
	
		return total

def read_ch_status(fifo_status_reg):
	#print ('FIFO status is: ')
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


def decade(c, i):
        os.system('poke 0x43c0001c 0x00000cb2') # set delays(first four:0000) and window widths(2nd 4: 0cb2) 
        print ('System Reset')
        os.system('poke 0x43c00000 0x00000001')
        os.system('poke 0x43c00000 0x00000000')
        os.system('poke 0x43c00000 0x00008000')

        #print ('Running calibration')
        #os.system('python3 Calibrate.py')
        time.sleep(0.1)

        os.system('poke 0x43c00000 0x00000000')  # reset stuff

        print('Attempting readout')

        #for [ch, fifo_status_reg, ts_hi_reg, ts_lo_reg] in [[2, '0x43c001bc', '0x43c00118', '0x43c0011c']]:
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
        print('Channel ' + str(ch) + ' calibration counts are: ' + str(counter))
        channelCounts[i].append(counter)
        #print('All the data is: ')
        #for i in range(0, len(data)):
        #   print(data[i])


for i in range(16): 
	cht = channels[i]
	for j in range(10):
		decade(cht, i)

	print("Array of counts: ")
	print(channelCounts[i])
	print("Average Number of Counts: ")
	print(avgArr(channelCounts[i]))

