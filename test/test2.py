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

    failure = False
    for prec in ['f','d','dd','qd']:
        print 'testing precision %s' % prec
        t, B, res = solve_amc(Q,R,c,prec)
        residual = numpy.max(numpy.abs(B-soln(n)))
        if residual > 1e-5:
            print 'residual: %.3e test failed for prec %s' % (residual,prec)
            failure = True
        else:
            print 'residual: %.3e test passed for prec %s' % (residual,prec)

        if failure:
            sys.exit(1)

main()
