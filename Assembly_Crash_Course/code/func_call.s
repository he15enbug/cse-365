.section .text
.global str_lower
.intel_syntax noprefix

str_lower:
    push rbp
    mov rbp, rsp
    
    mov rbx, 0x0
    cmp rdi, 0x0
    je retr

while_loop:

    cmp byte ptr [rdi], 0x00
    je retr

    cmp byte ptr [rdi], 0x5a
    jg skip_conversion

    // store rdi
    mov rdx, rdi
    // prepare argument for foo
    mov rdi, [rdi]
    shl rdi, 56
    shr rdi, 56
    // This is important, we cannot directly call 0x403000
    mov r8, 0x403000
    call r8

    // recover rdi
    mov rdi, rdx
    mov [rdi], al
    inc rbx

skip_conversion:
    inc rdi
    jmp while_loop

retr:
    mov rax, rbx

    pop rbp
    ret
