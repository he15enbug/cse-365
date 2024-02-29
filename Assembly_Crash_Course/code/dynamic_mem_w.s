.section .text
.global _start
.intel_syntax noprefix

_start:
    mov dword ptr [rdi], 0x00001337
    mov dword ptr [rdi + 4], 0xdeadbeef
    mov dword ptr [rsi], 0xffee0000
    mov dword ptr [rsi + 4], 0x000000c0
