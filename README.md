# CDOF

*CDOF* is a dynamic optimization framework for C.

## Tasks

* Connect valgrind source code to instructions
* Automate the dissassembling and reassalblimg process
* Determine what instructions access memory, and get registers used
* Insert the prefetch instruction  before the deliquent load

## Notes

* Determining function definitons is hard, maybe require a // @prefetch to be inserted above