
# routes/vote_routes.py
from utils.auth import auth_required
from flask import g
from flask import Blueprint, request, jsonify
from validators.discussion_schemas import VoteSchema
from config.db import SessionFactory
from services.uow import UnitOfWork
from utils.clock import Clock
from services.discussion_service import DiscussionService
from services.rc_service import RCService
from repositories.discussion_repository import DiscussionRepository
from repositories.settings_repository import SettingsRepository
from repositories.rc_repository import RCRepository

bp = Blueprint("vote", __name__)

uow = UnitOfWork(SessionFactory)
clock = Clock()

def disc_repo_factory(s): return DiscussionRepository(s)
def settings_repo_factory(s): return SettingsRepository(s)
def rc_repo_factory(s): return RCRepository(s)
rc_service = RCService(rc_repo_factory, uow, clock=clock)
discussion_service = DiscussionService(disc_repo_factory, rc_service, settings_repo_factory, uow, clock=clock)

@bp.route("/vote", methods=["POST"])
@auth_required
def vote():
    payload = VoteSchema().load(request.get_json() or {})
    result = discussion_service.vote(payload["comment_id"], g.user.id, payload["delta"])
    return jsonify(result), 200

 
