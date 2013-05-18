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

    print 'PERFORMANCE TESTS'
    print '-----------------'
    print 'Generating a random chain with N transient states',
    print 'and 50 absorbing states'
    print 'times are in seconds\n'

    if MPREAL_SUPPORT:
        print '| %8s | %8s | %8s | %8s | %8s | %8s |' % \
            ('N', 'float', 'double', 'dd_real', 'qd_real', 'mpreal')
        print '|:%8s:| %8s:| %8s:| %8s:| %8s:| %8s:|' % \
                ( 8*'-', 8*'-', 8*'-', 8*'-', 8*'-',8*'-')
    else:
        print '| %8s | %8s | %8s | %8s | %8s |' % \
                ('N', 'float', 'double', 'dd_real', 'qd_real')
        print '|:%8s:| %8s:| %8s:| %8s:| %8s:|' % \
                ( 8*'-', 8*'-', 8*'-', 8*'-', 8*'-',)

    precs = ['f','d','dd','qd']
    if MPREAL_SUPPORT:
        precs.append('mp')

    for Ntrans in [10,100,200,500,800]:
        times = []
        for prec in precs:
            p = 1e-5
            Nabs = 50
            Q,R,c = random_chain(Ntrans,Nabs,p)
            t1 = time()
            t, B, res, singular = solve_amc(Q,R,c,prec, mpreal_prec=512)
            t2 = time()
            times.append(t2-t1)
        if MPREAL_SUPPORT:
            fmt = '| %8i | %8.4f | %8.4f | %8.4f | %8.4f | %8.4f |'
            print  fmt % (Ntrans,times[0],times[1],times[2],times[3], times[4])
        else:
            fmt = '| %8i | %8.4f | %8.4f | %8.4f | %8.4f |'
            print  fmt % (Ntrans,times[0],times[1],times[2],times[3])

main()
