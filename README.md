Drunkard's Walk
===============

Drunkard's walk is a library for calculating the expected number of steps (or
time) until absorption and the absorption probabilities of an 
[absorbing Markov chain][amc]. The name is a reference to a type of 
[random walk][randomwalk] that can be modeled with absorbing Markov chains.

Currently the Drunkard's Walk library is used in [Eon][eon], which is a
software package for atomistic modeling of long timescale problems in
materials. By using the extended precision features offered in this library,
Eon is capable of solving absorbing Markov chains where the timescales involved
range from atomic vibrational periods (femtoseconds) to the age of the universe
(14 billion years).

The main feature of the library is that it supports extended precision floating
point arithmetic using the [QD library][qd] developed by David H. Bailey et
al., which supports double double (~32 decimal digits) and quad double (~64
decimal digits) floating point types. The reason for using QD instead of an
arbitrary precision math library, is that QD is very fast. By using these
extended precision types, one is able to accurately solve problems where the
absorption probabilities are vanishingly small.

The core of the code is written using [Eigen][eigen], which is a C++ template
library for linear algebra. As it is a template library, it supports working
with different scalar types such as float and double or the extended precision
types in QD.

[amc]: http://en.wikipedia.org/wiki/Absorbing_Markov_chain
[randomwalk]: http://en.wikipedia.org/wiki/Random_walk
[eon]: http://theory.cm.utexas.edu/eon/
[qd]: http://crd-legacy.lbl.gov/~dhbailey/mpdist/
[eigen]: http://eigen.tuxfamily.org/

Installation
------------

Drunkard's walk requires GNU Make and a C++ compiler. It currently has been
tested with the GNU (version 4.1 or newer) and Intel C++ compilers (version
13).

Compiling the library should be as simple as running `make`. The top level
makefile can be edited to use different compilers or compiler options.

Arbitrary precision support can be enabled by building with 
`make USE_MPREAL=1`. This requires [MPFR][mpfr] (>= 2.3.1) and 
[GMP][gmp] (>=4.2.1).

OpenMP threading can be enabled by enabling compiler support. With the GNU
C++ compiler this can be acomplished by added `-fopenmp` to `CXXFLAGS`
in the top-level makefile. The number of threads can be controlled via
the environment variable `OMP_NUM_THREADS`. The default compiler flags
do not enable threading.

Installing the library is done with `make install`. By default it is installed
to `/usr/local/lib`, however if you would like to install to a different
location that can be done with `make install PREFIX=/some/other/path`.

[mpfr]:http://www.mpfr.org
[gmp]:http://gmplib.org

Python Bindings
---------------

The python bindings can be installed using the included `setup.py` located in
the `python` directory. By default the library searches standard locations for
the compiled shared library installed in the previous step. If the library has
been installed to a custom directory, the path to the library needs to be set
the enironment variable `DRUNKARDSWALK_LIB`. This can be done in the bash shell
with `export DRUNKARDSWALK_LIB=/path/to/lib/libdrunkardswalk.so`.

Testing
-------

Running the tests requires Python 2.4 or newer and NumPy. The Python bindings
do not have to be installed first; the tests can be run after running `make`.
The tests are located in the `tests/` subdirectory. A simple test can be
executed by running `make test`.

Performance Benchmark
---------------------

The wall clock time to for solving an absorbing Markov chain with N transient
states and 50 absorbing states is listed in the table below. This timing data
was produced from the `tests/performance.py` test script.  The following timing
data were produced on a 2.8GHz Intel Core 2 Duo using a single thread.

|        N |    float |   double |  dd_real |  qd_real |   mpreal |
|:--------:| --------:| --------:| --------:| --------:| --------:|
|       10 |   0.0003 |   0.0002 |   0.0004 |   0.0015 |   0.0084 |
|      100 |   0.0013 |   0.0016 |   0.0168 |   0.1539 |   1.0164 |
|      200 |   0.0061 |   0.0080 |   0.0908 |   0.8232 |   5.5182 |
|      500 |   0.0864 |   0.1026 |   1.0912 |   9.9111 |  62.0800 |
|      800 |   0.3453 |   0.4596 |   4.6514 |  39.7816 | 215.9577 |

Python API
----------

There is just one function provided by the Python bindings:

```python
from drunkardswalk import solve_amc
t, B, residual, singular = solve_amc(Q, R, c, prec='dd', mpreal_prec=512)
```

`Q`: is a t by t NumPy array of relative transition probabilities
between transient states, where t is the number transient states.

`R`: is a t by r NumPy array of relative absorption probabilities
from the transient states to the absorbing states, where r is
the number of absorbing states. 

`c`: is a NumPy array of length
t that represents the average time spent in each transient states.
This could be a vector of ones if one wants to solve for the expected
number of times the chain is in each transient state. 

`prec`: is a string that represents the floating point precision that will
be used to solve the problem. The options are `f`, `d`, `dd`, and `qd`,
which correspond to single, double, double double, and quad double
precision respectively. If the library has been compiled with
`make USE_MPREAL=1` then an addition option is available: `mp`.
This corresponds to an arbitrary precision type whose precision
can be specified at runtime.

`mpreal_prec`: is the number of bits used to represent the significand 
when using the `mp` precision type.

The function returns a NumPy array of length t that represents the
expected amount of time spent in each state and a t by r NumPy
array of absorption probabilities, where the i,j entry is the
probability of being absorbed into state j if the chain states in 
state i. It also returns the relative residual error in the solution
for the absorption times and whether or not the linear system
of equations is singular. If singular is `True`, the answer cannot
be trusted to any level of precision regarless of the residual.

Example
-------

Here is an example of solving the drunkard's walk problem in python.

```python
from drunkardswalk import solve_amc
import numpy

#define the transient matrix
Q = numpy.array([ [0.0, 0.5, 0.0],
                  [0.5, 0.0, 0.5],
                  [0.0, 0.5, 0.0] ])

#define the recurrant matrix
R = numpy.array([ [0.5, 0.0],
                  [0.0, 0.0],
                  [0.0, 0.5] ])

#define vector of times for transient states
c = numpy.array([1.0, 1.0, 1.0])

#choose precision to solve problem in
#here we choose double double precision
prec = 'dd'

#solve for the time spent in each transient state (t)
#and the matrix of absorption probabilities (B)
#also returns a measure of the error in the solution (residual)
t, B, residual = solve_amc(Q,R,c,prec)

print "times:"
print t
print 'absorption probabilities:'
print B
```
The following output is produced:
```
times:
[3.0, 4.0, 3.0]
absorption probabilities:
[[ 0.75  0.25]
 [ 0.5   0.5 ]
 [ 0.25  0.75]]
```
