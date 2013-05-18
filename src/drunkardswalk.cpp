#include <drunkardswalk/solve.h>

#include <qd/dd_real.h>
#include <qd/qd_real.h>

#ifdef USE_MPREAL
#include "mpreal.h"
#endif

void solve_amc_float(int Qsize, double *Qflat, int Rcols, double *Rflat, 
                  double *c_in, double *B, double *t, double *residual,
                  int *singular) 
{
    solve_amc<float>(Qsize, Qflat, Rcols, Rflat, c_in, B, t, residual, 
            singular);
}

void solve_amc_double(int Qsize, double *Qflat, int Rcols, double *Rflat, 
                  double *c_in, double *B, double *t, double *residual,
                  int *singular) 
{
    solve_amc<double>(Qsize, Qflat, Rcols, Rflat, c_in, B, t, residual,
            singular);
}

void solve_amc_ddreal(int Qsize, double *Qflat, int Rcols, double *Rflat, 
                  double *c_in, double *B, double *t, double *residual,
                  int *singular) 
{
    //turns on round-to-double bit in FPU
    //needed for libqd to work on x86 due to the 80bit FPU registers
    unsigned int oldcw;
    fpu_fix_start(&oldcw);
    solve_amc<dd_real>(Qsize, Qflat, Rcols, Rflat, c_in, B, t, residual,
            singular);
    fpu_fix_end(&oldcw);
}

void solve_amc_qdreal(int Qsize, double *Qflat, int Rcols, double *Rflat, 
                  double *c_in, double *B, double *t, double *residual,
                  int *singular) 
{
    unsigned int oldcw;
    //turns on round-to-double bit in FPU
    //needed for libqd to work on x86 due to the 80bit FPU registers
    fpu_fix_start(&oldcw);
    solve_amc<qd_real>(Qsize, Qflat, Rcols, Rflat, c_in, B, t, residual,
            singular);
    fpu_fix_end(&oldcw);
}

#ifdef USE_MPREAL
void set_mpreal_prec(int prec) {
    mpfr_set_default_prec(prec);
}

void solve_amc_mpreal(int Qsize, double *Qflat, int Rcols, double *Rflat, 
                  double *c_in, double *B, double *t, double *residual,
                  int *singular) 
{
    solve_amc<mpfr::mpreal>(Qsize, Qflat, Rcols, Rflat, c_in, B, t, residual,
            singular);
}
#endif
