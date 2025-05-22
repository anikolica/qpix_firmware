### SAMPLE COLLECTION SCRIPT ##################################
# Authors: PURM Students Summer 2024, NCD, ACG
# Usage: python3 run_sampling.py
# Notes: samples all channels_in_use for a number of trials
###############################################################

import os
import sys
import time
import datetime
from commands.helper_functions import *
from commands.sampling_functions import *

### USER-DEFINED VALUES ###
win_width = 64e-6
win_wait = 5e-6 
reset_width = 5e-6
rst_cal_gap = 100e-9
trials_num = 3
interface = 2
external_clock = True
output_file = 'outputs/sampling_results.txt'
overwrite_old_file = False
###########################

if external_clock: set_ext_clock(1)
else: set_ext_clock(0)

set_sample_select(1) #ignores delta t

print(f'Sampling working channels with win width: {win_width}, win_wait: {10e-6}, reset_width: {reset_width}, number of trials: {trials_num}')
all_counts, all_timestamps = sample_n_trials(trials_num, win_width=win_width, win_wait=win_wait, reset_width=reset_width, rst_cal_gap = rst_cal_gap, external_clock=external_clock, sampling=True)

# record values in a running document that separates sampling by date + time
if overwrite_old_file:
    if os.path.exists(output_file):
        os.remove(output_file)
        print("\nOverwriting existing output file.")
else: print("\nAppending to existing output file.")
with open(output_file, 'a') as f:
    f.write(f'Sampling results below finished at: {datetime.datetime.now()}\n')
    print('\nRESULTS:')
    for c in range(16):
        if c not in get_channels_in_use(): continue
        f.write(f'Channel {c} results\n')
        print(f'Channel {c} results')
        f.write(f'Counts: {[counts[c] for counts in all_counts]}\n')
        print(f'Counts: {[counts[c] for counts in all_counts]}')
        for trial in range(trials_num):
            f.write(f'Trial {trial} timestamps: {all_timestamps[trial][c]}\n')
            print(f'Trial {trial} timestamps: {all_timestamps[trial][c]}')
        f.write('\n')
        print()
    f.write('******************************************************\n')
    f.close()



