"""
Initialize database tables for battalion content (events, announcements, gallery)
Run this script to create the new tables.
"""

from app import create_app, db
from app.models.battalion import Battalion
from app.models.battalion_content import BattalionEvent, BattalionAnnouncement, BattalionGallery

def init_battalion_content_tables():
    """Initialize database tables for battalion content"""
    app = create_app()
    
    with app.app_context():
        print("Creating battalion content tables...")
        
        # Create all tables
        db.create_all()
        
        print("✓ Battalion content tables created successfully!")
        print("  - battalion_events")
        print("  - battalion_announcements")
        print("  - battalion_gallery")
        print("\nYou can now use the battalion admin pages to manage content.")

if __name__ == '__main__':
    init_battalion_content_tables()
