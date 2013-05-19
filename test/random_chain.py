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
    numpy.random.seed(42)
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
    print 'Solving MCAMC problem with %i transient states and %i absorbing states.' % (Ntrans, Nabs)
    print 'The p column represents the relative absorption probability.'
    print
    print 'The values in the columns represent the relative residual'
    print  'error in the solution of the time vector.'
    print 
    print 'If it is not possible to calculate the fundamental matrix,' 
    print 'i.e. if the matrix I-Q is near singular for the precision'
    print 'of the scalar type, the it is denoted with (S).'
    print

    if MPREAL_SUPPORT:
        print '| %5s | %10s | %10s | %10s | %10s | %10s |' % \
                ('p', 'float', 'double', 'dd_real', 'qd_real', 'mpreal')
        print '|:%5s:| %10s:| %10s:| %10s:| %10s:| %10s:|' % \
                ( 5*'-', 10*'-', 10*'-', 10*'-', 10*'-',10*'-')
    else:
        print '| %5s | %10s | %10s | %10s | %10s |' % \
                ('p', 'float', 'double', 'dd_real', 'qd_real')
        print '|:%5s:| %10s:| %10s:| %10s:| %10s:|' % \
                ( 5*'-', 10*'-', 10*'-', 10*'-', 10*'-')

    precs = ['f','d','dd','qd']
    if MPREAL_SUPPORT:
        precs.append('mp')

    for p in [1e-5,1e-8,1e-10,1e-15,1e-25,1e-28,1e-30,1e-40,1e-50,1e-60,1e-70]:
        residuals = []
        singulars = []
        print '| %2.0e |'%p,
        for prec in precs:
            Q,R,c = random_chain(Ntrans,Nabs,p)
            t, B, res, singular = solve_amc(Q,R,c,prec,mpreal_prec=512, fullpiv=True)
            if not singular:
                print ' %-9.0e |' % res,
            else:
                print ' %-6.0e(S) |' % res,
        print
#            residuals.append(res)
#            singulars.append(str(singular)[0])
#        if MPREAL_SUPPORT:
#            fmt = '| %5.0e | %8s | %8s | %8s | %8s | %8s |'
#            print  fmt % (p,errors[0],errors[1],errors[2],errors[3], errors[4])
#        else:
#            fmt = '| %5.0e | %8s | %8s | %8s | %8s |'
#            fmt = '| %5.0e(%s) | %5.0e(%s) | %5.0e(%s) | %5.0e(%s) | %5.0e(%s) |'
#            print  fmt % (p,errors[0],singulars[0],errors[1],singulars[1],errors[2],singulars[2],errors[3],singulars[3])


main()
