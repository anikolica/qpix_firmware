# Written by PURM Students Summer 2024
# Meant to run the internal calibration 10 times
# python3 trigReadTen.py

import os
import sys
import time

print('Running Trig & Read FIFO all ch 10 times: ')
for i in range(10):
	os.system('trig_and_read_FIFO_all_ch.py')
