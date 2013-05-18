#!/usr/bin/env python
import numpy
from time import time
from os import environ
from os.path import dirname, abspath, join
import sys
module_path = join(dirname(abspath(__file__)), '..', 'python')
sys.path.insert(0,module_path)
environ['DRUNKARDSWALK_LIB'] = \
        join(dirname(abspath(__file__)), '..', 'src', 'libdrunkardswalk.so')
from drunkardswalk import *

def random_chain(t,r,p):
    Q = numpy.random.random((t,t))
    for i in xrange(len(Q)):
        Q[i,i] = 0.0
    R = p*numpy.random.random((t,r))
    c = numpy.ones(t)
    return Q,R,c

def main():
    Ntrans = 200
    Nabs = 50

    print 'PRECISION TESTING'
    print '-----------------'
    print 'Solving MCAMC problem with %i transient states and %i absorbing states' % (Ntrans, Nabs)
    print 'the p column represents the relative absorption probability'
    print 'error measured as the residual in the solution of the escape times:'
    print u'residual = ||(1-Q)*t - c||_\u221E'
    print

    if MPREAL_SUPPORT:
        print '| %5s | %8s | %8s | %8s | %8s | %8s |' % \
                ('p', 'float', 'double', 'dd_real', 'qd_real', 'mpreal')
        print '|:%5s:| %8s:| %8s:| %8s:| %8s:| %8s:|' % \
                ( 5*'-', 8*'-', 8*'-', 8*'-', 8*'-',8*'-')
    else:
        print '| %5s | %8s | %8s | %8s | %8s |' % \
                ('p', 'float', 'double', 'dd_real', 'qd_real')
        print '|:%5s:| %8s:| %8s:| %8s:| %8s:|' % \
                ( 5*'-', 8*'-', 8*'-', 8*'-', 8*'-')

    precs = ['f','d','dd','qd']
    if MPREAL_SUPPORT:
        precs.append('mp')

    for p in [1e-5,1e-8,1e-10,1e-15,1e-25,1e-28,1e-30,1e-40,1e-50,1e-60,1e-70]:
        errors = []
        for prec in precs:
            Q,R,c = random_chain(Ntrans,Nabs,p)
            t, B, res = solve_amc(Q,R,c,prec,mpreal_prec=512)
            errors.append(res)
        if MPREAL_SUPPORT:
            fmt = '| %5.0e | %8.1e | %8.1e | %8.1e | %8.1e | %8.1e |'
            print  fmt % (p,errors[0],errors[1],errors[2],errors[3], errors[4])
        else:
            fmt = '| %5.0e | %8.1e | %8.1e | %8.1e | %8.1e |'
            print  fmt % (p,errors[0],errors[1],errors[2],errors[3])


main()
