
import hashlib
from cryptography.fernet import Fernet
import os

FERNET_KEY = os.getenv("FERNET_KEY")
fernet = Fernet(FERNET_KEY.encode())


# ✅ Aadhaar encryption
def encrypt_aadhaar(aadhaar_number: str) -> str:
    return fernet.encrypt(aadhaar_number.encode()).decode()

# ✅ Aadhaar decryption
def decrypt_aadhaar(encrypted_value: str) -> str:
    return fernet.decrypt(encrypted_value.encode()).decode()

# ✅ Aadhaar hashing (for uniqueness check)
def hash_aadhaar(aadhaar):
    if not aadhaar or not aadhaar.isdigit() or len(aadhaar) != 12:
        return None
    return hashlib.sha256(aadhaar.encode()).hexdigest()



# Encrypt raw bytes (works for any file type)
def encrypt_bytes(data: bytes) -> bytes:
    return fernet.encrypt(data)


def decrypt_bytes(token: bytes) -> bytes:
    return fernet.decrypt(token)


# Keep text helpers if you also want to store plain strings
def encrypt_text(text: str) -> str:
    return encrypt_bytes(text.encode()).decode()


def decrypt_text(encrypted: str) -> str:
    return decrypt_bytes(encrypted.encode()).decode()


