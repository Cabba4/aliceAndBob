### ================================ Base implementation for Tutorial 9 ================= ###
### ====================== Implements Point addition and Scalar Multiplication ========== ###

from dataclasses import dataclass
from re import I
from random import randint

@dataclass
class PrimeGaloisField:
    prime: int

    def __contains__(self, field_value: "FieldElement") -> bool:
        return 0 <= field_value.value < self.prime


@dataclass
class FieldElement:
    value: int
    field: PrimeGaloisField

    def __repr__(self):
        return "0x" + f"{self.value:x}".zfill(64)
        
    @property
    def P(self) -> int:
        return self.field.prime
    
    def __add__(self, other: "FieldElement") -> "FieldElement":
        return FieldElement(
            value=(self.value + other.value) % self.P,
            field=self.field
        )
    
    def __sub__(self, other: "FieldElement") -> "FieldElement":
        return FieldElement(
            value=(self.value - other.value) % self.P,
            field=self.field
        )

    def __rmul__(self, scalar: int) -> "FieldValue":
        return FieldElement(
            value=(self.value * scalar) % self.P,
            field=self.field
        )

    def __mul__(self, other: "FieldElement") -> "FieldElement":
        return FieldElement(
            value=(self.value * other.value) % self.P,
            field=self.field
        )
        
    def __pow__(self, exponent: int) -> "FieldElement":
        return FieldElement(
            value=pow(self.value, exponent, self.P),
            field=self.field
        )

    def __truediv__(self, other: "FieldElement") -> "FieldElement":
        other_inv = other ** -1
        return self * other_inv


@dataclass
class EllipticCurve:
    a: int
    b: int

    field: PrimeGaloisField

    def __contains__(self, point: "ECCPoint") -> bool:
        x, y = point.x, point.y
        return y ** 2 == x ** 3 + self.a * x + self.b

    def __post_init__(self):
        # Encapsulate the int parameters in FieldElement
        self.a = FieldElement(self.a, self.field)
        self.b = FieldElement(self.b, self.field)

        # Whether the members of the curve parameters are in the field
        if self.a not in self.field or self.b not in self.field:
            raise ValueError

inf = float("inf")

# Representing an ECC Point using the curve equation yˆ2 = xˆ3 + ax + b
@dataclass
class ECCPoint:
    x: int
    y: int

    curve: EllipticCurve

    def __post_init__(self):
        if self.x is None and self.y is None:
            return
        
        # Encapsulate x and y in FieldElement
        self.x = FieldElement(self.x, self.curve.field)
        self.y = FieldElement(self.y, self.curve.field)

        # Ensure the ECCPoint satisfies the curve equation
        if self not in self.curve:
            raise ValueError

    ##  ======== Point addition P1 + P2 = P3 ============== ##
    def __add__(self, other):
        if self == I:                       # I + P2 = P2
            return other

        if other == I:
            return self                     # P1 + I = P1

        if self.x == other.x and self.y == (-1 * other.y):
            return I                        # P + (-P) = I

        if self.x != other.x:
            x1, x2 = self.x, other.x
            y1, y2 = self.y, other.y

            out = (y2 - y1) / (x2 - x1)
            x3 = out ** 2 - x1 - x2
            y3 = out * (x1 - x3) - y1

            return self.__class__(
                x = x3.value,
                y = y3.value,
                curve = curve256k1
            )

        if self == other and self.y == inf:
            return I

        if self == other:
            x1, y1, a = self.x, self.y, self.curve.a

            out = (3 * x1 ** 2 + a) / (2 * y1)
            x3 = out ** 2 - 2 * x1
            y3 = out * (x1 - x3) - y1

            return self.__class__(
                x = x3.value,
                y = y3.value,
                curve = curve256k1
            )

    ##  ======== Scalar Multiplication x * P1 = P1 ============== ##
    def __rmul__(self, scalar: int) -> "ECCPoint":
        inPoint = self
        outPoint = I

        while scalar:
            if scalar & 1:
                outPoint = outPoint + inPoint
            inPoint = inPoint + inPoint
            scalar >>= 1
        return outPoint


# Using the secp256k1 elliptic curve equation: yˆ2 = xˆ3 + 7
# Prime of the finite field
# Necessary parameters for the cryptographic operations
P: int = (
    0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
)

field = PrimeGaloisField(prime=P)

A: int = 0
B: int = 7

curve256k1 = EllipticCurve(
    a=A,
    b=B,
    field=field
)   

I = ECCPoint(x = None, y = None, curve = curve256k1)    # where I is a point at Infinity

# Generator point of the chosen group
G = ECCPoint(
    x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    y = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
    curve = curve256k1
)

# Order of the group generated by G, such that nG = I
q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


## ==================== Start your implementation below this line ============================== ##
## ==================== Feel free to pull the parameters into another file if you wish ========= ##
## ==================== If you notice any bugs, kindly draw our attention to it ================ ##

import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from random import randint

# Define the User class with necessary functions
class User:
    def __init__(self, user_id, curve, generator, x_master):
        """
        Initialize a new user with a unique ID, elliptic curve, and generator point.
        """
        self.user_id = user_id  # Unique identifier (e.g., "Alice")
        self.curve = curve
        self.G = generator

        # Step 1: Generate the user's secret value x_i
        self.x_i = randint(1, q-1)
        
        # Step 2: Compute the user's partial public key P_i = x_i * G
        self.P_i = self.x_i * self.G

        # These will be set later by the KGC
        self.r_i = None
        self.R_i = None
        self.d_i = None
        
        # Random values for U and V
        self.lA = randint(1,q-1)
        self.U = self.lA * self.G
        
        self.hA = randint(1,q-1)
        self.V = self.hA * self.G

        if x_master:
            self.generate_partial_key(x_master)

        self.ski, self.PKi = self.compute_full_keys()

    def __repr__(self):
        # This is the string representation of the User class
        return (f"User({self.user_id}):\n"
                f"  x_i = {self.x_i}\n"
                f"  P_i = ({self.P_i.x.value}, {self.P_i.y.value})\n"
                f"  r_i = {self.r_i}\n"
                f"  R_i = ({self.R_i.x.value}, {self.R_i.y.value})\n"
                f"  d_i = {self.d_i}\n"
                f"  Full Private Key (s_ki) = {self.ski}\n"
                f"Full Public Key (P_Ki) = ({self.PKi[0].x.value}, {self.PKi[0].y.value}), "
                f"({self.PKi[1].x.value}, {self.PKi[1].y.value})")

    def generate_hash(self):
        # Generate a hash based on user's information
        hash_input = str(self.user_id) + str(self.R_i.x.value) + str(self.R_i.y.value) + str(self.P_i.x.value) + str(self.P_i.y.value)
        hash_output = int(hashlib.sha256(hash_input.encode()).hexdigest(), 16)
        return hash_output

    def generate_partial_key(self, x_master):
        # Generate partial key for the user
        self.r_i = randint(1,q-1)
        self.R_i = self.r_i * self.G
        H_val = self.generate_hash()
        self.d_i = (self.r_i + x_master * H_val) % q

    def compute_full_keys(self):
        # Compute full private and public keys for the user
        ski = (self.d_i, self.x_i)
        PKi = (self.R_i, self.P_i)
        return ski, PKi


# Set up the elliptic curve and the generator G (not shown here)
x_master = randint(1, q-1)
Ppub_master = x_master * G

# Create two users: Alice and Bob
alice = User("Alice", curve256k1, G, x_master)
bob = User("Bob", curve256k1, G, x_master)

# Function to compute Y, T, and KAB
def compute_Y_and_T(user1, user2, Ppub_master):
    # Create a string for public key
    pk_str = (str(user2.PKi[0].x.value) + str(user2.PKi[0].y.value) +
              str(user2.PKi[1].x.value) + str(user2.PKi[1].y.value)).encode()
    
    # Create a hash input and compute the hash
    hash_input = (str(user2.user_id) + pk_str.decode()).encode()
    hash_output = int(hashlib.sha256(hash_input).hexdigest(), 16)
    
    # Compute Y and T values
    Y = user2.R_i + (hash_output * Ppub_master) + user2.P_i
    T = user1.hA * Y
    
    # Compute KAB (shared key)
    KAB_input = (str(Y) + str(user1.V) + str(T) + str(user2.user_id) + str(user2.P_i)).encode()
    KAB = int(hashlib.sha256(KAB_input).hexdigest(), 16)
    return Y, T, KAB

# Compute Y, T, and KAB using the above function
Y, T, KAB = compute_Y_and_T(alice, bob, Ppub_master)

# Print the KAB value (shared key)
print(KAB)

# AES encryption setup
# Convert KAB to 32 bytes (AES-256 key size)
key = KAB.to_bytes(32, byteorder='big')

# Generate a random plaintext message
plaintext = "This is a test message for encryption.".encode()

# Pad the plaintext to make it a multiple of AES block size (16 bytes)
padded_plaintext = pad(plaintext, AES.block_size)

# Encrypt the message using AES-256 in CBC mode
cipher = AES.new(key, AES.MODE_CBC)  # CBC mode
ciphertext = cipher.encrypt(padded_plaintext)

# To make the ciphertext and the IV (initialization vector) easily usable
iv = cipher.iv

# Function to encapsulate message
def encpsulate_message(user1, user2, message, T):
    input_data = [user1.U, message, T, user1.user_id, user2.user_id, user1.P_i, user2.P_i]
    hash_input = ''.join(map(str, input_data)).encode()
    hash_output = int(hashlib.sha256(hash_input).hexdigest(), 16)
    
    H = hash_output
    
    W = user1.d_i + user1.lA * H + user1.x_i * H
    phi = (user1.U, user1.V, W)
    return phi

# Encapsulate the message and return the phi
phi = encpsulate_message(alice, bob, ciphertext.hex(), T)

# Function to reverse Y and T
def reverse_Y_and_T(user2, phi):
    Y = (user2.d_i + user2.x_i) * user2.G
    T = (user2.d_i + user2.x_i) * phi[1]
    return Y, T

# Reverse Y and T to check if the values match
Y_return, T_return = reverse_Y_and_T(bob, phi)

# Check if reversed Y and T match the original ones
if Y_return == Y and T_return == T:
    print("Successfully got Y and T back")

# Function to reverse KAB
def reverse_KAB(Y, user1, T, user2):
    input_data = [Y, user1.V, T, user2.user_id, user2.P_i]
    hash_input = ''.join(map(str, input_data)).encode()
    KAB_reverse = int(hashlib.sha256(hash_input).hexdigest(), 16)
    return KAB_reverse

# Reverse KAB to check if we get the same shared key back
KAB_reverse = reverse_KAB(Y_return, alice, T_return, bob)

# Print the reversed KAB
print(KAB_reverse)

# Check if KAB matches the reversed KAB
if KAB == KAB_reverse:
    print("Successfully got KAB back")

# AES decryption setup
# Convert KAB_reverse to 32 bytes (AES-256 key size)
key = KAB_reverse.to_bytes(32, byteorder='big')

# Decrypt the message using AES-256
cipher = AES.new(key, AES.MODE_CBC, iv)  # Use the same IV as for encryption
decrypted_padded_plaintext = cipher.decrypt(ciphertext)

# Unpad the decrypted plaintext
decrypted_plaintext = unpad(decrypted_padded_plaintext, AES.block_size)

# Convert the decrypted plaintext back to a string
print(f"Decrypted Message: {decrypted_plaintext.decode()}")

