# Q-Pix Software Documentation

# Introduction

This is a refactoring of code previously written for the Q-Pix test setup. Directories like **outputs** and **configs** will contain many copies of similar files, but otherwise, this has been refactored to avoid copied code as much as possible.

# init.py

Formerly k:nown as “runMagicSequence.py,” this sets a handful of initial conditions that get Q-Pix up and running. This includes setting rst\_cal\_gap, reset\_width, the 10-bit DACs, performing integrator reset, and setting the serial interface.

# channels\_in\_use.csv

File that sets the working channels, this can be modified at any time and is referenced by any sampling done in either run\_calibration.py or run\_sampling.py. This is achieved through the function **get\_channels\_in\_use()** which is located in commands/helper\_functions.py, and returns a list with the contents of channels\_in\_use.csv. You can call get\_channels\_in\_use from wherever, assuming you have imported the helper\_functions.py module. For example:

| from commands.helper\_functions import \*for c in get\_channels\_in\_use():	print(c) \#or do something |
| :---- |

# configure.py

Given a configuration file name, this will run serial\_interface.py without having to use the Excel spreadsheet for the hex commands. A description of config files can be found later in this document. The file configure.py uses functions **read\_config\_file()** and **make\_serial\_command()** to extract the values from a given config file path, make a serial command, and run the serial interface with that command.

Usage:

| python3 configure.py 'configs/calibration.cfg' |
| :---- |

# run\_sampling.py

This file runs the sampling process for a given number of trials with user-selected variables at the top of the file. To select which channels are in use, please edit channels\_in\_use.csv. Outputs include counts and timestamps for each trial, which are written to both the console and an output file, which you can specify using the **output\_file** variable. If **overwrite\_old\_file** is True, it will delete the previously existing output file. Otherwise, it will add to the end of the previously existing output file. 

This script is meant to behave like samplesCollection\_ncd.py, which asserts window\_trig, triggers an arbitrary waveform generator, samples during a given window, and records counts and timestamps. This script calls functions in commands/sampling\_functions.py with specific settings for sampling (for one, asserting window\_trig, which is not done during calibration).

Usage:

| python3 run\_sampling.py |
| :---- |

# run\_calibration.py

This file is meant to behave like calibration\_sweep\_ncd.py, which runs the calibration routine over a given range of DAC settings for replenishment current. If you only want to run the calibration routine for one DAC setting, I suggest the following:

| DAC\_settings \= \[32\] \#or something like this |
| :---- |

A common option, however, would be the following:

| DAC\_settings \= range(32,16,-1) |
| :---- |

Like run\_sampling.py, run\_calibration.py calls functions in commands/sampling\_functions.py with specific settings for calibration instead of sampling.

# send\_trigger.py

This sends one trigger to the arbitrary waveform generator, and the results can be inspected on an oscilloscope.

# **commands**

Commands directory includes the lower-level commands that toggle certain settings, control the serial interface, etc. Each file in the commands directory is described below.

## helper\_functions.py

This file contains all helper\_functions that a user is unlikely to need to call directly from the terminal. The general goal is to move low-level, hex-encoded commands into this file so the user doesn’t need to worry about them. These functions include:

* **get\_channels\_in\_use()** reads the \~/channels\_in\_use.csv file and returns a list of integer “working” channels that will be used by other programs  
* **get\_channel\_registers(c)** takes an integer channel number and returns the fifo\_status\_reg, ts\_hi\_reg, and ts\_lo\_reg meant for reading FIFOs  
* **calibration\_pulse()** asserts REG\[0\] bit 4 without affecting other bits in the register  
* **startup()** asserts REG\[0\] bit 0, then desserts all bits in REG\[0\]  
  * Note: this turns external clocks off, which can be turned on again, either with the function set\_ext\_clock(1) or by running the toggle\_50MHz\_clock.py file (which calls that function)  
* **set\_ext\_clock(on)** asserts both REG\[0\] bits 16 and 17 without affecting other bits  
* **set\_win\_width(t)** sets the win width register bits without affecting other bits  
* **set\_rst\_cal\_gap(t)** sets the rst\_cal\_gap register bits without affecting other bits  
* **set\_reset\_width(t)** sets the reset\_width bits without affecting other bits  
* **set\_win\_wait(t)** sets the win\_wait bits without affecting other bits  
* **set\_sample\_select(on)** sets sample\_select bit without affecting other bits  
* **set\_delta\_t(on)** asserts the deltaT\_select bit  
* **read\_ch\_status(c)** reads the current status of the channel FIFOs  
* **read\_ch\_fifo(c)** reads the channel FIFOs for timestamps

In any file where you would like to use the above functions, you can add:

| from commands.helper\_functions import \* |
| :---- |

Though these functions aren’t really meant to be used outside of other routines, you can still call them in a python shell where helper\_functions is imported as above. Just start a python shell from the home directory: python3 and run the import line above.

## sampling\_functions.py

This file contains important functions used for sampling, called by both run\_calibration.py and run\_sampling.py, in slightly different ways. The main function is **sample\_n\_trials()**, which takes the number of trials, a win\_width, and win\_wait. These arguments can be passed in by whatever script calls this function.

## serial\_interface.py

Sends a hex-encoded command via serial interface. This is still usable, but \~/configure.py was created as a wrapper function to make reprogramming the serial interface a little easier, especially if you want to save all of your configurations. See the description of **configure.py** or **configs** for a more detailed description on how to send things easily via serial interface.

# **outputs**

This directory is largely free-form, but run\_sampling.py and run\_calibration.py should send their outputs here.

# **configs**

This directory will store .cfg files for the serial interface, so that the user can make custom serial interface settings. Send one of these settings through the serial interface via config.py.

The script that reads config files is rather rudimentary. It looks at the last character in each line and concatenates them to make a binary string, which is then converted to hex. This means that *order matters* when writing these files, and the keywords are just for readability. When making these config files, I suggest you copy an existing file and modify it.

For example, a configuration file begins like this:

| replCur1 \= 1replCur2 \= 1replCur3 \= 0replCur4 \= 1curReplen0 \= 0curReplen1 \= 1curReplen2 \= 0\#and so on... |
| :---- |

Apply a config file by running configure.py:

| python3 configure.py 'configs/filename.cfg' |
| :---- |

# **old\_files**

This directory will contain all old files.

## 
