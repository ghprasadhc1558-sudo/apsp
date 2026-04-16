import json
from app import create_app, db
from app.models.battalion import Battalion

app = create_app()

with app.app_context():
    # Get 2nd Battalion
    battalion = Battalion.query.filter_by(battalion_number=2).first()
    
    if battalion:
        # Create organizational structure
        org_structure = {
            "commandant": {
                "name": "Smt. M.Deepika Patil IPS",
                "rank": "Commandant"
            },
            "additional_commandant": {
                "name": "Sri V. Nagendra Rao",
                "groups": [
                    {"name": "Head Quarters Office", "incharge": "Sri G. Nagesh, RI"},
                    {"name": "Quarter Master Office", "incharge": "Sri I. Nagaraju, RI"},
                    {"name": "Motor Transport Office", "incharge": "Sri ML. Narendra RSI"},
                    {"name": "Training", "incharge": "Sri M. Ramanjaneyulu, RI"},
                    {"name": "Band", "incharge": "Sri B. Krishnaiah, ARSI 553"},
                    {"name": "JA", "incharge": "Sri J. Obuleshu, RSI"},
                    {"name": "Command And Control", "incharge": "Sri J. Obuleshu, RSI"},
                    {"name": "BATTALION Welfare Office", "incharge": "Sri R. Prabhakar Rao, RI"}
                ]
            },
            "assistant_commandants": [
                {
                    "name": "Sri S. Mahaboob Basha",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "A Company", "incharge": "Sri P. Sambasiva Rao RI"},
                        {"company": "B Company", "incharge": "K.V.Ranga Rao, RI"}
                    ]
                },
                {
                    "name": "Sri B. Venkata Sivudu",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "E Company", "incharge": "Sri M. Ravi Babu RI"},
                        {"company": "H Company", "incharge": "Sri T. Rama Rao RI"}
                    ]
                },
                {
                    "name": "Sri D.V. Ramana",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "C Company", "incharge": "Sri M.Karunakar RI"},
                        {"company": "K Company", "incharge": "Sri T.Rama Rao RI"},
                        {"company": "Training", "incharge": "Sri M.Ramanjaneyulu, RI"}
                    ]
                },
                {
                    "name": "Sri P. Ravi Kiran",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "F Company", "incharge": "Sri G.V. Rami Reddy RI"},
                        {"company": "G Company", "incharge": "Sri M. Surya Rao RI"}
                    ]
                }
            ]
        }
        
        # Update battalion with new organizational structure
        battalion.organizational_structure = json.dumps(org_structure)
        battalion.commandant_name = "Smt. M.Deepika Patil IPS"
        
        db.session.commit()
        
        print("✅ Successfully updated 2nd Battalion organizational structure!")
        print("\n📋 Updated Data:")
        print(f"Commandant: {org_structure['commandant']['name']}")
        print(f"Additional Commandant: {org_structure['additional_commandant']['name']}")
        print(f"  - Groups: {len(org_structure['additional_commandant']['groups'])}")
        print(f"Assistant Commandants: {len(org_structure['assistant_commandants'])}")
        for idx, ac in enumerate(org_structure['assistant_commandants'], 1):
            print(f"  {idx}. {ac['name']} - {len(ac['companies'])} companies")
    else:
        print("❌ 2nd Battalion not found in database!")
