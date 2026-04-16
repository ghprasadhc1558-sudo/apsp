
from app import create_app, db
from app.models.user import User
from werkzeug.security import generate_password_hash

def reset_password():
    app = create_app()
    with app.app_context():
        user = User.query.filter_by(username='battalion14_admin').first()
        if user:
            user.password = generate_password_hash('apsp@2024')
            db.session.commit()
            print("Password for battalion14_admin reset to apsp@2024")
        else:
            print("User battalion14_admin not found")

if __name__ == '__main__':
    reset_password()
