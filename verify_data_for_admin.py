"""Simple direct database query to verify data"""
from app import create_app
from app.models.battalion_content import BattalionEvent, BattalionAnnouncement, BattalionGallery

app = create_app()

with app.app_context():
    print("\n=== Current Battalion Content Data ===\n")
    
    # Battalion 1 data
    print("BATTALION 1:")
    events = BattalionEvent.query.filter_by(battalion_id=1).all()
    print(f"\n  Events ({len(events)}):")
    for e in events:
        print(f"    • {e.title} - {e.date} at {e.location}")
    
    announcements = BattalionAnnouncement.query.filter_by(battalion_id=1).all()
    print(f"\n  Announcements ({len(announcements)}):")
    for a in announcements:
        print(f"    • {a.title} - {a.date}")
        print(f"      {a.content[:50]}...")
    
    gallery = BattalionGallery.query.filter_by(battalion_id=1).all()
    print(f"\n  Gallery ({len(gallery)}):")
    for g in gallery:
        print(f"    • {g.caption or 'No caption'} - {g.image_path}")
    
    print("\n" + "="*50)
    print("\nTo view this data in the admin panel:")
    print("1. Open: http://localhost:5000/battalion-admin/login")
    print("2. Login with: battalion1_admin / apsp2024")
    print("3. Go to Edit Battalion Information")
    print("4. You should see:")
    print(f"   - {len(events)} events in Events Management section")
    print(f"   - {len(announcements)} announcements in Announcements Management section")
    print(f"   - {len(gallery)} images in Gallery Management section")
    print("\n" + "="*50 + "\n")
