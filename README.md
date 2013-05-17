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

Installing the library is done with `make install`. By default it is installed
to `/usr/local/lib`, however if you would like to install to a different
location that can be done with `make install PREFIX=/some/other/path`.

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
The tests are located in the `tests/` subdirectory. It is recommended to run
the test `simple.py` to ensure that everything is working.

Performance Benchmark
---------------------

The wall clock time to for solving an absorbing Markov chain with `N` transient
states and 50 absorbing states is listed in the table below. This timing data
was produced from the `performance.py` test script.  The following timing data
were produced on an 8-core 2.66GHz Intel Xeon X5355 with 8 threads.

|        N |    float |   double |  dd_real |  qd_real |
|:--------:| --------:| --------:| --------:| --------:|
|       10 |   0.0003 |   0.0002 |   0.0004 |   0.0018 |
|      100 |   0.0009 |   0.0011 |   0.0187 |   0.1951 |
|      200 |   0.0024 |   0.0037 |   0.0735 |   0.8157 |
|      500 |   0.0203 |   0.0268 |   0.5163 |   6.3047 |
|      800 |   0.0401 |   0.0647 |   1.5459 |  17.2294 |
|     1200 |   0.0920 |   0.1477 |   4.2870 |  48.9998 |
|     1500 |   0.1574 |   0.2332 |   7.7363 |  89.7005 |
|     2000 |   0.2800 |   0.4583 |  15.9154 | 185.3204 |

Python API
----------

There is just one function provided by the Python bindings:

```python
t, B = drunkardswalk.solve_amc(Q, R, c, prec='dd')
```

`Q` is a t by t NumPy array of relative transition probabilities
between transient states, where t is the number transient states.

`R` is a t by r NumPy array of relative absorption probabilities
from the transient states to the absorbing states, where r is
the number of absorbing states. 

`c` is a Numpy array of length
t that represents the average time spent in each transient states.
This could be a vector of ones if one wants to solve for the expected
number of times the chain is in each transient state. 

`prec` is a string that represents the floating point precision that will
be used to solve the problem. The options are `f`, `d`, `dd`, and `qd`
which correspond to single, double, double double, and quad double
precision respectively.

The function returns a NumPy array of length t that represents the
expected amount of time spent in each state and a t by r NumPy
array of absorption probabilities, where the i,j entry is the
probability of being absorbed into state j if the chain states in 
state i.

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
