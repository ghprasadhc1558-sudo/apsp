import json
from app import create_app, db
from app.models.battalion import Battalion

app = create_app()

with app.app_context():
    # Get 11th Battalion
    battalion = Battalion.query.filter_by(battalion_number=11).first()
    
    if battalion:
        # Create organizational structure
        org_structure = {
            "commandant": {
                "name": "K. Ananda Reddy (MOBILE : 9440796903)",
                "rank": "Commandant"
            },
            "additional_commandant": {
                "name": "Vacant",
                "groups": [
                    {"name": "Head Quarters Office", "incharge": "K. Nagaraju, RI – Mobile – 9440906622"},
                    {"name": "Quarter Master Office", "incharge": "D.C. Moulali, RI – Mobile – 9440906620"},
                    {"name": "Motor Transport Office", "incharge": "Y.Ramana Reddy, RI – Mobile – 9441993391"},
                    {"name": "Training", "incharge": "S.Narasimhulu, RI – Mobile – 9440906629"},
                    {"name": "Band", "incharge": "T.V. Ramana, ARSI 332 – Mobile – 9966275832"},
                    {"name": "JA", "incharge": "M. Rama Mohan, RSI – Mobile – 8106487760"},
                    {"name": "Command And Control", "incharge": "Mobile : 9440906630, 9440906609, Email Id : itcoreteam11apsp@gmail.com"},
                    {"name": "BATTALION Welfare Office", "incharge": "S. Ali Basha, RI – Mobile – 9440906616"}
                ]
            },
            "assistant_commandants": [
                {
                    "name": "P. Rajasekhar (MOBILE : 9440627455)",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "A Company", "incharge": "K.V. Ramana, RI – Mobile - 9440906595"},
                        {"company": "B Company", "incharge": "K.V. Ramana, RI – Mobile - 9440906595"},
                        {"company": "G Company", "incharge": "K.V. Ramana, RI – Mobile - 9440906595"}
                    ]
                },
                {
                    "name": "P.N.D. Prasad (MOBILE : 9440906452)",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "C Company", "incharge": "M. Anjaneyulu, RI – Mobile - 9490218145"},
                        {"company": "D Company", "incharge": "B. Mallikarjuna, RI – Mobile – 9440906600"},
                        {"company": "E Company", "incharge": "N. Maruthi Kumar, RI – Mobile – 9347775832"},
                        {"company": "F Company", "incharge": "N. Rami Reddy, RI – Mobile – 9550335597"},
                        {"company": "HQ Company", "incharge": "K. Nagaraju, RI – Mobile - 9440906622"}
                    ]
                }
            ]
        }
        
        # Update battalion with new organizational structure
        battalion.organizational_structure = json.dumps(org_structure)
        battalion.commandant_name = "K. Ananda Reddy"
        
        db.session.commit()
        
        print("✅ Successfully updated 11th Battalion organizational structure!")
        print("\n📋 Updated Data:")
        print(f"Commandant: {org_structure['commandant']['name']}")
        print(f"Additional Commandant: {org_structure['additional_commandant']['name']}")
        print(f"  - Groups: {len(org_structure['additional_commandant']['groups'])}")
        print(f"Assistant Commandants: {len(org_structure['assistant_commandants'])}")
        for idx, ac in enumerate(org_structure['assistant_commandants'], 1):
            print(f"  {idx}. {ac['name']} - {len(ac['companies'])} companies")
    else:
        print("❌ 11th Battalion not found in database!")
