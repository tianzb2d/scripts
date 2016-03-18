#!/usr/bin/python

import commands
import os
import re
import time

import MyFunctions

directory = ''
patt = ''
benchmarks = ''
cycles = ''
source = ''
target = ''
target_benchmark = ''

#get necessary information for functions
informations = MyFunctions.GetNecessaryInformation()
directory = informations[0]
patt = informations[1]
benchmarks = informations[2]
cycles = informations[3]
source = informations[4]
target = informations[5]
target_benchmark = informations[6]

#change directory to gem5
os.chdir('/home/tianzb/gem5-gpu/gem5')

#here something for preheat

#loop and get the information
MyFunctions.RunBenchmark(directory, patt, benchmarks, cycles, source, target, target_benchmark)
MyFunctions.RunAll(directory, patt, benchmarks, cycles, source, target)
