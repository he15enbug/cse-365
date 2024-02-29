.section .text
.global _start
.intel_syntax noprefix

_start:
    mov rax, [rsp]
    mov rbx, [rsp+8]
    mov rcx, [rsp+16]
    mov rsi, [rsp+24]
    xor rdx, rdx

    add rax, rbx
    jc overflow1
continue1:
    add rax, rcx
    jc overflow2
continue2:
    add rax, rsi
    jc overflow3
continue3:
    jmp end_calculation
  
overflow1:
    add rdx, 0x1
    jmp continue1
overflow2:
    add rdx, 0x1
    jmp continue2
overflow3:
    add rdx, 0x1
    jmp continue3

end_calculation:
    mov rcx, 0x4
    div rcx
    push rax
