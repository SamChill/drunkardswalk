Drunkard's Walk
==============

Drunkard's walk is a library for calculating the expected number of steps (or time) 
until absorption and the absorption probabilities of an absorbing Markov chain.

The main feature of the library is that it supports extended precision floating point arithmetic
using the [QD library][qd] developed by David H. Bailey et al., 
which supports double double (~32 decimal digits) and quad double (~64 decimal digits) 
floating point types. The reason for using QD instead of an arbitrary precision math library, 
is that QD is very fast. By using these extended precision types, one is able to solve
problems where the absorptions probabilities are extremely small.

Currently the Drunkard's Walk library is used in [Eon][eon], which is a software package
for atomistic modeling of long timescale problems in materials. By using the extended
precision features offered in this library, Eon is capable of solving absorbing Markov chains
where the timescales involved range from atomic vibrational periods (femtoseconds) to
the age of the universe (14 billion years).

[qd]: http://crd-legacy.lbl.gov/~dhbailey/mpdist/
[eon]: http://theory.cm.utexas.edu/eon/
