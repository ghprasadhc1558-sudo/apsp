from app import create_app, db
from app.models.battalion import Battalion

app = create_app()

with app.app_context():
    # Find 2nd Battalion
    battalion = Battalion.query.filter_by(battalion_number=2).first()
    
    if battalion:
        # Update commandant details
        battalion.commandant_name = "Smt. M. DEEPIKA"
        battalion.commandant_rank = "Dy.S.P"
        battalion.commandant_image = "2nd-bn-commandant.jpg"
        
        db.session.commit()
        print("✅ 2nd Battalion commandant updated successfully!")
        print(f"   Name: {battalion.commandant_name}")
        print(f"   Rank: {battalion.commandant_rank}")
        print(f"   Image: {battalion.commandant_image}")
    else:
        print("❌ 2nd Battalion not found in database!")
