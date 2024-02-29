.section .text
.global _start
.intel_syntax noprefix

_start:
    mov eax, [rdi]
    mov ebx, [rdi + 8]
    add eax, ebx
    mov [rsi], rax
