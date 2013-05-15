#!/usr/bin/env python
import ctypes
import ctypes.util
import numpy as np
from sys import stderr, exit
from os import environ
from os.path import join, abspath, dirname, isfile

libpath = None
if 'DRUNKARDSWALK_LIB' in environ:
    libpath = environ['DRUNKARDSWALK_LIB']
else:
    libpath = join(dirname(abspath(__file__)), 'libdrunkardswalk.so')
    if not isfile(libpath):
        libpath = ctypes.util.find_library('drunkardswalk')
if libpath == None:
    stderr.write('ERROR: unable to locate libdrunkardswalk.so\n')
    stderr.write('       either install to a standard location\n')
    stderr.write('       or set the environment variable DRUNKARDSWALK_LIB\n')
    exit(1)

libmcamc = ctypes.CDLL(libpath)

def solve_amc(Q, R, c, prec='dd'):
    Qflat = list(Q.ravel())
    Qflat = (ctypes.c_double * len(Qflat))(*Qflat)
    Rflat = list(R.ravel())
    Rflat = (ctypes.c_double * len(Rflat))(*Rflat)
    cflat = list(c)
    cflat = (ctypes.c_double * len(cflat))(*cflat)

    Bflat = (ctypes.c_double * len(Rflat))()
    tflat = (ctypes.c_double * len(cflat))()

    residual = (ctypes.c_double * 1)()

    if prec == 'f':
        solve = libmcamc.solve_amc_float
    elif prec == 'd':
        solve = libmcamc.solve_amc_double
    elif prec == 'dd':
        solve = libmcamc.solve_amc_ddreal
    elif prec == 'qd':
        solve = libmcamc.solve_amc_qdreal
    else:
        raise ValueError('Unknown prec value "%s"' % prec)
    # void solve(int Qsize, double *Qflat, int Rcols, double *Rflat, 
    #           double *c_in, double *B, double *t)
    solve(Q.shape[0], Qflat, R.shape[1], Rflat, cflat, Bflat, tflat, residual)

    B = np.array(list(Bflat)).reshape(R.shape)
    t = list(tflat)
    residual = list(residual)[0]

    return t, B, residual
