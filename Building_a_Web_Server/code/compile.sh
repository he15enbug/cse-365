#!/bin/bash

as -o $1.o $1.s && ld -o $1 $1.o