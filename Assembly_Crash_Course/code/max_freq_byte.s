.section .text
.global _start
.intel_syntax noprefix

_start:
    // src_addr  rdi
    // size      rsi
    push rbp
    mov rbp, rsp
    sub rsp, 0xff

    mov rbx, 0x0
loop1:
    cmp rbx, rsi
    jge exit1
    xor rdx, rdx
    mov dl, byte ptr [rdi + rbx]

    mov r8, rbp
    sub r8, rdx
    mov rcx, [r8]
    inc rcx
    mov [r8], rcx

    inc rbx
    jmp loop1
exit1:
    mov rax, 0x0
    mov rbx, 0x0
    mov rcx, 0x0

loop2:
    cmp rbx, 0xff
    jg exit2
    mov r8, rbp
    sub r8, rbx
    cmp cl, byte ptr [r8]
    jge inc_b
    mov cl, byte ptr [r8]
    mov rax, rbx

inc_b:
    inc rbx
    jmp loop2
exit2:
    add rsp, 0xff
    pop rbp
    ret
