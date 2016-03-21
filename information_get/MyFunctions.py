#!/usr/bin/python

import os
import re
import commands
import time

def GetNecessaryInformation():
    #local: benchmarks target_benchmark directory cycles source target_dir target patt
    #select the benchmark
    benchmarks = raw_input('Choose a benchmark suit:\n1.rodinia\n2.fkj\n3.nocopy\n-> ')

    #if only one benchmark, get the name information of it
    while True:
        choose = raw_input('You want to run all benchmarks?(y/n) ')
        if choose.lower() == 'n':
            target_benchmark = raw_input('Then which benchmark? -> ')
            break
        elif choose.lower() == 'y':
            target_benchmark = ''
            break
        else:
            print 'Only "y" or "n", fool!'

    #get directory information for functions
    directory = GetDirectory(benchmarks)

    #creat a file to save simulation result
    record = CreatRecord()
    cycles = record[0]
    source = record[1]
    target_dir = record[2]
    target = record[3]
    patt = record[4]

    return (directory, patt, benchmarks, cycles, source, target, target_benchmark, choose.lower())

def GetDirectory(benchmarks):
    if benchmarks == '1':
        directory = '/home/lixf/coop/benchmarks/rodinia/'
    elif benchmarks == '2':
        directory = '/home/lixf/coop/benchmarks/rodinia-nocopy-fkj/'
    elif benchmarks == '3':
        directory = '/home/lixf/coop/benchmarks/rodinia-nocopy/'
    return directory

def CreatRecord():
    #local: cycles, source, target_dir, target, patt
    #select cycles to loop
    cycles = raw_input('How many cycles do you want to loop: ')

    source = '/home/lixf/coop/gem5/m5out/output.txt'
    target_dir = '/home/lixf/coop/informations_get/'

    today = target_dir + time.strftime('%Y%m%d')
    now = time.strftime('%H%M%S')

    comment = raw_input('Enter the keyword you want to get(word1/word2/word3...)\n-> ')
    if len(comment) == 0:
        target = today + os.sep + now + '_' + cycles + '.txt'
    else :
        target = today + os.sep + now + '_' + cycles + '_' + comment.replace('/','&') + '.txt'

    if not os.path.exists(today):
        os.mkdir(today)

    patt = re.findall("[\w_]+", comment)
    return (cycles, source, target_dir, target, patt)

def RunBenchmark(directory, patt, benchmarks, cycles, source, target, target_benchmark):
    if target_benchmark == 'mummergpu':
        benchmark = os.path.join(directory, target_benchmark) + '/' + 'gem5_fusion_mummer'
    elif target_benchmark == 'ATAX':
        benchmark = os.path.join(directory, target_benchmark) + '/' + 'gem5_fusion_atax_m4.exe'
    elif target_benchmark == 'cfd':
        benchmark = os.path.join(directory, target_benchmark) + '/' + 'gem5_fusion_euler3d '
    elif target_benchmark == 'nw':
        benchmark = os.path.join(directory, target_benchmark) + '/' + 'gem5_fusion_needle'
    elif target_benchmark == '.hg' or target_benchmark == 'leukocyte' or \
    target_benchmark == 'common' or  target_benchmark == 'particlefilter': 
        benchmark = ''
    else:
        benchmark = os.path.join(directory, target_benchmark) + '/' + 'gem5_fusion_' + target_benchmark

    cmd = 'build/X86_VI_hammer_GPU/gem5.opt ../gem5-gpu/configs/se_fusion.py -c ' + benchmark
    if benchmarks == '3' or benchmarks == '2':
        cmd = cmd + ' --access-host-pagetable'
    opinion = raw_input('any other opinion for cmd?(Press enter if not)\n->')
    if len(opinion) != 0:
        cmd = cmd + ' ' + opinion

	print cmd

    for i in range(1, int(cycles) + 1):
        rm = commands.getoutput(cmd)
        print rm
        for j in patt:
            if j != '' :
                stats = open(source, 'r')
                wanted = open(target, 'a')
                keyword = '\w*' + j + '\w*'
                for eachLine in stats:
                    m = re.findall(keyword, eachLine)
                    if len(m) > 0:
                        wanted.writelines(repr(i) + eachLine)
                stats.close()
                wanted.close()

def RunAll(directory, patt, benchmarks, cycles, source, target):
    for root, dirs, filename in os.walk(directory):
        for benchmark in dirs:
            if benchmark == 'mummergpu':
                cmd = 'build/X86_VI_hammer_GPU/gem5.opt ../gem5-gpu/configs/se_fusion.py -c ' + os.path.join(root, benchmark) + '/' +'gem5_fusion_mummer'
            elif benchmark == 'cfd':
                cmd = 'build/X86_VI_hammer_GPU/gem5.opt ../gem5-gpu/configs/se_fusion.py -c ' + os.path.join(root, benchmark) + '/' +'gem5_fusion_euler3d'
            elif benchmark == 'nw' or benchmark == 'leukocyte' or benchmark == 'common' or benchmark == '.hg' or benchmark == 'particlefilter':
                continue
            else:
                cmd = 'build/X86_VI_hammer_GPU/gem5.opt ../gem5-gpu/configs/se_fusion.py -c ' + os.path.join(root, benchmark) + '/' +'gem5_fusion_' + benchmark
            test_cmd = re.findall('/', cmd)
            if benchmarks == '3':
                cmd = cmd + ' --access-host-pagetable'
            if len(test_cmd) == 12:
                for i in range(1, int(cycles)+1):
                    rm = commands.getoutput(cmd)
                    print 4 * '\n'
                    print 10 * '*' + 'Here comes a new benchmark!' + 10 * '*'
                    print 4 * '\n'
                    for j in patt:
                        if j != '' :
                            stats = open(source, 'r')
                            wanted = open(target, 'a')
                            keyword = '\w*' + j + '\w*'
                            for eachLine in stats:
                                m = re.findall(keyword, eachLine)
                                if len(m) > 0:
                                    wanted.writelines(repr(i) + eachLine)
                            stats.close()
                            wanted.close()
