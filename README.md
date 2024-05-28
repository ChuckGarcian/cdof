# CDOF

*CDOF* is a dynamic optimization framework for C.

## Tasks

* Connect valgrind source code to instructions
* Automate the disassembling and reassembling process
* Determine what instructions access memory, and get registers used
* Insert the prefetch instruction  before the delinquent load

## Notes

* Determining function definitions is hard, maybe require a // @prefetch to be inserted above
* Additionally, one must have the function type signature and name on the same line
  * TODO: Remove that restriction
* Another resteriction is that all lines of code in a function must be unique (Note, adding comments inline is fine)
  * TODO: Remove that restrictioin too
