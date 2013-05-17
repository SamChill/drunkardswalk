#!/usr/bin/env python
import ctypes
import ctypes.util
import numpy as np
from numpy.ctypeslib import ndpointer
from sys import stderr, exit
from os import environ
from os.path import join, abspath, dirname, isfile

libpath = None
if 'DRUNKARDSWALK_LIB' in environ:
    #env var takes precidence
    libpath = environ['DRUNKARDSWALK_LIB']
else:
    #look in the directory that this file is in
    libpath = join(dirname(abspath(__file__)), 'libdrunkardswalk.so')
    #search standard places
    if not isfile(libpath):
        libpath = ctypes.util.find_library('drunkardswalk')
    #also make sure to check /usr/local/lib
    if libpath == None and isfile('/usr/local/lib/libdrunkardswalk.so'):
        libpath = '/usr/local/lib/libdrunkardswalk.so'
if libpath == None:
    stderr.write('ERROR: unable to locate libdrunkardswalk.so\n')
    stderr.write('       either install to a standard location\n')
    stderr.write('       such as /usr/lib or /usr/local/lib\n')
    stderr.write('       or set the environment variable DRUNKARDSWALK_LIB\n')
    exit(1)

libmcamc = ctypes.CDLL(libpath)

def solve_amc(Q, R, c, prec='dd'):

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
    #           double *c_in, double *B, double *t, double *residual)
    B = np.zeros(R.shape)
    t = np.zeros(c.shape)
    residual = np.zeros(1)

    c_ptr = ndpointer(dtype=np.float64,flags=('C_CONTIGUOUS','WRITEABLE'))
    solve.argtypes = [ctypes.c_int, c_ptr, ctypes.c_int, c_ptr,
            c_ptr, c_ptr, c_ptr, c_ptr]

    solve(Q.shape[0], Q, R.shape[1], R, c, B, t, residual)

    return t, B, residual
