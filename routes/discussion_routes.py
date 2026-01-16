from flask import Blueprint, request, jsonify, g
from utils.auth import auth_required
from repositories.settings_repository import SettingsRepository
from services.rc_service import RCService
from services.discussion_service import DiscussionService
# ... diğer importlar (SessionFactory, UnitOfWork vs.)

bp = Blueprint("discussion", __name__)

# ... servis ve repo wiring

@bp.post("/comments")
@auth_required
def add_comment():
    data = request.get_json() or {}
    # ... mevcut iş mantığın
    return jsonify({"ok": True})
