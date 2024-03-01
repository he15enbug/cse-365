.section .text
.global _start
.intel_syntax noprefix

_start:
    xor rcx, rcx
    xor rdx, rdx
    xor rbx, rbx
    cmp rsi, 1
    jl done
loop_n:
    mov rax, 0x8
    mul rcx
    add rax, rdi

    add rbx, qword ptr [rax]

    jc carry
back:
    inc rcx
    cmp rcx, rsi
    jl loop_n
    jmp div_n

carry:
    inc rdx
    jmp back

div_n:
    mov rax, rbx
    div rsi
done:
    nop
