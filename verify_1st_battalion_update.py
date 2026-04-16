"""Verify 1st Battalion updated data"""
from app import create_app, db
from app.models.battalion import Battalion
import json

app = create_app()

with app.app_context():
    battalion = Battalion.query.filter_by(id=1).first()
    
    if battalion:
        print("\n=== 1st Battalion Current Data ===\n")
        print(f"Name: {battalion.name}")
        print(f"District: {battalion.district}")
        print(f"Commandant: {battalion.commandant_name}")
        print(f"\nOrganizational Structure (JSON):")
        print("=" * 70)
        
        if battalion.organizational_structure:
            org_data = json.loads(battalion.organizational_structure)
            print(json.dumps(org_data, indent=2))
        else:
            print("No organizational structure found!")
        
        print("\n" + "=" * 70)
        print("\n✅ Data verification complete!")
        print("\nTo view on website:")
        print("1. Go to: http://localhost:5000/battalion/1")
        print("2. Look for organizational structure display")
        
    else:
        print("❌ Battalion 1 not found!")
