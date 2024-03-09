.intel_syntax noprefix

.section .text
.global _start

_start:
    mov rdi, 2  # family:   AF_INET (IPv4)
    mov rsi, 1  # type:     SOCK_STREAM
    mov rdx, 0  # protocol: IPPROTO_IP
    mov rax, 41 # socket()
    syscall
    mov [server_fd], eax # store the socket FD for later use

    mov rdi, [server_fd]
    lea rsi, [addr_struct]  # load the address of addr_struct to rsi
    mov rdx, 16             # data length
    mov rax, 49 # bind()
    syscall

    mov rdi, [server_fd]
    mov rsi, 0   # backlog (maximum length of pending connection queue)
    mov rax, 50  # listen()
    syscall

process_requests:
    mov rdi, [server_fd]
    xor rsi, rsi # NULL
    xor rdx, rdx # NULL
    mov rax, 43  # accept()
    syscall
    mov [cli_fd], eax # store the client socket for later use

    # fork a child process to process request
    mov rax, 57 # fork()
    syscall
    test rax, rax
    je child_proc

    # close() the client FD
    mov rdi, [cli_fd]
    mov rax, 3          # close()
    syscall

    jmp process_requests

child_proc:
    # close() server FD because child process don not need to listen to it
    mov rdi, [server_fd]
    mov rax, 3          # close()
    syscall

    # read() data from client socket FD
    mov rdi, [cli_fd]
    lea rsi, [buf]    # a buffer to store the content
    mov rdx, 1024     # read at most 1024 bytes
    mov rax, 0        # read()
    syscall

    # extract file name from the request
    lea rax, [buf]
    lea rbx, [file_name]
    add rax, 4
get_file_name:
    mov cl, byte ptr [rax]
    mov byte ptr [rbx], cl
    inc rax
    inc rbx
    cmp  byte ptr [rax], 0x20
    jne get_file_name

    # open() the file
    lea rdi, [file_name]
    mov rsi, O_RDONLY    # open file with O_RDONLY flag
    xor rdx, rdx         # clear rdx to use default permission mode for newly created file
    mov rax, 2           # open()
    syscall
    mov [file_fd], eax

    # read() from the file
    mov rdi, [file_fd]
    lea rsi, [file_buf]
    mov rdx, 1024
    mov rax, 0        # read()
    syscall
    mov [file_size], rax

    # close() the file FD
    mov rdi, [file_fd]
    mov rax, 3        # close()
    syscall

    # write() HTTP OK to client
    mov rdi, [cli_fd]
    lea rsi, [static_resp]  # response content
    mov rdx, 19             # response length
    mov rax, 1              # write()
    syscall

    # write() file content to client
    mov rdi, [cli_fd]       # client socket FD
    lea rsi, [file_buf]     # file content
    mov rdx, [file_size]    # file size
    mov rax, 1              # write()
    syscall

    mov rdi, 0
    mov rax, 60 # exit()
    syscall

.section .data
O_RDONLY: .long 0
file_name: 
    .byte 0x22 # double quote
    .fill 200, 1, 0 # a 200-byte buffer
end_file_name: .byte 0
file_size: .quad 0
file_fd: .long 0
file_buf: .fill 1024, 1, 0 # a 1024-byte buffer
end_file_buf: .byte 0

static_resp: .ascii "HTTP/1.0 200 OK\r\n\r\n"
end_resp: .byte 0

buf: .fill 1024, 1, 0 # a 1024-byte buffer
end_buf: .byte 0

cli_fd: .long 0
cli_addr_len: .long 0
cli_family: .word 0
cli_port: .word 0  # port in network byte order (big-endian)
cli_addr: .long 0  # address in network byte order (big-endian)
cli_pad:  .fill 8, 1, 0 # padding: repeat 0 (each 0 is 1 byte) 8 times

server_fd: .long 0
addr_struct:
    .word 2       # family: AF_INET
    .word 0x5000  # port: 80 in network byte order (big-endian)
    .long 0       # address: 0.0.0.0 in network byte order (big-endian)
    .fill 8, 1, 0 # padding: repeat 0 (each 0 is 1 byte) 8 times
