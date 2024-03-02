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
- *level 6*: 

