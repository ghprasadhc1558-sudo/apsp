import json
from app import create_app, db
from app.models.battalion import Battalion

app = create_app()

with app.app_context():
    # Get 6th Battalion
    battalion = Battalion.query.filter_by(battalion_number=6).first()
    
    if battalion:
        # Create organizational structure
        org_structure = {
            "commandant": {
                "name": "K.Nagesh Babu",
                "rank": "Commandant"
            },
            "additional_commandant": {
                "name": "D.Aseervadam",
                "groups": [
                    {"name": "Head Quarters Office", "incharge": "M.Venkata Rao, RI"},
                    {"name": "Quarter Master Office", "incharge": "A.Simhardri Naidu , RI"},
                    {"name": "Motor Transport Office", "incharge": "S.Srinivasa Rao, RI"},
                    {"name": "Training", "incharge": "K.Satya Narayana, RI"},
                    {"name": "Band", "incharge": "S.Srinivasulu, ARSI"},
                    {"name": "JA", "incharge": "P.Ibrahim Khan, RSI"},
                    {"name": "Command And Control", "incharge": ""},
                    {"name": "BATTALION Welfare Office", "incharge": "G.Suresh , RI"}
                ]
            },
            "assistant_commandants": [
                {
                    "name": "P.V.Hanumanthu",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "C Company", "incharge": "B. Ramulu, RI"}
                    ]
                },
                {
                    "name": "Sri U.Ravi",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "D Company", "incharge": "P.T.Prasad, RI"},
                        {"company": "E Company", "incharge": "A.Ganapathi RI"},
                        {"company": "G Company", "incharge": "A.Ganapathi RI i/c OC"}
                    ]
                },
                {
                    "name": "K.Venkateswara Rao",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "A Company", "incharge": "G.Nagendra, RI"},
                        {"company": "K Company", "incharge": "M.Guru Naidu, RI"}
                    ]
                },
                {
                    "name": "K.Krishna Murthy",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "B Company", "incharge": "V.L.Chndra Sekhar, RI"},
                        {"company": "H Company", "incharge": "K.Yesu Dasu, RI"}
                    ]
                },
                {
                    "name": "D.Venkateswara Rao",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "F Company/SDRF", "incharge": "K.Venkateswarlu, RI"}
                    ]
                }
            ]
        }
        
        # Update battalion with new organizational structure
        battalion.organizational_structure = json.dumps(org_structure)
        battalion.commandant_name = "K.Nagesh Babu"
        
        db.session.commit()
        
        print("✅ Successfully updated 6th Battalion organizational structure!")
        print("\n📋 Updated Data:")
        print(f"Commandant: {org_structure['commandant']['name']}")
        print(f"Additional Commandant: {org_structure['additional_commandant']['name']}")
        print(f"  - Groups: {len(org_structure['additional_commandant']['groups'])}")
        print(f"Assistant Commandants: {len(org_structure['assistant_commandants'])}")
        for idx, ac in enumerate(org_structure['assistant_commandants'], 1):
            print(f"  {idx}. {ac['name']} - {len(ac['companies'])} companies")
    else:
        print("❌ 6th Battalion not found in database!")
