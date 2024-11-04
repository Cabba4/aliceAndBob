from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Your saved AES key (replace with the actual KSKE)
KSKE = '8da5ed8fdd57592c388e638fb56b82fecf3e563c37897a97893b33b4308f9c91'
KSKE = bytes.fromhex(KSKE)

# AES decryption function
def aes_decrypt(data, key):
    iv = data[:16]  # Extract the IV, which is the first 16 bytes
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(data[16:]) + decryptor.finalize()

# Specify the path to the encrypted file
encrypted_file_path = './textfiles/test_file_1.txt.enc'

# Read and decrypt the file
with open(encrypted_file_path, 'rb') as encrypted_file:
    encrypted_data = encrypted_file.read()

decrypted_data = aes_decrypt(encrypted_data, KSKE).decode()

# Print the decrypted content
print("Decrypted content:")
print(decrypted_data)
