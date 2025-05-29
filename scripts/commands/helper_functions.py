### ALL HELPER FUNCTIONS ########################
# Authors: ACG
# Usage: from commands.helper_functions import *
# Notes: contains all low-level helper functions
#################################################

import os
import sys
import time
import csv

def get_channels_in_use():
    # returns a list of the channels in use, as defined by the .csv in the main directory
    try:
        with open('channels_in_use.csv',newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                channels = row
            return [int(c) for c in channels]    
    except FileNotFoundError:
        with open('../channels_in_use.csv',newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader: 
                channels = row
            return [int(c) for c in channels]

def get_channel_registers(c):
    # returns a list with the read_bit, ts_hi_reg, and ts_lo_reg 
    channel_registers = [[0, '0x43c001b4', '0x43c00108', '0x43c0010c'],
    [1, '0x43c001b8', '0x43c00110', '0x43c00114'],
    [2, '0x43c001bc', '0x43c00118', '0x43c0011c'],
    [3, '0x43c001c0', '0x43c00120', '0x43c00124'],
    [4, '0x43c001c4', '0x43c00128', '0x43c0012c'],
    [5, '0x43c001c8', '0x43c00130', '0x43c00134'],
    [6, '0x43c001cc', '0x43c00138', '0x43c0013c'],
    [7, '0x43c001d0', '0x43c00140', '0x43c00144'],
    [8, '0x43c001d4', '0x43c00148', '0x43c0014c'],
    [9, '0x43c001d8', '0x43c00150', '0x43c00154'],
    [10, '0x43c001dc', '0x43c00158', '0x43c0015c'],
    [11, '0x43c001e0', '0x43c00160', '0x43c00164'],
    [12, '0x43c001e4', '0x43c00168', '0x43c0016c'],
    [13, '0x43c001e8', '0x43c00170', '0x43c00174'],
    [14, '0x43c001ec', '0x43c00178', '0x43c0017c'],
    [15, '0x43c001f0', '0x43c00180', '0x43c00184']]
    return channel_registers[c][1:]

def calibration_pulse():
    initial_setting_hex = os.popen("peek 0x43c00000").read() #get initial setting of register, hex string
    initial_setting_bin = bin(int(initial_setting_hex[2:],16))[2:] #convert to binary string
    initial_setting_bin = '0'*(32-len(initial_setting_bin)) + initial_setting_bin #convert to 32-bit binary
    new_setting_bin = initial_setting_bin[0:27] + '1' + initial_setting_bin[28:] #insert a 1 in the desired bit
    new_setting_int = int(new_setting_bin, 2) #convert new setting to int
    new_setting_hex = f'0x{new_setting_int:08X}' #convert new setting to hex
    os.system(f'poke 0x43c00000 {new_setting_hex}') #poke new setting
    print('Asserting calibration pulse sequence on cal_control1,2 and RST_EXT1,2.')

def sample_pulse():
    initial_setting_hex = os.popen("peek 0x43c00000").read()
    initial_setting_bin = bin(int(initial_setting_hex[2:],16))[2:]
    initial_setting_bin = '0'*(32-len(initial_setting_bin)) + initial_setting_bin
    new_setting_bin = initial_setting_bin[0:16] + '1' + initial_setting_bin[17:]
    new_setting_int = int(new_setting_bin, 2)
    new_setting_hex = f'0x{new_setting_int:08X}'
    os.system(f'poke 0x43c00000 {new_setting_hex}')
    print('Asserting sampling sequence on window_trig.')


def startup():
    # resets FPGA internal logic. note: this turns of ext clock, so it may be good to turn back on
    os.system('poke 0x43c00000 0x00000001') #system reset
    print ('Asserting master logic reset...', end='')
    os.system('poke 0x43c00000 0x00000000')
    print(" done.")

def set_ext_clock(on):
    if on == 1:
        state = 'on'
        data = '11'
    elif on == 0: 
        state = 'off'
        data = '00'
    else:
        print("Invalid argument to set_ext_clock(). Options are 1 or 0.")
        sys.exit()
    initial_setting_hex = os.popen("peek 0x43c00000").read()
    initial_setting_bin = bin(int(initial_setting_hex[2:],16))[2:]
    initial_setting_bin = '0'*(32-len(initial_setting_bin)) + initial_setting_bin
    new_setting_bin = initial_setting_bin[0:14] + data + initial_setting_bin[16:]
    new_setting_int = int(new_setting_bin, 2)
    new_setting_hex = f'0x{new_setting_int:08X}'
    os.system(f'poke 0x43c00000 {new_setting_hex}')
    print(f'Replenishment clocks {state}.')

def set_win_width(t): # number of 50MHz clock ticks to sample data for
    width = int(t/20e-9)
    if not (0 <= width < (1<<33)): raise ValueError("Win_width must be a 32-bit unsigned integer")
    width_hex = f'0x{width:08X}'
    os.system('poke 0x43c0001c "' + width_hex + '" ') # set window widths 

def set_rst_cal_gap(t): # set reset cal gap in s
    initial_hex = os.popen('peek 0x43c00020').read()
    initial_bin = bin(int(initial_hex, 16))[2:]#want to make this into binary
    initial_bin = '0'*(32-len(initial_bin)) + initial_bin #32 bits!!! this is a string
    reset_width_bin = initial_bin[16:] #want to keep the 16 LSBs!!! this is a string
    rst_cal_gap = int(t/20e-9) #take user input for the second half, in decimal, change this from s to 50MHz clock ticks
    if not (0 <= rst_cal_gap < (1<<17)): raise ValueError("Rst_cal_gap must be a 16-bit unsigned integer")
    rst_cal_gap_bin = bin(rst_cal_gap)[2:] #make the second half in binary
    rst_cal_gap_bin = '0'*(16-len(rst_cal_gap_bin)) + rst_cal_gap_bin #16 bits!!!
    final_bin = rst_cal_gap_bin + reset_width_bin #concatenate the first and second half
    final = int(final_bin, 2) #put back into int
    os.system('poke 0x43c00020 "' + f'0x{final:08X}' + '" ')

def set_reset_width(t): # set reset width in set
    initial_hex = os.popen('peek 0x43c00020').read()
    initial_bin = bin(int(initial_hex, 16))[2:]#want to make this into binary
    initial_bin = '0'*(32-len(initial_bin)) + initial_bin #32 bits!!! this is a string
    rst_cal_gap_bin = initial_bin[0:16] #want to keep the 16 MSBs!!! this is a string
    reset_width = int(t/20e-9) #take user input for the second half, in decimal, change this from s to 50MHz clock ticks
    if not (0 <= reset_width < (1<<17)): raise ValueError("Reset width must be a 16-bit unsigned integer")
    reset_width_bin = bin(reset_width)[2:] #make the second half in binary
    reset_width_bin = '0'*(16-len(reset_width_bin)) + reset_width_bin #16 bits!!!
    final_bin = rst_cal_gap_bin + reset_width_bin #concatenate the first and second half
    final = int(final_bin, 2) #put back into int
    os.system('poke 0x43c00020 "' + f'0x{final:08X}' + '" ')

def set_win_wait(t): #set window wait in s
    initial_hex = os.popen('peek 0x43c00024').read() #get the initial setting of this address
    initial_bin = bin(int(initial_hex, 16))[2:]
    initial_bin = '0'*(32-len(initial_bin)) + initial_bin #32 bits!!! this is a string
    sample_select_bin = initial_bin[0] #MSB
    win_wait = int(t/20e-9) # get number of 50MHz clock ticks 
    if not (0 <= win_wait < (1<<32)): raise ValueError("Window wait must be a 31-bit unsigned integer")
    win_wait_bin = bin(win_wait)[2:]
    win_wait_bin = '0'*(31-len(win_wait_bin)) + win_wait_bin
    final_bin = sample_select_bin + win_wait_bin
    final = int(final_bin, 2)
    os.system('poke 0x43c00024 "' + f'0x{final:08X}' + '" ')

def set_sample_select(on): #set sample_select (1 or 0)
    if on not in (1,0): raise ValueError("Sample select must be 0 or 1")
    initial_hex = os.popen('peek 0x43c00024').read() #get the initial setting of this address
    initial_bin = bin(int(initial_hex, 16))[2:]
    initial_bin = '0'*(32-len(initial_bin)) + initial_bin #32 bits!!! this is a string
    win_wait_bin = initial_bin[1:]
    sample_select_bin = str(on)
    final_bin = sample_select_bin + win_wait_bin
    final = int(final_bin, 2)
    os.system('poke 0x43c00024 "' + f'0x{final:08X}' + '" ')

def set_delta_t(on): #set deltT_select (1 or 0)
    os.system('poke 0x43c00028 "' + f'0x{on:08x}' + '" ')
    print(f'deltaT_select set to {on}')

def read_ch_status(c):
    fifo_status_reg, ts_hi_reg, ts_lo_reg = get_channel_registers(c)
    #read current status of channel FIFO
    ch_read = os.popen('peek ' + fifo_status_reg).read()
    ch_status = int(ch_read, 16)
    ch_empty = (ch_status & 0x00000001)
    ch_almost_empty = (ch_status & 0x00000002) >> 1
    ch_rd_rst_busy = (ch_status & 0x00000003) >> 2
    ch_full = (ch_status & 0x00000010) >> 8
    ch_almost_full = (ch_status & 0x00000020) >> 9
    ch_wr_rst_busy = (ch_status & 0x00000030) >> 10
    return ch_wr_rst_busy, ch_almost_full, ch_full, ch_rd_rst_busy, ch_almost_empty, ch_empty

def read_ch_fifo(c):
    fifo_status_reg, ts_hi_reg, ts_lo_reg = get_channel_registers(c)
    os.system('poke 0x43c00018 ' + str(hex(1 << c)))
    os.system('poke 0x43c00018 0x00000000')
    fifo_ts_hi = os.popen('peek ' + ts_hi_reg).read()
    fifo_ts_lo = os.popen('peek ' + ts_lo_reg).read()
    fifo_ts = (int(fifo_ts_hi, 16) << 32) + int(fifo_ts_lo, 16)
    return fifo_ts

def read_config_file(filename):
    if not os.path.exists(filename):
        print(f'Error: Config file {filename} does not exist.')
        sys.exit()
    settings_string = ''
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0][-1] not in ('1', '0'):
                print(f'Error: Config file not formatted properly.')
                sys.exit()
            settings_string += row[0][-1]
    if len(settings_string) != 32:
        print(f'Error: Config file is wrong length.')
        sys.exit()
    return settings_string

def make_serial_command(settings_string): #takes input in binary
    hex_command = f'0x{int(settings_string, 2):08X}'
    return hex_command


