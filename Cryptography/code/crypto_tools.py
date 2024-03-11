#!/usr/bin/env python

import base64

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

def b64_msg_gen(msg_len):
    msg_bytes = bytes([1 for i in range(0, msg_len)])
    msg_b64   = base64.b64encode(msg_bytes)
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
