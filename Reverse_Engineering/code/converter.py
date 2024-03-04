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

def SWAP(brray, idx1, idx2):
    tmp = brray[idx1]
    brray[idx1] = brray[idx2]
    brray[idx2] = tmp
    return brray

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

def XOR_by_MOD(hex_list, xors):
    len1 = len(hex_list)
    mod = len(xors)
    for i in range(0, len1):
        hex_list[i] = hex_list[i] ^ xors[i % mod]
    print_array_hex(hex_list)
    return hex_list

########################## For babyrev_level7.1 ##########################
def babyrev_level7_1(hex_string_with_spaces):
    exp_res = byte_array(hex_string_with_spaces)
    res = XOR_by_MOD(exp_res, [0x15, 0x2e, 0xd, 0x77])
    res = XOR(res, [0xa3])
    res = SWAP(res, 9, 25)

    hex4printf(array2hex(res))

# babyrev_level7_1('d7 ec cf b3 d0 e8 cb b0 dd e7 c4 bc de e5 c6 ba db ff de a3 c0 f8 d4 ad ce f5')
##########################################################################

########################## For babyrev_level8.0 ##########################
def babyrev_level8_0(hex_string_with_spaces):
    exp_res = byte_array(hex_string_with_spaces)
    res = REV(exp_res)
    res = SWAP(res, 5, 8)
    res = REV(res)
    res = SWAP(res, 7, 27)
    res = SWAP(res, 18, 30)
    res = SWAP(res, 32, 33)
    hex4printf(array2hex(res))

# babyrev_level8_0('61 61 61 61 62 62 63 63 63 63 64 64 64 66 66 67 68 68 69 6b 6b 6c 6d 6e 6e 70 70 71 71 71 72 72 73 73 75 76 78 79 7a')
##########################################################################

########################## For babyrev_level8.1 ##########################
def babyrev_level8_1(hex_string_with_spaces):
    res = byte_array(hex_string_with_spaces)
    res = XOR_by_MOD(res, [0x27, 0x65, 0xf3, 0x68, 0x1f, 0x9a, 0x80])
    res = SWAP(res, 4, 10)
    res = REV(res)
    res = SWAP(res, 12, 23)
    res = XOR_by_MOD(res, [0xe7, 0x16, 0x9f, 0x0e, 0x91, 0x33])
    res = XOR_by_MOD(res, [0x9, 0x8b, 0x58, 0x38])
    hex4printf(array2hex(res))

# babyrev_level8_1('d8 9a 0f 91 f4 63 77 c8 88 18 91 bc 47 5c fc b3 20 a4 a0 25 38 8b 84 53 e4 96 1e f1 4d 38 a2 27 50 d6 c1')
##########################################################################