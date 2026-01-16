from flask import Blueprint, request, jsonify, g
from utils.auth import auth_required
from validators.action_schemas import ActionCreateSchema, ActionTransitionSchema, ActionCloseSchema
from services.action_service import ActionService
from services.uow import UnitOfWork
from repositories.action_repository import ActionRepository
from repositories.rc_repository import RCRepository
from repositories.user_repository import UserRepository
from utils.clock import Clock
from config.db import SessionFactory

bp = Blueprint("action", __name__)
uow = UnitOfWork(SessionFactory)
clock = Clock()

def action_repo_factory(s): return ActionRepository(s)
def rc_repo_factory(s): return RCRepository(s)
def user_repo_factory(s): return UserRepository(s)

action_service = ActionService(action_repo_factory, rc_repo_factory, user_repo_factory, clock, uow)

@bp.route("/actions", methods=["POST"])
@auth_required
def create_action():
    data = ActionCreateSchema().load(request.get_json() or {})
    action_id = action_service.propose(**data)
    return jsonify({"id": action_id}), 201

@bp.route("/actions/<int:action_id>/plan", methods=["POST"])
@auth_required
def plan_action(action_id: int):
    payload = ActionTransitionSchema().load(request.get_json() or {})
    ok = action_service.plan(action_id, by_user=g.user.id, **payload)
    return jsonify({"ok": ok})

@bp.route("/actions/<int:action_id>/complete", methods=["POST"])
@auth_required
def complete_action(action_id: int):
    payload = ActionTransitionSchema().load(request.get_json() or {})
    ok = action_service.complete(action_id, by_user=g.user.id, **payload)
    return jsonify({"ok": ok})

@bp.route("/actions/<int:action_id>/close", methods=["POST"])
@auth_required
def close_action(action_id: int):
    payload = ActionCloseSchema().load(request.get_json() or {})
    res = action_service.close(action_id, by_user=g.user.id, approved=payload["approved"], note=payload.get("note"))
    return jsonify(res)
