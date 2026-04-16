import json
from app import create_app, db
from app.models.battalion import Battalion

app = create_app()

with app.app_context():
    # Get 3rd Battalion
    battalion = Battalion.query.filter_by(battalion_number=3).first()
    
    if battalion:
        # Create organizational structure
        org_structure = {
            "commandant": {
                "name": "Sri S. Devandarao",
                "rank": "I/C Commandant"
            },
            "additional_commandant": {
                "name": "S.Devananda rao",
                "groups": [
                    {"name": "Head Quarters Office", "incharge": "K.Ajay Kumar, RI"},
                    {"name": "Quarter Master Office", "incharge": "K. Hari Babu, RI"},
                    {"name": "Motor Transport Office", "incharge": "D.G.V.B.S.V.Prasad RI"},
                    {"name": "Band", "incharge": "K. Satyanarayana, ARSI"},
                    {"name": "JA", "incharge": "T. RamaSeshu Babu , RSI"},
                    {"name": "Command And Control", "incharge": ""},
                    {"name": "BATTALION Welfare Office", "incharge": "B. Murali Mohan, RI"}
                ]
            },
            "assistant_commandants": [
                {
                    "name": "D. Murali Kumar",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "A Company", "incharge": "B. Srinivasarao, RI"},
                        {"company": "C Company", "incharge": "B.N.R, Kumar RI"}
                    ]
                },
                {
                    "name": "D.D.GangaRaju",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "B Company", "incharge": "M. Siva Rama Krishna, RI"},
                        {"company": "F Company", "incharge": "D. Raju RI"},
                        {"company": "Training", "incharge": "K. Ravi Shnakararao Ri"}
                    ]
                },
                {
                    "name": "B.Chandra Shekararao",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "G Company", "incharge": "D. Nirmal Kumar, RI"},
                        {"company": "E Company", "incharge": "G.V Ravi Kumar RI"}
                    ]
                },
                {
                    "name": "S.Manmadharao",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "H Company", "incharge": "R. Chandra Mohan, RI"},
                        {"company": "D Company", "incharge": "B. Vitaleswararao , RI"}
                    ]
                },
                {
                    "name": "M.Mohanarao",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "K/SDRF Company", "incharge": "V.Ramu RI"}
                    ]
                }
            ]
        }
        
        # Update battalion with new organizational structure
        battalion.organizational_structure = json.dumps(org_structure)
        battalion.commandant_name = "Sri S. Devandarao (I/C Commandant)"
        
        db.session.commit()
        
        print("✅ Successfully updated 3rd Battalion organizational structure!")
        print("\n📋 Updated Data:")
        print(f"I/C Commandant: {org_structure['commandant']['name']}")
        print(f"Additional Commandant: {org_structure['additional_commandant']['name']}")
        print(f"  - Groups: {len(org_structure['additional_commandant']['groups'])}")
        print(f"Assistant Commandants: {len(org_structure['assistant_commandants'])}")
        for idx, ac in enumerate(org_structure['assistant_commandants'], 1):
            print(f"  {idx}. {ac['name']} - {len(ac['companies'])} companies")
    else:
        print("❌ 3rd Battalion not found in database!")
