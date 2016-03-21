#!/usr/bin/python

import os
import func

#You can set directory informations here.
source = '/home/lixf/coop/gem5/m5out/output.txt'
target = './array3.txt'

func.to3array(source, target)

start = func.toStart(target)

points = 0
# points = func.getPoints()

func.CreatTypeFile('0', start, target, points)
func.CreatTypeFile('1', start, target, points)

func.draw()

#If you need middle files, disable this function.
func.delmidfile()
