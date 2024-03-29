# Cryptography
- *level 1*: decode base64 data
- *level 2*: decrypt a secret encrypted with *One-Time-Pad* using the key: `msg = ciphertext ^ key` (bit by bit)
- *level 3*: decrypt a secret encrypted with *One-Time-Pad*, we can get the ciphertext of arbitrary message with a reused key: `msg = ciphertext ^ msg2 ^ ciphertext2`, because `key = msg2 ^ ciphertext2`
- *level 4*: decrypt a secret encrypted with AES using the ECB mode
- *level 5*: decrypt a secret encrypted with AES-ECB, where arbitrary data is appended to the secret and the key is reused
    - Each block of the ECB mode is encrypted individually, and the plaintext will be padded to multiple of block size (16 bytes in this challenge)
    - The ciphertext is 64 bytes, try different length of input until the ciphertext becomes 80 bytes (and our input is `X` bytes), then we can know that the last block being encrypted is 16 bytes of `0x10` ([*PKCS#7*](https://en.wikipedia.org/wiki/PKCS_7)), and the plaintext is `64-X` bytes. If we input one more byte, then the last block being encrypted will be the last byte of the plaintext (`L`), plus 15 bytes of `0x0f`, this is where we can get in, we can guess this byte, pad it to 16 bytes, then input it into the oracle, the first block will be `b'<GUESSING_BYTE>\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f'`. Then, we can continue to guess the second-to-last byte, third-to-last byte, ...
- *level 6*: just to perform the steps of *Diffie-Hellman Key Exchange*, after computed the shared key (a number), we need to convert it to bytes, we need to use little endian, and then truncate the key to the size of the secret, then XOR each byte
- *level 7*: convert secret message (bytes) to a number, compute the plaintext number, and convert it back to bytes, use little endian
- *level 8*: we need to calculate `d` and `n` using `p` and `q`, where `n=p*q`, `d=e^-1 mod (p-1)*(q-1)`. In Python, we can directly get the modular inverse of `e` using `pow(e, -1, (p-1)*(q-1))`
- *level 9*: find a small hash collision, where the first 2 bytes is the same as the given value, brute force. For convenience, we enumerate numbers from 1 to 1000000, and convert it to a byte string (byte order does not matter)
- *level 10*: an easy version of proof-of-work
- *level 11*: RSA challenge response, the program will give the key pair and a challenge
- *level 12*: RSA challenge response, we need to provide the key pair, use `RSA.generate(key_length)` to generate the key pair
- *level 13*: we need to use the RSA private key to sign a user certificate. A root certificate and signature is provided. Notice that the RSA signature is performed on the SHA256 digest of the certificate (we can verify that by signing the root certificate, and compare it to the given signature)
- *level 14*: Perform a simplified TLS handshake as server, it combines the DH key exchange, and certificate signing, remember to refer to the code of '/challenge/run', so we can know more details about the verifying process
