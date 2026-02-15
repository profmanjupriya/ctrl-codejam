from flask import Flask
from flask_cors import CORS

from config import SECRET_KEY
from db import init_db
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.questions import questions_bp
from routes.timer import timer_bp

app = Flask(__name__)
app.secret_key = SECRET_KEY
CORS(app, supports_credentials=True)

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(questions_bp)
app.register_blueprint(timer_bp)


@app.route("/api/health")
def health():
    return {"ok": True}


if __name__ == "__main__":
    init_db()  # creates tables and ensures admin user exists
    app.run(host="0.0.0.0", port=5000, debug=True)
