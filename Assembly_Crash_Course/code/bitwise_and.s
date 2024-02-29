.section .text
.global _start
.intel_syntax noprefix

_start:
    and rdi, rsi
    xor rax, rax
    or rax, rdi
