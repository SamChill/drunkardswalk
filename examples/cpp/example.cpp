#include <stdio.h>
#include <drunkardswalk/solve.h>

#define Ntransient 3
#define Nabsorbing 2

void printMatrix(double *matrix, int rows, int cols, const char *fmt)
{
    for (int i=0;i<rows;i++) {
        for (int j=0;j<cols;j++) {
            printf(fmt, matrix[i*cols+j]);
        }
        printf("\n");
    }
}

int main()
{
    double Q[Ntransient*Ntransient], R[Ntransient*Nabsorbing];
    double c[Ntransient];
    double B[Ntransient*Nabsorbing], t[Ntransient];
    double residual;
    int singular=1;

    int i;

    i=0;
    Q[i++] = 0.0; Q[i++] = 0.5; Q[i++] = 0.0;
    Q[i++] = 0.5; Q[i++] = 0.0; Q[i++] = 0.5;
    Q[i++] = 0.0; Q[i++] = 0.5; Q[i++] = 0.0;

    i=0;
    R[i++] = 0.5; R[i++] = 0.0;
    R[i++] = 0.0; R[i++] = 0.0;
    R[i++] = 0.0; R[i++] = 0.5;

    i=0;
    c[i++] = 1.0;
    c[i++] = 1.0; 
    c[i++] = 1.0;

    printf("Q:\n");
    printMatrix(Q, Ntransient, Ntransient, "%.2f ");
    printf("\nR:\n");
    printMatrix(R, Ntransient, Nabsorbing, "%.2f ");
    printf("\nc:\n");
    printMatrix(c, 1, Ntransient, "%.2f ");

    solve_amc<double>(Ntransient, Q, Nabsorbing, R, c, B, t, &residual,
            &singular);

    printf("\nB:\n");
    printMatrix(B, Ntransient, Nabsorbing, "%.2f ");
    printf("\nt:\n");
    printMatrix(t, 1, Ntransient, "%.2f ");

    return 0;
}
