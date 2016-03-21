#!/usr/bin/python

import os

import MyFunctions

#get necessary information for functions
informations = MyFunctions.GetNecessaryInformation()
directory = informations[0]
patt = informations[1]
benchmarks = informations[2]
cycles = informations[3]
source = informations[4]
target = informations[5]
target_benchmark = informations[6]
choose = informations[7]

#change directory to gem5
os.chdir('/home/lixf/coop/gem5')

#here something for preheat 

#loop and get the information
if choose == 'n':
    MyFunctions.RunBenchmark(directory, patt, benchmarks, cycles, source, target, target_benchmark)
else:
    MyFunctions.RunAll(directory, patt, benchmarks, cycles, source, target)
