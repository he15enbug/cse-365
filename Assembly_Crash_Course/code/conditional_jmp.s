.section .text
.global _start
.intel_syntax noprefix

_start:
    mov eax, dword ptr [rdi + 4]
    mov ebx, dword ptr [rdi + 8]
    mov ecx, dword ptr [rdi + 12]

    // The given information x = rdi is totally WRONG! x = [rdi]
    mov edx, [rdi] 

    cmp edx, 0x7f454c46
    je eq1

    cmp edx, 0x00005A4D
    je eq2

    imul eax, ebx
    imul eax, ecx
    jmp done

eq1:
    add eax, ebx
    add eax, ecx
    jmp done
eq2:
    sub eax, ebx
    sub eax, ecx
done:
    nop
