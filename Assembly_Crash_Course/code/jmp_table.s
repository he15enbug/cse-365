.section .text
.global _start
.intel_syntax noprefix

_start:
    cmp rdi, 0x4
    jg gt_4
continue:
    mov rax, rdi
    mov rbx, 0x8
    mul rbx
    add rax, rsi
    jmp [rax]

gt_4:
    mov rdi, 0x4
    jmp continue
