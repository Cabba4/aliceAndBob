def diffieHellman(a,b,g,n):
    A = pow(g,a) % n
    B = pow(g,b) % n
    aliceShared = pow(B, a) % n
    bobShared = pow(A, b) % n
    return A, B, aliceShared, bobShared

def main():
    a, b = map(int , input("Enter numbers for a and b: ").split(' '))
    g, n = map(int, input("Enter numbers for g and n: ").split(' '))
    A, B, aliceShared, bobShared = diffieHellman(a,b,g,n)
    print(f"Intermeditate values are {A} and {B}")
    print(f"Shared key is {aliceShared} and {bobShared}") 
    
    
def findNumber(X, Y, g, p):
    a = None
    for i in range(p):
        if pow(g, i, p) == X:
            a = i
            break
    b = None
    for i in range(p):
        if pow(g, i, p) == Y:
            b = i
            break
    return a, b

def shiftCipher(key, ciphertext):
    result = []
    for ch in ciphertext:
        if ch.isalpha():
            c = ord(ch.upper()) - 65
            shifted = (c + key) % 26
            result.append(chr(shifted + 65))
        else:
            result.append(ch)
    return result

# main()

a, b = findNumber(5, 23, 5, 47)
print(a,b)
A, B, alice, bob = diffieHellman(a,b, 5, 47)
print(alice, bob)
cipherText = "Rxu rqob vhfxulwb lv rxu delolwb wr fkdqjh -Mrkq Oloob"
result = shiftCipher(alice, cipherText)
print(' '.join(map(str, result)))