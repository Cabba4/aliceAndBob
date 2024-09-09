import time

def caesar_cipher(text, key):
    result = ""
    text = text.upper()

    for char in text:
        if char.isalpha():
            shifted = (ord(char) - 65 + key) % 26 + 65
            result += chr(shifted)
        else:
            result += char
    return result

def decrypt_all_shifts(text):
    start_time = time.time()
    print("Possible Decryptions:\n")
    for key in range(26):
        decrypted_text = caesar_cipher(text, -key)
        print(f"Key {key}: {decrypted_text}")
    end_time = time.time()
    print(f"Time taken for finding correct key and decryption is: {(end_time - start_time):.6f} seconds")

def main():
    text = input("Enter the text to decrypt: ")
    decrypt_all_shifts(text)

if __name__ == "__main__":
    main()
