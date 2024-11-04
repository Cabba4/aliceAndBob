import os
import random

# Folder path for the generated .txt files
folder_path = 'textfiles/'

# Ensure the folder exists
os.makedirs(folder_path, exist_ok=True)

# List of common English words
word_list = [
    "apple", "banana", "orange", "grape", "pineapple", "strawberry", "blueberry", "mango", "peach", "lemon",
    "cherry", "watermelon", "pear", "plum", "kiwi", "melon", "lime", "coconut", "apricot", "grapefruit",
    "berry", "papaya", "guava", "fig", "date", "pomegranate", "citrus", "nectarine", "raspberry", "blackberry"
]

# Function to generate random text content with one unique word per line
def generate_random_text():
    # Choose a random number of unique words for the file (between 5 and 30)
    num_words = random.randint(5, min(30, len(word_list)))  # Ensure it doesn't exceed the number of unique words
    chosen_words = random.sample(word_list, k=num_words)  # Choose unique words
    
    return '\n'.join(chosen_words)  # Join words with line breaks

# Generate 25 .txt files with varied sizes
for i in range(1, 26):
    file_content = generate_random_text()  # Generate unique words for each file
    
    file_path = os.path.join(folder_path, f'test_file_{i}.txt')
    with open(file_path, 'w') as f:
        f.write(file_content)

print("25 .txt files with random unique words per line have been created.")
