### CALIBRATION SCRIPT ########################################
# Authors: PURM Students Summer 2024, NCD, ACG
# Usage: python3 run_calibration.py
# Notes: can run for a range of DAC settings OR one DAC setting
###############################################################

import sys
import os
import time
from commands.sampling_functions import *
from commands.helper_functions import *
import statistics as stats

### USER INPUTS ###
DAC_settings = range(32, 16, -1) 
#DAC_settings = [32]
trials_num  = 3
interface = 2
delta_t = 1
win_width = 64e-6
win_wait = 10e-6
reset_width = 50e-6
rst_cal_gap = 100e-9
config_file = 'configs/calibration.cfg'
external_clock = True
###################

if external_clock: set_ext_clock(1)
else: set_ext_clock(0)

set_sample_select(0)

def make_hex_command(DAC_setting): 
    #take integer setting, make a hex command that overwrites the first four entries in calibration.cfg
    default_settings_bin = read_config_file(config_file)
    DAC_setting_bin = bin(DAC_setting)[2:]
    replCur0 = DAC_setting_bin[4]
    replCur1_4 = DAC_setting_bin[:4][::-1]
    final_setting_bin = replCur1_4 + default_settings_bin[4:24] + replCur0 + default_settings_bin[25:]
    final_setting = int(final_setting_bin, 2)
    hex_command = f'0x{final_setting:08X}'
    return hex_command

for c in range(16):
    fname = f'outputs/ch{c}_calib.txt'
    if os.path.exists(fname):
        os.remove(fname)
        print(f'Deleted old file: {fname}')


print("Running Calibration...")
i = 0
set_delta_t(delta_t)
for DAC_setting in DAC_settings:
    i += 1
    hex_command = make_hex_command(DAC_setting)
    print(f'*** DAC setting: {str(DAC_setting)}, ({i} out of {len(DAC_settings)}) ***')
    os.system('python3 commands/serial_interface.py ' + str(interface) + ' "' + hex_command + '" ') 
    all_counts, all_timestamps = sample_n_trials(trials_num, win_width=win_width, win_wait=win_wait, reset_width = reset_width, rst_cal_gap=rst_cal_gap, cal_pulse=True, external_clock=external_clock)
    print()
    for c in range(16):
        fname = f'outputs/ch{c}_calib.txt'
        with open(fname, 'a') as f:
            counts = [counts[c] for counts in all_counts]
            f.write(f'DAC setting: {DAC_setting}\n')
            f.write(f'Counts: {counts}\n')
            f.write(f'Mean: {sum(counts)/len(counts):.2f}\n')
            f.write(f'Stdev: {stats.stdev(counts):.2f}\n')
            if c in get_channels_in_use():
                print(f'Channel {c} results:')
                print(f'Counts: {[counts[c] for counts in all_counts]}')
                print(f'Mean: {sum(counts)/len(counts):.2f}')
                print(f'Stdev: {stats.stdev(counts):.2f}')
    print("#"*10)
    print()
