import os
import base64
import hashlib
import json
import sys
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_key(password, salt):
    """Generate a key from password and salt using PBKDF2"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def encrypt_file(file_path, password="mysecretpassword"):
    """Encrypt a file and return its hash and base64 encoded content"""
    # Read the file content
    with open(file_path, 'rb') as file:
        file_content = file.read()
    
    # Generate a hash of the file
    file_hash = hashlib.sha256(file_content).hexdigest()
    
    # Generate a salt
    salt = os.urandom(16)
    
    # Generate a key from the password and salt
    key = generate_key(password, salt)
    
    # Encrypt the file content
    cipher = Fernet(key)
    encrypted_content = cipher.encrypt(file_content)
    
    # Base64 encode the encrypted content for storage
    encoded_content = base64.b64encode(encrypted_content).decode()
    
    # Create a dictionary with the file hash, encrypted content, and salt
    result = {
        "filehash": file_hash,
        "filecontents": encoded_content,
        "salt": base64.b64encode(salt).decode()  # Store salt for decryption
    }
    
    return result

def process_folder(folder_path, password="mysecretpassword"):
    """Process all files in a folder, encrypt them and save results"""
    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} does not exist.")
        return
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Skip directories and non-file items
        if not os.path.isfile(file_path):
            continue
        
        # Skip .calcs files (in case it run the script multiple times)
        if filename.endswith('.calcs'):
            continue
        
        try:
            # Encrypt the file
            result = encrypt_file(file_path, password)
            
            # Save the result in a .calcs file
            output_file = f"{file_path}.calcs"
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            
            print(f"Processed {filename} -> {output_file}")
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python encrypt_files.py <folder_path> [password]")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    password = sys.argv[2] if len(sys.argv) > 2 else "mysecretpassword"
    
    process_folder(folder_path, password)
