# routes/rc_routes.py
from flask import Blueprint, request, jsonify, g
from config.db import SessionFactory
from services.uow import UnitOfWork
from utils.clock import Clock
from services.rc_service import RCService
from repositories.rc_repository import RCRepository

bp = Blueprint("rc", __name__)

uow = UnitOfWork(SessionFactory)
clock = Clock()
def rc_repo_factory(s): return RCRepository(s)
rc_service = RCService(rc_repo_factory, uow, clock)

@bp.get("/rc/ping")        # teşhis için
def ping():
    return jsonify({"rc": "ok"})

@bp.post("/rc")            # <-- tam beklediğimiz yol
def create_rc():
    res = rc_service.create_manual(created_by=g.user.id)
    return jsonify(res), 201

@bp.delete("/rc/<int:rc_id>")
def delete_rc(rc_id: int):
    reason = (request.get_json() or {}).get("reason")
    res = rc_service.delete_by_admin(rc_id, reason)
    return jsonify(res), 200
