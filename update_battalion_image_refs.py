from app import create_app, db
from app.models.battalion import Battalion
import os

app = create_app()

with app.app_context():
    print("🔄 Updating Battalion Image References in Database...")
    print("=" * 70)
    
    # Update battalions 1 and 8 to use JPEG instead of PNG
    updates = [
        (1, '1st-bn.jpeg'),
        (8, '8th-bn.jpeg')
    ]
    
    for bn_num, new_filename in updates:
        battalion = Battalion.query.filter_by(battalion_number=bn_num).first()
        if battalion:
            old_value = battalion.image
            battalion.image = new_filename
            db.session.commit()
            print(f"✅ Battalion {bn_num:2d}: {old_value} → {new_filename}")
    
    print("=" * 70)
    
    # Now set all battalions to their default image filenames
    print("\n🔄 Setting default image filenames for all battalions...")
    print("=" * 70)
    
    battalions = Battalion.query.all()
    battalion_dir = 'app/static/images/battalions'
    
    for battalion in battalions:
        # Check if JPEG file exists
        jpeg_filename = f'{battalion.battalion_number}th-bn.jpeg'
        jpeg_path = os.path.join(battalion_dir, jpeg_filename)
        
        if os.path.exists(jpeg_path):
            if battalion.image != jpeg_filename:
                battalion.image = jpeg_filename
                db.session.commit()
                print(f"✅ Battalion {battalion.battalion_number:2d}: Set to {jpeg_filename}")
            else:
                print(f"✓  Battalion {battalion.battalion_number:2d}: Already correct ({jpeg_filename})")
        else:
            print(f"⚠️  Battalion {battalion.battalion_number:2d}: File not found ({jpeg_filename})")
    
    print("=" * 70)
    print("\n✅ Database updated! Refresh battalion pages to see images.")
