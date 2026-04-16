"""
Verification script to test the announcement feature
"""
from app import create_app, db
from app.models.announcement import Announcement

def verify_feature():
    app = create_app()
    
    with app.app_context():
        print("="*50)
        print("ANNOUNCEMENT FEATURE VERIFICATION")
        print("="*50)
        
        # Test 1: Check if table exists
        try:
            count = Announcement.query.count()
            print(f"✅ Database table exists")
            print(f"✅ Found {count} announcements in database")
        except Exception as e:
            print(f"❌ Database error: {e}")
            return False
        
        # Test 2: List all announcements
        announcements = Announcement.query.order_by(Announcement.order).all()
        if announcements:
            print("\n📢 Current Announcements:")
            for idx, ann in enumerate(announcements, 1):
                status = "✓ Active" if ann.is_active else "✗ Inactive"
                print(f"   {idx}. [{status}] {ann.content}")
        else:
            print("\n⚠️  No announcements found")
        
        # Test 3: Check model functionality
        print("\n🔧 Testing model functionality...")
        test_ann = Announcement(
            content="Test Announcement - Please Delete",
            is_active=False,
            order=999
        )
        db.session.add(test_ann)
        db.session.commit()
        print("   ✅ Can create announcements")
        
        # Clean up test
        db.session.delete(test_ann)
        db.session.commit()
        print("   ✅ Can delete announcements")
        
        print("\n" + "="*50)
        print("✅ ALL TESTS PASSED!")
        print("="*50)
        print("\nNext steps:")
        print("1. Start the server: python run.py")
        print("2. Login to admin: /admin/login")
        print("3. Navigate to Announcements section")
        print("4. Start managing announcements!")
        
        return True

if __name__ == '__main__':
    try:
        verify_feature()
    except Exception as e:
        print(f"\n❌ Verification failed: {e}")
        import traceback
        traceback.print_exc()
