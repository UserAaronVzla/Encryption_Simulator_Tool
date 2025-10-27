# Ransomware Technique Simulator (Educational Red-Team Lab)
I built this project on my **Windows** workstation to practice the **red-team mechanics** common in ransomware workflows—file discovery, encryption, metadata recording, and full restoration—while strengthening my Python skills. The tool operates only on **folders I explicitly select** in my lab.


## Objective
My goal is to emulate the technical steps a typical ransomware operator performs on disk, **without** any persistence, lateral movement, or network/C2, so I can:

- Understand the crypto and file-handling details end-to-end.
- Reproduce realistic artifacts for blue-team validation and detection tuning.
- Keep the workflow fully reversible for safe demonstrations.


### Scope & Ethics
- **Environment:** My local, controlled **Windows** lab.
- **Data:** Only data and directories I own and intentionally select.
- **Non-goals:** No self-propagation, no privilege abuse, no registry persistence, no scheduled tasks, no external communication.

This repository is for **education and professional practice only.**


## How It Works
For each input file in a target folder, I generate a sibling `*.calcs` file containing:

- `filehash`: SHA-256 of the original (hex).
- `filecontents`: the original file’s bytes, **encrypted** with Fernet (AES + HMAC, AEAD) and then **Base64-encoded**.

On decryption, I reconstruct the file and verify its integrity by recomputing the SHA-256 and comparing it to `filehash`.


### Cryptography & Key Management
- **Cipher**: Fernet (AES + HMAC; authenticated encryption).
- **KDF**: PBKDF2-HMAC-SHA256 derived from a user password.
- **Salt**: Random salt stored in the `.calcs` payload so the password is the only secret needed at restore time.
- **Integrity**: AEAD (Fernet) plus an explicit SHA-256 verification step after decryption.

## Quick Start (Windows)
Create a virtual environment (recommended) and install dependencies:

```PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Encrypt a folder
```PowerShell
python encrypt_files.py C:\Path\To\LabFolder [optional_password]
```
- Produces `file.ext.calcs` for each file.
- Originals remain intact (no destructive behavior by default).

### Decrypt and verify
```PowerShell
python decrypt_files.py C:\Path\To\LabFolder [optional_output_folder] [optional_password]
```
- Restores files from their `*.calcs` counterparts.
- Verifies integrity by recomputing SHA-256 and comparing with `filehash`.

> If I omit the password, the scripts can prompt me securely.


## Data Format (`*.calcs`)
Each `.calcs` is JSON. Example:

```JSON
{
  "filehash": "HASHINHEX",
  "filecontents": "SOMEBASE64",
  "salt": "BASE64_SALT",
  "kdf": "PBKDF2-HMAC-SHA256",
  "kdf_iterations": 200000
}
```
> (If iterations differ in your environment, the script’s value is authoritative.)


### Operational Notes
- **Performance**: CPU-bound due to KDF + crypto; I keep it single-process for clarity.
- **Safety**: All operations are local; no network calls or persistence.
- **Restorability**: `.calcs` bundle includes everything needed except the password.


### Troubleshooting
- **InvalidToken** during decryption: wrong password or corrupted `.calcs`.
- **Hash mismatch** after restore: indicates tampering or truncation—re-run with the correct password and intact `.calcs`.
- **UnicodeDecodeError**: expected if you try to open binary data as text—use the decryptor.


## Potential Extensions (Roadmap)
- `--include/--exclude` globbing for file selection.
- `--wipe` (delete originals after successful `.calcs` creation; for stricter simulations only).
- `--workers N` for parallel encryption.
- `--keyfile` mode to avoid passwords (generate/load a symmetric key).
- Progress bar and structured logging.
- Unit tests for round-trip and negative cases.


## License
Educational and professional practice only. Choose a permissive license (e.g., MIT) and retain this intent in forks.


## Social
- 📧 A.eskenazicohen@gmail.com
- 💼 [LinkedIn](https://linkedin.com/in/aaron-eskenazi-vzla)
- 🐈‍⬛ [GitHub](https://github.com/UserAaronVzla)










