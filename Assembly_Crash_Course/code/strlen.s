.section .text
.global _start
.intel_syntax noprefix

_start:
    xor rax, rax
    // IMPORTANT
    cmp rdi, 0
    je done
loop:
    mov dl, [rdi]
    cmp dl, 0x00
    je done
    add rax, 0x1
    add rdi, 0x1
    jmp loop
done:
