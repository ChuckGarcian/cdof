# Adding prefetch instructions

## Actually Adding

* Cachegrind can tell us what specific lines of code have $ misses
* Callgrind can do similar and can get instruction grained data
  * To get instruction data requires a GUI app however
* Assuming stuff is compiled with debugging symbols, we can use objdump -dS to
get instructions that map to source files

## Getting the address to prefetch

* We cant really add the prefetch instruction right before the miss, we want
it to be a little further back
  * The cpu will already be dealing with stuff
  * Exact matches will be hell, for example pointer chasing
  * We could try and just use the address calculation and cross our fingers.
* This will likely require lots of experimentation on what is the best.

## License changes

* Probably need to update the license to AGPL 3.0 as that is what the
Reassembleable disassembler (ddiasm) that I found is licensed under.

## ddiasm

* Docker really is the best way to run it, so need to determine a good way
to automate the running of our patch and then reassembling to become a simple
script with no user interaction.
