.section .text
.global _start
.intel_syntax noprefix

_start:
    and rdi, 0x1
    xor rdi, 0x1
    xor rax, rax
    or rax, rdi
