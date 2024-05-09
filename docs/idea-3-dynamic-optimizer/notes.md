# C Loop Optimizer
- Assume input is a trivially simple code file that contains loops
- Identify all loops
- Identify working data set and apply packing

High Level:
- Optimize nested for loops
- Automatic packing
- Stride considerations

For now, we assume the following:
- All iterations of nested execution (i.e., nested loops or not) are assumed to be loop independent.
- Access stride is dependent on the induction variable and is easily computed with every iteration.
- All accesses in loops are indirect, non-pointer based, and not dependent on a sub-array.
- Every iteration is based only on induction.

Automatic Packing:
- Identify structured data routinely accessed within inner loops.

Benchmarks and Testing:
- Benchmarks shall include testing for both correctness and performance gains.
- We shall benchmark performance against the BLIS implementation.

Potential Future Additions:
- Instead of applying optimizations to every loop/branch, utilize real-time performance profiling data to prioritize code sections that are used more.