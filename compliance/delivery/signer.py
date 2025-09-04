from typing import Tuple
from pgpy import PGPKey, PGPMessage
def sign_and_encrypt(csv_bytes: bytes, pubkey_armored: str) -> bytes:
    msg = PGPMessage.new(csv_bytes, file=True)
    key, _ = PGPKey.from_blob(pubkey_armored)
    return bytes(key.encrypt(msg))
