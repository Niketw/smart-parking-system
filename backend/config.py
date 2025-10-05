import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(os.path.dirname(__file__), 'app.db')}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Twilio
    TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
    TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER", "")

    # CORS origins (comma-separated). Defaults to localhost:3000
    FRONTEND_ORIGINS = (
        os.environ.get("FRONTEND_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
        .split(",")
    )


