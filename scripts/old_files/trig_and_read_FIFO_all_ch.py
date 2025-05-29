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

print ('System Reset')
os.system('poke 0x43c00000 0x00000001')
os.system('poke 0x43c00000 0x00000000')

print ('Running calibration')
os.system('python3 Calibrate.py')
time.sleep(0.1)

print('Attempting readout')
for [ch, fifo_status_reg, ts_hi_reg, ts_lo_reg] in [[0, '0x43c001b4', '0x43c00108', '0x43c0010c'],
                                                   [1, '0x43c001b8', '0x43c00110', '0x43c00114'],
                                                   [2, '0x43c001bc', '0x43c00118', '0x43c0011c'],
                                                   [3, '0x43c001c0', '0x43c00120', '0x43c00124'],
                                                   [4, '0x43c001c4', '0x43c00128', '0x43c0012c'],
                                               #    [5, '0x43c001c8', '0x43c00130', '0x43c00134'],
                                                   [6, '0x43c001cc', '0x43c00138', '0x43c0013c'],
                                                   [7, '0x43c001d0', '0x43c00140', '0x43c00144'],
                                                   [8, '0x43c001d4', '0x43c00148', '0x43c0014c'],
                                                   [9, '0x43c001d8', '0x43c00150', '0x43c00154'],
                                                   [10, '0x43c001dc', '0x43c00158', '0x43c0015c'],
                                                   [11, '0x43c001e0', '0x43c00160', '0x43c00164'],
                                                   [12, '0x43c001e4', '0x43c00168', '0x43c0016c'],
                                                   [13, '0x43c001e8', '0x43c00170', '0x43c00174'],
                                                   [14, '0x43c001ec', '0x43c00178', '0x43c0017c'],
                                                   [15, '0x43c001f0', '0x43c00180', '0x43c00184']]:
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

