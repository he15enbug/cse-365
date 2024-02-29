.section .text
.global _start
.intel_syntax noprefix

_start:
    mov rax, [0x404000]
    add dword ptr [0x404000], 0x1337

