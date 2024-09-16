import time, base64, os
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def generate_ecc_key_pair(username):
    priv_key_file = f"{username}_ECC_private_Key.pem"
    pub_key_file = f"{username}_ECC_public_Key.pem"
    
    if os.path.exists(priv_key_file) and os.path.exists(pub_key_file):
        print(f"ECC Keys already exist for {username}. Returning existing keys.")
        
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
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    with open(f"{username}_ECC_Private_Key.pem", "wb") as priv_file:
        priv_file.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open(f"{username}_ECC_Public_Key.pem", "wb") as pub_file:
        pub_file.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    return private_key, public_key
        
def derive_shared_secret(private_key, peer_public_key):
    shared_secret = private_key.exchange(ec.ECDH(), peer_public_key)  # ECDH Key Exchange
    # Derive a symmetric key from the shared secret using HKDF (HMAC-based Key Derivation Function)
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,  # 256-bit AES key
        salt=None,
        info=b'handshake data',
    ).derive(shared_secret)
    return derived_key

# 3. Encrypt Function (Using AES-GCM for encryption)
def encrypt_message(derived_key, plaintext):
    # Generate a random 12-byte initialization vector (IV) for AES-GCM
    iv = os.urandom(12)
    encryptor = Cipher(
        algorithms.AES(derived_key),
        modes.GCM(iv)
    ).encryptor()

    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    return iv, ciphertext, encryptor.tag  # Return IV, Ciphertext, and GCM Tag

# 4. Decrypt Function (Using AES-GCM for decryption)
def decrypt_message(derived_key, iv, ciphertext, tag):
    decryptor = Cipher(
        algorithms.AES(derived_key),
        modes.GCM(iv, tag)
    ).decryptor()

    decrypted_message = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_message.decode()

def measure_time(derived_key_sender, derived_key_receiver, plaintext):
    start_encrypt = time.time()
    iv, ciphertext, encrypt_tag = encrypt_message(derived_key_sender, plaintext)
    end_encrypt = time.time()

    start_decrypt = time.time()
    decrypted_text = decrypt_message(derived_key_receiver, iv, ciphertext, encrypt_tag)
    end_decrypt = time.time()

    return ciphertext, decrypted_text, end_encrypt - start_encrypt, end_decrypt - start_decrypt

# Example usage
if __name__ == "__main__":
    sender, receiver = input("Enter names for sender and receiver: ").split()
    # Generate ECC key pairs for two parties (simulating sender and receiver)
    private_key_sender, public_key_sender = generate_ecc_key_pair(sender)
    private_key_receiver, public_key_receiver = generate_ecc_key_pair(receiver)

    # Derive shared secret for both parties (this should match if keys are valid)
    derived_key_sender = derive_shared_secret(private_key_sender, public_key_receiver)
    derived_key_receiver = derive_shared_secret(private_key_receiver, public_key_sender)

    # Encrypt message with sender's derived key
    message = "This is a paragraph for encryption testing using asymmetric encryption."
    ciphertext, decrypted_text, enc_time, dec_time = measure_time(derived_key_sender, derived_key_receiver, message)
    
    print(f"Ciphertext: {ciphertext}")
    print(f"Decrypted Message: {decrypted_text}")
    print(f"Encryption time: {enc_time} seconds")
    print(f"Decryption time: {dec_time} seconds")