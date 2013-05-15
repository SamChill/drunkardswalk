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
    prec = 'dd'
    n=1e300
    Q,R,c = dw(n)
    t, B, res = solve_amc(Q,R,c,prec)

    residual = numpy.max(numpy.abs(B-soln(n)))
    print "%.3e" % residual

main()
