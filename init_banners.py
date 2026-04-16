from app import create_app, db
from app.models.banner import Banner

app = create_app()

with app.app_context():
    # Create banner table
    db.create_all()
    
    print("Banner table created successfully!")
    print("You can now add banners through the admin dashboard.")
