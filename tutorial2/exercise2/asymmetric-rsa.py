import time, base64, os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

def generate_rsa_key_pair(username):
    
    priv_key_file = f"{username}_private_Key.pem"
    pub_key_file = f"{username}_public_Key.pem"
    
    if os.path.exists(priv_key_file) and os.path.exists(pub_key_file):
        print(f"Keys already exist for {username}. Returning existing keys.")
        
        # Read and load the private key
        with open(priv_key_file, "rb") as priv_file:
            private_key = serialization.load_pem_private_key(
                priv_file.read(),
                password=None
            )
        
        # Read and load the public key
        with open(pub_key_file, "rb") as pub_file:
            public_key = serialization.load_pem_public_key(
                pub_file.read()
            )
        
        return private_key, public_key
    
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    
    with open(f"{username}_private_key.pem" , "wb") as priv_file:
        priv_file.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    with open(f"{username}_public_key.pem", "wb") as pub_file:
        pub_file.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    
    return private_key, public_key

def encrypt_text(public_key, plaintext):
    ciphertext = public_key.encrypt(
        plaintext.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

def decrypt_text(private_key, ciphertext):
    decrypted_text = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_text.decode()

def generate_text_file():
    text = "This is a paragraph for encryption testing using asymmetric encryption."
    with open("text_file.txt", "w") as f:
        f.write(text)
    return text

def measure_time(private_key, public_key, plaintext):
    start_encrypt = time.time()
    ciphertext = encrypt_text(public_key, plaintext)
    end_encrypt = time.time()

    start_decrypt = time.time()
    decrypted_text = decrypt_text(private_key, ciphertext)
    end_decrypt = time.time()

    return ciphertext, decrypted_text, end_encrypt - start_encrypt, end_decrypt - start_decrypt

if __name__ == "__main__":

    plaintext = generate_text_file()
    username = input("Enter your name (eg Alice): ")
    private_key, public_key = generate_rsa_key_pair(username)
    ciphertext, decrypted_text, enc_time, dec_time = measure_time(private_key, public_key, plaintext)
    
    print("\nCiphertext: ", base64.b64encode(ciphertext))
    print(f"Decrypted text: {decrypted_text}")
    print(f"Encryption time: {enc_time} seconds")
    print(f"Decryption time: {dec_time} seconds")
    