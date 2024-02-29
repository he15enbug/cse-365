.section .text
.global _start
.intel_syntax noprefix

_start:
    pop rax
    sub rax, rdi
    push rax
