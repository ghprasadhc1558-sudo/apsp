import json
from app import create_app, db
from app.models.battalion import Battalion

app = create_app()

with app.app_context():
    # Get 5th Battalion
    battalion = Battalion.query.filter_by(battalion_number=5).first()
    
    if battalion:
        # Create organizational structure
        org_structure = {
            "commandant": {
                "name": "Sri Y.Ravi Sankar Reddy, IPS",
                "rank": "Commandant"
            },
            "additional_commandant": {
                "name": "C.Raja Reddy (Mobile No. 9440627405)",
                "groups": [
                    {"name": "Head Quarters Office", "incharge": "G.Ravindra Kumar, RI - Mobile : 9440906368"},
                    {"name": "Quarter Master Office", "incharge": "A.Srinivasa Rao, RI – 9493428010"},
                    {"name": "Motor Transport Office", "incharge": "M.Srinu, RI - Mobile :- 9440906342"},
                    {"name": "RI Training", "incharge": "P.Sudhakara Babu, RI - Mobile : 9440906327"},
                    {"name": "Battalion Welfare Office", "incharge": "N.Ganesh, RI - Mobile : 9440906345"},
                    {"name": "JA", "incharge": "P.Lokeswara Rao, RSI - Mobile : 9440906318"},
                    {"name": "Band", "incharge": "G.Krishana Rao, ARSI - Mobile : 9441306992"},
                    {"name": "Command & Control", "incharge": "Mobile : 9440906321 , Email Id : itcoreteam5apsp@gmail.com"}
                ]
            },
            "assistant_commandants": [
                {
                    "name": "D.V.Ramana Murthy (Mobile No. 7330760452)",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "A Company", "incharge": "Y.V.Kesava Ramu, RI – Mobile : 9440906356"},
                        {"company": "G Company", "incharge": "M.Ramajogi Naidu, RI - Mobile : 9440906358"}
                    ]
                },
                {
                    "name": "G.V.Prabhakara Rao (Mobile No. 9866608297)",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "C Company", "incharge": "K.Sanyasi Rao, RI - Mobile : 9440906364"},
                        {"company": "E Company", "incharge": "B.B.K.Chowdary, RI - Mobile : 8555864874"}
                    ]
                },
                {
                    "name": "S.Bapujee (Mobile No. 9490393988)",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "B Company", "incharge": "K.Samarpana Rao, RI - Mobile : 9440906347"},
                        {"company": "D Company", "incharge": "J.V.Ramana, RI – Mobile: 8008086599"},
                        {"company": "F Company", "incharge": "G.Damodhara Rao, RI – Mobile: 9440906370"}
                    ]
                },
                {
                    "name": "G.Laxmi Narayana (Mobile No. 9440627434)",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "H Company/SDRF", "incharge": "S.Chandra Sekhar, RI - Mobile : 9440906329"}
                    ]
                }
            ]
        }
        
        # Update battalion with new organizational structure
        battalion.organizational_structure = json.dumps(org_structure)
        battalion.commandant_name = "Sri Y.Ravi Sankar Reddy, IPS"
        
        db.session.commit()
        
        print("✅ Successfully updated 5th Battalion organizational structure!")
        print("\n📋 Updated Data:")
        print(f"Commandant: {org_structure['commandant']['name']}")
        print(f"Additional Commandant: {org_structure['additional_commandant']['name']}")
        print(f"  - Groups: {len(org_structure['additional_commandant']['groups'])}")
        print(f"Assistant Commandants: {len(org_structure['assistant_commandants'])}")
        for idx, ac in enumerate(org_structure['assistant_commandants'], 1):
            print(f"  {idx}. {ac['name']} - {len(ac['companies'])} companies")
    else:
        print("❌ 5th Battalion not found in database!")
