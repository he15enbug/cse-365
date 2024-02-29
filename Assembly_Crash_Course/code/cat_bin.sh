#!/bin/bash

# assemble to an object file
as -o $1.o $1.s

# copy .text section to a bin file
objcopy -O binary --only-section=.text $1.o $1.bin

# cat the binary
cat "$1".bin