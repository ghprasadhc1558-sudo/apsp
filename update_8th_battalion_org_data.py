import json
from app import create_app, db
from app.models.battalion import Battalion

app = create_app()

with app.app_context():
    # Get 8th Battalion
    battalion = Battalion.query.filter_by(battalion_number=8).first()
    
    if battalion:
        # Create organizational structure
        org_structure = {
            "commandant": {
                "name": "K.Naveen Kumar (Cell No.8978971076)",
                "rank": "Commandant"
            },
            "additional_commandant": {
                "name": "M.L.Manohar (Cell No. 9441122555)",
                "groups": [
                    {"name": "Head Quarter Office", "incharge": "B.Bhaskar, RI, Cell No.9490838049"},
                    {"name": "Quarter Master office", "incharge": "K.Srinivasulu, RI, Cell No.9490915798"},
                    {"name": "Motor Transport office", "incharge": "K.Sailendra Babu"},
                    {"name": "Battalion Welfare office", "incharge": "B.Obul reddy, Cell No.9440105303"},
                    {"name": "Training", "incharge": "-"},
                    {"name": "Band", "incharge": "-"},
                    {"name": "JA", "incharge": "-"},
                    {"name": "Command And Control", "incharge": "-"}
                ]
            },
            "assistant_commandants": [
                {
                    "name": "V.Yugandhar (Cell No.9441632329)",
                    "rank": "Assistant Commandant",
                    "companies": []
                },
                {
                    "name": "K.V.N.B.Mallikarjun (Cell No.9533070129)",
                    "rank": "Assistant Commandant",
                    "companies": []
                },
                {
                    "name": "SK.Jhonny Saida (Cell No.9966191677)",
                    "rank": "Assistant Commandant/DSP",
                    "companies": []
                }
            ]
        }
        
        # Update battalion with new organizational structure
        battalion.organizational_structure = json.dumps(org_structure)
        battalion.commandant_name = "K.Naveen Kumar"
        
        db.session.commit()
        
        print("✅ Successfully updated 8th Battalion organizational structure!")
        print("\n📋 Updated Data:")
        print(f"Commandant: {org_structure['commandant']['name']}")
        print(f"Additional Commandant: {org_structure['additional_commandant']['name']}")
        print(f"  - Groups: {len(org_structure['additional_commandant']['groups'])}")
        print(f"  - Filled groups: {sum(1 for g in org_structure['additional_commandant']['groups'] if g['incharge'] != '-')}")
        print(f"  - Empty groups (marked with -): {sum(1 for g in org_structure['additional_commandant']['groups'] if g['incharge'] == '-')}")
        print(f"Assistant Commandants: {len(org_structure['assistant_commandants'])}")
        for idx, ac in enumerate(org_structure['assistant_commandants'], 1):
            print(f"  {idx}. {ac['name']} - {len(ac['companies'])} companies")
    else:
        print("❌ 8th Battalion not found in database!")
