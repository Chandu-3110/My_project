import random
import string

def generate_key():
    # 8-character hex key like 7b392b7c
    return ''.join(random.choice('0123456789abcdef') for _ in range(8))

key = generate_key()

print("Generated Decryption Key:")
print(key)

# optional: save key
with open("key.txt", "w") as f:
    f.write(key)

print("Key saved to key.txt")