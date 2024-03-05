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
- *level 7.0*: nothing new
- *level 7.1*: debug it
    1. the input is 26 bytes, before the first loop, it swaps some bytes, the start address of the input data is `0x7ffe44265d80`, i.e., `$rbp-0x30`. The following code actually swaps `input[25]` and `input[9]`
        ```
        0x55d1db53756d:      movzx  eax,BYTE PTR [rbp-0x17]
        0x55d1db537571:      mov    BYTE PTR [rbp-0x43],al
        0x55d1db537574:      movzx  eax,BYTE PTR [rbp-0x43]
        0x55d1db537578:      mov    BYTE PTR [rbp-0x27],al
        0x55d1db53757b:      movzx  eax,BYTE PTR [rbp-0x44]
        0x55d1db53757f:      mov    BYTE PTR [rbp-0x17],al
        ```
    2. the first loop (25 iterations): each byte of the input is XORed with `0xa3`
    3. the second loop is a nested loop, what it does is to compare 2 adjacent bytes each time, if `input[i] > input[i+1]`, it will swap them. So, the entire second loop actually sort these bytes in ascending order
        ```
        (code for swapping adjacent bytes)
        0x55d1db5375d9:      jbe    0x55d1db537615
        0x55d1db5375db:      mov    eax,DWORD PTR [rbp-0x38]
        0x55d1db5375de:      cdqe   
        0x55d1db5375e0:      movzx  eax,BYTE PTR [rbp+rax*1-0x30]
        0x55d1db5375e5:      mov    BYTE PTR [rbp-0x42],al    <-- temp1=input[i]
        0x55d1db5375e8:      mov    eax,DWORD PTR [rbp-0x38]
        0x55d1db5375eb:      add    eax,0x1
        0x55d1db5375ee:      cdqe   
        0x55d1db5375f0:      movzx  eax,BYTE PTR [rbp+rax*1-0x30]
        0x55d1db5375f5:      mov    BYTE PTR [rbp-0x41],al    <-- temp2=input[i+1]
        0x55d1db5375f8:      mov    eax,DWORD PTR [rbp-0x38]
        0x55d1db5375fb:      cdqe   
        0x55d1db5375fd:      movzx  edx,BYTE PTR [rbp-0x41]
        0x55d1db537601:      mov    BYTE PTR [rbp+rax*1-0x30],dl <-- input[i]=temp2
        0x55d1db537605:      mov    eax,DWORD PTR [rbp-0x38]
        0x55d1db537608:      add    eax,0x1
        0x55d1db53760b:      cdqe   
        0x55d1db53760d:      movzx  edx,BYTE PTR [rbp-0x42]
        0x55d1db537611:      mov    BYTE PTR [rbp+rax*1-0x30],dl <-- input[i+1]=temp1
        ``` 
    4. the third loop has 25 iterations, there will be multiple branches, it will first do some computation on `eax` and `edx`, then it will jump to different places (i.e., the current byte will be XORed with different value). When all 25 iterations are done, the result will be compared to the expected result. In high-level, in the i-th iteration, the condition is `$eax = ((($edx >> 0x1e) + i) AND 0x3) - $edx`, notice that `cdq` will make `$edx = 0`, so `$eax = i AND 0x3`, we can also represent it as `i%4`, the range is `{0, 1, 2, 3}`, the number being XORed is `0x77` (`i%3==3`), `0xd` (`i%3==2`), `0x2e` (`i%3==1`), `0x15` (`i%3==0`)
        ```
        0x55d1db53763c:      mov    eax,DWORD PTR [rbp-0x34]
        0x55d1db53763f:      cdq    
        0x55d1db537640:      shr    edx,0x1e
        0x55d1db537643:      add    eax,edx
        0x55d1db537645:      and    eax,0x3
        0x55d1db537648:      sub    eax,edx
        0x55d1db53764a:      cmp    eax,0x3
        0x55d1db53764d:      je     0x55d1db5376b7 <-- XOR 0x77
        0x55d1db53764f:      cmp    eax,0x3
        0x55d1db537652:      jg     0x55d1db5376d0 <-- nothing to do
        0x55d1db537654:      cmp    eax,0x2
        0x55d1db537657:      je     0x55d1db53769d <-- XOR 0xd
        0x55d1db537659:      cmp    eax,0x2
        0x55d1db53765c:      jg     0x55d1db5376d0 <-- nothing to do
        0x55d1db53765e:      test   eax,eax
        0x55d1db537660:      je     0x55d1db537669 <-- XOR 0x15
        0x55d1db537662:      cmp    eax,0x1
        0x55d1db537665:      je     0x55d1db537683 <-- XOR 0x2e
        0x55d1db537667:      jmp    0x55d1db5376d0
        ```
    5. based on previous analysis, we can use the following Python program to get a valid license key
        ```
        def mod_with_condition(hex_list):
            xors = [0x15, 0x2e, 0xd]
            len1 = len(hex_list)
            for i in range(0, len1):
                hex_list[i] = hex_list[i] ^ xors[i % 3]
            return hex_list
        ```
- *level 8.0*: easy
- *level 8.1*: debug the program, the input is 35 bytes
    1. After `read`ing the input, we get the first loop, it's similar to the third loop in level 7.1. The condition is the same, `i%4`
        ```
        $eax(i%4)    XORed value
           0            0x09
           1            0x8b
           2            0x58
           3            0x38
        ```
    2. The second loop also contains a few branches, the code is more complex, instead of analyzing the static code, I ran a few (`> 6`) iterations, and found that it actually XORed each byte with a value depending on `i%6`
        ```
         $eax(i%4)    XORed value
           0            0xe7
           1            0x16
           2            0x9f
           3            0x0e
           4            0x91
           5            0x33
        ```
    3. The third loop is nested, looks like a sort function as we have analyzed in level 7.1, set a break point at where this loop ends, by checking the processed input value, it's indeed sorting all bytes in ascending order
    4. Then, it swaped `input[12]` and `input[23]`
    5. The fourth loop is swapping `input[i]` and `input[34-i]`, i.e., reversing the input
    6. Then, it swaped `input[4]` and `input[10]`
    7. The last loop is like the second one, run it and see what value is XORed in each iteration, we can figure out that the XORed value depends on `i%7`, for result from `0` to `6`, the XORed value is `0x27, 0x65, 0xf3, 0x68, 0x1f, 0x9a, 0x80`
- *level 9.0*: this time the computation on the input can not be reversed (e.g., it can calculate some hash value of our input, in that case, even given the expected result, it is computationally hard to find a valid input), but we can patch up to 5 bytes. Debug the program to see what it does
    1. the program first calls `mprotect` to set the permission for a segment of memory, it set's the memory as readable, writable, and executable to the current process. This segment of memory is actually where we will modify later (up to 5 bytes). After calling `mprotect`, if it succeeds (`$rax==0`), it will do this again, i.e., modifying the permission of the next segment of `0x1000` bytes memory to `rwx`, and loop again, until it fails. An important information is that it can change the permission of `0x6000` bytes in total (from `0x56021448b000` to `0x560214491000`), which means the whole program is now readable, writable, and executable
        ```
        rdi: [rbp-0xa8]     <- base address
        rsi: 0x1000         <- length
        rdx: 0x7            <- mode, 0x7 represent rwx
        ```
    2. modify up to 5 bytes, `set [BASE + OFFSET] = TARGET`
        ```
        <main+495>:   movzx  ecx,BYTE PTR [rbp-0xc3]  <- TARGET
        <main+502>:   movzx  eax,WORD PTR [rbp-0xc2]  <- OFFSET
        <main+509>:   movzx  edx,ax
        <main+512>:   mov    rax,QWORD PTR [rbp-0xa8] <- BASE
        <main+519>:   add    rax,rdx                  <- BASE + OFFSET
        <main+522>:   mov    edx,ecx
        <main+524>:   mov    BYTE PTR [rax],dl        <- [BASE + OFFSET] = TARGET
        ```
    3. the core computation on the input is calculating the MD5 in the following way
        ```
        <main+776>:   lea    rax,[rbp-0xa0] <- param 1: hold the MD5 context here
        <main+783>:   mov    rdi,rax
        <main+786>:   call   0x55573f526270 <MD5_Init@plt>
        <main+791>:   lea    rcx,[rbp-0x30]
        <main+795>:   lea    rax,[rbp-0xa0]
        <main+802>:   mov    edx,0x1c       <- param 3: data length
        <main+807>:   mov    rsi,rcx        <- param 2: address of data
        <main+810>:   mov    rdi,rax        <- param 1: address of MD5 context
        <main+813>:   call   0x55573f526230 <MD5_Update@plt>
        <main+818>:   lea    rdx,[rbp-0xa0]
        <main+825>:   lea    rax,[rbp-0x40]
        <main+829>:   mov    rsi,rdx        <- param 2: address of MD5 context
        <main+832>:   mov    rdi,rax        <- param 1: address of result
        <main+835>:   call   0x55573f526220 <MD5_Final@plt>
        ```
    - strategy: we can modify 5 bytes, we know that our input is stored at `$rbp-0x30`, the hash result is stored at `$rbp-0x40`. After getting the hash value, the `memset` will clear the original input at `$rbp-0x30`. Then, the program copied 2 q-words (16 bytes in total) at `$rbp-0x40` to `$rbp-0x30`. Finally, the `memcmp` will compare a number of bytes at `$rbp-0x30` with the expected result, it is impractical to modify the data itself, we can modify the following:
        1. let `memset` clear the content at somewhere else, so our input will be kept. Notice that `memset` clears `0x1c` bytes, if we let it clear from `$rbp-0x40`, it will still clear some of our input, instead, we can let it clear the content at `$rbp-0x50`
            ```
            <main+840>: lea rax,[rbp-0x30] <--- 0x30 -> 0x50
            ```
        2. after the MD5 finishes, prevent the 2 q-words being copied to `$rbp-0x30`, we can modify 2 bytes in the code in the following way
            ```
            <main+862>:   mov    rax,QWORD PTR [rbp-0x40]
            <main+866>:   mov    rdx,QWORD PTR [rbp-0x38]
            <main+870>:   mov    QWORD PTR [rbp-0x30],rax <--- 0x30 -> 0x40
            <main+874>:   mov    QWORD PTR [rbp-0x28],rdx <--- 0x28 -> 0x38
            ```
    - if we succeed, we can just input the expected result itself, and we will pass the verification
    - we need figure out the offset of 3 bytes
        1. the `0x30` in `0x56021448d75a <main+840>: lea rax,[rbp-0x30]` (before the `memset`)
        2. the `0x30` in `0x56021448d778 <main+870>: mov QWORD PTR [rbp-0x30],rax`
        3. the `0x28` in `0x56021448d77c <main+874>: mov QWORD PTR [rbp-0x28],rdx` 
    - we can use `x/16bx <ADDRESS>` to check the bytes (each of the above instruction is 4 bytes)
        ```
        (gdb) x/4bx 0x56021448d75a
        0x56021448d75a <main+840>:      0x48    0x8d    0x45    0xd0
        (gdb) x/4bx 0x56021448d778
        0x56021448d778 <main+870>:      0x48    0x89    0x45    0xd0
        (gdb) x/4bx 0x56021448d77c
        0x56021448d77c <main+874>:      0x48    0x89    0x55    0xd8
        ```
    - we can notice that `0xd0` is the displacement of `-0x30`, `0xd8` is the displacement of `-0x28`, what we need is
        1. `-0x50` (`0x80`) at `OFFSET = 0x56021448d75d - 0x56021448b000 = 0x275d`
        2. `-0x40` (`0xc0`) at `OFFSET = 0x56021448d77b - 0x56021448b000 = 0x277b`
        3. `-0x38` (`0xc8`) at `OFFSET = 0x56021448d77f - 0x56021448b000 = 0x277f`
    - and the expected result is
        ```
        81 0c c8 01 30 37 53 31 bb 76 d8 8d 7b 48 5a aa 00 00 00 00 00 00 00 00 00 00 00 00
        ```
    - to directly input bytes, we need
        ```
        printf "0x275d\n0x80\n0x277b\n0xc0\n0x277f\n0xc8\n0\n0\n0\n0\n\x81\x0C\xC8\x01\x30\x37\x53\x31\xBB\x76\xD8\x8D\x7B\x48\x5A\xAA\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" | /challenge/babyrev_level9.0
        ```
- *level 9.1*: like previous challenges of level `*.1`, there is no `main` function, we need to get somewhere at the beginning of the program, `break printf`, and use `nexti` to get to the address right after the `printf` returns, then we can see the entire logic of the program using `x/160i $rip`. It is the same as level 9.0
    1. use `mprotect` to change the permission of `6000` bytes in total from `[rbp-0xa8]` (`0x5590c7f9d000`)
    2. input the offset (base address `[rbp-0xac]`) and new value of the 5 bytes to be modified
    3. input the data, stored at `$rbp-0x30`
    4. calculate MD5, the data length is `0x1d`
    5. use `memset` to clear `0x1d` bytes at `$rbp-0x30`, and copy 2 q-words (16 bytes) at `$rbp-0x40` to `$rbp-0x30`
    6. compare `0x1d` bytes at `$rbp-0x30` with the expected result
    - similarly, we just need to modify 3 bytes
        ```
        lea rax,[rbp-0x30]
        0x5590c7f9e953: 0x48 0x8d 0x45 0xd0 <-- 0xd0 to 0x80
        OFFSET: 0x5590c7f9e956 - 0x5590c7f9d000 = 0x1956

        mov QWORD PTR [rbp-0x30],rax
        0x5590c7f9e971: 0x48 0x89 0x45 0xd0 <-- 0xd0 to 0xc0
        OFFSET: 0x5590c7f9e974 - 0x5590c7f9d000 = 0x1974

        mov QWORD PTR [rbp-0x28],rdx
        0x5590c7f9e975: 0x48 0x89 0x55 0xd8 <-- 0xd8 to 0xc8
        OFFSET: 0x5590c7f9e978 - 0x5590c7f9d000 = 0x1978
        ```
    - result
        ```
        printf "0x1956\n0x80\n0x1974\n0xc0\n0x1978\n0xc8\n0\n0\n0\n0\n\x88\x29\xB8\x8F\x93\xD5\x73\x8C\xC1\x38\x6A\x53\xF3\x33\x7C\x8F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" | /challenge/babyrev_level9.1
        ```
- *level 10.0*: we can only patch 1 byte, it's impractical to prevent our input from being modified. 
    - However, we can try to do something to the parameters of `memcmp`, when the program loads the address of the expected result to `rsi`, it uses `lea rsi,[rip+0x2724]`, if we can modify 1 byte of the instruction, let this address the same to `rbp-0x30`, then, the `memcmp` will always get an equal result. Specifically, when executiing `lea rsi,[rip+0x2724]`, the next is truction is `0x55593da9e8ec`, and we can know that `rbp-0x30` is `0x7ffc52a24dc0`, `0x7ffc52a24dc0 - 0x55593da9e8ec = 0x2aa314f864d4`, the instruction we need is `lea rsi,[rip+0x2aa314f864d4]`, it seems impossible to achieve this by modifying only 1 byte
    - Instead of making `memcmp` return `0` (equal), we can modify the condition of the jump
        ```
        0x55593da9e8ef <main+1217>: call   0x55593da9d290 <memcmp@plt>
        0x55593da9e8f4 <main+1222>: test   eax,eax
        0x55593da9e8f6 <main+1224>: jne    0x55593da9e90c <main+1246>
        ```
        ```
        0x55593da9e8f6 <main+1224>: 0x75 0x14 <-- 0x75 to 0x74
        OFFSET = 0x55593da9e8f6 - 0x55593da9c000 = 0x28f6
        ```
    - Fortunately, `jne` is just 1 byte `0x75`, we modify it to `je` (`0x74`), then when the MD5 of our input is not equal to the expected result, the program will execute `win` and print out the flags
    - run `printf "0x28f6\n0x74\n0" | /challenge/babyrev_level10.0`
- *level 10.1*: we can still patch only 1 byte
    - address of `jne` after `memcmp`: `0x555c4f4df395`
    - base address (for patching the program) `0x555c4f4dd000`
    - offset: `0x555c4f4df395 - 0x555c4f4dd000 = 0x2395`
    - run `printf "0x2395\n0x74\n0" | /challenge/babyrev_level10.1`
- *level 11.0*: this time we can patch 2 bytes
- *level 11.1*