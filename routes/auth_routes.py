from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from config.db import SessionFactory
from services.uow import UnitOfWork
from repositories.user_repository import UserRepository
from utils.auth import create_jwt

bp = Blueprint("auth", __name__)
uow = UnitOfWork(SessionFactory)
def user_repo_factory(s): return UserRepository(s)

@bp.get("/auth/ping")
def auth_ping():
    return jsonify({"auth": "ok"})

@bp.post("/auth/login")
def login():
    data = request.get_json() or {}
    user_code = (data.get("user_code") or "").strip()
    password = data.get("password") or ""
    if not user_code or not password:
        return jsonify({"error": "user_code_and_password_required"}), 400

    with uow() as s:
        users = user_repo_factory(s)
        u = users.get_by_user_code(user_code)
        if not u or not u.get("is_active"):
            return jsonify({"error": "invalid_credentials"}), 401
        if not check_password_hash(u["password_hash"], password):
            return jsonify({"error": "invalid_credentials"}), 401

        token = create_jwt(u["id"], u["role"])
        return jsonify({"token": token, "user": {"id": u["id"], "name": u["name"], "role": u["role"]}})
