import json
from app import create_app, db
from app.models.battalion import Battalion

app = create_app()

with app.app_context():
    # Get 4th Battalion
    battalion = Battalion.query.filter_by(battalion_number=4).first()
    
    if battalion:
        # Create organizational structure
        org_structure = {
            "commandant": {
                "name": "P SATTI BABU",
                "rank": "Commandant"
            },
            "additional_commandant": {
                "name": "Vacancy",
                "groups": [
                    {"name": "Head Quarter Office", "incharge": "K.Narasimha Rao, RI, Cell No. 7331133838"},
                    {"name": "Quarter Master office", "incharge": "S Murali Krishna, RI, Cell No. 7331185252"},
                    {"name": "Motor Transport office", "incharge": "B.S.Naresh RI, Cell no 7331155757"},
                    {"name": "Battalion Welfare office", "incharge": "B.Kantha Rao,RI, Cell No. 7331185454"},
                    {"name": "Training In Door", "incharge": "S Murali Krishna Cell NO 9493762228"},
                    {"name": "Training Out Door", "incharge": "A Ganesh Cell No 8331985615"},
                    {"name": "JA", "incharge": "Sri Y. Kumar Naik Rathla, Cell NO 8328110352"}
                ]
            },
            "assistant_commandants": [
                {
                    "name": "LSKDV Prasad (Cell No.7331110602)",
                    "rank": "Assistant Commandant",
                    "companies": []
                },
                {
                    "name": "VVV.Satyanarayana (Cell No.7331110604)",
                    "rank": "Assistant Commandant",
                    "companies": []
                },
                {
                    "name": "T.Ravi (Cell No.7331110605)",
                    "rank": "Assistant Commandant",
                    "companies": []
                }
            ]
        }
        
        # Update battalion with new organizational structure
        battalion.organizational_structure = json.dumps(org_structure)
        battalion.commandant_name = "P SATTI BABU"
        
        db.session.commit()
        
        print("✅ Successfully updated 4th Battalion organizational structure!")
        print("\n📋 Updated Data:")
        print(f"Commandant: {org_structure['commandant']['name']}")
        print(f"Additional Commandant: {org_structure['additional_commandant']['name']}")
        print(f"  - Groups: {len(org_structure['additional_commandant']['groups'])}")
        print(f"Assistant Commandants: {len(org_structure['assistant_commandants'])}")
        for idx, ac in enumerate(org_structure['assistant_commandants'], 1):
            print(f"  {idx}. {ac['name']}")
    else:
        print("❌ 4th Battalion not found in database!")
