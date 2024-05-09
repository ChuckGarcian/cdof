# Runtime Autovectorization - Project Summary 
Create a dynamic runtime optimizer for C that identifies loops that are potentially vectorizable and performs optimization on them. The optimizer utilizes Skylake architecture performance counters to identify loops that can be optimized with vector instructions. 

In some cases where loop dependence is intractable, it may be that static loop dependence in a symbolic manner is tractable for symbolic analysis but easier and tractable for scalar values.

Hence, this project uses the current execution trace to identify the innermost loops that iterate independently. Once the independent iterations are identified, an optimized "patch is generated" - which is copied over to a patch cache buffer in memory. 

# Project Abstract
Vector instructions are utilized in high-performance applications where there are high degrees of data-level parallelism. Ideally, compilers can statically analyze code and identify portions of code (i.e. loops) that can be parallelized.

however, in practice, for certain pieces of code, loop dependence analysis is intractable. Loop optimizations like loop unrolling and loop vectorization are able to be performed statically by the compiler in "simple" cases. However, there are some cases where loop dependence analysis becomes intractable. 

This project aims to solve this issue by analyzing loop traces at runtime and generating optimizations during runtime that replace the loop. This is a form of software speculative execution since we perform the optimization and hope that the optimization is 'valid' for all iterations of the loop. If not, then we roll back and use the unoptimized code. Furthermore, we can add software prefetching.