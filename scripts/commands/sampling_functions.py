import os
import sys
import time
import datetime
from commands.helper_functions import *

def sample_channel(c): #sample one channel
    timestamps = []
    counter = 0
    ch_wr_rst_busy, ch_almost_full, ch_full, ch_rd_rst_busy, ch_almost_empty, ch_empty = read_ch_status(c)
    while (ch_empty != 1):
        current_ts = read_ch_fifo(c)
        timestamps.append(current_ts)
        ch_wr_rst_busy, ch_almost_full, ch_full, ch_rd_rst_busy, ch_almost_empty, ch_empty = read_ch_status(c)
        counter += 1
    print('\tChannel ' + str(c) + ' counts are: ' + str(counter))
    return counter, timestamps

def sample_working_channels(): #for one trial, sample all working channels
    working_channels = get_channels_in_use()
    trial_counts = [] #counts for each channel in this trial
    trial_timestamps = [] #timestamps for each channel in this trial ([channel][timestamp number])
    for c in range(16):
        if c in working_channels:
            count, timestamps = sample_channel(c)
            trial_counts.append(count)
            trial_timestamps.append(timestamps)
        else:
            trial_counts.append(0)
            trial_timestamps.append([])
    return trial_counts, trial_timestamps

def sample_n_trials(trials_num, win_width=64e-6, win_wait=10e-6, reset_width=50e-6,\
                                rst_cal_gap=100e-9,external_clock=True, cal_pulse=False, sampling=False):
    set_win_width(win_width)
    set_win_wait(win_wait)
    set_reset_width(reset_width)
    set_rst_cal_gap(rst_cal_gap)

    all_counts = [] #2D list containing each trial's channel counts ([trial][channel])
    all_timestamps = [] #3D list containing each trial's timestamps ([trial][channel][[timestamp number])

    startup() # system reset: note this turns ext clock off.
    for j in range(trials_num): 
        if external_clock: set_ext_clock(1) #clock back on!!
        else: set_ext_clock(0)
        if cal_pulse: calibration_pulse() #if calibrating, assert calibration sequence
        if sampling: sample_pulse() #if sampling, assert sampling sequence
        print("\tTrial: " , j+1 , " of " , trials_num)
        trial_counts, trial_timestamps = sample_working_channels() #sample
        all_counts.append(trial_counts)
        all_timestamps.append(trial_timestamps)
        startup() #important: this deasserts the calibration or sampling sequence
    return all_counts, all_timestamps

