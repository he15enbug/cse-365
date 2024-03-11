# Cryptography
- *level 1*: decode base64 data
- *level 2*: decrypt a secret encrypted with *One-Time-Pad* using the key: `msg = ciphertext ^ key` (bit by bit)
- *level 3*: decrypt a secret encrypted with *One-Time-Pad*, we can get the ciphertext of arbitrary message with a reused key: `msg = ciphertext ^ msg2 ^ ciphertext2`, because `key = msg2 ^ ciphertext2`
- *level 4*: decrypt a secret encrypted with AES using the ECB mode
- *level 5*: decrypt a secret encrypted with AES-ECB, where arbitrary data is appended to the secret and the key is reused