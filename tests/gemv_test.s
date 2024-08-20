
#===================================
.section .interp ,"a",@progbits
#===================================

.align 1
          .byte 0x2f
          .byte 0x6c
          .byte 0x69
          .byte 0x62
          .byte 0x36
          .byte 0x34
          .byte 0x2f
          .byte 0x6c
          .byte 0x64
          .byte 0x2d
          .byte 0x6c
          .byte 0x69
          .byte 0x6e
          .byte 0x75
          .byte 0x78
          .byte 0x2d
          .byte 0x78
          .byte 0x38
          .byte 0x36
          .byte 0x2d
          .byte 0x36
          .byte 0x34
          .byte 0x2e
          .byte 0x73
          .byte 0x6f
          .byte 0x2e
          .byte 0x32
          .byte 0x0
#===================================
# end section .interp
#===================================

#===================================
.section .note.gnu.property ,"a"
#===================================

.align 8
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x47
          .byte 0x4e
          .byte 0x55
          .byte 0x0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0xc0
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2
          .byte 0x80
          .byte 0x0
          .byte 0xc0
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#===================================
# end section .note.gnu.property
#===================================

#===================================
.section .note.gnu.build-id ,"a"
#===================================

.align 4
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x47
          .byte 0x4e
          .byte 0x55
          .byte 0x0
          .byte 0xcd
          .byte 0x89
          .byte 0x67
          .byte 0x4e
          .byte 0xee
          .byte 0x16
          .byte 0xfa
          .byte 0x5e
          .byte 0x6f
          .byte 0x1e
          .byte 0x82
          .byte 0xbe
          .byte 0xe4
          .byte 0xfc
          .byte 0xd0
          .byte 0x40
          .byte 0x53
          .byte 0x17
          .byte 0x82
          .byte 0x7d
#===================================
# end section .note.gnu.build-id
#===================================

#===================================
.section .note.ABI-tag ,"a"
#===================================

.align 4
#-----------------------------------
.type __abi_tag, @object
.size __abi_tag, 32
#-----------------------------------
__abi_tag:
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x47
          .byte 0x4e
          .byte 0x55
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#===================================
# end section .note.ABI-tag
#===================================

#===================================
.section .init ,"ax",@progbits
#===================================

.align 4
#-----------------------------------
.globl _init
.hidden _init
.type _init, @function
#-----------------------------------
_init:

            endbr64 
            subq $8,%rsp
            movq __gmon_start__@GOTPCREL(%rip),%rax
            testq %rax,%rax
            je .L_1016

            callq *%rax
.L_1016:

            addq $8,%rsp
            retq 
.size _init, . - _init
#===================================
# end section .init
#===================================

#===================================
.text
#===================================

.align 16
#-----------------------------------
.globl _start
.type _start, @function
#-----------------------------------
_start:

.cfi_startproc 
.cfi_lsda 255
.cfi_personality 255
.cfi_def_cfa 7, 8
.cfi_offset 16, -8
            endbr64 
.cfi_undefined 16
            xorl %ebp,%ebp
            movq %rdx,%r9
            popq %rsi
            movq %rsp,%rdx
            andq $-16,%rsp
            pushq %rax
            pushq %rsp
            xorl %r8d,%r8d
            xorl %ecx,%ecx
            leaq main(%rip),%rdi
            callq *__libc_start_main@GOTPCREL(%rip)

            hlt 
.cfi_endproc 

            nop
            nop
            nop
            nop
            nop
            nop
            nop
            nop
            nop
            nop
.size _start, . - _start
#-----------------------------------
.type deregister_tm_clones, @function
#-----------------------------------
deregister_tm_clones:

            leaq completed.0(%rip),%rdi
            leaq completed.0(%rip),%rax
            cmpq %rdi,%rax
            je .L_1158

            movq _ITM_deregisterTMCloneTable@GOTPCREL(%rip),%rax
            testq %rax,%rax
            je .L_1158

            jmpq *%rax
          .byte 0xf
          .byte 0x1f
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
.L_1158:

            retq 
.size deregister_tm_clones, . - deregister_tm_clones
          .byte 0xf
          .byte 0x1f
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#-----------------------------------
.type register_tm_clones, @function
#-----------------------------------
register_tm_clones:

            leaq completed.0(%rip),%rdi
            leaq completed.0(%rip),%rsi
            subq %rdi,%rsi
            movq %rsi,%rax
            shrq $63,%rsi
            sarq $3,%rax
            addq %rax,%rsi
            sarq $1,%rsi
            je .L_1198

            movq _ITM_registerTMCloneTable@GOTPCREL(%rip),%rax
            testq %rax,%rax
            je .L_1198

            jmpq *%rax
          .byte 0x66
          .byte 0xf
          .byte 0x1f
          .byte 0x44
          .byte 0x0
          .byte 0x0
.L_1198:

            retq 
.size register_tm_clones, . - register_tm_clones
          .byte 0xf
          .byte 0x1f
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#-----------------------------------
.type __do_global_dtors_aux, @function
#-----------------------------------
__do_global_dtors_aux:

            endbr64 
            cmpb $0,completed.0(%rip)
            jne .L_11d8

            pushq %rbp
            cmpq $0,__cxa_finalize@GOTPCREL(%rip)
            movq %rsp,%rbp
            je .L_11c7

            movq .L_4008(%rip),%rdi
            callq __cxa_finalize@PLT
.L_11c7:

            callq deregister_tm_clones

            movb $1,completed.0(%rip)
            popq %rbp
            retq 
          .byte 0xf
          .byte 0x1f
          .byte 0x0
.L_11d8:

            retq 
.size __do_global_dtors_aux, . - __do_global_dtors_aux
          .byte 0xf
          .byte 0x1f
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#-----------------------------------
.type frame_dummy, @function
#-----------------------------------
frame_dummy:

            endbr64 
            jmp register_tm_clones
.size frame_dummy, . - frame_dummy
#-----------------------------------
.globl main
.type main, @function
#-----------------------------------
main:

.cfi_startproc 
.cfi_lsda 255
.cfi_personality 255
.cfi_def_cfa 7, 8
.cfi_offset 16, -8
            endbr64 
            pushq %rbp
.cfi_def_cfa_offset 16
.cfi_offset 6, -16
            movq %rsp,%rbp
.cfi_def_cfa_register 6
            subq $64,%rsp
            movl %edi,-52(%rbp)
            movq %rsi,-64(%rbp)
            leaq .L_2004(%rip),%rax
            movq %rax,%rdi
            callq puts@PLT

            movq -64(%rbp),%rax
            movq 8(%rax),%rax
            movq %rax,-40(%rbp)
            movq -64(%rbp),%rax
            movq 16(%rax),%rax
            movq %rax,-32(%rbp)
            movq -40(%rbp),%rax
            movq %rax,%rdi
            callq atoi@PLT

            movl %eax,-48(%rbp)
            movq -32(%rbp),%rax
            movq %rax,%rdi
            callq atoi@PLT

            movl %eax,-44(%rbp)
            movl -48(%rbp),%eax
            movl %eax,%esi
            leaq .L_2019(%rip),%rax
            movq %rax,%rdi
            movl $0,%eax
            callq printf@PLT

            movl -44(%rbp),%eax
            movl %eax,%esi
            leaq .L_2019(%rip),%rax
            movq %rax,%rdi
            movl $0,%eax
            callq printf@PLT

            movl -44(%rbp),%eax
            imull -48(%rbp),%eax
            cltq 
            shlq $3,%rax
            movq %rax,%rdi
            callq malloc@PLT

            movq %rax,-24(%rbp)
            movl -44(%rbp),%eax
            cltq 
            shlq $3,%rax
            movq %rax,%rdi
            callq malloc@PLT

            movq %rax,-16(%rbp)
            movl -48(%rbp),%eax
            cltq 
            movl $8,%esi
            movq %rax,%rdi
            callq calloc@PLT

            movq %rax,-8(%rbp)
            movq -24(%rbp),%rdx
            movl -44(%rbp),%ecx
            movl -48(%rbp),%eax
            movl %ecx,%esi
            movl %eax,%edi
            callq RandomMatrix

            movq -16(%rbp),%rdx
            movl -44(%rbp),%eax
            movl %eax,%esi
            movl $1,%edi
            callq RandomMatrix

            movq -8(%rbp),%rdi
            movq -16(%rbp),%rcx
            movq -24(%rbp),%rdx
            movl -44(%rbp),%esi
            movl -48(%rbp),%eax
            movq %rdi,%r8
            movl %eax,%edi
            callq gemv

            leaq .L_201f(%rip),%rax
            movq %rax,%rdi
            callq puts@PLT

            movl $0,%eax
            leave 
.cfi_def_cfa 7, 8
            retq 
.cfi_endproc 
.size main, . - main
#-----------------------------------
.globl gemv
.type gemv, @function
#-----------------------------------
gemv:

.cfi_startproc 
.cfi_lsda 255
.cfi_personality 255
.cfi_def_cfa 7, 8
.cfi_offset 16, -8
            endbr64 
            pushq %rbp
.cfi_def_cfa_offset 16
.cfi_offset 6, -16
            movq %rsp,%rbp
.cfi_def_cfa_register 6
            movl %edi,-20(%rbp)
            movl %esi,-24(%rbp)
            movq %rdx,-32(%rbp)
            movq %rcx,-40(%rbp)
            movq %r8,-48(%rbp)
            movl $0,-8(%rbp)
            jmp .L_13c1
.L_1335:

            movl $0,-4(%rbp)
            jmp .L_13b5
.L_133e:

            movl -8(%rbp),%eax
            cltq 
            leaq (,%rax,8),%rdx
            movq -48(%rbp),%rax
            addq %rdx,%rax
            movsd (%rax),%xmm1
            movl -4(%rbp),%eax
            imull -20(%rbp),%eax
            movl %eax,%edx
            movl -8(%rbp),%eax
            addl %edx,%eax
            cltq 
            leaq (,%rax,8),%rdx
            movq -32(%rbp),%rax
            addq %rdx,%rax
            movsd (%rax),%xmm2
            movl -4(%rbp),%eax
            cltq 
            leaq (,%rax,8),%rdx
            movq -40(%rbp),%rax
            addq %rdx,%rax
            movsd (%rax),%xmm0
            mulsd %xmm2,%xmm0
            movl -8(%rbp),%eax
            cltq 
            leaq (,%rax,8),%rdx
            movq -48(%rbp),%rax
            addq %rdx,%rax
            addsd %xmm1,%xmm0
            movsd %xmm0,(%rax)
            addl $1,-4(%rbp)
.L_13b5:

            movl -4(%rbp),%eax
            cmpl -24(%rbp),%eax
            jl .L_133e

            addl $1,-8(%rbp)
.L_13c1:

            movl -8(%rbp),%eax
            cmpl -20(%rbp),%eax
            jl .L_1335

            nop
            nop
            popq %rbp
.cfi_def_cfa 7, 8
            retq 
.cfi_endproc 
.size gemv, . - gemv
#-----------------------------------
.globl RandomMatrix
.type RandomMatrix, @function
#-----------------------------------
RandomMatrix:

.cfi_startproc 
.cfi_lsda 255
.cfi_personality 255
.cfi_def_cfa 7, 8
.cfi_offset 16, -8
            endbr64 
            pushq %rbp
.cfi_def_cfa_offset 16
.cfi_offset 6, -16
            movq %rsp,%rbp
.cfi_def_cfa_register 6
            pushq %rbx
            subq $40,%rsp
.cfi_offset 3, -24
            movl %edi,-36(%rbp)
            movl %esi,-40(%rbp)
            movq %rdx,-48(%rbp)
            movl $0,-24(%rbp)
            jmp .L_1437
.L_13f1:

            movl $0,-20(%rbp)
            jmp .L_142b
.L_13fa:

            movl -20(%rbp),%eax
            imull -36(%rbp),%eax
            movl %eax,%edx
            movl -24(%rbp),%eax
            addl %edx,%eax
            cltq 
            leaq (,%rax,8),%rdx
            movq -48(%rbp),%rax
            leaq (%rdx,%rax),%rbx
            callq drand48@PLT

            movq %xmm0,%rax
            movq %rax,(%rbx)
            addl $1,-20(%rbp)
.L_142b:

            movl -20(%rbp),%eax
            cmpl -40(%rbp),%eax
            jl .L_13fa

            addl $1,-24(%rbp)
.L_1437:

            movl -24(%rbp),%eax
            cmpl -36(%rbp),%eax
            jl .L_13f1

            nop
            nop
            movq -8(%rbp),%rbx
            leave 
.cfi_def_cfa 7, 8
            retq 
.cfi_endproc 
.size RandomMatrix, . - RandomMatrix
#===================================
# end section .text
#===================================

#===================================
.section .fini ,"ax",@progbits
#===================================

.align 4
#-----------------------------------
.globl _fini
.hidden _fini
.type _fini, @function
#-----------------------------------
_fini:

            endbr64 
            subq $8,%rsp
            addq $8,%rsp
            retq 
.size _fini, . - _fini
#===================================
# end section .fini
#===================================

#===================================
.section .rodata ,"a",@progbits
#===================================

.align 4
.L_2000:
#-----------------------------------
.globl _IO_stdin_used
.type _IO_stdin_used, @object
.size _IO_stdin_used, 4
#-----------------------------------
_IO_stdin_used:
          .byte 0x1
          .byte 0x0
          .byte 0x2
          .byte 0x0
.L_2004:
          .string "gemv_test: Starting "
.L_2019:
          .string "m: %d"
.L_201f:
          .string "gemv_test: Done "
#===================================
# end section .rodata
#===================================

#===================================
.section .init_array ,"wa"
#===================================

.align 8
#-----------------------------------
.type __frame_dummy_init_array_entry, @object
#-----------------------------------
__frame_dummy_init_array_entry:
          .quad frame_dummy
#===================================
# end section .init_array
#===================================

#===================================
.section .fini_array ,"wa"
#===================================

.align 8
#-----------------------------------
.type __do_global_dtors_aux_fini_array_entry, @object
#-----------------------------------
__do_global_dtors_aux_fini_array_entry:
          .quad __do_global_dtors_aux
#-----------------------------------
.type _DYNAMIC, @object
#-----------------------------------
_DYNAMIC:
#===================================
# end section .fini_array
#===================================

#===================================
.data
#===================================

.align 8
#-----------------------------------
.weak data_start
.type data_start, @notype
#-----------------------------------
data_start:
#-----------------------------------
.globl __data_start
.type __data_start, @notype
#-----------------------------------
__data_start:
          .zero 8
.L_4008:
#-----------------------------------
.globl __dso_handle
.hidden __dso_handle
.type __dso_handle, @object
#-----------------------------------
__dso_handle:
          .quad .L_4008
#-----------------------------------
.globl __TMC_END__
.hidden __TMC_END__
.type __TMC_END__, @object
#-----------------------------------
__TMC_END__:
#-----------------------------------
.globl _edata
.type _edata, @notype
#-----------------------------------
_edata:
#===================================
# end section .data
#===================================

#===================================
.bss
#===================================

.align 1
#-----------------------------------
.type completed.0, @object
.size completed.0, 1
#-----------------------------------
completed.0:
#-----------------------------------
.globl __bss_start
.type __bss_start, @notype
#-----------------------------------
__bss_start:
          .zero 8
#-----------------------------------
.globl _end
.type _end, @notype
#-----------------------------------
_end:
.L_4018:
#===================================
# end section .bss
#===================================
# WARNING: integral symbol .L_0 may not have been correctly relocated
.set .L_0, 0
#-----------------------------------
.weak _ITM_deregisterTMCloneTable
.type _ITM_deregisterTMCloneTable, @notype
#-----------------------------------
#-----------------------------------
.weak _ITM_registerTMCloneTable
.type _ITM_registerTMCloneTable, @notype
#-----------------------------------
#-----------------------------------
.symver __cxa_finalize,__cxa_finalize@GLIBC_2.2.5
.weak __cxa_finalize
.type __cxa_finalize, @function
#-----------------------------------
#-----------------------------------
.weak __gmon_start__
.type __gmon_start__, @notype
#-----------------------------------
#-----------------------------------
.symver __libc_start_main,__libc_start_main@GLIBC_2.34
.globl __libc_start_main
.type __libc_start_main, @function
#-----------------------------------
#-----------------------------------
.symver atoi,atoi@GLIBC_2.2.5
.globl atoi
.type atoi, @function
#-----------------------------------
#-----------------------------------
.symver calloc,calloc@GLIBC_2.2.5
.globl calloc
.type calloc, @function
#-----------------------------------
#-----------------------------------
.symver drand48,drand48@GLIBC_2.2.5
.globl drand48
.type drand48, @function
#-----------------------------------
#-----------------------------------
.symver malloc,malloc@GLIBC_2.2.5
.globl malloc
.type malloc, @function
#-----------------------------------
#-----------------------------------
.symver printf,printf@GLIBC_2.2.5
.globl printf
.type printf, @function
#-----------------------------------
#-----------------------------------
.symver puts,puts@GLIBC_2.2.5
.globl puts
.type puts, @function
#-----------------------------------
