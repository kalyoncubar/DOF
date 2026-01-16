# utils/auth.py
from __future__ import annotations
import os, time
import jwt
from functools import wraps
from flask import request, g, jsonify
from sqlalchemy import select


JWT_ALG = "HS256"
JWT_TTL_SECONDS = 3600  # 1 saat

def _secret():
    # PROD: env var kullan; yoksa fallback
    return os.environ.get("JWT_SECRET", "dev-secret-change-me")

def create_jwt(user_id: int, role: str) -> str:
    now = int(time.time())
    payload = {"sub": user_id, "role": role, "iat": now, "exp": now + JWT_TTL_SECONDS}
    return jwt.encode(payload, _secret(), algorithm=JWT_ALG)

def decode_jwt(token: str) -> dict:
    return jwt.decode(token, _secret(), algorithms=[JWT_ALG])

def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Authorization: Bearer <token>
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "missing_or_invalid_token"}), 401
        token = auth.split(" ", 1)[1]
        try:
            payload = decode_jwt(token)
        except Exception:
            return jsonify({"error": "invalid_token"}), 401

        # basit g.user nesnesi
        class U: ...
        u = U()
        u.id = int(payload["sub"])
        u.role = str(payload.get("role", "user"))
        g.user = u
        return f(*args, **kwargs)
    return wrapper

