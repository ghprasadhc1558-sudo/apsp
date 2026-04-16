"""
Script to add announcements table to database and populate with default data
"""
from app import create_app, db
from app.models.announcement import Announcement

def init_announcements():
    app = create_app()
    
    with app.app_context():
        # Create announcements table
        db.create_all()
        print("✓ Announcements table created")
        
        # Check if there are any announcements
        existing = Announcement.query.first()
        if existing:
            print("✓ Announcements already exist in database")
            return
        
        # Add default announcements (from the current hardcoded text)
        default_announcements = [
            "DPC RSIs TO RIs 2024-25",
            "Combined seniority list of ARSIs 01.01.2024",
            "ARSI Seniority List 2023",
            "Commemoration Day 2024",
            "ID Parade 2024",
            "Panel of RSI to RI 2023-24"
        ]
        
        for idx, content in enumerate(default_announcements, start=1):
            announcement = Announcement(
                content=content,
                is_active=True,
                order=idx
            )
            db.session.add(announcement)
        
        db.session.commit()
        print(f"✓ Added {len(default_announcements)} default announcements")
        print("\nDefault announcements added:")
        for idx, content in enumerate(default_announcements, start=1):
            print(f"  {idx}. {content}")

if __name__ == '__main__':
    init_announcements()
    print("\n✅ Announcements initialization complete!")
    print("\nYou can now manage announcements through the admin dashboard.")
