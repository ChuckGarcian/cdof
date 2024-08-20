/*
  Naive Matrix Transpose
*/
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

void transpose (int m, int n, double *A);
void fill (int m, int n, double *A);
void print_mat (int m, int n, double *A);

int main (int argc, char *argv[])
{
  char *_m, *_n;
  int m, n; 
  double *A, *x, *y;
  
  printf ("mtrans_test: Starting \n");  

  /* Get Object Size */
  assert (argc == 3);
  _m = argv[1];
  _n = argv[2];  
  
  m = atoi(_m);
  n = atoi (_n);
  
  /* Column Stored */
  A = (double *) malloc (n * m * sizeof (double)); 
  fill (m, n, A);
  print_mat (m, n, A);
  
  /* A ← A.T */  
  transpose (m, n, A);
  
  printf ("after transpose \n");
  print_mat (n, m, A);
  printf ("mtrans_test: Done \n");
  return 0;
}

// @prefetch
void transpose(int m, int n, double *A)
{
    for (int i = 0; i < m; i++) {
        for (int j = i + 1; j < n; j++) {
            double temp = A[i + j * m];
            A[i + j * m] = A[j + i * m];
            A[j + i * m] = temp;
        }
    }
}
void print_mat(int m, int n, double *A)
{
    for (int i = 0; i < m; i++)
    {
        for (int j = 0; j < n; j++)
            printf("%f ", A[(j * m) + i]);
        printf("\n");
    }  
}

void fill (int m, int n, double *A)
{
  int k = 0;
  
  for (int i = 0; i < m; i++)
  {
    for (int j = 0; j < n; j++)
    {
      A[(j * m) + i] = k;
      k++;
    }
  }  
}