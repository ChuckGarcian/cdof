# Adding Instructions

## Dissassembling

 Dissassemble with https://github.com/GrammaTech/ddisasm

 Then the .gtirb file can be processed with this code
 using an invocation like ```gtirb-rewriting --run my-pass input.gtirb output.gtirb```

 after running the pass ```gtirb-pprinter ex.gtirb -b ex_rewritten``` can be used 
 to reassamble the binary with the sample pass being ran

 This code needs to be ran with python 3.10 (or possibly earlier), and needs gitrb rewriting to be installed.
