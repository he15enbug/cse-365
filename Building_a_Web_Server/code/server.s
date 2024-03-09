.intel_syntax noprefix

.section .text
.global _start

_start:
    mov rdi, 2  # family:   AF_INET (IPv4)
    mov rsi, 1  # type:     SOCK_STREAM
    mov rdx, 0  # protocol: IPPROTO_IP
    mov rax, 41 # socket()
    syscall

    mov rdi, rax            # FD of the socket
    lea rsi, [addr_struct]  # load the address of addr_struct to rsi
    mov rdx, 16             # data length
    mov rax, 49 # bind()
    syscall

    mov rdi, 0
    mov rax, 60 # exit()
    syscall

.section .data
addr_struct:
    .word 2       # family: AF_INET
    .word 0x5000  # port: 80 in network byte order (big-endian)
    .long 0       # address: 0.0.0.0 in network byte order (big-endian)
    .fill 8, 1, 0 # padding: repeat 0 (each 0 is 1 byte) 8 times