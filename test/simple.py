#!/usr/bin/env python
import numpy
from os import environ
from os.path import dirname, abspath, join
import sys
module_path = join(dirname(abspath(__file__)), '..', 'python')
sys.path.insert(0,module_path)
environ['DRUNKARDSWALK_LIB'] = \
        join(dirname(abspath(__file__)), '..', 'src', 'libdrunkardswalk.so')
from drunkardswalk import solve_amc


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
    prec_to_name = {'f':'float','d':'double','dd':'dd_real','qd':'qd_real'}
    tol = {'f':1e-5,'d':1e-10,'dd':1e-20,'qd':1e-40}
    for prec in ['f','d','dd','qd']:
        print 'testing %s:' % prec_to_name[prec]
        t, B, res = solve_amc(Q,R,c,prec)
        residual = numpy.max(numpy.abs(B-soln(n)))
        if residual > tol[prec]:
            print '        residual: %.3e > %.3e' % (residual, tol[prec])
            print '        test failed'
            failures += 1
        else:
            print '        residual: %.3e < %.3e' % (residual, tol[prec])
            print '        test passed'

    print 'ran 4 tests'
    print '%i failures' % failures
    if failures > 0:
        sys.exit(1)

main()
