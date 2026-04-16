from app import create_app, db
from app.models.battalion import Battalion

app = create_app()

with app.app_context():
    print("🔄 Updating commandant photo filenames in database...")
    print("=" * 70)
    
    battalions = Battalion.query.all()
    
    for battalion in battalions:
        if battalion.commandant_image:
            old_filename = battalion.commandant_image
            # Convert any extension to .jpg
            if old_filename.endswith(('.jpeg', '.png', '.gif', '.webp', '.bmp')):
                new_filename = old_filename.rsplit('.', 1)[0] + '.jpg'
                battalion.commandant_image = new_filename
                db.session.commit()
                print(f"✅ Battalion {battalion.battalion_number:2d}: {old_filename} → {new_filename}")
            else:
                print(f"✓  Battalion {battalion.battalion_number:2d}: {old_filename} (already correct)")
    
    print("=" * 70)
    print("✅ Database updated! Photos will now display correctly!")
