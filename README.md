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
