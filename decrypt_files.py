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

def decrypt_file(calcs_file, output_file, password="mysecretpassword"):
    """Decrypt a .calcs file and save the original file"""
    # Read the JSON data
    with open(calcs_file, 'r') as f:
        data = json.load(f)
    
    # Extract the data
    file_hash = data["filehash"]
    encoded_content = data["filecontents"]
    salt = base64.b64decode(data["salt"])
    
    # Generate the key using the password and salt
    key = generate_key(password, salt)
    
    # Decrypt the content
    cipher = Fernet(key)
    encrypted_content = base64.b64decode(encoded_content)
    decrypted_content = cipher.decrypt(encrypted_content)
    
    # Verify the hash
    decrypted_hash = hashlib.sha256(decrypted_content).hexdigest()
    if decrypted_hash != file_hash:
        print(f"Warning: Hash verification failed for {calcs_file}")
        print(f"Original hash: {file_hash}")
        print(f"Decrypted hash: {decrypted_hash}")
    else:
        print(f"Hash verification successful for {calcs_file}")
    
    # Save the decrypted content
    with open(output_file, 'wb') as f:
        f.write(decrypted_content)
    
    return decrypted_hash == file_hash

def process_calcs_files(folder_path, output_folder=None, password="mysecretpassword"):
    """Process all .calcs files in a folder, decrypt them and save the original files"""
    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} does not exist.")
        return
    
    # If output folder is not specified, use the input folder
    if output_folder is None:
        output_folder = os.path.join(folder_path, "decrypted")
    
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    successful = 0
    failed = 0
    
    for filename in os.listdir(folder_path):
        if not filename.endswith('.calcs'):
            continue
        
        calcs_file = os.path.join(folder_path, filename)
        
        # Create the output file name (remove the .calcs extension)
        original_name = filename[:-6]  # Remove '.calcs'
        output_file = os.path.join(output_folder, original_name)
        
        try:
            # Decrypt the file
            result = decrypt_file(calcs_file, output_file, password)
            
            if result:
                successful += 1
                print(f"Successfully decrypted {filename} -> {output_file}")
            else:
                failed += 1
                print(f"Decryption failed for {filename}")
            
        except Exception as e:
            failed += 1
            print(f"Error processing {filename}: {e}")
    
    print(f"\nDecryption complete: {successful} successful, {failed} failed")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python decrypt_files.py <folder_path> [output_folder] [password]")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    output_folder = sys.argv[2] if len(sys.argv) > 2 else None
    password = sys.argv[3] if len(sys.argv) > 3 else "mysecretpassword"
    
    process_calcs_files(folder_path, output_folder, password)
