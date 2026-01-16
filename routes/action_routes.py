from flask import g
# routes/action_routes.py
from flask import Blueprint, request, jsonify
from validators.action_schemas import ActionCreateSchema, ActionTransitionSchema, ActionCloseSchema

from config.db import SessionFactory
from services.uow import UnitOfWork
from utils.clock import Clock
from services.action_service import ActionService
from repositories.action_repository import ActionRepository
from repositories.rc_repository import RCRepository
from repositories.user_repository import UserRepository

bp = Blueprint("action", __name__)
uow = UnitOfWork(SessionFactory)
clock = Clock()

def action_repo_factory(s): return ActionRepository(s)
def rc_repo_factory(s): return RCRepository(s)
def user_repo_factory(s): return UserRepository(s)
action_service = ActionService(action_repo_factory, rc_repo_factory, user_repo_factory, clock, uow)

@bp.route("/actions", methods=["POST"])
def create_action():
    data = ActionCreateSchema().load(request.get_json() or {})
    action_id = action_service.propose(**data)
    return jsonify({"id": action_id}), 201

@bp.route("/actions/<int:action_id>/plan", methods=["POST"])
def plan_action(action_id: int):
    payload = ActionTransitionSchema().load(request.get_json() or {})
    action_service.plan(action_id, by_user=g.user.id, note=payload.get("note"))
    return jsonify({"ok": True})

@bp.route("/actions/<int:action_id>/complete", methods=["POST"])
def complete_action(action_id: int):
    payload = ActionTransitionSchema().load(request.get_json() or {})
    action_service.complete(action_id, by_user=g.user.id, note=payload.get("note"))
    return jsonify({"ok": True})

@bp.route("/actions/<int:action_id>/close", methods=["POST"])
def close_action(action_id: int):
    payload = ActionCloseSchema().load(request.get_json() or {})
    res = action_service.close(action_id, by_user=g.user.id,
                               approved=payload["approved"], note=payload.get("note"))
    return jsonify(res)
