from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii

# Load the key from hexadecimal format
hex_key = '8A5DEC68615185AD'  # 16 characters long
key = binascii.unhexlify(hex_key)  # Convert from hex to bytes

# Check the key length
print("Key length (in bytes):", len(key))  # Should be 16 bytes

# Data to be encrypted
data = b'important_info.txt0'

# Create an AES cipher object in ECB mode
cipher = AES.new(key, AES.MODE_ECB)

# Encrypt the data
encrypted_data = cipher.encrypt(pad(data, AES.block_size))

# Convert to hexadecimal format and print
encrypted_hex = encrypted_data.hex()
print("Encrypted data in hex:", encrypted_hex)
