import json
from app import create_app, db
from app.models.battalion import Battalion

app = create_app()

with app.app_context():
    # Get 1st Battalion
    battalion = Battalion.query.filter_by(battalion_number=1).first()
    
    if battalion:
        org_data = json.loads(battalion.organizational_structure)
        
        # Update Assistant Commandants with empty company placeholders
        if org_data.get('assistant_commandants'):
            for ac in org_data['assistant_commandants']:
                if not ac.get('companies') or len(ac['companies']) == 0:
                    # Add placeholder companies
                    ac['companies'] = [
                        {"company": "-", "incharge": "-"},
                        {"company": "-", "incharge": "-"}
                    ]
        
        battalion.organizational_structure = json.dumps(org_data)
        db.session.commit()
        print("✅ Updated 1st Battalion with company placeholders!")
    
    # Get 4th Battalion
    battalion = Battalion.query.filter_by(battalion_number=4).first()
    
    if battalion:
        org_data = json.loads(battalion.organizational_structure)
        
        # Update Assistant Commandants with empty company placeholders
        if org_data.get('assistant_commandants'):
            for ac in org_data['assistant_commandants']:
                if not ac.get('companies') or len(ac['companies']) == 0:
                    ac['companies'] = [
                        {"company": "-", "incharge": "-"},
                        {"company": "-", "incharge": "-"}
                    ]
        
        battalion.organizational_structure = json.dumps(org_data)
        db.session.commit()
        print("✅ Updated 4th Battalion with company placeholders!")
    
    # Get 7th Battalion
    battalion = Battalion.query.filter_by(battalion_number=7).first()
    
    if battalion:
        # Check if organizational structure exists
        if not battalion.organizational_structure or battalion.organizational_structure.strip() == "":
            # Create basic structure with placeholders
            org_structure = {
                "commandant": {
                    "name": battalion.commandant_name if battalion.commandant_name else "-",
                    "rank": "Commandant"
                },
                "additional_commandant": {
                    "name": "-",
                    "groups": [
                        {"name": "Head Quarters Office", "incharge": "-"},
                        {"name": "Quarter Master Office", "incharge": "-"},
                        {"name": "Motor Transport Office", "incharge": "-"},
                        {"name": "Training", "incharge": "-"},
                        {"name": "Band", "incharge": "-"},
                        {"name": "JA", "incharge": "-"},
                        {"name": "Command And Control", "incharge": "-"},
                        {"name": "BATTALION Welfare Office", "incharge": "-"}
                    ]
                },
                "assistant_commandants": [
                    {
                        "name": "-",
                        "rank": "Assistant Commandant",
                        "companies": [
                            {"company": "-", "incharge": "-"},
                            {"company": "-", "incharge": "-"}
                        ]
                    },
                    {
                        "name": "-",
                        "rank": "Assistant Commandant",
                        "companies": [
                            {"company": "-", "incharge": "-"},
                            {"company": "-", "incharge": "-"}
                        ]
                    },
                    {
                        "name": "-",
                        "rank": "Assistant Commandant",
                        "companies": [
                            {"company": "-", "incharge": "-"},
                            {"company": "-", "incharge": "-"}
                        ]
                    }
                ]
            }
            battalion.organizational_structure = json.dumps(org_structure)
            db.session.commit()
            print("✅ Updated 7th Battalion with company placeholders!")
        else:
            org_data = json.loads(battalion.organizational_structure)
            if org_data.get('assistant_commandants'):
                for ac in org_data['assistant_commandants']:
                    if not ac.get('companies') or len(ac['companies']) == 0:
                        ac['companies'] = [
                            {"company": "-", "incharge": "-"},
                            {"company": "-", "incharge": "-"}
                        ]
                battalion.organizational_structure = json.dumps(org_data)
                db.session.commit()
                print("✅ Updated 7th Battalion with company placeholders!")
    
    # Get 8th Battalion
    battalion = Battalion.query.filter_by(battalion_number=8).first()
    
    if battalion:
        org_data = json.loads(battalion.organizational_structure)
        
        # Update Assistant Commandants with empty company placeholders
        if org_data.get('assistant_commandants'):
            for ac in org_data['assistant_commandants']:
                if not ac.get('companies') or len(ac['companies']) == 0:
                    ac['companies'] = [
                        {"company": "-", "incharge": "-"},
                        {"company": "-", "incharge": "-"}
                    ]
        
        battalion.organizational_structure = json.dumps(org_data)
        db.session.commit()
        print("✅ Updated 8th Battalion with company placeholders!")
    
    print("\n✅ All battalions updated successfully!")
    print("📋 1st, 4th, 7th, 8th Battalions now have company placeholders marked with '-'")
    print("🔄 You can easily add company names and incharges in future!")
