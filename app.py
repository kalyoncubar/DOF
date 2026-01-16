from flask import Flask, jsonify
from routes.auth_routes import bp as auth_bp
from routes.action_routes import bp as action_bp
from routes.vote_routes import bp as vote_bp
from routes.discussion_routes import bp as discussion_bp
from routes.nc_routes import bp as nc_bp
from routes.rc_routes import bp as rc_bp

def create_app():
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return jsonify({"ok": True})

    @app.get("/")
    def index():
        return jsonify({"message": "DOF API çalışıyor",
                        "try": ["/health", "POST /api/rc", "POST /api/nc"]})

    # Blueprints
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(action_bp, url_prefix="/api")
    app.register_blueprint(vote_bp, url_prefix="/api")
    app.register_blueprint(discussion_bp, url_prefix="/api")
    app.register_blueprint(nc_bp, url_prefix="/api")
    app.register_blueprint(rc_bp, url_prefix="/api")

    print("Registered routes:")
    for r in app.url_map.iter_rules():
        print(f" - {r.rule}  [{','.join(sorted(r.methods))}] -> {r.endpoint}")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
