import time
import random
from sympy import isprime, mod_inverse  # Ensure modular arithmetic and prime-checking


# Function to generate a large prime for P (Example: 512 bits)
def large_prime_generation(bits=512):
    while True:
        prime_candidate = random.getrandbits(bits)
        if isprime(prime_candidate):
            return prime_candidate


# ElGamal KeyGen Algorithm
def elgamal_keygen(lambda_param):
    # Step 1: Generate prime P, Q, and generator G
    P = large_prime_generation(lambda_param)
    Q = (P - 1) // 2
    G = random.randint(2, P - 1) ** 2 % P

    # Step 2: Generate private (X) and public key (Y)
    X = random.randint(1, P - 1)
    Y = pow(G, X, P)

    return {'P': P, 'Q': Q, 'G': G, 'X': X, 'Y': Y}


# FE KeyGen for DDH to create master keys mpk and msk
def fe_keygen_ddh(paramElG, L):
    P, G, Q = paramElG['P'], paramElG['G'], paramElG['Q']
    msk = []
    mpk = []
    for _ in range(L):
        X = random.randint(1, P - 1)
        msk.append(X)
        mpk.append(pow(G, X, P))
    return mpk, msk


# FE Encryption for vector x
def fe_encrypt(mpk, paramElG, x):
    P, G, Q = paramElG['P'], paramElG['G'], paramElG['Q']
    r = random.randint(2, Q)
    ct0 = pow(G, r, P)
    c = [ct0]

    # Encrypt each element of x
    for i, xi in enumerate(x):
        cti = (pow(mpk[i], r, P) * pow(G, xi, P)) % P
        c.append(cti)
    return c


# Generate functional encryption key (skf) for inner-product
def fe_generate_skf(msk, y, Q):
    skf = sum((msk[i] * y[i]) % Q for i in range(len(msk))) % Q
    return skf


# FE Decryption with skf and vector y
def fe_decrypt(skf, paramElG, c, y):
    P = paramElG['P']
    num = 1
    for i, yi in enumerate(y):
        num = (num * pow(c[i + 1], yi, P)) % P

    d = pow(c[0], skf, P)
    r = (num * mod_inverse(d, P)) % P
    return r


# Test with specific vectors x = [1, 2, 3] and y = [4, 5, 6] with timing
def test_fe_scheme():
    # Initialize parameters and vectors
    x = [1, 2, 3]  # Vector to encrypt
    y = [4, 5, 6]  # Plaintext vector for inner product calculation

    # Measure key generation time
    start_time = time.time()
    paramElG = elgamal_keygen(lambda_param=512)
    mpk, msk = fe_keygen_ddh(paramElG, L=len(x))
    keygen_time = time.time() - start_time

    # Measure encryption time
    start_time = time.time()
    c = fe_encrypt(mpk, paramElG, x)
    encryption_time = time.time() - start_time

    # Generate functional encryption key for inner-product
    start_time = time.time()
    skf = fe_generate_skf(msk, y, paramElG['Q'])
    skf_time = time.time() - start_time

    # Measure decryption time
    start_time = time.time()
    result = fe_decrypt(skf, paramElG, c, y)
    decryption_time = time.time() - start_time

    # Expected result (manual inner product of x and y)
    expected_result = sum(xi * yi for xi, yi in zip(x, y))

    # Print results and timing
    print("Decrypted Result:", result)
    print("Expected Inner Product:", expected_result)
    print(f"Key Generation Time: {keygen_time:.6f} seconds")
    print(f"Encryption Time: {encryption_time:.6f} seconds")
    print(f"Functional Key Generation Time: {skf_time:.6f} seconds")
    print(f"Decryption Time: {decryption_time:.6f} seconds")


# Run test
test_fe_scheme()
