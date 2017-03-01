#/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 10:51:40 2016

@author: jikunli@cmu.edu
"""

import numpy
import matplotlib.pyplot as plt

def read_mb(filename, nPoints=256):
    with open(filename, mode='r') as f1:
        delta = [];
        intensity = [];
        [f1.readline() for j in range(10)]
        for j in range(nPoints):
            line1 = [float(x) for x in f1.readline().split()]
            delta.append(line1[0])
            intensity.append(line1[1])
        return numpy.array(delta), numpy.array(intensity)
