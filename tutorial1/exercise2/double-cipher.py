import time

def caesar_cipher(text, shift):
    text = text.upper()
    result = ""
    
    for char in text:
        if char.isalpha():
            result += chr((ord(char) - 65 + shift) % 26 + 65)
        else:
            result += char
    
    return result

def double_caesar_cipher(text, key1, key2, mode):
    if mode == "encrypt":
        encrypted_text = caesar_cipher(text, key1)
        double_encrypted_text = caesar_cipher(encrypted_text, key2)
        return double_encrypted_text
    elif mode == "decrypt":
        decrypted_text = caesar_cipher(text, -key2)
        double_decrypted_text = caesar_cipher(decrypted_text, -key1)
        return double_decrypted_text

def measure_time(text, key1, key2, mode):
    start_time = time.time()
    output = double_caesar_cipher(text, key1, key2, mode)
    end_time = time.time()

    return output, end_time - start_time

def main():
    # while True:
    #     try:
    #         shift = int(input("Enter the shift number (K): "))
    #         break
    #     except ValueError:
    #         print("Invalid input. Please enter an integer.")
    keys = [13,9]
    
    mode = input("Type 'encrypt' to encrypt or 'decrypt' to decrypt: ").lower()

    if mode not in ['encrypt', 'decrypt']:
        print("Invalid mode. Please type 'encrypt' or 'decrypt'.")
        return
    
    text = input("Enter the text: ")
    
    output, total_time = measure_time(text, keys[0], keys[1], mode)
    print(f"Output: {output}")
    print(f"Time taken: {total_time:.6f} seconds")

if __name__ == "__main__":
    main()