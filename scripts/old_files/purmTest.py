import os
import sys
import time

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

os.system('poke 0x43c0001c 0x00000cb2') # set delays and window widths 

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

def decade():
        ch = 2
        fifo_status_reg ='0x43c001bc'
        ts_hi_reg = '0x43c00118'
        ts_lo_reg = '0x43c0011c'
        data = []
        counter = 0
        ch_wr_rst_busy, ch_almost_full, ch_full, ch_rd_rst_busy, ch_almost_empty, ch_empty = read_ch_status(fifo_status_reg)
        while (ch_empty != 1):
            current_ts = read_ch_fifo(ch, ts_hi_reg, ts_lo_reg)
            data.append(current_ts)
            ch_wr_rst_busy, ch_almost_full, ch_full, ch_rd_rst_busy, ch_almost_empty, ch_empty = read_ch_status(fifo_status_reg)
            counter = counter+1;
        print('Channel ' + str(ch) + ' calibration counts are: ' + str(counter))
        #print('All the data is: ')
        #for i in range(0, len(data)):
        #   print(data[i])

for i in range(10):
	decade() 

