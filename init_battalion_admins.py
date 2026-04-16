"""
Initialize Battalion Admin Users
Creates admin users for all 12 battalions with default passwords
"""
from app import create_app, db
from app.models.user import User
from app.models.battalion import Battalion
from werkzeug.security import generate_password_hash

def init_battalion_admins():
    """Create battalion admin users for all battalions"""
    app = create_app()
    
    with app.app_context():
        # Get all battalions
        battalions = Battalion.query.order_by(Battalion.battalion_number).all()
        
        print(f"Found {len(battalions)} battalions")
        
        created_count = 0
        updated_count = 0
        
        for battalion in battalions:
            bn_number = battalion.battalion_number
            username = f"battalion{bn_number}_admin"
            default_password = f"Bn{bn_number}@APSP2024"  # Default password
            
            # Check if user already exists
            existing_user = User.query.filter_by(username=username).first()
            
            if existing_user:
                # Update existing user
                existing_user.is_battalion_admin = True
                existing_user.battalion_id = battalion.id
                # Don't change password if user already exists
                print(f"✓ Updated existing user: {username} for {battalion.name}")
                updated_count += 1
            else:
                # Create new battalion admin user
                new_admin = User(
                    username=username,
                    password=generate_password_hash(default_password),
                    is_admin=False,
                    is_battalion_admin=True,
                    battalion_id=battalion.id
                )
                db.session.add(new_admin)
                print(f"✓ Created new user: {username} for {battalion.name}")
                print(f"  Default password: {default_password}")
                created_count += 1
        
        try:
            db.session.commit()
            print(f"\n{'='*60}")
            print(f"Battalion Admin Initialization Complete!")
            print(f"{'='*60}")
            print(f"New users created: {created_count}")
            print(f"Existing users updated: {updated_count}")
            print(f"Total battalion admins: {created_count + updated_count}")
            print(f"\nBattalion Admin Login Details:")
            print(f"{'='*60}")
            
            # Display all battalion admin credentials
            for battalion in battalions:
                bn_number = battalion.battalion_number
                username = f"battalion{bn_number}_admin"
                default_password = f"Bn{bn_number}@APSP2024"
                print(f"\n{battalion.name}:")
                print(f"  Username: {username}")
                print(f"  Default Password: {default_password}")
                print(f"  Login URL: /battalion-admin/login")
            
            print(f"\n{'='*60}")
            print("IMPORTANT SECURITY NOTES:")
            print("1. All battalion admins should change their passwords after first login")
            print("2. Share credentials securely with respective battalion commandants")
            print("3. Each battalion admin can only access their own battalion data")
            print(f"{'='*60}\n")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error: {str(e)}")
            raise

if __name__ == '__main__':
    init_battalion_admins()
