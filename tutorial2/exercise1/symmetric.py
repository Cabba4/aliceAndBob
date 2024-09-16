import time
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding
import os

def generate_key():
    key = os.urandom(32)
    return key

def encrypt_text(key, plaintext):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()
    
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    return iv, ciphertext

def decrypt_text(key, iv, ciphertext):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    decrypted_padded = decryptor.update(ciphertext) +  decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    decrypted_data = unpadder.update(decrypted_padded) + unpadder.finalize()
    
    return decrypted_data.decode()

def measure_time(key, plaintext):
    start_encrypt = time.time()
    iv, ciphertext = encrypt_text(key, plaintext)
    end_encrypt = time.time()

    start_decrypt = time.time()
    decrypted_text = decrypt_text(key, iv, ciphertext)
    end_decrypt = time.time()

    return iv, ciphertext, decrypted_text, end_encrypt - start_encrypt, end_decrypt - start_decrypt

if __name__ == "__main__":
    key = generate_key()
    plaintext = input("Enter the text to encrypt: ")

    iv, ciphertext, decrypted_text, enc_time, dec_time = measure_time(key, plaintext)

    # Print the results
    print("\nCiphertext:", base64.b64encode(ciphertext).decode())
    print("Decrypted text:", decrypted_text)
    print("Encryption time:", enc_time)
    print("Decryption time:", dec_time)

    # Encode key in base64 for sharing
    print("\nYour key (base64 encoded):", base64.b64encode(key).decode())