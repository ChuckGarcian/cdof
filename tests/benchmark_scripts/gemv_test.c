/*
  Naive GEMV implementation. 
*/
#include <stdio.h>
#include <stdlib.h>

void gemv (int m, int n, double *A, double *x, double *y);
void RandomMatrix (int m, int n, double *A);

int main (int argc, char *argv[])
{
  char *_m, *_n;
  int m, n; 
  double *A, *x, *y;
  
  printf ("gemv_test: Starting \n");  

  /* Get Object Sizes */
  _m = argv[1];
  _n = argv[2];  
  
  m = atoi(_m);
  n = atoi (_n);
  
  /* Column Stored */
  A = (double *) malloc (n * m * sizeof (double)); 
	x = (double *) malloc (n * sizeof (double));
  y = (double *) calloc (m, sizeof (double));  

  RandomMatrix (m, n, A);
  RandomMatrix (1, n, x);
  
  /* y ← A*x + y */  
  gemv (m, n, A, x, y);

  printf ("gemv_test: Done \n");
  return 0;
}

// @prefetch
void gemv (int m, int n, double *A, double *x, double *y)
{
  // Axpy
  // for (int j = 0; j < n; j++)
  //   for (int i = 0; i < m; i++)
  //     y [i] += A [j*m + i] * x[j];
  
  // Dots
  for (int i = 0; i < m; i++)
    for (int j = 0; j < n; j++) 
      y[i] += A[j*m + i] * x [j];
}

/* RandomMatrix overwrite A with random values. */
void RandomMatrix( int m, int n, double *A)
{
  int  i, j;

  for ( i=0; i<m; i++ )
    for ( j=0; j<n; j++ )
        A[i + j*m] = drand48();
}


