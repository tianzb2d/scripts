#!/usr/bin/python

'''This file contains some functions
we need when getting necessary informations
from output.txt (some parameters kaijie get)
and transform them into a diragram.'''

import re
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import pylab as pl

def to3array(OutputFileDir, Array3Dir):
    '''The key words in output.txt are like some strings,
    they are easy for human to read, but difficult for a
    computer to handle, so first transform these strings
    to arrays with three clomns.'''
    source = open(OutputFileDir, 'r')
    target = open(Array3Dir, 'w')

    i = 0
    patt = '\d+'
    for eachLine in source:
       num = re.search(patt, eachLine)
       if type(num) != type(None):
        target.write(num.group())
        target.write('\t')
        i = i + 1
       if i == 3:
        target.write('\n')
        i = 0

    source.close()
    target.close()

def getPoints():
    '''Sometimes the data is too large to put into
    one figure, this function can limit the points
    we use, CPU&GPU will have the same points as set.'''
    points = raw_input('Enter the points number here.\n-->')
    if len(points) == 0:
        points = '0'
    points = int(points)
    return points

def toStart(Array3Dir):
    '''We focus on the GPU&CPU requests together,
    so we need to skip the beginning where there are
    only CPU requests, that's what this function do.'''
    start = 0
    source = open(Array3Dir, 'r')
    for eachLine in source:
        num = re.match('1', eachLine)
        if type(num) != type(None):
            start = source.tell()
            source.seek(0, 2)
            end = source.tell()
            cycles = start - end
            print 'About %s points' %(cycles/4)
            break
    source.close()
    return start

def CreatTypeFile(coreType, start, Array3Dir, points):
    '''When we use plot function to draw a figure, it
    will be easier if we devide the two type requests,
    this function will do that.'''
    source = open(Array3Dir, 'r')
    source.seek(start)
    target = open('type' + coreType + '.txt', 'w')

    cnt = 0
    for eachLine in source:
        num = re.match(coreType, eachLine)
        if type(num) != type(None):
            target.write(eachLine)
            cnt = cnt + 1
            if cnt == points:
                break

    target.close()
    source.close()

def draw():
    '''Use matplotlib to draw the figure, and make some
    configurations to beauty the figure.'''
    end_tick = getKuadu()
    type0 = npload('type0.txt', end_tick)
    type1 = npload('type1.txt', end_tick)

    if len(type0) != 0:
        plot1 = pl.plot(type0[1], type0[2], 'ro')
    else:
        print 'No CPU Requests'
    if len(type1) != 0:
        plot2 = pl.plot(type1[1], type1[2], 'g*')
    else:
        print 'No GPU Requests'

    pl.ylim(0., 15.)
    pl.title('CPU&GPU Requests')
    pl.xlabel('Request Arrive Time')
    pl.ylabel('Bank ID')
    pl.savefig('pic.pdf')

def getKuadu():
    '''Sometimes the simulation time will be too long,
    and we just need a short period between it, this function
    will set the time, start from the first GPU request come.'''
    c = np.loadtxt('type0.txt')
    begin = c[0,1]
    end = c[len(c) - 1, 1]
    print 'About %s ticks' %(end - begin)
    tick_num = raw_input('How many ticks you want? (Not Necessery)\n--> ')
    if len(tick_num) == 0:
        tick_num = int(end - begin)
    return int(begin) + int(tick_num)

def npload(typefile, end_tick):
    '''This function transform the colomn into row, in
    order to be used by plot function.'''
    source = np.loadtxt(typefile)
    target = []
    for i in source:
        if i[1] < end_tick:
            target.append(i)
        else:
            break
    final = np.transpose(target)
    return final

def delmidfile():
    '''Delete the middle file to make directory clear.'''
    os.system('rm array3.txt type0.txt type1.txt')
