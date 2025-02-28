The exercise is demonstrating how to handle files by applying several security-related operations: hashing, encrypting, and encoding. You have a folder containing one or more files (for instance, `file.ext`). For each file in that folder, you must create a new file named `file.ext.calcs` that contains:

1. The file’s cryptographic hash (in hexadecimal format).
2. The file’s *encrypted* contents, which are then Base64-encoded, all embedded in JSON.

An example of the JSON structure for each `file.ext.calcs` might look like:

```
{
  "filehash": "HASHINHEX",
  "filecontents": "SOMEBASE64"
}
```

In other words, you read the original file, compute its hash (e.g., using SHA-256), encrypt the file data (using some agreed-upon cipher), and finally Base64-encode the encrypted result to store it neatly in the JSON. The second part of the exercise asks you to perform the reverse procedure: read the `.calcs` file, decode and decrypt the data, and verify the hash matches the original file—ensuring it has not been tampered with.

The key concepts illustrated here are:

1. **Encoding:** Turning binary data into a textual format (Base64) so it can be stored or transmitted more easily.
2. **Hashing:** Generating a short, fixed-length “fingerprint” of a file, allowing you to detect any changes.
3. **Encryption:** Protecting the file contents so that only those with the right key can recover the original data.
4. **Verification:** After decrypting, confirming the resulting file is valid by comparing the newly computed hash with the stored hash.
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
