#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Reads and plots circular dichroism data.
Created on Tue Oct 11 16:13:06 2016

@author: Jikun Li<jikunli@cmu.edu>
"""
import numpy
import matplotlib.pyplot as plt

def readCD(filename):
    with open(filename, mode='r') as f1:
        [f1.readline() for j in range(14)]
        nPoints = int(f1.readline().split()[1])
        [f1.readline() for j in range(4)]
        CD1 = []; HT1 = []; wl1 = [];
        for j in range(nPoints):
            line1 = [float(x) for x in f1.readline().split()]
            wl1.append(line1[0])
            CD1.append(line1[1])
            HT1.append(line1[2])
        f1.close()
    return numpy.array(wl1), numpy.array(CD1), numpy.array(HT1)
    
#fig_count = 0

def plotCD(wl, CD, HT, textLabel):
#    global fig_count
#    fig_count += 1
    fig1, ax1 = plt.subplots(2, sharex = True)
    nPlots = len(wl)
    if (nPlots == len(CD)) and (nPlots == len(HT)) and (nPlots == len(textLabel)):
        for j in range(nPlots):
            ax1[1].plot(wl[j], HT[j], label = textLabel[j])
            ax1[0].plot(wl[j], CD[j], label = textLabel[j])    
        plt.legend(bbox_to_anchor=(0., 2.22, 1., 0.1), loc=3,
           ncol=min(nPlots, 4), mode="expand", borderaxespad=0.)
        plt.xlabel('Wavelength (nm)', fontsize=16)
        plt.tick_params(axis='both', labelsize=14)
        plt.show()

def plotFiles(filenames, transform=[], labels=[]): 
    wl = []; CD = []; HT = [];
    for file1 in filenames:
        wl1, CD1, HT1 = readCD(file1)
        wl.append(wl1)
        CD.append(CD1)
        HT.append(HT1)
    if transform and numpy.array([numpy.abs(wl[j] - wl[0]) for j in range(1, len(wl))]).max() == 0.0:
        transform_ = numpy.array(transform)
        wl_ = numpy.array([wl1 for j in range(transform_.shape[0])])
        CD_ = numpy.dot(transform_, CD)
        HT_ = numpy.dot(transform_, HT)
        r = len(transform)
    else:
        wl_ = wl; CD_ = CD; HT_ = HT
        r = len(filenames)
    if labels and len(labels) >= r:
        labels_ = labels[0:r]
    else:
        labels_ = filenames[0:r]
    plotCD(wl_, CD_, HT_, labels_)
