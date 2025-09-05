import os
import pytest
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def _env_tokens(monkeypatch):
    monkeypatch.setenv("JWT_ISSUER", "local")
    monkeypatch.setenv("JWT_AUDIENCE", "ingestion")
    monkeypatch.delenv("JWT_PUBLIC_KEY_BASE64", raising=False)


class FakeRedis:
    def __init__(self):
        self.store = {}

    def set(self, name, value, nx=False, ex=None):
        if nx and name in self.store:
            return False
        self.store[name] = value
        return True

    def get(self, name):
        return self.store.get(name)


@pytest.fixture
def client(monkeypatch):
    # Import after env fixture
    from ingestion_api.app import main

    main.redis = FakeRedis()
    monkeypatch.setattr(main, "produce_transaction", lambda payload: None)
    return TestClient(main.api)


@pytest.fixture
def jwt_token():
    import jwt

    return jwt.encode({"iss": "local", "aud": "ingestion"}, "secret", algorithm="HS256")
