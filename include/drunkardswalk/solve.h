#ifndef DRUNKARDS_WALK_SOLVE_H
#define DRUNKARDS_WALK_SOLVE_H

extern "C" {
    void solve_amc_float(int, double*, int, double*, double*, double*, 
            double*, double*, int*);
    void solve_amc_double(int, double*, int, double*, double*, double*, 
            double*, double*, int*);
    void solve_amc_ddreal(int, double*, int, double*, double*, 
            double*, double*, double*, int*);
    void solve_amc_qdreal(int, double*, int, double*, double*, double*, 
            double*, double*, int*);
#ifdef USE_MPREAL
    void set_mpreal_prec(int prec);
    void solve_amc_mpreal(int, double*, int, double*, double*, double*, 
            double*, double*, int*);
#endif
}

#ifdef __cplusplus
#include <Eigen/Dense>
#include <iostream>

template<typename scalar> void solve_amc(int Qsize, double* Qflat, int Rcols, 
        double* Rflat, double* c_in, double* B, double* t, double* residual,
        int* singular)
{
    using namespace Eigen;
    typedef Matrix<scalar,Dynamic,Dynamic> MatrixXdd;
    typedef Matrix<scalar,Dynamic,1> VectorXdd;

    int i, row, col;

    // Build an Eigen vector out of c_in.
    VectorXdd c = VectorXdd(Qsize);
    for (i = 0; i < Qsize; i++) {
        c(i) = 1.0 / c_in[i];
    }

    // Convert the Qflat array into an Eigen matrix.
    MatrixXdd Q = MatrixXdd(Qsize, Qsize);
    MatrixXdd R = MatrixXdd(Qsize, Rcols);

    for (row = 0; row < Qsize; row++) {
        scalar total = 0;
        for (col = 0; col < Qsize; col++) {
            Q(row, col) =  Qflat[row*Qsize + col];    
            total += Q(row, col);
        }
        for (col = 0; col < Rcols; col++) {
            R(row,col) =  Rflat[row*Rcols + col];    
            total += R(row, col);
        }
        Q.row(row) /= total;
        R.row(row) /= total;
    }

    MatrixXdd A = MatrixXdd(Qsize, Qsize);
    A.setIdentity();
    A = A - Q;

    VectorXdd t_calc;
    MatrixXdd B_calc;

    if (*singular == 1) {
        //Use LU w/ full pivoting, this is very expensive for a large number of
        //transient states.
        //This is a rank revealing decomposition that can determine if the
        //matrix is singular within the working precision for "scalar".
        FullPivLU<MatrixXdd> lu(A);
        *singular = (int)!lu.isInvertible();
        t_calc = lu.solve(c);
        B_calc = lu.solve(R);
    }else{
        PartialPivLU<MatrixXdd> lu(A);
        *singular = 0;
        t_calc = lu.solve(c);
        B_calc = lu.solve(R);
    }


    // Calculate the relative residual
    scalar res =  (A*t_calc-c).template lpNorm<Infinity>()/
            c.template lpNorm<Infinity>();
    *residual = (double)res;

    // Store the solution t_calc into the array t.
    for (i = 0; i < Qsize; i++) {
        t[i] = (double)t_calc[i];
    }

    // Store the solution B_calc into the array B.
    for (row = 0; row < Qsize; row++) {
        for (col = 0; col < Rcols; col++) {
            B[row*Rcols+col] = (double)B_calc(row, col);
        }
    }

}

#endif
#endif
