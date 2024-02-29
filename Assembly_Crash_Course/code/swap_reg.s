.section .text
.global _start
.intel_syntax noprefix

_start:
    push rdi
    push rsi
    pop rdi
    pop rsi
