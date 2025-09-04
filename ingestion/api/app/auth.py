import base64, time, jwt
from fastapi import HTTPException, Header
from .config import JWT_AUDIENCE, JWT_ISSUER, JWT_PUBLIC_KEY_BASE64
def verify_jwt(authorization: str = Header(...)) -> dict:
    if not authorization.startswith("Bearer "): raise HTTPException(status_code=401, detail="invalid auth header")
    token = authorization.split(" ",1)[1]
    options = {"verify_signature": bool(JWT_PUBLIC_KEY_BASE64)}
    key = base64.b64decode(JWT_PUBLIC_KEY_BASE64) if JWT_PUBLIC_KEY_BASE64 else None
    try:
        payload = jwt.decode(token, key, algorithms=["RS256","HS256"], audience=JWT_AUDIENCE, issuer=JWT_ISSUER, options={"verify_aud": True, "verify_iss": True, **options})
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"jwt error: {e}")
    if payload.get("exp", time.time()+1) < time.time(): raise HTTPException(status_code=401, detail="token expired")
    return payload
