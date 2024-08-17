# CDOF

*CDOF* is a dynamic optimization framework for C.

## Installing CDOF 

Install cdof using the `setup.py` file:

```
pip install .
```

Once installed, cdof is command line callable.

## Running CDOF 

To optimize a C program using CDOF:

1. Disassemble the target file using [ddisasm](https://github.com/grammatech/ddisasm):

    ```sh
    ddisasm example.o --ir example.gtirb
    gtirb-pprinter example.gtirb --asm example.s
    ```

2. Create a `test_runs` file with all execution runs:

    ```sh
    example.o -i 5
    example.o -i 10
    example.o -i 15
    ```

3. Call the CDOF driver:

    ```sh
    cdof.py test_runs.txt example.s
    ```

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

* need valgrind 3.23.0
  * [Source link](https://valgrind.org/downloads/repository.html)
