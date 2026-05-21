from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import json

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database configuration
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        # For production (PostgreSQL on Render)
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    else:
        # For development (SQLite)
        instance_path = os.path.join(os.path.dirname(__file__), '..', 'instance')
        os.makedirs(instance_path, exist_ok=True)
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_path, "apsp.db")}'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'images')
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

    db.init_app(app)
    login_manager.init_app(app)
    
    # Add JSON filter for templates
    @app.template_filter('fromjson')
    def fromjson_filter(s):
        if s:
            return json.loads(s)
        return {}

    # Register routes
    try:
        from . import routes
        app.register_blueprint(routes.bp)
    except Exception as e:
        print(f"Error loading routes: {e}")
        import traceback
        traceback.print_exc()
        raise

    return app
