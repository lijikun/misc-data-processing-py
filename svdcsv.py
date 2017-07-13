#/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Reads stopped-flow .csv data files.

@author: jikunli@cmu.edu
"""

import numpy
import matplotlib.pyplot as plt

def read_csv(filename):
    with open(filename, mode='r') as f1:
        nt = 0
        t = []
        Z = []
        wl = []        
        while True:
            line1 = f1.readline()
            if 'Time,' in line1:
                nt = int(line1.split(sep=',')[1].split()[0])
                break
        while True:
            line1 = f1.readline()
            if 'Time,Wavelength' in line1:
                line1 = f1.readline()
                wl = [float(x) for x in line1.split(sep=',')[1:-1]]
                break
        if wl:
            for j in range(nt):
                line1 = [float(x) for x in f1.readline().split(sep=',')]
                t.append(line1[0])
                Z.append(line1[1:])
        f1.close()
        return numpy.array(Z), numpy.array(wl), numpy.array(t)

fig_count = 0
       
def plot_timetraces(Z, wl, t, wavelengths, ref = False, rel = False):
    if ref:
        Z_ = self_ref(Z)
    else:
        Z_ = Z
    global fig_count
    plt.figure(fig_count)    
    fig_count += 1    
    for wl1 in wavelengths:
        wl1_index = abs(wl - wl1).argmin()
        y = numpy.copy(Z_[:, wl1_index])
        if rel:
            y /= y[0]
        plt.plot(t, y, label = "{0:.2f} nm".format(wl[wl1_index]), linewidth = 2.0)        
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), ncol=min(len(wavelengths), 4), loc=3, mode="expand", borderaxespad=0.)
    plt.xscale('log')
    plt.xlabel('Time (s)')
    plt.show()
    
def plot_spectra(Z, wl, t, timepoints, ref = False):
    if ref:
        Z_ = self_ref(Z)
    else:
        Z_ = Z
    global fig_count
    plt.figure(fig_count)
    fig_count += 1
    for t1 in timepoints:
        t1_index = abs(t - t1).argmin()
        y = Z_[t1_index, :]
        plt.plot(wl, y, label = "{0:.4g} s".format(t[t1_index]), linewidth = 2.0)
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), ncol=min(len(timepoints), 4), loc=3, mode="expand", borderaxespad=0.)
    plt.xlabel('Wavelength (nm)')    
    plt.show()
    
def add_data(filenames, weight = []):    
    n = len(filenames)
    Z = []; wl = []; t = []
    for file1 in filenames:
        Z1, wl1, t1 = read_csv(file1)
        if not Z:
            wl = wl1; t = t1
        elif (wl1 != wl).any() or (t1 != t).any():
            print('Error: Spectra not taken under the same condition.')
            return
        Z.append(Z1)
    if not weight:
        weight = [1.0 / n] * n
    Z_ = numpy.zeros(Z[0].shape)
    for i in range(n):
        Z_ += Z[i] * weight[i]
    return Z_, wl, t
    
def plot_data(filenames, wavelengths = [], timepoints = [], weight = [], ref = False):
    Z, wl, t = add_data(filenames, weight = weight)
    if wavelengths:
        plot_timetraces(Z, wl, t, wavelengths = wavelengths, ref = ref)
    if timepoints:
        plot_spectra(Z, wl, t, timepoints = timepoints, ref = ref)
    
def plot_svd(wl, t, U, V, n):
    global fig_count
    fig1 = plt.figure(fig_count)
    fig_count += 1
    fig1a = fig1.add_subplot(121)
    fig1b = fig1.add_subplot(122)
    for j in range(n):
        fig1a.plot(wl, V[j], label = 'Vector ' + str(j), linewidth = 2.0)
        fig1b.plot(t, U[:, j], label = 'Vector ' + str(j), linewidth = 2.0)        
    fig1b.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    fig1a.set_xlabel('Wavelength (nm)', fontsize=16)
    fig1a.tick_params(axis='both', which='major', labelsize=14)    
    fig1b.set_xscale('log')
    fig1b.set_xlabel('Time (s)', fontsize=16)
    fig1b.tick_params(axis='both', which='major', labelsize=14) 
    plt.show()
    
def plot2_svd(filename, wl0 = 250, wl1 = 750, n = 4, ref = False, 
             baseline = '', rot = 0, p = 10, 
             wavelengths = [], timepoints = [], weight = [], rel = False):
    # Reads raw data, process if multiple files are given.
    if filename.__class__.__name__ == 'list':
        Z, wl, t = add_data(filename, weight = weight)
    else:
        Z, wl, t = read_csv(filename)
    # Plots the mundane plots first.
    if wavelengths:
        plot_timetraces(Z, wl, t, wavelengths, rel = rel)
    if timepoints:
        plot_spectra(Z, wl, t, timepoints)
    # Weighs data by baseline.
    if baseline:
        Z0 = read_baseline(baseline)        
        for j in range(Z.shape[1]):
                Z[:, j] *= Z0[j]
    # Calculates difference spectra.
    if ref:
        Z = self_ref(Z)
    # Truncates the data according to wavelengths.
    wl_ = wl[(wl >= wl0) & (wl <= wl1)]
    Z_ = Z[:, (wl >= wl0) & (wl <= wl1)]    
    # Does the real SVD.
    U_, s_, V_ = numpy.linalg.svd(Z_)
    # Performs rotation.
    if rot == 1:
        R = rot_autocorr(U_, p)
        U_ = numpy.dot(U_, R)
        V_ = numpy.dot(U_.T, Z_)
    elif rot == 2:
        R = rot_autocorr(V_.T, p)
        V_ = numpy.dot(R.T, V_)
        U_ = numpy.dot(Z_, V_.T)
    else:
        print(s_[0:n])
    # Reverses baseline weighing if done initially.
    if baseline:
        Z0_ = Z0[(wl >= wl0) & (wl <= wl1)]
        for j in range(Z_.shape[1]):
            Z_[:, j] /= Z0_[j]
            V_[:, j] /= Z0_[j]
    # Plots the data.
    plot_svd(wl_, t, U_, V_, n)
    # return Z_, wl_, t, U_, s_, V_
    
def read_baseline(baseline):
    with open(baseline, mode='r') as f2:
        Z0 = []
        [f2.readline() for j in range(24)]
        for j in range(256):
            Z0.append(float(f2.readline().split(sep=',')[1]))
    return numpy.array(Z0)
    
def self_ref(Z):
    n0, n1 = Z.shape
    Z_ = numpy.zeros((n0, n1))
    for i in range(n0):
        for j in range(n1):
            Z_[i, j] = Z[i, j] - Z[0, j] -  Z[i, -1]
    return Z_
    
def rot_autocorr(U, p):
    n0, n1 = U.shape
    Corr = numpy.zeros((p, p))
    for i in range(p):
        for j in range(p):
            corr1 = 0.0
            for k in range(n0 - 1):
                corr1 += (U[k, i] * U[k + 1, j])
            Corr[i, j] = corr1
    w, v = numpy.linalg.eigh((Corr + Corr.T) / 2.0)
    R = numpy.identity(n1)
    R[0:p, 0:p] = numpy.fliplr(v)
    return R
