import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
# Check for DATABASE_URL, POSTGRES_URL (Vercel default), or other integration variants
database_url = (
    os.environ.get("DATABASE_URL") or 
    os.environ.get("POSTGRES_URL") or 
    os.environ.get("POSTGRES_PRISMA_URL") or 
    os.environ.get("POSTGRES_URL_NON_POOLING") or 
    "sqlite:///medicare.db"
)
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import models to ensure tables are created
    try:
        import models  # noqa: F401
        db.create_all()
        logging.info("Database tables created")
    except Exception as e:
        logging.error(f"Error initializing database: {e}")
        # We don't re-raise here to allow the app to start and show logs


@app.route('/debug-db')
def debug_db():
    try:
        db.create_all()
        user_count = User.query.count()
        return f"Database connected! Tables created. User count: {user_count}"
    except Exception as e:
        return f"Database error: {str(e)}"

# Import routes to ensure they are registered
import routes  # noqa: F401, E402


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
