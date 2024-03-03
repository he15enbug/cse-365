#!/usr/bin/env python

def print_array_hex(arr):
    for num in arr:
        print(format(num, '02X'), end=' ')
    print()

def hex4printf(hex_string):
    byte_string = "".join([r'\x' + hex_string[i:i+2] for i in range(0, len(hex_string), 2)])
    print(byte_string)

def array2hex(arr):
    hex_str = ''.join(hex(num)[2:].zfill(2) for num in arr)
    return hex_str.upper()

def byte_array(hex_string_with_spaces):
    hex_list = [int(x, 16) for x in hex_string_with_spaces.split()]
    print_array_hex(hex_list)
    return hex_list

def hex_number(brray):
    hex_num = "0x" + "".join(["{:02x}".format(num) for num in brray])
    print(hex_num)

def XOR(hex_list1, hex_list2):
    len1 = len(hex_list1)
    len2 = len(hex_list2)
    i = 0
    j = 0
    ret = []
    while(i < len1):
        if(j >= len2):
            j -= len2
        ret.append(hex_list1[i] ^ hex_list2[j])
        i = i + 1
        j = j + 1
    print_array_hex(ret)
    return ret

def REV(hex_list):
    len1 = len(hex_list)
    ret = []
    for i in range(0, len1):
        ret.append(hex_list[len1 - 1 - i])
    print_array_hex(ret)
    return ret

########################## For babyrev_level7.1 ##########################
def mod_with_condition(hex_list):
    xors = [0x15, 0x2e, 0xd, 0x77]
    len1 = len(hex_list)
    for i in range(0, len1):
        hex_list[i] = hex_list[i] ^ xors[i % 4]
    print_array_hex(hex_list)
    return hex_list

def babyrev_level7_1(hex_string_with_spaces):
    exp_res = byte_array(hex_string_with_spaces)
    res_1 = mod_with_condition(exp_res)
    res_2 = XOR(res_1, [0xa3])
    tmp = res_2[9]
    res_2[9] = res_2[25]
    res_2[25] = tmp

    hex4printf(array2hex(res_2))

# babyrev_level7_1('d7 ec cf b3 d0 e8 cb b0 dd e7 c4 bc de e5 c6 ba db ff de a3 c0 f8 d4 ad ce f5')
##########################################################################