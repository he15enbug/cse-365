#!/usr/bin/env python

from pwn import *
import re

def is_subset(A, B):
    return all(a in B for a in A)

def answer(question, level_table):
    levels = []
    categories = []

    idx = question.find('Subject with level ') + len('Subject with level ')
    levels.append(question[idx:].split()[0])
    idx = question.find('Object with level ') + len('Object with level ')
    levels.append(question[idx:].split()[0])

    idx = question.find('categories ') + len('categories ')
    bg  = question[idx:].find('{')
    ed  = question[idx:].find('}')

    category_str = question[idx:][bg + 1: ed]
    category_arr = category_str.split(', ')
    if(len(category_arr) == 1 and category_arr[0] == ''):
        category_arr = []
    categories.append(category_arr)

    idx = question.find('Object')
    bg  = question[idx:].find('{')
    ed  = question[idx:].find('}')
    category_str = question[idx:][bg + 1: ed]

    category_arr = category_str.split(', ')
    if(len(category_arr) == 1 and category_arr[0] == ''):
        category_arr = []
    categories.append(category_arr)

    for level, category_list in zip(levels, categories):
        print("Level:", level)
        print("Categories:", category_list)

    levels = [level_table[k] for k in levels]
    print(levels)
    if('write' in question):
        if(levels[0] < levels[1]):
            return 'NO'
        if(is_subset(categories[0], categories[1]) == False):
            return 'NO'
    else:
        if(levels[0] > levels[1]):
            return 'NO'
        if(is_subset(categories[1], categories[0]) == False):
            return 'NO'
    return 'YES'


def auto_anwser(total):
    categories = {'UFO': 0, 'NUC': 1, 'NATO': 2, 'ACE': 3}
    p = process('/challenge/run')

    p.readuntil('Levels (first is highest aka more sensitive):')
    p.readline()

    level_num = 0
    level_table = {}
    while True:
        level = p.readline()[:-1].decode('utf-8')
        if('Categories:' in level):
            break
        level_table[level] = level_num
        level_num = level_num + 1
    
    print(level_table)

    for i in range(0, total):
        p.readuntil('Q ')
        Q = p.readline()
        print(Q.decode('utf-8'))
        p.sendline(answer(Q.decode('utf-8'), level_table).encode('utf-8'))
    p.readuntil('flag:')
    p.readline()
    print(p.readline())

auto_anwser(128)
