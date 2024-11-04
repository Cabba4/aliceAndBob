import hashlib
import time
import sqlite3
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import re

# Define your AES key here (the KSKE from the previous script)
KSKE = '8da5ed8fdd57592c388e638fb56b82fecf3e563c37897a97893b33b4308f9c91'  # Replace this with your actual KSKE key from earlier
KSKE = bytes.fromhex(KSKE)

# AES decryption function
def aes_decrypt(data, key):
    iv = data[:16]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(data[16:]) + decryptor.finalize()

# SHA-256 hash function for keywords
def hash_word(word):
    print(f"Hash of {word} is: ", hashlib.sha256(word.encode()).hexdigest())
    return hashlib.sha256(word.encode()).hexdigest()

# Keyword key computation
def keyword_key(keyword, numsearch):
    combined = f"{keyword}{numsearch}".encode()
    return hashlib.sha256(combined).hexdigest()

# Compute csp_keywords_address
def csp_keyword_address(Kw, numfiles):
    combined = f"{Kw}{numfiles}".encode()
    return hashlib.sha256(combined).hexdigest()

# Connect to the database
conn = sqlite3.connect('./sse_schema.db')
cursor = conn.cursor()

# Start search timer
start_time = time.time()

# 1. Ask Bob to enter a word to search for
search_word = input("Enter the word you want to search for: ")

# 2. Create SHA-256 hash of the word to generate the keyword value
keyword_hash = hash_word(search_word)

# 3. Retrieve numfiles and numsearch for the keyword from sse_keywords table
cursor.execute('''
SELECT sse_keyword_numfiles, sse_keyword_numsearch FROM sse_keywords WHERE sse_keyword = ?
''', (keyword_hash,))
result = cursor.fetchone()

if result:
    numfiles, numsearch = result

    # 4. Compute the keyword key Kw
    Kw = keyword_key(keyword_hash, numsearch)
    # print(Kw, numsearch)

    # 5. Compute csp_keywords_address
    csp_address = csp_keyword_address(Kw, numfiles)
    # print(csp_address, numfiles)

    # 6. Retrieve csp_keyvalue using csp_keywords_address
    cursor.execute('''
    SELECT csp_keyvalue FROM sse_csp_keywords WHERE csp_keywords_address = ?
    ''', (csp_address,))
    encrypted_filename_result = cursor.fetchall()

    if encrypted_filename_result:
        # If results are found, decrypt each associated file
        for (encrypted_filename,) in encrypted_filename_result:
            print(encrypted_filename.hex())
            # 7. Decrypt the filename and numfiles from csp_keyvalue
            decrypted_info = aes_decrypt(encrypted_filename, KSKE).decode()
            print("Checking: ", decrypted_info)
            
            decrypted_info = re.sub(r'\\.*$', '', repr(decrypted_info))
            match = re.match(r"(.+?)(\d+)$", decrypted_info)

            if match:
                filename = match.group(1).lstrip("'")   # Extracts 'test_file_1.txt'
                file_num = match.group(2)   # Extracts '1'
                print("Filename:", filename)
                print("File Number:", file_num)

                # 8. Decrypt the file content
                file_path = f'./textfiles/{filename}.enc'
                try:
                    with open(file_path, 'rb') as encrypted_file:
                        encrypted_data = encrypted_file.read()

                    decrypted_data = aes_decrypt(encrypted_data, KSKE).decode()
                    print(f"Decrypted content of {filename}:")
                    print(decrypted_data)
                except FileNotFoundError:
                    print(f"File {file_path} not found.")
            else:
                print("Format error in decrypted_info.")
    else:
        print("No CSP key values found for the specified keyword.")

else:
    print("No files found containing the specified word.")

# Measure end time and calculate search time
end_time = time.time()
search_time = end_time - start_time
print(f"Time taken to search for the keyword: {search_time:.2f} seconds")

# Close database connection
conn.close()
