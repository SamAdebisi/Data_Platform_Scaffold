import base64, time, jwt
from fastapi import HTTPException, Header
from .config import JWT_AUDIENCE, JWT_ISSUER, JWT_PUBLIC_KEY_BASE64

from __future__ import annotations
import base64
from typing import Optional
import jwt
from fastapi import HTTPException
from .config import JWT_AUDIENCE, JWT_ISSUER, JWT_PUBLIC_KEY_BASE64, JWT_HS256_SECRET


def _public_key() -> Optional[str]:
    if JWT_PUBLIC_KEY_BASE64:
        try:
            return base64.b64decode(JWT_PUBLIC_KEY_BASE64).decode("utf-8")
        except Exception:
            raise HTTPException(status_code=500, detail="invalid public key")
    return None


def verify_jwt(token: str) -> dict:
    """Accept RS256 if public key provided, else HS256 with local secret.
    Why: keep local dev simple while supporting real JWT in prod.
    """
    options = {"verify_aud": True, "verify_iss": True}
    try:
        pub = _public_key()
        if pub:
            return jwt.decode(
                token,
                pub,
                algorithms=["RS256"],
                audience=JWT_AUDIENCE,
                issuer=JWT_ISSUER,
                options=options,
            )
        return jwt.decode(
            token,
            JWT_HS256_SECRET,
            algorithms=["HS256"],
            audience=JWT_AUDIENCE,
            issuer=JWT_ISSUER,
            options=options,
        )
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail=f"invalid token: {e}")


# def verify_jwt(authorization: str = Header(...)) -> dict:
#     if not authorization.startswith("Bearer "): raise HTTPException(status_code=401, detail="invalid auth header")
#     token = authorization.split(" ",1)[1]
#     options = {"verify_signature": bool(JWT_PUBLIC_KEY_BASE64)}
#     key = base64.b64decode(JWT_PUBLIC_KEY_BASE64) if JWT_PUBLIC_KEY_BASE64 else None
#     try:
#         payload = jwt.decode(token, key, algorithms=["RS256","HS256"], audience=JWT_AUDIENCE, issuer=JWT_ISSUER, options={"verify_aud": True, "verify_iss": True, **options})
#     except Exception as e:
#         raise HTTPException(status_code=401, detail=f"jwt error: {e}")
#     if payload.get("exp", time.time()+1) < time.time(): raise HTTPException(status_code=401, detail="token expired")
#     return payload
