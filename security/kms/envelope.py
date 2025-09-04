import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
def generate_wrapped_dek():
    dek=os.urandom(32); key=rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pub=key.public_key().encrypt(dek, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    return key, pub, dek
