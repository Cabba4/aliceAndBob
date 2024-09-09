mod_inverse_table = {
    1: 1, 3: 9, 5: 21, 7: 15, 9: 3, 11: 19,
    15: 7, 17: 23, 19: 11, 21: 5, 23: 17, 25: 25
}

def affine_encrypt(text, a, b):
    result = ""
    text = text.upper()
    
    for char in text:
        if char.isalpha():
            x = ord(char) - 65
            encrypted_char = (a * x + b) % 26
            result += chr(encrypted_char + 65)
        else:
            result += char
    return result

def affince_decrypt(text, a, b):
    result = ""
    text = text.upper()
    
    if a in mod_inverse_table:
        a_inv = mod_inverse_table[a]
    else:
        raise ValueError("Inverse not in table for given a")
    
    for char in text:
        if char.isalpha():
            y = ord(char) - 65
            decrypted_text = (a_inv * (y - b)) % 26
            result += chr(decrypted_text + 65)
        else:
            result += char
    return result
    
def main():
    a, b = map(int, input("Input values for a and b: ").split())
    mode = input("Type 'encrypt' to encrypt or 'decrypt' to decrypt: ").lower()
    
    if mode == "encrypt":
        text = input("Enter text to encrypt: ")
        result = affine_encrypt(text, a, b)
    elif mode == "decrypt":
        text = input("Enter text to decrypt: ")
        result = affince_decrypt(text, a, b)
    else:
        print("Invalid mode. Please type 'encrypt' or 'decrypt'.")
        return
    
    print("Output is ", result)

    
if __name__ == "__main__":
    main()
