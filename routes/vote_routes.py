from flask import Blueprint, request, jsonify, g
from utils.auth import auth_required
# ... diğer importlar

bp = Blueprint("vote", __name__)

@bp.post("/vote")
@auth_required
def vote():
    data = request.get_json() or {}
    # ... mevcut iş mantığın
    return jsonify({"ok": True})
