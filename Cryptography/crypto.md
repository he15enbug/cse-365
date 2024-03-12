# Cryptography
- *level 1*: decode base64 data
- *level 2*: decrypt a secret encrypted with *One-Time-Pad* using the key: `msg = ciphertext ^ key` (bit by bit)
- *level 3*: decrypt a secret encrypted with *One-Time-Pad*, we can get the ciphertext of arbitrary message with a reused key: `msg = ciphertext ^ msg2 ^ ciphertext2`, because `key = msg2 ^ ciphertext2`
- *level 4*: decrypt a secret encrypted with AES using the ECB mode
- *level 5*: decrypt a secret encrypted with AES-ECB, where arbitrary data is appended to the secret and the key is reused
    - Each block of the ECB mode is encrypted individually, and the plaintext will be padded to multiple of block size (16 bytes in this challenge)
    - The ciphertext is 64 bytes, try different length of input until the ciphertext becomes 80 bytes (and our input is `X` bytes), then we can know that the last block being encrypted is 16 bytes of `0x10` ([*PKCS#7*](https://en.wikipedia.org/wiki/PKCS_7)), and the plaintext is `64-X` bytes. If we input one more byte, then the last block being encrypted will be the last byte of the plaintext (`L`), plus 15 bytes of `0x0f`, this is where we can get in, we can guess this byte, pad it to 16 bytes, then input it into the oracle, the first block will be `b'<GUESSING_BYTE>\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f'`. Then, we can continue to guess the second-to-last byte, third-to-last byte, ...
- *level 6*: 