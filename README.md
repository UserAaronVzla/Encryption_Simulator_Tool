Encrypt and create a <file>.calcs file containing:
The SHA-256 hash of the original file in hex.
The base64-encoded ciphertext of the file.
Decrypt the .calcs file back into the original file (verifying the hash matches).
This code uses the cryptography library for encryption/decryption, so ensure it is installed (e.g., pip install cryptography).
-----------------------------------------------------------------------------------------------------------------------------------------------------
## How to Use ##

**For encryption:**

```bash
python encrypt_files.py /path/to/folder [optional_password]

```

**For decryption:**

```bash
python decrypt_files.py /path/to/folder [optional_output_folder] [optional_password]

```

These scripts handle all the requirements:

- The first script creates a .calcs file for each file in the folder
- The .calcs files contain JSON with the file hash and base64-encoded encrypted content
- The second script decrypts the files and verifies the hash matches the original
- Both scripts use proper encryption (Fernet, which is AES-based) and secure key derivation

You'll need to install the required libraries:

```bash
pip install cryptography

```
