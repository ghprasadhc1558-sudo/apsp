"""Add sample battalion content data for testing"""
from app import create_app, db
from app.models.battalion_content import BattalionEvent, BattalionAnnouncement, BattalionGallery
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    print("\n=== Adding Sample Battalion Content ===\n")
    
    # Add sample events for Battalion 1
    events = [
        BattalionEvent(
            battalion_id=1,
            title="Independence Day Celebration",
            description="Grand Independence Day celebration at battalion headquarters with flag hoisting ceremony.",
            date=datetime.now().date(),
            location="Battalion Headquarters"
        ),
        BattalionEvent(
            battalion_id=1,
            title="Sports Day 2026",
            description="Annual sports competition between different companies.",
            date=(datetime.now() + timedelta(days=30)).date(),
            location="Sports Ground"
        ),
    ]
    
    # Add sample announcements for Battalion 1
    announcements = [
        BattalionAnnouncement(
            battalion_id=1,
            title="Training Schedule Update",
            content="New training schedule effective from next month. All personnel must attend mandatory sessions.",
            date=datetime.now().date()
        ),
        BattalionAnnouncement(
            battalion_id=1,
            title="Leave Policy Revision",
            content="Updated leave policy has been implemented. Check with your commanding officer for details.",
            date=(datetime.now() - timedelta(days=5)).date()
        ),
    ]
    
    # Note: For gallery, we'll leave it empty as it requires actual image files
    # Users can upload images through the admin panel
    
    try:
        # Add all events
        for event in events:
            db.session.add(event)
        print(f"✓ Added {len(events)} sample events for Battalion 1")
        
        # Add all announcements
        for announcement in announcements:
            db.session.add(announcement)
        print(f"✓ Added {len(announcements)} sample announcements for Battalion 1")
        
        db.session.commit()
        print("\n✓ Sample data added successfully!")
        print("\nNote: Gallery images should be uploaded through the admin panel.")
        
    except Exception as e:
        db.session.rollback()
        print(f"\n✗ Error: {str(e)}")
    
    print("\n=== Complete ===\n")
