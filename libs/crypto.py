import base64
import hashlib
import os

import bcrypt


def hash_key(master_key: str) -> str:
    key_bytes = master_key.encode("utf-8")
    hashed = bcrypt.hashpw(key_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_key(master_key: str, stored_hash: str) -> bool:
    key_bytes = master_key.encode("utf-8")
    hash_bytes = stored_hash.encode("utf-8")
    return bcrypt.checkpw(key_bytes, hash_bytes)


def encrypt(password: str, master_key: str) -> str:
    key_bytes = master_key.encode("utf-8")
    pwd_bytes = password.encode("utf-8")

    salt = os.urandom(16)
    key_stream = hashlib.pbkdf2_hmac(
        "sha256",
        key_bytes,
        salt,
        100000,
        len(pwd_bytes),
    )

    encrypted = bytes(a ^ b for a, b in zip(pwd_bytes, key_stream))
    result = base64.b64encode(salt + encrypted).decode("utf-8")

    return result


def decrypt(encrypted_b64: str, master_key: str) -> str:
    key_bytes = master_key.encode("utf-8")

    raw = base64.b64decode(encrypted_b64.encode("utf-8"))
    salt = raw[:16]
    encrypted = raw[16:]

    key_stream = hashlib.pbkdf2_hmac(
        "sha256",
        key_bytes,
        salt,
        100000,
        len(encrypted),
    )

    decrypted = bytes(a ^ b for a, b in zip(encrypted, key_stream))
    return decrypted.decode("utf-8")