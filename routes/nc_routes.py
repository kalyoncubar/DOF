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
    try:
        res = nc_service.open(title=title, opened_by=g.user.id)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify(res), 201

@bp.get("/nc")
@auth_required
def list_nc():
    res = nc_service.list_all()
    return jsonify(res), 200

@bp.get("/nc/<int:nc_id>")
@auth_required
def get_nc(nc_id: int):
    try:
        res = nc_service.get(nc_id=nc_id)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404
    return jsonify(res), 200

@bp.patch("/nc/<int:nc_id>")
@auth_required
def update_nc(nc_id: int):
    payload = request.get_json() or {}
    title = (payload.get("title") or "").strip()
    try:
        res = nc_service.update_title(nc_id=nc_id, title=title)
    except ValueError as exc:
        status = 404 if str(exc) == "NC bulunamadı" else 400
        return jsonify({"error": str(exc)}), status
    return jsonify(res), 200

@bp.post("/nc/<int:nc_id>/close")
@auth_required
def close_nc(nc_id: int):
    try:
        res = nc_service.close(nc_id=nc_id, admin_user_id=g.user.id)
    except ValueError as exc:
        status = 404 if str(exc) == "NC bulunamadı" else 400
        return jsonify({"error": str(exc)}), status
    return jsonify(res), 200

@bp.post("/nc/<int:nc_id>/reopen")
@auth_required
def reopen_nc(nc_id: int):
    try:
        res = nc_service.reopen(nc_id=nc_id, admin_user_id=g.user.id)
    except ValueError as exc:
        status = 404 if str(exc) == "NC bulunamadı" else 400
        return jsonify({"error": str(exc)}), status
    return jsonify(res), 200
