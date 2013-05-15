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
from drunkardswalk import solve_amc


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
    print 'error measured as the residual in the solution of the escape times:'
    print u'residual = ||(1-Q)*t - c||_\u221E'

    print '%5s %5s %5s %5s %5s' % ('p', 'f', 'd', 'dd', 'qd')
    for p in [1e-5,1e-8,1e-10,1e-15,1e-25,1e-28,1e-30,1e-40,1e-50,1e-60,1e-70]:
        errors = []
        for prec in ['f','d','dd','qd']:
            Q,R,c = random_chain(Ntrans,Nabs,p)
            t, B, res = solve_amc(Q,R,c,prec)
            errors.append(res)
        fmt = '%5.0e %5.0e %5.0e %5.0e %5.0e' 
        print fmt % (p,errors[0],errors[1],errors[2],errors[3])

    import sys;sys.exit(0)

    print '\nPERFORMANCE TESTING'
    print '-------------------'

    print '%8s %8s %8s %8s %8s' % ('N', 'f', 'd', 'dd', 'qd')
    for Ntrans in [10,100,200,500,800]:
        times = []
        for prec in ['f','d','dd','qd']:
            p = 1e-5
            Nabs = 50
            Q,R,c = random_chain(Ntrans,Nabs,p)
            t1 = time()
            t, B, res = solve_amc(Q,R,c,prec)
            t2 = time()
            times.append(t2-t1)
        fmt = '%8i %8.3f %8.3f %8.3f %8.3f'
        print  fmt % (Ntrans,times[0],times[1],times[2],times[3])

main()
