from app import create_app, db
from app.models.battalion import Battalion

app = create_app()

with app.app_context():
    print("📋 Checking Battalion Images in Database:")
    print("=" * 70)
    
    battalions = Battalion.query.order_by(Battalion.battalion_number).all()
    
    for battalion in battalions:
        image_status = "✅" if battalion.image else "⚠️"
        image_value = battalion.image if battalion.image else "Not set"
        print(f"{image_status} Battalion {battalion.battalion_number:2d}: {image_value}")
    
    print("=" * 70)
    print("\n💡 Tip: If 'Not set', upload image through admin panel")
