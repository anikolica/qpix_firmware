import matplotlib.pyplot as plt
import csv
import os
import numpy as np
import statistics as stat

channels = [8, 10, 11, 12, 13, 14, 15]

dac_settings = [i for i in range(31, 14, -1)]

n_trials = 5

for c in channels:
    fname = "fch" + str(c) + ".csv"
    csvfile = open(fname, "r")
    csvreader = csv.reader(csvfile)
    last_line = csvreader[-1]
    values = last_line.split(",")
    values = values[2:]
    values = [int(string) for string in values]
    means = []
    stdevs = []

    for dac in dac_settings:
        first_five = values[0:n_trials]
        mean = 100/np.mean(first_five)
        means.append(mean)
        stdev = stat.stdev(first_five)
        stdevs.append(stdev)
        values = values[n_trials:]

    plt.plot(dac_settings, means)

    plt.errorbar(dac_settings, means, yerr=[stdev/np.sqrt(n_trials) for stdev in stdevs])

    plt.grid(True)

    plt.title(f'Channel {c} calibration curve')

    plt.xlabel("DAC Setting")

    plt.ylabel("fC/count")




