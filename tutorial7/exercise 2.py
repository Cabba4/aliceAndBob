import random
import time
from sympy import isprime  # Ensure modular arithmetic and prime-checking

# Helper function to generate a large prime
def large_prime_generation(bits=512):
    while True:
        prime_candidate = random.getrandbits(bits)
        if isprime(prime_candidate):
            return prime_candidate

# MIFE key generation
def mife_keygen(L):
    P = large_prime_generation()
    Q = (P - 1) // 2
    G = random.randint(2, P - 1)
    msk = [random.randint(1, P - 1) for _ in range(L)]
    mpk = [pow(G, x, P) for x in msk]
    return mpk, msk, P, G, Q

# MIFE encryption
def mife_encrypt(mpk, x, P, G):
    r = random.randint(1, P - 1)
    c = [pow(G, r, P)]
    for i in range(len(x)):
        c_i = (pow(mpk[i], r, P) * pow(G, x[i], P)) % P
        c.append(c_i)
    return c

# MIFE decryption
def mife_decrypt(c, skf, P):
    num = 1
    for i in range(len(c) - 1):
        num = (num * pow(c[i + 1], skf[i], P)) % P
    return num

# Testing MIFE
def test_mife(x, y):
    mpk, msk, P, G, Q = mife_keygen(len(x))
    skf = [random.randint(1, P - 1) for _ in range(len(y))]  # Simplified skf generation
    c = mife_encrypt(mpk, x, P, G)
    result = mife_decrypt(c, skf, P)
    expected_result = sum(xi * yi for xi, yi in zip(x, y))
    return result, expected_result

# ABE Class
class ABE:
    def __init__(self):
        self.attributes = {}

    def keygen(self, attributes):
        secret_key = {}
        for attr in attributes:
            secret_key[attr] = random.randint(1, 100)  # Simple secret generation
        self.attributes[tuple(attributes)] = secret_key
        return secret_key

    def encrypt(self, msg, attributes):
        cipher = []
        for attr in attributes:
            # Encrypt each message element with a random addition
            cipher.append([m + random.randint(1, 10) for m in msg])  # Corrected to keep msg as list
        return cipher

    def decrypt(self, cipher, secret_key):
        result = 0
        for attr, value in zip(secret_key.keys(), cipher):
            if attr in secret_key:
                for v in value:
                    result += v - secret_key[attr]  # Simplified decryption
        return result

# Testing ABE
def test_abe(x, y):
    abe = ABE()
    secret_key = abe.keygen(["attr1", "attr2", "attr3"])
    cipher = abe.encrypt(x, ["attr1", "attr2", "attr3"])
    result = abe.decrypt(cipher, secret_key)
    expected_result = sum(xi * yi for xi, yi in zip(x, y))
    return result, expected_result

# MA-ABE Class
class MultiAuthorityABE:
    def __init__(self):
        self.authorities = {}

    def add_authority(self, authority):
        self.authorities[authority] = {}

    def keygen(self, authority, attributes):
        if authority not in self.authorities:
            raise ValueError("Authority not found!")
        secret_key = {}
        for attr in attributes:
            secret_key[attr] = random.randint(1, 100)
        self.authorities[authority][tuple(attributes)] = secret_key
        return secret_key

    def encrypt(self, msg, attributes):
        cipher = []
        for attr in attributes:
            cipher.append([m + random.randint(1, 10) for m in msg])  # Corrected to keep msg as list
        return cipher

    def decrypt(self, cipher, secret_keys):
        result = 0
        for attr, value in zip(secret_keys[0].keys(), cipher):
            for sk in secret_keys:
                if attr in sk:
                    for v in value:
                        result += v - sk[attr]
        return result

# Testing MA-ABE
def test_ma_abe(x, y):
    ma_abe = MultiAuthorityABE()
    ma_abe.add_authority("Authority1")
    ma_abe.add_authority("Authority2")

    sk1 = ma_abe.keygen("Authority1", ["attr1", "attr2"])
    sk2 = ma_abe.keygen("Authority2", ["attr3"])

    cipher = ma_abe.encrypt(x, ["attr1", "attr2", "attr3"])
    result = ma_abe.decrypt(cipher, [sk1, sk2])
    expected_result = sum(xi * yi for xi, yi in zip(x, y))
    return result, expected_result

# Function to time an experiment
def run_experiment():
    x = [1, 2, 3]
    y = [4, 5, 6]

    # Testing MIFE
    start_time = time.time()
    result_mife, expected_mife = test_mife(x, y)
    mife_time = time.time() - start_time

    # Testing ABE
    start_time = time.time()
    result_abe, expected_abe = test_abe(x, y)
    abe_time = time.time() - start_time

    # Testing MA-ABE
    start_time = time.time()
    result_ma_abe, expected_ma_abe = test_ma_abe(x, y)
    ma_abe_time = time.time() - start_time

    # Print results
    print("\n=== Experiment Results ===")
    print(f"MIFE: Decrypted Result: {result_mife}, Expected: {expected_mife}, Time: {mife_time:.6f} seconds")
    print(f"ABE: Decrypted Result: {result_abe}, Expected: {expected_abe}, Time: {abe_time:.6f} seconds")
    print(f"MA-ABE: Decrypted Result: {result_ma_abe}, Expected: {expected_ma_abe}, Time: {ma_abe_time:.6f} seconds")

# Run the full experiment
run_experiment()
