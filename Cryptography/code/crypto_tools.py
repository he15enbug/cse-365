#!/usr/bin/env python

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Hash.SHA256 import SHA256Hash
import base64
import struct
from pwn import *
import random
import hashlib
import json

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

def DH_read(p, stop_str):
    p.readuntil(stop_str)
    return int(p.readline()[2:-1].decode('utf-8'), 16)

def DH_read_secret(p):
    p.readuntil('secret ciphertext (b64): ')
    return p.readline()[0:-1]

def DH_send_B(p, B):
    p.readuntil('B: ')
    p.sendline(hex(B).encode())

def key_gen(key_len):
    hex_digits = '0123456789abcdef'
    hex_str = ''
    for i in range(0, key_len):
        hex_str = hex_str + random.choice(hex_digits)
    return int(hex_str, 16)

def DH_exchange():
    # initialization
    p = process('/challenge/run')
    p_val = DH_read(p, 'p: ')
    g_val = DH_read(p, 'g: ')
    # print(hex(p_val))

    # key generation
    B_sk = key_gen(len(hex(p_val)) - 2)

    # public key exchange
    A = DH_read(p, 'A: ')
    B = pow(g_val, B_sk, p_val)
    DH_send_B(p, B)
    print(hex(B))

    S = pow(A, B_sk, p_val)
    key = bytes.fromhex(hex(S)[2:])
    print(f'Shared key: {key}\n')
    key = S.to_bytes(256, 'little')
    print(f'Shared key: {key}\n')
    # 
    secret_b64 = DH_read_secret(p)
    secret     = decode_base64(secret_b64)
    print(f'Secret: {secret}\nSecret size: {len(secret)}\n')

    print(bytes([i ^ j for i, j in zip(key[:len(secret)], secret)]).decode('utf-8'))

def decrypt_RSA(e, d, n, secret_val):
    msg_val = pow(secret_val, d, n)
    byte_str = msg_val.to_bytes((msg_val.bit_length() + 7) // 8, byteorder='little')
    return byte_str

def solve_lv_7():
    e = 0x10001
    d = 0x61e847df56a73ec7998f08bbdee5c01ada2cd62e95121e61655b81e1468f0d8c56f121d928b25934199d29f5dc2ac03fe9df8f719a7472ee6c8ea857bf3b18b328be68289e3f724e236919d00701cea2c107feeb985962223c5063f1a48f0f207688a4cda9b103606fcecc0ad83e94d22eb8007e1a10e9102c8fe8775c6fbe92ca4e0fcffc9c164e9673c3c51a328dc686e1d0be2c9ced8f16ccae75d142c914a146e76931fcfe2d415ee70ac505ed2e7037a0aa0564dee9bb9a56bba928b8738b0346615fac6892a4176e6a1764a5abbf71ba0bfd8be9c99d2b654b158cefaa6eebb8d2bb226b0ad5d99e422c6124d3da3d2e906aba930539f11d6351beac41
    n = 0xccec53c84307a1acbd99fc2a2f1b11ed1dc1ddf388b46b2a057803a2ee36521cd0c18b23465722faca60919e76c8601a81c2fc9bbf6d99776d77574de534e9bf63f41a7b4718dbe04261903adf4fd77c44e52edc378154139bf32eb777f5f5237f17e68b0a95c19d433b395febab9a1a73fbad3ee055d6ac107ba8ad3c5cd60973a221da1e59452cf59575f2f8cc6fcf59692787a40b5463aab72b18a354e079b49e38ccae67384d3219e7899973639c996465ead24918ffdd89f9f3f96ac087fee1a2a518f2fe70a6eb46da664714ffc053f7dea8f693fc4be8c70dba5b34cdd08b8c11b56c3dc4994321dc21b678ec38f64427efb8a176944ad0192d854631
    secret_b64 = 'Gp3SOhjbbZ7Q5LDyCEITE02l3bGJZmyRlk9tR9RI5JOcB0ebOAUjYh/YqxH40Y10NntERvnSnLwsHKP+5wbONCdqlnm7OllsIO6wkRtYMofQIyHnMrkUBdX3LPDGzN+ZIOP5/ommpRSBBHPF8ecW4Rh4l5H9FK0Z7zOSs9CLJyxzcyAO6tYGC04HSwZeil5GQLF24rW6W0YmjRWeluICX0NniUdA5oG1BT+3AbVlVSAXYp21fmKAd1rD7PvCasX8JgCxsdHpgsE8T6lYxvM22r3zZgn5QTXISkDGCbT94gsG9DVd0giy+XXvseRqklZ8eeuRi7W4uKDUiO53Hfr9iw=='
    secret = decode_base64(secret_b64)
    secret_val = int.from_bytes(secret, byteorder='little')
    print(decrypt_RSA(e, d, n, secret_val))

def decrypt_RSA_prime_factors(e, p, q, secret_val):
    n = p * q
    d = pow(e, -1, (p - 1) * (q - 1))
    msg_val = pow(secret_val, d, n)
    byte_str = msg_val.to_bytes((msg_val.bit_length() + 7) // 8, byteorder='little')
    return byte_str

def solve_lv_8():
    e = 0x10001
    p = 0xbf676899602b730066ea150f3c2d6e3ca8e280723861feb9256202e4a9d58b6b4073fec4b52fc2d8ba761b8d3abbc075f45ac69cd95b65bb1ff8bc0d86657c7818e7dd062c051d42b412c718ea9026ca180d3f143835223c85a0b9ebc9da15afe7028a595e63116ccf0c1e920ae7189cb64ec28614ce4d9fe66bf3280e0db253
    q = 0xdc8ef9bfe07bd01c1eaf4166b721c5c36dfe12833097ace437fe8c3b040f11e2f4dd91b2e9f6994c91762a4acf10ef131391dfc65fd49bc034528931829197eb24a08d038820d89a3db3957ec6eeb289371e96bf1a68a4cd76130759e2912b7c966934b8246bb306dc9960c504dd120fbce54e9a45395811f83c54e61b89b0ab
    secret_b64 = 'WPX/IVvRC0DLVydOjOvwSrkuH1bt9sS0Ar/0w40tQQQHsovmTqQpyUHDDAlGue/o1Nv1/wcOXZ7+ZgSgwgewmYG//nSr6BiUQ/A5X9unGbd/1oKNd1yljkOZJ756KwZg2/0xq/vpqLI6UzrPDnQ3uYaE/QPXlMij3LP/0NltKFVP/MTTsKnALxupJluViZEDHg3s7Oy8RTpgkkFwIwUYMWACGYmrNFdKVx/kHGEu/GA+ytVDpTu5b1PfdKX1Ebj3Kljxq3WgSaAeiU+Bct4kK8GLAw0kgN4nxWXk78UrE7kRdhiD+XUily4wlp+JMxmwS/oSubxtDKAu0/rn8Hjhaw=='
    secret = decode_base64(secret_b64)
    secret_val = int.from_bytes(secret, byteorder='little')
    print(decrypt_RSA_prime_factors(e, p, q, secret_val))

def collision_2_bytes():
    p = process('/challenge/run')
    p.readuntil('secret sha256[:2] (b64): ')
    two = decode_base64(p.readline()[:-1])
    print(two)

    collision_b64 = ''
    for i in range(0, 1000000):
        msg = i.to_bytes((i.bit_length() + 7) // 8, byteorder='little')
        sha256 = hashlib.sha256()
        sha256.update(msg)
        sha256_hash = sha256.digest()
        pre = sha256_hash[0:2]
        print(f'First 2 bytes of sha256({i}): {pre}')
        if(pre == two):
            collision_b64 = encode_base64(msg)
            print(f'Collision Message (b64): {collision_b64}')
            break
    p.readuntil('collision (b64): ')
    p.sendline(collision_b64)

    p.readuntil('flag: ')
    print(p.readline())

def PoW():
    p = process('/challenge/run')
    p.readuntil('challenge (b64): ')
    challenge = decode_base64(p.readline()[:-1])
    print(challenge)

    collision_b64 = ''
    for i in range(0, 1000000):
        msg = i.to_bytes((i.bit_length() + 7) // 8, byteorder='little')
        sha256 = hashlib.sha256()
        sha256.update(challenge + msg)
        sha256_hash = sha256.digest()
        pre = sha256_hash[0:2]
        print(f'First 2 bytes of sha256(challenge+msg): {pre}')
        if(pre == b'\x00\x00'):
            collision_b64 = encode_base64(msg)
            print(f'Collision Message (b64): {collision_b64}')
            break
    p.readuntil('response (b64): ')
    p.sendline(collision_b64)

    p.readuntil('flag: ')
    print(p.readline())

def p_read_hex_val(p, stop_str):
    p.readuntil(stop_str)
    return int(p.readline()[2:-1], 16)

def p_send_hex_val(p, stop_str, val):
    p.readuntil(stop_str)
    p.sendline(hex(val))

def p_send_b64(p, stop_str, byte_str):
    p.readuntil(stop_str)
    p.sendline(encode_base64(byte_str))

def p_read_b64(p, stop_str):
    p.readuntil(stop_str)
    res_b64 = p.readline()[:-1]
    return decode_base64(res_b64)

def RSA_challenge_response():
    p = process('/challenge/run')
    e = p_read_hex_val(p, 'e: ')
    d = p_read_hex_val(p, 'd: ')
    n = p_read_hex_val(p, 'n: ')
    challenge = p_read_hex_val(p, 'challenge: ')
    response  = decrypt_RSA(e, d, n, challenge, False)
    print(hex(response))
    p_send_hex_val(p, 'response: ', response)

    p.readuntil('flag: ')
    print(p.readline())

def RSA_public_key_gen():
    key = RSA.generate(1024)
    e, d, n = key.e, key.d, key.n
    p = process('/challenge/run')
    p_send_hex_val(p, 'e: ', e)
    p_send_hex_val(p, 'n: ', n)
    challenge = p_read_hex_val(p, 'challenge: ')
    response  = decrypt_RSA(e, d, n, challenge, False)
    print(hex(response))
    p_send_hex_val(p, 'response: ', response)

    secret_val = int.from_bytes(p_read_b64('secret ciphertext (b64): '), 'little')

    print(decrypt_RSA(e, d, n, secret_val))

def sign(e, d, n, cert_bytes, return_bytes = True):
    sha256 = hashlib.sha256()
    sha256.update(cert_bytes)
    cert_val = int.from_bytes(sha256.digest(), 'little')
    sig_val = pow(cert_val, d, n)
    if(return_bytes):
        return sig_val.to_bytes((sig_val.bit_length() + 7) // 8, byteorder='little')
    return sig_val

def sign_cert():
    p = process('/challenge/run')
    d = p_read_hex_val(p, 'root key d: ')
    root_cert = p_read_b64(p, 'root certificate (b64): ')
    root_cert_sig = p_read_b64(p, 'root certificate signature (b64): ')

    cert_str = root_cert.decode('utf-8')  # Decode byte string to regular string
    root_cert_json = json.loads(cert_str)
    n = root_cert_json['key']['n']
    e = root_cert_json['key']['e']
    
    user_cert_json = root_cert_json
    key = RSA.generate(1024)
    user_e, user_d, user_n = key.e, key.d, key.n
    user_cert_json['name'] = 'user'
    user_cert_json['key']['n'] = user_n
    user_cert_json['key']['e'] = user_e

    user_cert_bytes = json.dumps(user_cert_json).encode('utf-8')
    user_cert_sig   = sign(e, d, n, user_cert_bytes)

    p_send_b64(p, 'user certificate (b64): ', user_cert_bytes)
    p_send_b64(p, 'user certificate signature (b64): ', user_cert_sig)

    secret = p_read_b64(p, 'secret ciphertext (b64): ')
    secret_val = int.from_bytes(secret, byteorder='little')
    print(decrypt_RSA(user_e, user_d, user_n, secret_val).decode('utf-8'))

def p_read_str(p, stop_str):
    p.readuntil(stop_str)
    return p.readline()[:-1]

def TLS_handshake():
    p = process('/challenge/run')
    p_val = DH_read(p, 'p: ')
    g_val = DH_read(p, 'g: ')
    
    d = p_read_hex_val(p, 'root key d: ')
    root_cert = p_read_b64(p, 'root certificate (b64): ')
    root_cert_sig = p_read_b64(p, 'root certificate signature (b64): ')

    cert_str = root_cert.decode('utf-8')
    root_cert_json = json.loads(cert_str)
    n = root_cert_json['key']['n']
    e = root_cert_json['key']['e']

    B_sk = key_gen(len(hex(p_val)) - 2)
    user_name = p_read_str(p, 'name: ').decode('utf-8')
    A = DH_read(p, 'A: ')
    B = pow(g_val, B_sk, p_val)
    DH_send_B(p, B)

    S = pow(A, B_sk, p_val)
    key = SHA256Hash(S.to_bytes(256, "little")).digest()[:16] # use the same key as in /challenge/run
    cipher_encrypt = AES.new(key=key, mode=AES.MODE_CBC, iv=b"\0"*16)
    cipher_decrypt = AES.new(key=key, mode=AES.MODE_CBC, iv=b"\0"*16)

    user_cert_json = root_cert_json
    key = RSA.generate(1024)
    user_e, user_d, user_n = key.e, key.d, key.n
    user_cert_json['name'] = user_name
    user_cert_json['key']['n'] = user_n
    user_cert_json['key']['e'] = user_e
    user_cert_json['signer']   = 'root'

    user_cert_bytes = json.dumps(user_cert_json).encode('utf-8')
    user_cert_sig   = sign(e, d, n, user_cert_bytes)
    user_signature_data = (
        user_name.encode().ljust(256, b"\0") +
        A.to_bytes(256, "little") +
        B.to_bytes(256, "little")
    )
    user_sig        = sign(user_e, user_d, user_n, user_signature_data)

    user_cert_enc     = cipher_encrypt.encrypt(pad_pkcs7(user_cert_bytes))
    user_cert_sig_enc = cipher_encrypt.encrypt(pad_pkcs7(user_cert_sig))
    user_sig_enc      = cipher_encrypt.encrypt(pad_pkcs7(user_sig))

    p_send_b64(p, 'user certificate (b64): ', user_cert_enc)
    p_send_b64(p, 'user certificate signature (b64): ', user_cert_sig_enc)
    p_send_b64(p, 'user signature (b64): ', user_sig_enc)

    secret = p_read_b64(p, 'secret ciphertext (b64): ')
    print(cipher_decrypt.decrypt(secret))
