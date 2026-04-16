import json
from app import create_app, db
from app.models.battalion import Battalion

app = create_app()

with app.app_context():
    # Get 9th Battalion
    battalion = Battalion.query.filter_by(battalion_number=9).first()
    
    if battalion:
        # Create organizational structure
        org_structure = {
            "commandant": {
                "name": "E.S.Sai Prasadh (MOBILE : 9440627447)",
                "rank": "Commandant"
            },
            "additional_commandant": {
                "name": "Vacant",
                "groups": [
                    {"name": "Head Quarters Office", "incharge": "U.Sivaiah , RI – Mobile – 9705898293"},
                    {"name": "Quarter Master Office", "incharge": "B.Subba rao , RI – Mobile – 9490651592"},
                    {"name": "Motor Transport Office", "incharge": "K.Govindha Rao, RI – Mobile – 9441618954"},
                    {"name": "Training", "incharge": "G.Laxmaiah, RI – Mobile –9440906548"},
                    {"name": "Band", "incharge": "K.Venkataiah ARSI 423 – Mobile – 8500752565"},
                    {"name": "JA", "incharge": "P.Suresh kumar , RSI – Mobile- 9440906554"},
                    {"name": "Command And Control", "incharge": "Mobile : 9440906532, Email Id : itcoreteam9apsp@gmail.com"},
                    {"name": "BATTALION Welfare Office", "incharge": "J.N.V.Sathyanarayana RI – Mobile – 9440906547"}
                ]
            },
            "assistant_commandants": [
                {
                    "name": "T.Ramakrishna (MOBILE : 9440906557)",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "A Company", "incharge": "M.Ravi teja , RI Mobile - 6303240004"},
                        {"company": "B Company", "incharge": "V.Rajasekhar,RI Mobile - 9440906556"},
                        {"company": "C Company", "incharge": "Y.Venkateswarlu, RI Mobile - 9440001477"}
                    ]
                },
                {
                    "name": "N.H.Vijayanandh (MOBILE : 9440906551)",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "D Company", "incharge": "M.Durvasulu, RI – Mobile - 9492197974"},
                        {"company": "E Company", "incharge": "Y.Jalaiah, RI Mobile – 9491179682"}
                    ]
                },
                {
                    "name": "T.Ramakrishna (MOBILE : 9440906557)",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "F Company", "incharge": "S.Govindharaju, RI – Mobile – 9440906543"}
                    ]
                },
                {
                    "name": "B.Anadhkanna (MOBILE :9963296565)",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "G Company/ SDRF", "incharge": "D.Venkateswarlu, RI – Mobile – 7702798403"}
                    ]
                }
            ]
        }
        
        # Update battalion with new organizational structure
        battalion.organizational_structure = json.dumps(org_structure)
        battalion.commandant_name = "E.S.Sai Prasadh"
        
        db.session.commit()
        
        print("✅ Successfully updated 9th Battalion organizational structure!")
        print("\n📋 Updated Data:")
        print(f"Commandant: {org_structure['commandant']['name']}")
        print(f"Additional Commandant: {org_structure['additional_commandant']['name']}")
        print(f"  - Groups: {len(org_structure['additional_commandant']['groups'])}")
        print(f"Assistant Commandants: {len(org_structure['assistant_commandants'])}")
        for idx, ac in enumerate(org_structure['assistant_commandants'], 1):
            print(f"  {idx}. {ac['name']} - {len(ac['companies'])} companies")
    else:
        print("❌ 9th Battalion not found in database!")
