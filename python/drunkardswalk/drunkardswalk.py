#!/usr/bin/env python
import ctypes
import ctypes.util
import numpy as np
from numpy.ctypeslib import ndpointer
from sys import stderr, exit
from os import environ
from os.path import join, abspath, dirname, isfile
import signal

__all__ = ['MPREAL_SUPPORT', 'solve_amc']

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

libdw = ctypes.CDLL(libpath)

MPREAL_SUPPORT = True
try:
    getattr(libdw, 'solve_amc_mpreal')
except AttributeError:
    MPREAL_SUPPORT = False

def solve_amc(Q, R, c, prec='dd', mpreal_prec=512):

    if prec == 'f':
        solve = libdw.solve_amc_float
    elif prec == 'd':
        solve = libdw.solve_amc_double
    elif prec == 'dd':
        solve = libdw.solve_amc_ddreal
    elif prec == 'qd':
        solve = libdw.solve_amc_qdreal
    elif prec == 'mp':
        if MPREAL_SUPPORT == False:
            msg =  "Drunkard's Walk not compiled with mpreal support\n"
            msg += 'recompile library with "make USE_MPREAL=1"'
            raise ValueError(msg)
        libdw.set_mpreal_prec(mpreal_prec)
        solve = libdw.solve_amc_mpreal
    else:
        raise ValueError('Unknown prec value "%s"' % prec)
    # void solve(int Qsize, double *Qflat, int Rcols, double *Rflat, 
    #           double *c_in, double *B, double *t, double *residual)
    ntrans = Q.shape[0]
    nabs = R.shape[1]
    B = np.zeros((ntrans,nabs))
    t = np.zeros(ntrans)
    residual = np.zeros(1)
    singular = ctypes.c_int()

    d_ptr = ndpointer(dtype=np.float64,flags=('C_CONTIGUOUS','WRITEABLE'))
    solve.argtypes = [ctypes.c_int, d_ptr, ctypes.c_int, d_ptr,
            d_ptr, d_ptr, d_ptr, d_ptr, ctypes.POINTER(ctypes.c_int)]

    #make control-c work when calling c code
    old_handler = signal.signal(signal.SIGINT, signal.SIG_DFL)

    solve(ntrans, Q, nabs, R, c, B, t, residual, ctypes.byref(singular))

    #reset signal handler back to previous value
    old_handler = signal.signal(signal.SIGINT, old_handler)

    residual = residual[0]

    if singular.value == 1:
        singular = True
    else:
        singular = False

    return t, B, residual, singular
