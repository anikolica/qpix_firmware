import os
import sys
import time

def read_ch15_status():
	print ('ch0 FIFO status is: ')
	ch15_read = os.popen('peek 0x43c001b8').read()
	#time.sleep(0.1)
	ch15_status = int(ch15_read, 16)
	ch15_empty = (ch15_status & 0x00000001)
	ch15_almost_empty = (ch15_status & 0x00000002) >> 1 
	ch15_rd_rst_busy = (ch15_status & 0x00000003) >> 2
	ch15_full = (ch15_status & 0x00000010) >> 8
	ch15_almost_full = (ch15_status & 0x00000020) >> 9 
	ch15_wr_rst_busy = (ch15_status & 0x00000030) >> 10
	print ('empty: ' + str(ch15_empty) + ' almost empty: ' + str(ch15_almost_empty) + ' read reset busy: ' + str(ch15_rd_rst_busy))
	print ('full: ' + str(ch15_full) + ' almost full: ' + str(ch15_almost_full) + ' write reset busy: ' + str(ch15_wr_rst_busy))
	return ch15_wr_rst_busy, ch15_almost_full, ch15_full, ch15_rd_rst_busy, ch15_almost_empty, ch15_empty

def read_ch15_fifo():
	
	print ('Reading ch0 FIFO')
	os.system('poke 0x43c00018 0x00000002')
	#time.sleep(0.1)
	os.system('poke 0x43c00018 0x00000000')
	#time.sleep(0.1)
	fifo_ts_hi = os.popen('peek 0x43c00110').read()
	#time.sleep(0.1)
	fifo_ts_lo = os.popen('peek 0x43c00114').read()
	#time.sleep(0.1)
	fifo_ts = (int(fifo_ts_hi, 16) << 32) + int(fifo_ts_lo, 16)
	print ('ch0 FIFO word (timestamp) is: ' + str(fifo_ts))
	return fifo_ts

print ('System Reset')
os.system('poke 0x43c00000 0x00000001')
time.sleep(0.1)
os.system('poke 0x43c00000 0x00000000')
time.sleep(0.1)

os.system('python3 Calibrate.py')
time.sleep(0.1)

print('Attempting readout')
ch15_wr_rst_busy, ch15_almost_full, ch15_full, ch15_rd_rst_busy, ch15_almost_empty, ch15_empty = read_ch15_status()
data = []
counter = 0
while (ch15_empty != 1):
        current_ts = read_ch15_fifo()
        data.append(current_ts)
        ch15_wr_rst_busy, ch15_almost_full, ch15_full, ch15_rd_rst_busy, ch15_almost_empty, ch15_empty = read_ch15_status()
        counter = counter+1;
        print(counter)	

print('All the data is: ')
for i in range(0, len(data)):
    print(data[i])

