from flask import Blueprint, request, jsonify, g
from config.db import SessionFactory
from services.uow import UnitOfWork
from utils.clock import Clock
from utils.auth import auth_required
from repositories.nc_repository import NCRepository
from services.nc_service import NCService

bp = Blueprint("nc", __name__)

# --- wiring ---
uow = UnitOfWork(SessionFactory)
clock = Clock()
def nc_repo_factory(s): return NCRepository(s)
nc_service = NCService(nc_repo_factory, uow, clock)

@bp.get("/nc/ping")  # teşhis
def ping_nc():
    return jsonify({"nc": "ok"})

@bp.post("/nc")
@auth_required
def open_nc():
    payload = request.get_json() or {}
    title = (payload.get("title") or "").strip()
    res = nc_service.open(title=title, opened_by=g.user.id)
    return jsonify(res), 201

@bp.post("/nc/<int:nc_id>/close")
@auth_required
def close_nc(nc_id: int):
    res = nc_service.close(nc_id=nc_id, by_user=g.user.id)
    return jsonify(res), 200

@bp.post("/nc/<int:nc_id>/reopen")
@auth_required
def reopen_nc(nc_id: int):
    res = nc_service.reopen(nc_id=nc_id, by_user=g.user.id)
    return jsonify(res), 200
