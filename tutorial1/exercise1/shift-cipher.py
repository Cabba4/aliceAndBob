import time

def caesar_cipher(text, shift, mode):
    text = text.upper()
    result = ""
    
    if mode == 'decrypt':
        shift = -shift
    
    for char in text:
        if char.isalpha():
            result += chr((ord(char) - 65 + shift) % 26 + 65)
        else:
            result += char
    
    return result

def measure_time(text, key, mode):
    start_time = time.time()
    output = caesar_cipher(text, key, mode)
    end_time = time.time()

    return output, end_time - start_time

def main():
    while True:
        try:
            shift = int(input("Enter the shift number (K): "))
            break
        except ValueError:
            print("Invalid input. Please enter an integer.")
    
    mode = input("Type 'encrypt' to encrypt or 'decrypt' to decrypt: ").lower()

    if mode not in ['encrypt', 'decrypt']:
        print("Invalid mode. Please type 'encrypt' or 'decrypt'.")
        return
    
    text = input("Enter the text: ")
    
    output, total_time = measure_time(text, shift, mode)
    print(f"Output: {output}")
    print(f"Time taken: {total_time:.6f} seconds")

if __name__ == "__main__":
    main()