# routes/nc_routes.py
from flask import Blueprint, request, jsonify, g

from config.db import SessionFactory
from services.uow import UnitOfWork
from utils.clock import Clock

from services.nc_service import NCService
from repositories.nc_repository import NCRepository

# --- wiring (DI) ---
uow = UnitOfWork(SessionFactory)
clock = Clock()
def nc_repo_factory(s): return NCRepository(s)

# Pylance hatasını çözen kısım: nc_service burada tanımlanıyor
nc_service = NCService(nc_repo_factory, uow, clock)

# --- routes ---
bp = Blueprint("nc", __name__)

@bp.post("/nc")
def open_nc():
    data = request.get_json() or {}
    title = data.get("title", "")
    res = nc_service.open(title=title, opened_by=g.user.id)
    return jsonify(res), 201

@bp.post("/nc/<int:nc_id>/close")
def close_nc(nc_id: int):
    res = nc_service.close_nc(nc_id, admin_user_id=g.user.id)
    return jsonify(res), 200

@bp.post("/nc/<int:nc_id>/reopen")
def reopen_nc(nc_id: int):
    res = nc_service.reopen_nc(nc_id, admin_user_id=g.user.id)
    return jsonify(res), 200
