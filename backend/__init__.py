from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from .config import Config
from .models import db


def create_app() -> Flask:
    # Load environment variables from a .env file if present
    load_dotenv()
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)

    # Enable CORS (configurable via FRONTEND_ORIGINS)
    CORS(
        app,
        resources={r"/api/*": {"origins": Config.FRONTEND_ORIGINS}},
        supports_credentials=True,
    )

    # Database
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Blueprints (Views)
    from .views.tickets import tickets_bp
    from .views.sms import sms_bp

    app.register_blueprint(tickets_bp, url_prefix="/api/tickets")
    app.register_blueprint(sms_bp, url_prefix="/sms")

    @app.get("/api/health")
    def health() -> dict:
        return {"status": "ok"}

    return app


