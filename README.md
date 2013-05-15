Drunkard's Walk
===============

Drunkard's walk is a library for calculating the expected number of steps (or time) 
until absorption and the absorption probabilities of an [absorbing Markov chain][amc].
The name is a reference to a type of [random walk][randomwalk]
that can be modeled with absorbing Markov chains.

Currently the Drunkard's Walk library is used in [Eon][eon], which is a software package
for atomistic modeling of long timescale problems in materials. By using the extended
precision features offered in this library, Eon is capable of solving absorbing Markov chains
where the timescales involved range from atomic vibrational periods (femtoseconds) to
the age of the universe (14 billion years).

The main feature of the library is that it supports extended precision floating point arithmetic
using the [QD library][qd] developed by David H. Bailey et al., 
which supports double double (~32 decimal digits) and quad double (~64 decimal digits) 
floating point types. The reason for using QD instead of an arbitrary precision math library, 
is that QD is very fast. By using these extended precision types, one is able to accurately solve
problems where the absorptions probabilities are vanishingly small.

The core of the code is written using [Eigen][eigen], which is a C++ template library
for linear algebra. As it is a template library, it supports working with different scalar
types such as float and double or the extended precision types in QD.

[amc]: http://en.wikipedia.org/wiki/Absorbing_Markov_chain
[randomwalk]: http://en.wikipedia.org/wiki/Random_walk
[eon]: http://theory.cm.utexas.edu/eon/
[qd]: http://crd-legacy.lbl.gov/~dhbailey/mpdist/
[eigen]: http://eigen.tuxfamily.org/

Installation
------------

Drunkard's walk requires GNU Make and a C++ compiler. 
It currently has only been testing with the GNU C++ compiler and should work with version 4.1 or newer.

Compiling the library should be as simple as running `make`. 
The top level makefile can be edited to use different compiler options.

Installing the library is done with `make install`. By default it is installed to
`/usr/local/lib`, however if you would like to install to a different location
that can be done with `make install PREFIX=/some/other/path`.

Python Bindings
---------------

The python bindings can be installed using the included `setup.py` located
in the `python` directory. By default the library searches standard
locations for the compiled shared library installed in the previous step.
If the library has been installed to a custom directory, the path to the
library needs to be set the enironment variable `DRUNKARDSWALK_LIB`.
This can be done in the bash shell with `export DRUNKARDSWALK_LIB=/path/to/lib/libdrunkardswalk.so`.

Testing
-------

Running the tests requires Python 2.4 or newer and numpy. The tests are located in the `tests/` subdirectory.
It is recommended to run the test `simple.py` to ensure that everything is working.
The tests require that Python and NumPy are installed.
