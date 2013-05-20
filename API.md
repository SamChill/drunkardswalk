Python API
----------

There is just one function provided by the Python bindings:

```python
from drunkardswalk import solve_amc
t, B, residual, singular = solve_amc(Q, R, c, prec='dd', mpreal_prec=512)
```

`Q`: is a t by t array of transition probabilities between transient states,
where t is the number transient states.

`R`: is a t by r array of absorption probabilities from the transient states to
the absorbing states, where r is the number of absorbing states. 

Both `Q` and `R` may contain unnormalized probabilities. The normalization
will be carried out in the precision specified by `prec`. All arrays
passed must be numpy arrays using double precision (`numpy.float64`),
which is the default for most NumPy arrays.

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

C++ API
-------

```c++
template<typename scalar> void solve_amc(int Qsize, double* Qflat, int Rcols, 
        double* Rflat, double* c_in, double* B, double* t, double* residual,
        int* singular);
```

Template parameters:

`scalar`: The data type used to represent scalars. This can be any C++ type
that that has arithmetic operator overloading. Examples are `float`, `double`,
`dd_real`, `qd_real`, `dd_real`, and `mpreal`.

Input Arguments:

`Qsize`: The number of transient states.

`Qflat`: A pointer to a `Qsize*Qsize` length array of unnormalized
transition probabilities between the transient states.

`Rcols`: The number of absorbing states.

`Rflat`: A pointer to a `Qsize*Rcols` length array of unnormalized transition
probabilities from the transient states to the  absorbing states.

`c_in`: A pointer to a `Qsize` length array of average times per transient
state.

Output Arguments:

`B`: A pointer to a `Qsize*Rcols` array where the absorption probabilities will
be written. The i,j entry of B represents the probability of absorption to
state j when starting from state i.

`t`: A pointer to a `Qsize` array where the mean time until absorption is
written in each state.

`residual`: A pointer to a double where the relative residual error in `t` will
be written.

Input/Output Arguments:

`singular`: If singular is set to `1` then the matrix (I-Q) will be checked to
see if it is singular to machine precision. This uses a much more expensive rank
revealing matrix decomposition and is recommended for testing purposes only.
On return, `singular` will be set to `0` if (I-Q) is invertible.
