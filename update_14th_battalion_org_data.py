import json
from app import create_app, db
from app.models.battalion import Battalion

app = create_app()

with app.app_context():
    # Get 14th Battalion
    battalion = Battalion.query.filter_by(battalion_number=14).first()
    
    if battalion:
        # Create organizational structure
        org_structure = {
            "commandant": {
                "name": "K. Prabhu Kumar (MOBILE : 9550110646)",
                "rank": "Commandant"
            },
            "additional_commandant": {
                "name": "V.Keshava Reddy (MOBILE: 9849344724)",
                "groups": [
                    {"name": "Head Quarters Office", "incharge": "T.Raghavendra, RI – Mobile – 8500016291"},
                    {"name": "Quarter Master Office", "incharge": "D.sudheer kumar, RSI – Mobile – 83092 82637"},
                    {"name": "Motor Transport Office", "incharge": "Y. Jagadeesh RI – Mobile – 9703242252"},
                    {"name": "Training", "incharge": "G.Ramu, RI – Mobile – 94900 76167"},
                    {"name": "Band", "incharge": "K.Adinararayan Prasad, ARSI 446 – Mobile – 9966275832"},
                    {"name": "JA", "incharge": "G.Chandra Babu, RSI – Mobile – 94949 30923"},
                    {"name": "Command And Control", "incharge": "Mobile : 9440906750, Email Id : tcoreteam14apsp@gmail.com"},
                    {"name": "BATTALION Welfare Office", "incharge": "V.Sreedhar, RSI – Mobile – 94409 22375"}
                ]
            },
            "assistant_commandants": [
                {
                    "name": "B.Venkata Siva Reddy (MOBILE : 85001 45244)",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "A Company", "incharge": "T.V. Rama Rao, RI – Mobile - 94934 84917"},
                        {"company": "B Company", "incharge": "G.Pradeep Kumar, RI – Mobile - 9398023384"}
                    ]
                },
                {
                    "name": "A.Sivaji Raju (MOBILE : 9949341133)",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "C Company", "incharge": "G.Ramu, RI – Mobile - 9490076167"},
                        {"company": "D Company", "incharge": "S.Nagendra, RI – Mobile – 9381903654"},
                        {"company": "E Company", "incharge": "S.R.P.V.Raju, RI – Mobile – 9441505942"}
                    ]
                },
                {
                    "name": "Sri R.Wilson Care (MOBILE : 989643099)",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {"company": "F Company", "incharge": "C.H.Sudheer Kumar, RI – Mobile – 9618550985"},
                        {"company": "G Company", "incharge": "V.V.G.S.R.Murthy, RI- Mobile-8332989937"}
                    ]
                }
            ]
        }
        
        # Update battalion with new organizational structure
        battalion.organizational_structure = json.dumps(org_structure)
        battalion.commandant_name = "K. Prabhu Kumar"
        
        db.session.commit()
        
        print("✅ Successfully updated 14th Battalion organizational structure!")
        print("\n📋 Updated Data:")
        print(f"Commandant: {org_structure['commandant']['name']}")
        print(f"Additional Commandant: {org_structure['additional_commandant']['name']}")
        print(f"  - Groups: {len(org_structure['additional_commandant']['groups'])}")
        print(f"Assistant Commandants: {len(org_structure['assistant_commandants'])}")
        for idx, ac in enumerate(org_structure['assistant_commandants'], 1):
            print(f"  {idx}. {ac['name']} - {len(ac['companies'])} companies")
    else:
        print("❌ 14th Battalion not found in database!")
