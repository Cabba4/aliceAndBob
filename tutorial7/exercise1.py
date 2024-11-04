import time
import random
from sympy import nextprime, mod_inverse

def generate_large_prime(bits):
    """ Generate a large prime number with the specified number of bits. """
    p = random.getrandbits(bits)
    return nextprime(p)

def generate_key_parameters(lambda_value):
    """ Generate ElGamal key parameters. """
    P = generate_large_prime(lambda_value)
    Q = (P -1 )// 2  # Simplified for example; ideally, you should check for primality

    G = pow(random.randint(1, P-1), 2, P)

    X = random.randint(1, P - 1) % P
    Y = pow(G, X, P)

    return {
        "P": P,
        "Q": Q,
        "G": G,
        "X": X,
        "Y": Y
    }

def generate_ddh_keys(paramElG, L):
    """ Generate master secret key (msk) and master public key (mpk) for the DDH scheme. """
    P = paramElG["P"]
    msk = []
    mpk = []

    for _ in range(L):
        X = random.randint(1, P - 1)
        msk.append(X)
        mpk_value = pow(paramElG["G"], X, P)
        mpk.append(mpk_value)

    return msk, mpk

def encrypt(mpk, paramElG, x):
    """ Encrypt input x using the DDH scheme. """
    P = paramElG["P"]
    Q = paramElG["Q"]
    
    # Generate r
    r = random.randint(3, Q - 1)  # Ensure 2 < r < Q

    ct0 = pow(paramElG["G"], r, P)
    c = [ct0]

    for i in range(len(x)):
        cti = (pow(mpk[i], r, P) * pow(paramElG["G"], x[i], P)) % P
        c.append(cti)

    return c

def fe_generate_skf(msk, y, Q):
    skf = sum((msk[i] * y[i]) % Q for i in range(len(msk))) % Q
    return skf


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
    lambda_param = 512
    # Initialize parameters and vectors
    x = [1, 2, 3]  # Vector to encrypt
    y = [4, 5, 6]  # Plaintext vector for inner product calculation

    # Measure key generation time
    start_time = time.time()
    paramElG = generate_key_parameters(lambda_param)
    mpk, msk = generate_ddh_keys(paramElG, L=len(x))
    keygen_time = time.time() - start_time

    # Measure encryption time
    start_time = time.time()
    c = encrypt(mpk, paramElG, x)
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