import random
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

g = 5
p = 37

alice_private = random.randint(1, p-1)
bob_private = random.randint(1, p-1)

A = pow(g,alice_private) % p  # Alice's public key
B = pow(g,bob_private) % p     # Bob's public key

shared_secret_alice = pow(B, alice_private) % p  # Alice's computed secret
shared_secret_bob = pow(A,bob_private) % p       # Bob's computed secret

assert shared_secret_alice == shared_secret_bob

# Hash the shared secret to create a 128-bit key
shared_secret = shared_secret_alice.to_bytes(16, 'big')  # Convert to bytes and use Big endian
key = hashlib.sha256(shared_secret).digest()[:16]  # Get 128 bits (16 bytes)


def encrypt(message, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv, ct_bytes

def decrypt(iv, ct_bytes, key):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct_bytes), AES.block_size)
    return pt.decode()

# Example message to encrypt
dummy_message = "Hello, Bob!"
iv, ct_bytes = encrypt(dummy_message, key)
print("Encrypted:", ct_bytes)

decrypted_message = decrypt(iv, ct_bytes, key)
print("Decrypted:", decrypted_message)

print(f"Alice's Private Key: {alice_private}")
print(f"Alice's Public Key: {A}")
print(f"Bob's Private Key: {bob_private}")
print(f"Bob's Public Key: {B}")
print(f"Shared Secret: {shared_secret_alice}")
print(f"Derived Key: {key.hex()}")
