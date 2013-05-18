#!/usr/bin/env python
import numpy
from os import environ
from os.path import dirname, abspath, join
import sys
module_path = join(dirname(abspath(__file__)), '..', 'python')
sys.path.insert(0,module_path)
environ['DRUNKARDSWALK_LIB'] = \
        join(dirname(abspath(__file__)), '..', 'src', 'libdrunkardswalk.so')
from drunkardswalk import *


def dw(n):
    Q = numpy.zeros((3,3))
    R = numpy.zeros((3,2))
    Q[1,0] = Q[1,2] = 0.5
    R[0,0] = 1.0/float(n)
    Q[0,1] = 1.0-R[0,0]
    R[2,1] = 1.0/float(n)
    Q[2,1] = 1.0-R[2,1]
    c = numpy.ones(3)
    return Q,R,c

def soln(n):
    B = [ [.5+.5/n, .5-.5/n],
          [.5, .5],
          [0.5-.5/n, .5+.5/n]]
    return numpy.array(B)

def main():
    n=64
    Q,R,c = dw(n)

    failures = 0

    prec_to_name = {'f':'float','d':'double','dd':'dd_real','qd':'qd_real',
            'mp':'mpreal'}
    precs = ['f','d','dd','qd']
    if MPREAL_SUPPORT:
        precs.append('mp')

    tol = {'f':1e-5,'d':1e-10,'dd':1e-20,'qd':1e-40,'mp':1e-80}

    for prec in precs:
        print 'testing %s:' % prec_to_name[prec]
        t, B, res = solve_amc(Q,R,c,prec,mpreal_prec=512)
        residual = numpy.max(numpy.abs(B-soln(n)))
        if res > tol[prec] or not numpy.isfinite(res):
            print '        residual: %.3e > %.3e' % (residual, tol[prec])
            print '        test failed'
            failures += 1
        else:
            print '        residual: %.3e < %.3e' % (residual, tol[prec])
            print '        test passed'

    print 'ran %i tests' % len(precs)
    print '%i failures' % failures
    if failures > 0:
        sys.exit(1)

main()
