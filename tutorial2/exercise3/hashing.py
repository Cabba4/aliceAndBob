import hashlib

def compute_sha256(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as file:
        while chunk := file.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def verify_integrity(file_path, expected_digest):
    return compute_sha256(file_path) == expected_digest

def generate_text_file():
    text = "This is a paragraph for checking hash functions!!"
    with open("sample.txt", "w") as f:
        f.write(text)
    return text
# Example usage

if __name__ == "__main__":
    generate_text_file()
    file_path = "sample.txt"
    print("File in use is - ", file_path)
    with open(file_path, "r") as file:
        print(file.readline())
    digest = compute_sha256(file_path)
    print(f"SHA256 digest for text is: {digest}")
    
    received_digest = input("Provide expected hashdigest: ")  # Replace with the actual digest
    is_valid = verify_integrity(file_path, received_digest)
    print(f"File integrity verified: {is_valid}")