#!/bin/bash

gcc -nostdlib -static $1.s -o shellcode-elf
objcopy --dump-section .text=shellcode-raw shellcode-elf
cat shellcode-raw