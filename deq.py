#!/usr/bin/python3
''' Takes 3 float numbers as parameters in atomic unit, and calculates Moessbauer quadrupole splitting
in mm/s.

    Usage: deq.py eig1 eig2 eig3
'''

import sys
import math

try:
    eigs = sorted([float(x) for x in sys.argv[1:4]])
except ValueError:
    print("Invalid input!")
else:
    if abs(eigs[2]) < abs(eigs[0]):
        eigs[0], eigs[2] = eigs[2], eigs[0]
    eta = (eigs[1] - eigs[0]) / eigs[2] 
    ev = 0.5 * 9.717e21 * 0.16e-28 * eigs[2] * math.sqrt(1 + eta * eta / 3)
    mms = ev / 1.4413e4 * 2.9979e11
    print('DeltaEq = ', mms)
    print('eta = ', eta)
