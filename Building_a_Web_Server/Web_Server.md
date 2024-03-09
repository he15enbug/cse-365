# Building a Web Server
## Background Knowledge
- [System calls](https://x64.syscall.sh/)
- `socket()` creates an endpoint for communication and returns a file descriptor that refers to that endpoint
    ```
    int socket(
        int domain, 
        int type, 
        int protocol
        )
    ```
- when a socket is created with `socket()`, it exists in a name space (address family) but has no address assigned to it. `bind()` assgins the address specified by `addr` to the socket referred to by the file descriptor `sockfd`
    ```
    int bind(
        int sockfd,
        struct sockaddr *addr,
        socklen_t addrlen
        )
    ```
- `sockaddr`
    ```
    // not specific to any particular address family protocol
    struct sockaddr {
        uint16_t sa_family;
        uint8_t  sa_data[14];
    }
    // for IPv4
    struct sockaddr_in {
        uint16_t sin_family;
        uint16_t sin_port;
        uint32_t sin_addr;
        uint8_t  __pad[8];
    }
    // example
    struct sockaddr_in addr = {
        AF_INET,
        htons(80),
        {inet_addr("127.0.0.1")},
        {0}
    }
    ```
- `listen()` marks the socket referred to by `sockfd` as a passive socket, that is, as a socket that will be used to accept incoming connection requests using `accept()`
    ```
    int listen(
        int sockfd,
        int backlog
    )
    ```
- `accept()` is used with connection-based socket types (`SOCK_STREAM`, `SOCK_SEQPACKET`). It extracts the first connection request on the queue of pending connections for the listening socket, `sockfd`, creates a new connected socket, and returns a new file descriptor referring to that socket
    ```
    int accept(
        int sockfd,
        struct sockaddr *addr,
        socklen_t *addrlen
    )
    ```
- `fork()` creates a new process by duplicating the calling process. The new process is referred to as the child process. The calling process is referred to as the parent process. On success, the PID of the child process is returned to the parent, and `0` is returned to the child

## Challenges
- *level 1*: exit a program, use system call `exit()` (`60`)
- *level 2*: create a socket, `socket(AF_INET, SOCK_STREAM, IPPROTO_IP)` (`41`)
- *level 3*: bind a socket, `bind()` (`49`), mind the byte order!
    ```
    .section .data
    addr_struct:
        .word 2       # family: AF_INET
        .word 0x5000  # port: 80 in network byte order (big-endian)
        .long 0       # address: 0.0.0.0 in network byte order (big-endian)
        .fill 8, 1, 0 # padding: repeat 0 (each 0 is 1 byte) 8 times
    ```
- *level 4*: call `listen()`
- *level 5*: call `accept()`
- *level 6*: call `read()` and `write()`, use `write()` to return static content to the client
- *level 7*: extract the path from `read()` content, and open the file, `write()` the file content back. We need to take care of the sizes, e.g., `size_t` in 64-bit system should be 64-bit (`.quad`); file descriptors are 32-bit (`.long`), so when loading the returned FD from `rax`, we need to use `[fd], eax`, otherwise, the content after `fd` will be overwritten

