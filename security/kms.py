from __future__ import annotations
import os, json
from typing import Tuple
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import secrets

# Why: simple envelope encryption demo

def generate_data_key() -> bytes:
    return secrets.token_bytes(32)


def wrap_data_key(master_secret: bytes, dek: bytes) -> dict:
    salt = secrets.token_bytes(16)
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=salt, info=b"kms-wrap")
    kek = hkdf.derive(master_secret)
    aes = AESGCM(kek)
    nonce = secrets.token_bytes(12)
    ct = aes.encrypt(nonce, dek, None)
    return {"salt": salt.hex(), "nonce": nonce.hex(), "ct": ct.hex()}


def unwrap_data_key(master_secret: bytes, wrapped: dict) -> bytes:
    salt = bytes.fromhex(wrapped["salt"])  # type: ignore
    nonce = bytes.fromhex(wrapped["nonce"])  # type: ignore
    ct = bytes.fromhex(wrapped["ct"])  # type: ignore
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=salt, info=b"kms-wrap")
    kek = hkdf.derive(master_secret)
    aes = AESGCM(kek)
    return aes.decrypt(nonce, ct, None)


def encrypt_with_dek(dek: bytes, plaintext: bytes) -> dict:
    aes = AESGCM(dek)
    nonce = secrets.token_bytes(12)
    ct = aes.encrypt(nonce, plaintext, None)
    return {"nonce": nonce.hex(), "ct": ct.hex()}


def decrypt_with_dek(dek: bytes, blob: dict) -> bytes:
    aes = AESGCM(dek)
    nonce = bytes.fromhex(blob["nonce"])  # type: ignore
    ct = bytes.fromhex(blob["ct"])  # type: ignore
    return aes.decrypt(nonce, ct, None)
