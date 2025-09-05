from __future__ import annotations
import os, hmac, hashlib, base64

TOK_SECRET = os.getenv("TOK_SECRET", "tok-secret")


def tokenize(value: str) -> str:
    # Why: deterministic non-reversible token for PAN-like fields
    mac = hmac.new(TOK_SECRET.encode(), msg=value.encode(), digestmod=hashlib.sha256).digest()
    return base64.urlsafe_b64encode(mac)[:32].decode()
