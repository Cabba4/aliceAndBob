import sqlite3
import os
import hashlib
import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import secrets
from cryptography.hazmat.primitives import padding

# Connect to the SQLite database
conn = sqlite3.connect('./sse_schema.db')
cursor = conn.cursor()

# Create necessary tables if they don't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS sse_csp_keywords (
    csp_keywords_id INTEGER PRIMARY KEY AUTOINCREMENT,
    csp_keywords_address TEXT,
    csp_keyvalue TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS sse_keywords (
    sse_keywords_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sse_keyword TEXT,
    sse_keyword_numfiles INTEGER,
    sse_keyword_numsearch INTEGER
)''')

conn.commit()

# Define folder path for text files
folder_path = './textfiles/'

# Define AES key (use your actual KSKE here)
KSKE_hex = '8da5ed8fdd57592c388e638fb56b82fecf3e563c37897a97893b33b4308f9c91'
KSKE = bytes.fromhex(KSKE_hex)

# AES encryption function with padding
def aes_encrypt(data, key):
    iv = secrets.token_bytes(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad data to ensure it's a multiple of 16 bytes (AES block size)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    return iv + encryptor.update(padded_data) + encryptor.finalize()

# SHA-256 hash function for keywords
def hash_word(word):
    return hashlib.sha256(word.encode()).hexdigest()

# Keyword key computation
def keyword_key(keyword, numsearch):
    combined = f"{keyword}{numsearch}".encode()
    return hashlib.sha256(combined).hexdigest()

# Compute CSP keywords address
def csp_keyword_address(Kw, numfiles):
    combined = f"{Kw}{numfiles}".encode()
    return hashlib.sha256(combined).hexdigest()

# Insert or update keyword in the database
def insert_or_update_keyword(cursor, keyword_hash, numfiles, numsearch):
    # Check if the keyword already exists
    cursor.execute('''
    SELECT sse_keyword_numfiles, sse_keyword_numsearch FROM sse_keywords WHERE sse_keyword = ?
    ''', (keyword_hash,))
    result = cursor.fetchone()
    
    if result:
        # Keyword exists, update numfiles and numsearch
        existing_numfiles, existing_numsearch = result
        new_numfiles = existing_numfiles + numfiles  # Increment numfiles
        # new_numsearch = existing_numsearch + 1       # Increment numsearch
        
        cursor.execute('''
        UPDATE sse_keywords SET sse_keyword_numfiles = ?
        WHERE sse_keyword = ?
        ''', (new_numfiles, keyword_hash))
    else:
        # Keyword doesn't exist, insert new record
        cursor.execute('''
        INSERT INTO sse_keywords (sse_keyword, sse_keyword_numfiles, sse_keyword_numsearch)
        VALUES (?, ?, ?)
        ''', (keyword_hash, numfiles, numsearch))

# Collect all CSP keywords data for later processing
def collect_csp_keywords_data(cursor):
    cursor.execute('''
    SELECT sse_keyword, sse_keyword_numfiles FROM sse_keywords
    ''')
    return cursor.fetchall()

total_size = sum(os.path.getsize(os.path.join(folder_path, f)) for f in os.listdir(folder_path) if f.endswith('.txt'))

# Start execution timer
start_time = time.time()

# First Pass: Process each file to update the sse_keywords table
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)

        # Read the original file to extract keywords
        with open(file_path, 'r') as file:
            words = file.read().split()
        
        numfiles = 1  # Each file contains these keywords at least once

        # Process each word to update the sse_keywords table
        for word in words:
            keyword_hash = hash_word(word)
            insert_or_update_keyword(cursor, keyword_hash, numfiles, 1)

# Second Pass: Encrypt and delete all files
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)

        # Read and encrypt the file
        with open(file_path, 'rb') as file:
            data = file.read()
            encrypted_data = aes_encrypt(data, KSKE)
        
        # Save encrypted file and delete the original
        with open(file_path + '.enc', 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)
        
        os.remove(file_path)  # Delete original .txt file

# Third Pass: Compute and insert CSP keywords based on the populated sse_keywords table
csp_keywords_data = []
for keyword, numfiles in collect_csp_keywords_data(cursor):
    kw = keyword_key(keyword, 1)
    
    # Print parameters before calculating CSP address
    # print(f"Calculating CSP address with keyword: '{kw}' and numfiles: {numfiles}")
    
    address = csp_keyword_address(kw, numfiles)
    encrypted_filename = aes_encrypt(f"{filename}{numfiles}".encode(), KSKE)
    # print(f"Encrypted with aes: {filename} + {numfiles}")
    csp_keywords_data.append((address, encrypted_filename))

# Insert collected CSP keywords data into the database
for address, encrypted_filename in csp_keywords_data:
    cursor.execute('''
    INSERT INTO sse_csp_keywords (csp_keywords_address, csp_keyvalue)
    VALUES (?, ?)
    ''', (address, encrypted_filename))

# Commit all changes
conn.commit()

# End execution timer
end_time = time.time()
execution_time = end_time - start_time

print(f"Total execution time: {execution_time:.2f} seconds")
print(f"Total combined size of test files: {total_size} bytes")

conn.close()
