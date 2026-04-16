"""
Add Battalion Admin Columns to User Table
"""
from app import create_app, db
from sqlalchemy import text

def migrate_user_table():
    """Add battalion admin columns to user table"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if columns already exist
            result = db.session.execute(text("PRAGMA table_info(user)"))
            columns = [row[1] for row in result]
            
            print("Current columns in user table:", columns)
            
            # Add is_battalion_admin column if it doesn't exist
            if 'is_battalion_admin' not in columns:
                print("Adding is_battalion_admin column...")
                db.session.execute(text("ALTER TABLE user ADD COLUMN is_battalion_admin BOOLEAN DEFAULT 0"))
                print("✓ Added is_battalion_admin column")
            else:
                print("✓ is_battalion_admin column already exists")
            
            # Add battalion_id column if it doesn't exist
            if 'battalion_id' not in columns:
                print("Adding battalion_id column...")
                db.session.execute(text("ALTER TABLE user ADD COLUMN battalion_id INTEGER"))
                print("✓ Added battalion_id column")
            else:
                print("✓ battalion_id column already exists")
            
            db.session.commit()
            print("\n" + "="*60)
            print("Database migration completed successfully!")
            print("="*60)
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error during migration: {str(e)}")
            raise

if __name__ == '__main__':
    migrate_user_table()
