"""Check if battalion content tables have data"""
from app import create_app, db
from app.models.battalion_content import BattalionEvent, BattalionAnnouncement, BattalionGallery

app = create_app()

with app.app_context():
    print("\n=== Battalion Content Check ===\n")
    
    # Check events
    events = BattalionEvent.query.all()
    print(f"Total Events: {len(events)}")
    for event in events[:5]:  # Show first 5
        print(f"  - Battalion {event.battalion_id}: {event.title} ({event.date})")
    
    # Check announcements
    announcements = BattalionAnnouncement.query.all()
    print(f"\nTotal Announcements: {len(announcements)}")
    for ann in announcements[:5]:  # Show first 5
        print(f"  - Battalion {ann.battalion_id}: {ann.title} ({ann.date})")
    
    # Check gallery
    gallery = BattalionGallery.query.all()
    print(f"\nTotal Gallery Images: {len(gallery)}")
    for img in gallery[:5]:  # Show first 5
        print(f"  - Battalion {img.battalion_id}: {img.caption or 'No caption'}")
    
    print("\n=== Check Complete ===\n")
