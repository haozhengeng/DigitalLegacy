from cryptography.fernet import Fernet
import base64
import hashlib
import os

from app.config import settings


def _derive_key(secret: str) -> bytes:
    key = hashlib.sha256(secret.encode()).digest()
    return base64.urlsafe_b64encode(key)


def encrypt_content(plaintext: str, key_secret: str | None = None) -> str:
    secret = key_secret or settings.SECRET_KEY
    key = _derive_key(secret)
    f = Fernet(key)
    return f.encrypt(plaintext.encode()).decode()


def decrypt_content(ciphertext: str, key_secret: str | None = None) -> str:
    secret = key_secret or settings.SECRET_KEY
    key = _derive_key(secret)
    f = Fernet(key)
    return f.decrypt(ciphertext.encode()).decode()


def generate_key_fragment() -> tuple[str, str]:
    key = Fernet.generate_key()
    f = Fernet(key)
    half = len(key) // 2
    fragment_a = base64.urlsafe_b64encode(key[:half]).decode()
    fragment_b = base64.urlsafe_b64encode(key[half:]).decode()
    return fragment_a, fragment_b


def combine_key_fragments(fragment_a: str, fragment_b: str) -> bytes:
    a = base64.urlsafe_b64decode(fragment_a.encode())
    b = base64.urlsafe_b64decode(fragment_b.encode())
    return a + b
