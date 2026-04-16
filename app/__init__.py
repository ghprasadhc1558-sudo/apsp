from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import json

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///apsp.db'
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

    from . import routes
    app.register_blueprint(routes.bp)

    return app
