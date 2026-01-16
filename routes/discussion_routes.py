# routes/discussion_routes.py
from flask import Blueprint, request, jsonify, g
from validators.discussion_schemas import CommentCreateSchema
from config.db import SessionFactory
from services.uow import UnitOfWork
from utils.clock import Clock                      # <-- EKLE
from services.discussion_service import DiscussionService
from services.rc_service import RCService
from repositories.discussion_repository import DiscussionRepository
from repositories.settings_repository import SettingsRepository
from repositories.rc_repository import RCRepository

bp = Blueprint("discussion", __name__)

uow = UnitOfWork(SessionFactory)
clock = Clock()                                     # <-- EKLE
def disc_repo_factory(s): return DiscussionRepository(s)
def settings_repo_factory(s): return SettingsRepository(s)
def rc_repo_factory(s): return RCRepository(s)
rc_service = RCService(rc_repo_factory, uow, clock) # <-- clock PARAMETRESİNİ VER
discussion_service = DiscussionService(disc_repo_factory, rc_service, settings_repo_factory, uow, clock=clock)

@bp.route("/comments", methods=["POST"])
def add_comment():
    payload = CommentCreateSchema().load(request.get_json() or {})
    comment_id = discussion_service.add_comment(
        nc_id=payload["nc_id"],
        user_id=g.user.id,
        text=payload["text"],
        parent_id=payload.get("parent_id")
    )
    return jsonify({"id": comment_id}), 201
