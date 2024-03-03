# Course Material
## ELF file
- *Sections*
    - `.text`: executable code
    - `.data`: used for pre-initialized global writable data, such as global arrays with initial values
    - `.bss`: used for uninitialized global writable data, such as global arrays without initial values
    - `.rodata`: used for global read-only data, such as string constants
    - `.symtab`: symbol table
    - `.strtab`: string table
    - ...
## The Stack
- *Initial Layout*
    - the stack starts out storing (among some other things) the environment variables and the program arguments
- *Calling a Function*
    - When calling a function, the return address (the address of the next instruction) will be **implicitly** pushed onto the stack
    - When the called function (callee) returns, the return address will be **implicitly** popped by the function (the `ret` instruction)
- *Prologue*
    1. `push rbp`
    2. `mov rbp, rsp` (so, `rbp` stores the address of the previous base pointer)
    3. `sub rsp, <ALLOC_SIZE>` allocate space on the stack
- *Epilogue*
    1. `mov rsp, rbp` deallocate space (data is still in memory by default)
    2. `pop rbp`, restore the previous base pointer
- Compiling with option `-fomit-frame-pointer`: modern compilers can omit frame pointer in most cases, to allow `rbp` to be used as a general purpose register

## The Data
- Data can be in:
    - `.data`
    - `.rodata`
    - `.bss`
    - Stack: for statically-allocated local variables
    - Heap: for dynamically-allocated (`malloc()`ed) variables
- Accessing data on stack: `push`, `pop`, `mov <REGISTER>, [rbp - <OFFSET>]`
- Accessing data in ELF sections: `mov <REGISTER>, [rip + <OFFSET>]`
- Accessing data on the heap (pointers to heap data are generally stored in memory or on the stack): example: `mov rax, [rsp]`, then `mov rdx, [rax]`, the first load the content at the address in `rsp` to `rax`, it is a pointer to some heap data, we can use `[rax]` to load the data in the heap

## Static Tools
- Static (as opposed to dynamic) reverse engineering: analyzing a program at rest
- Simple Stuff
    - [`kaitai struct`](https://ide.kaitai.io/): file format parser and exploer
    - `nm`: lists symbols used/provided by ELF files
    - `strings`: dumps ASCII (and other format) strings found in a file
    - `objdump`: simple disassembler
    - [`checksec`](https://github.com/slimm609/checksec.sh): analyzes security features used by an executable
- Advanced Disassemblers: several state-of-the-art tools
    - Commercial
        - [`IDA Pro`](https://www.hex-rays.com/products/ida/)
        - [`Binary Ninja`](https://binary.ninja/)
    - Free
        - [`Binary Ninja Cloud`](https://cloud.binary.ninja/): a version of Binary Ninja that runs in the browser
    - Open source
        - [`angr management`](https://github.com/angr/angr-management/releases)
        - [`ghidra`](https://ghidra-sre.org/)
        - [`cutter`](https://cutter.re/)

## Dynamic Tools
- Dynamic (as opposed to static) reverse engineering: analyzing a program at runtime
- Program Tracking
    - `ltrace` traces library calls
    - `strace` traces system calls
    - running the program with multiple different inputs might get us farther
        - `ltrace` the program with input A
        - `ltrace` the program again with input B
        - see if we can reverse the algorithm from looking at input and output
        - still does not scale to complex algorithms
- Debugging: use `gdb`
    - Errata: Dealing with PIE
        - *Position-Dependent Executables* are loaded at a static address in memory
        - *Position-Independent Executables* are not
        - `gdb` tries to help by always loading them (depending on `gdb` and kernel version) at `0x0000555555554000` or `0x7ffff7ffc000`
        - Easies way to deal with this is to put this in our `.gdbinit`: `set $base = 0x7ffff7ffc000`
        - Afterwards, we can do stuff like: `break *($base + 0x1023)`
    - Timeless Debugging
        - Timeless debugging frees us from having to think of breakpoints ahead of time
            1. record execution
            2. rewind execution
            3. replay execution
        - Relevant tools
            - [`gdb`'s built-in record-replay functionality](https://sourceware.org/gdb/current/onlinedocs/gdb/Process-Record-and-Replay.html)
            - [`rr`](https://github.com/mozilla/rr): a highly-performant record-replay engine
            - [`qira`](https://qira.me/): a timeless debugger

## License Checkers
- How does the software that has to be installable with out Internet access ensure that it is legitimate? License key checks
    - Have a secret algorithm that takes in input, performs some calculation, and validates the result
    - Ideally, the company selling the software can generate multiple valid keys
    - Ideally, pirates cannot generate valid keys
- This method implicitly trusts the binary code to keep the secret license key verification algorithm safe
- Simple Example
    - [**Crackmes**](https://en.wikipedia.org/wiki/Crackme) are small programs designed to test a hacker's reverse engineering skills inspired by real-world license key verification systems
    - Many many [crackmes](https://crackmes.one)

## Alternatives to Keygens
- With ubiquitous Internet access and increased ability to have unbreakable server-side license key checks, keygenning diminished in viability
- Alternatives
    1. Cracks that patch the executable to remove the check altogether (but what to crack?)
    2. Legally purchasing the software

## Evolution of *DRM, Digital Rights Management*
- Modern DRM has taken on more and more clever approaches, such as
    - *Anti-debugging*: techniques to fight dynamic analysis
    - *VMing*: wrapping the DRM code in a heavily obfuscated, protected emulator for a custom architecture, with the DRM logic inside that architecture
    - *Trusted Execution Environments*: moving the DRM outside of the CPU into protected hardware

## Reverse Engineering for Modding
- Another application of reverse engineering: modding. When modders hit the limits of modding a game's data files, they start modding the code
- Examples
    - *Skyrim*: the Skyrim Script Engine (SKSE)
    - *Dwarf Fortress*: DFHack
    - And the dark side: cheating in online games

## Usage of `gdb`
- start the program `start`
- set breakpoint `break main`, `b main`, `break *<instruction_address>`
- continue to run `continue`, `c`
- check registers `print rax`, `p rax`, `p/x rax` (print out `rax`'s value in hex)
- examine the contents of memory `x/<n><u><f> <address>`
    - `<u>` unit size to display (`b`: 1 byte, `h`: 2 bytes, `w`: 4 bytes, `g`: 8 bytes)
    - `<f>` the format to display it in (`d`: decimal, `x`: hexadecimal, `s`: string, `i`: instruction)
    - `<n>` the number of elements to display
    - `<address>` can be specified using register name, symbol name, or absolute address, we can supply mathematical expressions when specifying the address
    - view instructions using the CORRECT assembly syntax. You can do that with the command `set disassembly-flavor intel`
    - move `n` steps forward `stepi <n>`/`si <n>`
    - move `n` steps forward `nexti <n>`/`ni <n>`, while stepping over function calls 
    - always display some information: `display/<n><u><f>`
    - `layout regs`: put `gdb` into its TUI mode and show the contents of all registers, as well as nearby instructions
    - modify the state of the target program
        - `set $rdi = 0`
        - `set *((uint64_t *) $rsp) = 0x1234` to set the first value (64-bit) on the stack to `0x1234`
        - `set *((uint16_t *) 0x31337000) = 0x1337` to set the 2 bytes from address `0x31337000` to `0x1337`
    - break on system calls `catch syscall read`


### `gdb` scripting
- we can write the `gdb` commands to a `.gdb` file, then launch `gdb` using the flag `-x <PATH_TO_SCRIPT>`. The file will execute all commands after `gdb` launches
- Alternatively, we can execute individual commands with `-ex <COMMAND>`, we can pass multiple commands with multiple `-ex` arguments
- Finally, we can have some commands be always executed for any `gdb` session by putting them in `~/.gdbinit`, e.g., we can put `set disassembly-flavor intel` in there

# Challenges
## Debugging Refresher
- *level 1*: skipped
- *level 2*: skipped
- *level 3*: set a break point right after calling `read`, by inspecting the `rsi` and `rdx`, we can know it reads 8 bytes from `/dev/urandom`, run `x/1gh $rsi`, then we can get the random value
- *level 4*: the solution is similar to the solution for level 3, however, we need to get the random number for multiple times. Set a break point right after the `read` call, and get the random number using `x/1gh $rsi`. After a few loops, we will get the flag
- *level 5*: just write a `gdb` script, set a break point right after the `read` call, then print out the 8-byte value at `[rsi]`. There will be more loops than in previous task, with this script, we can get the flag more efficiently
    ```
    start
    break *main+709
    commands
        silent
        set $rand_val = *(unsigned long long *)($rsi)
        printf "Current random value: %llx\n", $rand_val
        continue
    end
    continue
    ```
- *level 6*: `gdb` can also modify the behavior of a program. The key for this challenge is to figure out how to automatically input data to the system call `__isoc99_scanf`, by inspecting its arguments, we can know that the first argument, specified in `rdi`, is a format string; the second argument, specified by `rsi`, is an address where the input will be stored, there are 2 subtasks we need to do
    1. skip the manual input process, this can be done by setting the format string a null string, i.e., set the first byte at `[rdi]` to `0x00`: `set *((uint8_t *) $rdi) = 0`
    2. directly put the random value at `[rsi]`: `set *((uint64_t *) $rsi) = $rand_val`
- *level 7*: this is an elevated instance of `gdb`, run `call (void)win()`
- *level 8*: we cannot directly use `call (void)win()` to run `win()`, it will show the following information
    ```
    The program being debugged was signaled while in a function called from GDB.
    GDB remains in the frame where the signal was received.
    To change this behavior use "set unwindonsignal on".
    Evaluation of the expression containing the function
    (win) will be abandoned.
    When the function is done executing, GDB will silently stop.
    ```
    - However, we can directly control the execution flow by setting the value in the register `rip`
    - After we start, run `set $rip=*win` first
    - There are 2 instructions in the `win` function that will cause an exception, `<win+24>: mov eax, DWORD PTR [rax]` and `<win+33> mov DWORD PTR [rax], edx`, in both cases, the value of `rax` is zero, so `[rax]` will cause invalid memory access. Before executing these 2 instructions, we can set `rip` to skip them
    ```
    start
    display/16i $rip
    set $rip=*win
    nexti 6
    set $rip=$rip+2
    nexti 2
    set $rip=$rip+2
    continue
    ```
## Reverse Engineering
- *level 1.0*: run the program, and try some input, we can know that it takes 5 characters as the input, and from `a` to `z`, the byte will be `0x61` to `0x7a`, and the expected result will be given `6d 65 63 62 65`, so the license key is `mecbe`
- *level 1.1*: this time, the expected result will not be printed out, but it's fine, we can `gdb` the program. Another problem is that if we run `start`, it will tell us that no `main` function is found, since our ultimate goal is to get the correct key, the program actually uses `memcmp` to check whether our input is correct, we can set a break point there, `break memcmp`, get there, then check the values at `rdi` and `rsi`, in our case, the expected key is stored at `rsi`, we can see it using `x/1s $rsi` or `x/5bx $rsi`
    ```
    (gdb) x/5bx $rsi
    0x5610f12d8010: 0x6a    0x66    0x69    0x71    0x7a
    (gdb) x/1s $rsi
    0x5610f12d8010: "jfiqz"
    ```
- *level 2.0*: this time, our input will be modified somehow before being compared to the correct key. It directly tells us that it swaps the bytes at indexes `0` and `2`, and the expected result is `6f 6d 61 73 72` (`omasr`), so, we can input `amosr` to get the flag
- *level 2.1*: it will not tell us the way it process our input, `gdb` the program, similarly to level 1.1, we get into `memcmp`, check the string at `rsi` and `rdi`, our input is `abcde`, and the string at `rdi` is `ebcad`, and the string at `rsi` is `yxugw` (the expected result), so, our input should be `gxuyw`
    ```
    x/1s $rsi       x/1s $rdi
        gxuyw           abcde
        |  |            |  |
        yxugw           dbcae
    ```
- *level 3.0*: it will reverse the input, just input the reversed expected result
- *level 3.1*: similar to level 2.1
- *level 4.0*: it will sort the input, just input the expected result in any order
- *level 4.1*: debug the program
- *level 5.0*: each byte will be XORed with `0x99`, input the expected result XORed with `0x9999999999`
- *level 5.1*: debug the program to get the expected result, we can find out that each byte is XORed with `0x8d`
- *level 6.0*: the key becomes 16 bytes, swap the bytes at indexes `0` and `9`, then XOR each 2-byte block with `0xbf46`, the expected result contains bytes that are not ASCII printable, we can use `printf` to input these bytes: `printf "\x9f\x66\x9a\x61\x98\x6e\x8e\x73\x77\x8b\x71\x89\x6e\x93\x66\x9a" | /challenge/babyrev_level6.0`
- *level 6.1*: since the process algorithm becomes more and more complex, we cannot directly know how it process the input by inspecting the result, I did the following
    1. inspect the assembly code to figure out how the program processes our input, first, `break read` and `start`, we get into the `read` system call, use `nexti` to run a few instructions, then we get out of the `read`, and start the processing logic
    2. this is the first loop (process the first 9 bytes of the input), its function is to swap `input[i]` and `input[17-i]` for `0 <= i && i <= 8`. An easy way to learn about the functionality of this loop is to `display/18bx $rbp-0x20`, and set a break point at `0x5624f7d34591` (the `jle` instruction), then we can run `continue` to see what happens in each round of the loop
        ```
        0x5624f7d3453d:      call   0x5624f7d341a0 <read@plt>
        0x5624f7d34542:      mov    DWORD PTR [rbp-0x2c],0x0
        0x5624f7d34549:      jmp    0x5624f7d3458d
        0x5624f7d3454b:      mov    eax,DWORD PTR [rbp-0x2c]
        0x5624f7d3454e:      cdqe   
        0x5624f7d34550:      movzx  eax,BYTE PTR [rbp+rax*1-0x20]
        0x5624f7d34555:      mov    BYTE PTR [rbp-0x2e],al
        0x5624f7d34558:      mov    eax,0x11
        0x5624f7d3455d:      sub    eax,DWORD PTR [rbp-0x2c]
        0x5624f7d34560:      cdqe   
        0x5624f7d34562:      movzx  eax,BYTE PTR [rbp+rax*1-0x20]
        0x5624f7d34567:      mov    BYTE PTR [rbp-0x2d],al
        0x5624f7d3456a:      mov    eax,DWORD PTR [rbp-0x2c]
        0x5624f7d3456d:      cdqe   
        0x5624f7d3456f:      movzx  edx,BYTE PTR [rbp-0x2d]
        0x5624f7d34573:      mov    BYTE PTR [rbp+rax*1-0x20],dl
        0x5624f7d34577:      mov    eax,0x11
        0x5624f7d3457c:      sub    eax,DWORD PTR [rbp-0x2c]
        0x5624f7d3457f:      cdqe   
        0x5624f7d34581:      movzx  edx,BYTE PTR [rbp-0x2e]
        0x5624f7d34585:      mov    BYTE PTR [rbp+rax*1-0x20],dl
        0x5624f7d34589:      add    DWORD PTR [rbp-0x2c],0x1
        0x5624f7d3458d:      cmp    DWORD PTR [rbp-0x2c],0x8
        0x5624f7d34591:      jle    0x5624f7d3454b
        ```
    3. then there is the second loop, change all bytes back, i.e., swap `input[i]` and `input[17-i]` for `0 <= i && i <= 8` again
    4. then there is the third loop, which XOR `input[i]` with `0xbb` for `0 <= i && i <= 17`
    5. through previous analysis, we know that the key is actually 18 bytes, get to `memcmp`, and inspect the 18 bytes from `$rsi`, the expected output is:
        ```
        (gdb) x/18bx $rsi
        0x560c7d3ce010: 0xcc    0xd4    0xd7    0xc9    0xd9    0xd9    0xd9    0xcd
        0x560c7d3ce018: 0xcd    0xdf    0xd2    0xcd    0xd1    0xda    0xd9    0xce
        0x560c7d3ce020: 0xd9    0xd6
        ```
    6. XOR each byte with `0xbb`, input this result
        ```
        printf "\x77\x6f\x6c\x72\x62\x62\x62\x76\x76\x64\x69\x76\x6a\x61\x62\x75\x62\x6d" | /challenge/babyrev_level6.1
        ```
- *level 7.0*
- *level 7.1*