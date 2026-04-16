"""
Reset all battalion admin passwords to default: apsp@2024
"""
from app import create_app, db
from app.models.user import User
from werkzeug.security import generate_password_hash

def reset_passwords():
    """Reset all battalion admin passwords"""
    app = create_app()
    
    with app.app_context():
        # Get all battalion admin users
        battalion_admins = User.query.filter_by(is_battalion_admin=True).all()
        
        print(f"Found {len(battalion_admins)} battalion admin users")
        print("="*60)
        
        default_password = "apsp@2024"  # Simple default password for all
        
        for admin in battalion_admins:
            admin.password = generate_password_hash(default_password)
            print(f"✓ Reset password for: {admin.username}")
            print(f"  New password: {default_password}")
        
        db.session.commit()
        
        print("="*60)
        print(f"All battalion admin passwords reset to: {default_password}")
        print(f"Total admins updated: {len(battalion_admins)}")
        print("="*60)
        print("\nBattalion Admin Login Credentials:")
        print("-" * 60)
        
        for admin in battalion_admins:
            print(f"Username: {admin.username:<25} Password: {default_password}")
        
        print("-" * 60)
        print("\nIMPORTANT: Ask battalion admins to change their password after first login!")

if __name__ == '__main__':
    reset_passwords()
