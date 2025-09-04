import base64, os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
def tokenize(value: str, dek: bytes) -> str:
    aes=AESGCM(dek); nonce=os.urandom(12); ct=aes.encrypt(nonce, value.encode(), None); return base64.b64encode(nonce+ct).decode()
def detokenize(token: str, dek: bytes) -> str:
    raw=base64.b64decode(token); aes=AESGCM(dek); return aes.decrypt(raw[:12], raw[12:], None).decode()
