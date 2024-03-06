.intel_syntax noprefix
.section .text
.global _start

_start:
    mov rdi, 0
    mov rax, 60 # 
    syscall
