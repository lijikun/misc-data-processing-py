#!/usr/bin/python3

# Refactored stopped-flow data import and export
# from Applied Photophysics instruments.

from os import path
import numpy

def spliceData(z, w, t, wmin, wmax, tmin, tmax):
    if z.shape == (len(w), len(t)):
        return ((z[(w >= wmin) & (w <= wmax),:])[:, (t >= tmin) & (t <= tmax)],
                  w[(w >= wmin) & (w <= wmax)], 
                  t[(t >= tmin) & (t <= tmax)])
        

def exportData(z, w, t, fileName):
    fileName1 = fileName + ('.txt' 
                            if path.splitext(fileName)[1]!='.txt' else '')
    with open(fileName1, 'w') as f1:
        f1.write('Time')
        for w1 in w:
            f1.write('\t{0}'.format(w1))
        f1.write('\n')
        for j in range(len(t)):
            f1.write('{0}'.format(t[j]))
            for k in range(len(w)):
                f1.write('\t{0}'.format(z[k][j]))
            f1.write('\n')
    f1.close()

def importData(fileName):
    extension = path.splitext(fileName)[1]
    z = []
    t = []
    w = []
    flag_wt = False        
    with open(fileName, mode='r') as f1: 
        validFile = True
        # Searches for and reads header line.
        if extension == '.csv':
            while True: # two possible formats in input file
                line1 = f1.readline()
                if 'Time,Wavelength' in line1:
                    line1 = f1.readline()
                    try:
                        w = [float(x) for x in line1.split(sep=',')[1:-1]]
                    except ValueError:
                        validFile = False
                    break
                if 'Wavelength,Time' in line1:
                    line1 = f1.readline()
                    try:
                        t = [float(x) for x in line1.split(sep=',')[1:-1]]
                    except ValueError: 
                        validFile = False
                    flag_wt = True
                    break
                if not line1: # error: detects premature EOF 
                    break
        elif extension == '.txt':
            line1 = f1.readline()
            line1Items = line1.split()
            if line1Items[0] == 'Time' and len(line1Items) > 1:
                w = [float(x) for x in line1Items[1:]]
        # Reads the rest of the data, if any.        
        if w:
            sepString = ',' if extension == '.csv' else None
            while True:
                line1 = f1.readline()
                if line1.strip():
                    try:
                        line1_Numbers = [float(x) for x in line1.split(sep=sepString)]
                    except ValueError: 
                        validFile = False
                    if len(line1_Numbers) == 1 + len(w):
                        t.append(line1_Numbers[0])
                        z.append(line1_Numbers[1:])
                    else:
                        break
                else:
                    break
        elif t:
            while True:
                line1 = f1.readline()
                if line1.strip():
                    try:
                        line1_Numbers = [float(x) for x in line1.split(sep=',')] 
                    except ValueError: 
                        validFile = False
                    if len(line1_Numbers) == 1 + len(t):
                        w.append(line1_Numbers[0])
                        z.append(line1_Numbers[1:])
                    else:
                        break
                else:
                    break
    f1.close()
    if not (len(w) > 0 and len(t) > 0 and validFile):
        print("Invalid input file!")
    print(fileName, ': ', sum(len(x) for x in z), '=', len(w), '*', len(t))
    
    return (numpy.array(z if flag_wt else list(map(list, zip(*z)))),
            numpy.array(w), numpy.array(t))