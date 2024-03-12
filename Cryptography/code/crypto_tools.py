#!/usr/bin/env python

from Crypto.Cipher import AES
import base64
import struct
from pwn import *

def encode_base64(byte_str, printout = False):
    base64_str = base64.b64encode(byte_str)
    if(printout):
        print(base64_str)
    return base64_str

def decode_base64(base64_str, printable = False):
    decoded_bytes = base64.b64decode(base64_str)
    if(printable):
        print(decoded_bytes.decode('utf-8'))
    return decoded_bytes

def solve_lv_1():
    decode_base64('cHduLmNvbGxlZ2V7dzNlSFdEYS1iOHg2NzNHT3BSbkVrUHVoUVFKLmROek56TURMMmt6TTRReld9Cg==', True)

def decrypt_OTP(key_b64, ciphertext_b64):
    key        = decode_base64(key_b64)
    ciphertext = decode_base64(ciphertext_b64)
    plaintext  = bytes([a ^ b for a, b in zip(key, ciphertext)])
    print(plaintext.decode('utf-8'))
    return plaintext

def solve_lv_2():
    key_b64        = 'T5WiKBI65dyLFt/svyewOmaz+HmU8drw3qO0jrMse7FXS0I37yN/BW+Yv+kPA54uN47BrIGjI+9MTA=='
    ciphertext_b64 = 'P+LMBnFVibDucbqX+kWDfQPQ1Uvlieqym9re9+pnEOg8ehZ+o2sHKwvKxad1TtpiBeW74bXyWbgxRg=='
    decrypt_OTP(key_b64, ciphertext_b64)

def b64_msg_gen(msg_len, printout = False):
    msg_bytes = bytes([1 for i in range(0, msg_len)])
    msg_b64   = base64.b64encode(msg_bytes)
    if(printout):
        print(msg_b64)
    return msg_b64

def decrypt_OTP_key_reused(msg_b64, ctext_b64, target_ctext_b64):
    msg          = decode_base64(msg_b64)
    ctext        = decode_base64(ctext_b64)
    target_ctext = decode_base64(target_ctext_b64)
    target_msg   = bytes([i ^ j ^ k for i, j, k in zip(msg, ctext, target_ctext)])
    print(target_msg.decode('utf-8'))
    return target_msg

def solve_lv_3():
    target_ctext_b64 = '/ioVPxdRjii6WfUvx0IfPNeblLXhjlPpkPB82JVKXp9X5dg59dj8I9KNux1UIGVfkGfjgDSgpH9Rlw=='
    target_len       = len(decode_base64(target_ctext_b64))
    msg_b64          = b64_msg_gen(target_len)
    # input msg_b64 to the /challenge/run program to get ctext_b64
    ctext_b64        = 'j1x6EHU/40XeP5FVlxAreITb1vin0BC345o5m6Q5ct0YlZ8BoZyZDLfawFIvbCASow2YzAHw3yktnA=='
    decrypt_OTP_key_reused(msg_b64, ctext_b64, target_ctext_b64)

def decrypt_AES_ECB(key_b64, ctext_b64):
    key       = decode_base64(key_b64)
    ctext     = decode_base64(ctext_b64)
    cipher    = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(ctext)
    print(plaintext.decode('utf-8'))

def solve_lv_4():
    key_b64   = 'txQUTVOylI3xW9/LWBQ01A=='
    ctext_b64 = 'stYGLowKEcX4UOpP3CVYwe/eaUBqg0HHKft7DaTf4nBGSTYkl/Q74RLFEvm5JdBzkEwY3fLiPL6/4woVpvK/aw=='
    decrypt_AES_ECB(key_b64, ctext_b64)

def pad_pkcs7(byte_str):
    len_byte = len(byte_str)
    len_pad  = 16 - (len_byte % 16)
    # print(len_pad)
    for i in range(0, len_pad):
        byte_str = byte_str + struct.pack('B', len_pad)
    encode_base64(byte_str)
    return byte_str

def p_send(p, msg):
    p.readuntil('plaintext prefix (b64): ')
    p.sendline(msg)

def p_read(p):
    p.readuntil('ciphertext (b64): ')
    res_b64 = p.readline()[:-1]
    p.readuntil('ciphertext (hex): ')
    res_hex = p.readline()[:-1].split()
    return res_b64, res_hex

def solve_lv_5():
    p = process('/challenge/run')

    p.readuntil('secret ciphertext (b64): ')
    CT_B64    = p.readline()[:-1] # drop the last byte '\n'
    p.readuntil('secret ciphertext (hex): ')
    CT_BLOCKS = p.readline()[:-1].split()
    N_BLOCK = len(CT_BLOCKS)
    LEN_HEX = len(decode_base64(CT_B64))
    print(CT_B64)
    print(CT_BLOCKS)

    # try different length of prefix to figure out the length of padding
    print('\n************** Finding the length of plaintext... **************\n')
    LEN_PADDING = 0
    LEN_PLAIN   = 0
    for i in range(0, 16):
        p_send(p, b64_msg_gen(i))
        _, res_hex = p_read(p)
        # At this point, the last new block is full of paddings
        if(len(res_hex) > N_BLOCK):
            LEN_PADDING = i
            LEN_PLAIN   = LEN_HEX - i
            print(f'plaintext length: {LEN_PLAIN}\npadding length: {LEN_PADDING}')
            break
    print('\n***************************************************************************\n')

    print('\n***************** Guessing the plaintext byte by byte... ******************\n')

    PLAINTEXT = b''

    for i in range(0, LEN_PLAIN):
        len_pre = i + LEN_PADDING + 1
        pre_b64 = b64_msg_gen(len_pre)
        p_send(p, pre_b64)
        _, hex_blocks = p_read(p)
        # the current byte we are guessing is the first byte in the block of index NBLOCK
        target_block  = hex_blocks[N_BLOCK]

        for b in range(0, 256):
            first_block = struct.pack('B', b) + PLAINTEXT
            if i < 15:
                first_block = pad_pkcs7(first_block)
            first_block = encode_base64(first_block[0: 16])
            p_send(p, first_block)
            _, hex_blocks = p_read(p)
            if(hex_blocks[0] == target_block):
                PLAINTEXT = struct.pack('B', b) + PLAINTEXT
                print(f'The {i}-th from the end is {b}')
                print(PLAINTEXT)
                break

        print(f'Plaintext: {PLAINTEXT}')

    print('\n*****************************************************************\n')
