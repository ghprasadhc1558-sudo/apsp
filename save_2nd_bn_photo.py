from app import create_app, db
from app.models.battalion import Battalion

app = create_app()

with app.app_context():
    # Update 2nd Battalion commandant image to use the real photo
    battalion = Battalion.query.filter_by(battalion_number=2).first()
    
    if battalion:
        # The photo will be named commandant_2_deepika.jpg
        battalion.commandant_image = 'commandant_2_deepika.jpg'
        db.session.commit()
        print("✓ Updated 2nd Battalion commandant image to real photo")
        print(f"  Commandant: {battalion.commandant_name}")
        print(f"  Image: {battalion.commandant_image}")
    else:
        print("✗ 2nd Battalion not found")
