#include <assert.h>
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <stdint.h>

#define WAYS_TLB 4
#define SETS_TLB 16

#define LINE_SIZE (64/8)
#define WAYS_L1 8
#define SETS_L1 64

#define MIN_EXPONENT_SIZE  (9)
#define MAX_EXPONENT_SIZE  (27)
#define MAX_ENTRIES        (1 << MAX_EXPONENT_SIZE)

#define PAGE_SIZE          (4096)
#define EXTRA              (PAGE_SIZE)


unsigned long int data[MAX_ENTRIES + EXTRA];  /* The array we'll be traversing */
unsigned long int *mem;

void init_data_slow(unsigned long int *, unsigned long int);
void chase_indices(unsigned long int *mem);

// External function references
int main(int argc, char *argv[])
{
    int size = 1, arg_exp;

    if (argc >= 2) 
    {
      arg_exp = atoi(argv[1]);
      if (arg_exp < MIN_EXPONENT_SIZE || arg_exp > MAX_EXPONENT_SIZE)
        {
          printf("Memory size is (2^exponent) where %d <= exponent <= %d.\n",
                  MIN_EXPONENT_SIZE, MAX_EXPONENT_SIZE );
          exit(1);
          }
      else
        size = 1 << arg_exp;
    }
    
    // Set pointer mem to the beginning of a (4K-address-aligned) page.
    mem = (unsigned long int *)
      ((uintptr_t) data + PAGE_SIZE - ((uintptr_t) data % PAGE_SIZE));

    printf ("memchase_test: Starting \n");
    init_data_slow(mem, size);    
    chase_indices (mem);
    printf ("memchase_test: Done \n");
    
    return 0;
}

// @prefetch
void chase_indices(unsigned long int *mem)
{
    // Chase your pointers.
    unsigned long int val = 0;
    unsigned long int iters = 0;
    // unsigned long int idx, idxv;
    do {
      do {
        iters++;
        // 0
        val = mem[val];
        val = mem[val];
        val = mem[val];
        val = mem[val];
        // 4
        val = mem[val];
        val = mem[val];
        val = mem[val];
        val = mem[val];
        // 8
        val = mem[val];
        val = mem[val];
        val = mem[val];
        val = mem[val];
        // 12
        val = mem[val];
        val = mem[val];
        val = mem[val];
        //W idx = val;
        val = mem[val];
        // 16
        // Set memory value to 0
        //W idxv = val;
        //W mem[ idx ] = 0;
        // 16
        val = mem[val];
        val = mem[val];
        val = mem[val];
        val = mem[val];
        // 20
        val = mem[val];
        val = mem[val];
        val = mem[val];
        val = mem[val];
        // 24
        val = mem[val];
        val = mem[val];
        val = mem[val];
        val = mem[val];
        // 28
        val = mem[val];
        val = mem[val];
        val = mem[val];
        val = mem[val];
        // 32
        // Restore memory value
        //W mem[ idx ] = idxv;
      }
      while (val);
    }
    while (iters < 4000000);

    // printf("Iters: %ld, Val: %ld\n", iters, val);
}

static void shuffle_arr (unsigned long int mem[], unsigned long int size);

void init_data_fast(unsigned long int mem[], unsigned long int size)
{
  // Simple, in-order accesses
  unsigned long int i;

  for (i = 0; i < size; i++)
    mem[i] = (i + 1);

  // And now, we overwrite the final entry
  mem[size - 1] = 0;
}
static void shuffle_arr (unsigned long int mem[], unsigned long int size)
{
  srand(time(NULL));  
  unsigned long int i;
  
  /* Randomize it */
  for (i = 0; i < size; i++)
  {    
    int new = rand() % size;
    unsigned long int v1 = mem[i];
    mem[i] = mem[new];
    mem[new] = v1;
  } 
}

/*
  Random access to target prefetching behavior
*/
void init_data_slow (unsigned long int mem[], unsigned long int size)
{    
 
  /* Initialize sequentially */
  init_data_fast (mem, size);
  shuffle_arr (mem, size);  
}