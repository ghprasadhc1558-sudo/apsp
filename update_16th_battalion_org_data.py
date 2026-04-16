import json
from app import create_app, db
from app.models.battalion import Battalion

app = create_app()

with app.app_context():
    # Get 16th Battalion
    battalion = Battalion.query.filter_by(battalion_number=16).first()
    
    if battalion:
        # Create organizational structure
        org_structure = {
            "commandant": {
                "name": "M.Arun Bose",
                "rank": "Commandant"
            },
            "additional_commandant": {
                "name": "M.Srinivasa Rao",
                "groups": [
                    {"name": "Head Quarters Office", "incharge": "K.Babu Rao, RI"},
                    {"name": "Quarter Master Office", "incharge": "T.RAVI KUMAR, RI"},
                    {"name": "Motor Transport Office", "incharge": "J.CHENNAKESAVA RAO, RI"},
                    {"name": "Training", "incharge": "S.V.Ramana, RI"},
                    {"name": "Band", "incharge": "K. PANDU RANGA RAO, HC 259"},
                    {"name": "JA", "incharge": "A.Ravi Babu, RSI"},
                    {"name": "Command And Control", "incharge": ""},
                    {"name": "BATTALION Welfare Office", "incharge": "K.Srinivasa Rao, RI"}
                ]
            },
            "assistant_commandants": [
                {
                    "name": "P.SATYAM",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "A Company", "incharge": "A.Sateesh, RI"},
                        {"company": "Training", "incharge": "S.V.Ramana, RI"}
                    ]
                },
                {
                    "name": "G.ELIA SAGAR",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "E Company", "incharge": "K.V.Ranga Rao, RI"}
                    ]
                },
                {
                    "name": "V.NARAYANA RAO",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "G/SDRF Company", "incharge": "T.Ramakrishna, RI"}
                    ]
                },
                {
                    "name": "N.MURALIDHAR",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "B Company", "incharge": "B.Narayana, RI"},
                        {"company": "C Company", "incharge": "P.Duryodhana Rao, RI"}
                    ]
                },
                {
                    "name": "B.RAMAKRISHNA",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "D Company", "incharge": "G.Narayana, RI"},
                        {"company": "F Company", "incharge": "T.Murali, RI"}
                    ]
                }
            ]
        }
        
        # Update battalion with new organizational structure
        battalion.organizational_structure = json.dumps(org_structure)
        battalion.commandant_name = "M.Arun Bose"
        
        db.session.commit()
        
        print("✅ Successfully updated 16th Battalion organizational structure!")
        print("\n📋 Updated Data:")
        print(f"Commandant: {org_structure['commandant']['name']}")
        print(f"Additional Commandant: {org_structure['additional_commandant']['name']}")
        print(f"  - Groups: {len(org_structure['additional_commandant']['groups'])}")
        print(f"Assistant Commandants: {len(org_structure['assistant_commandants'])}")
        for idx, ac in enumerate(org_structure['assistant_commandants'], 1):
            print(f"  {idx}. {ac['name']} - {len(ac['companies'])} companies")
    else:
        print("❌ 16th Battalion not found in database!")
