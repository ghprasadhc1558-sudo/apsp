"""Update 1st Battalion organizational structure with new data"""
from app import create_app, db
from app.models.battalion import Battalion

app = create_app()

new_org_structure = {
    "commandant": {
        "name": "CH.V.S.PADMANABHA RAJU",
        "rank": "Commandant"
    },
    "additional_commandant": {
        "name": "VACANCY",
        "groups": [
            {
                "name": "Head Quarters Office",
                "incharge": "P.Sridhar Kumar, RI"
            },
            {
                "name": "Quarter Master Office",
                "incharge": "K.Siva Kumar, RI"
            },
            {
                "name": "Motor Transport Office",
                "incharge": "D.V.M.M.Sumesh Kumar, RI"
            },
            {
                "name": "Training",
                "incharge": ""
            },
            {
                "name": "Band",
                "incharge": ""
            },
            {
                "name": "JA",
                "incharge": ""
            },
            {
                "name": "Command And Control",
                "incharge": ""
            },
            {
                "name": "BATTALION Welfare Office",
                "incharge": "P.Satyanarayana, RI"
            }
        ]
    },
    "assistant_commandants": [
        {
            "name": "G.Nageswara Reddy, DSP",
            "rank": "Assistant Commandant",
            "companies": []
        },
        {
            "name": "T.N.Srinivasa Rao",
            "rank": "Assistant Commandant",
            "companies": []
        },
        {
            "name": "B.Nagesh Babu",
            "rank": "Assistant Commandant",
            "companies": []
        },
        {
            "name": "M.Gopala Krishna",
            "rank": "Assistant Commandant",
            "companies": []
        }
    ]
}

with app.app_context():
    print("\n=== Updating 1st Battalion Organizational Structure ===\n")
    
    battalion = Battalion.query.filter_by(id=1).first()
    
    if battalion:
        print(f"Found: {battalion.name}")
        print(f"District: {battalion.district}")
        
        # Convert to JSON string
        import json
        battalion.organizational_structure = json.dumps(new_org_structure, indent=2)
        
        db.session.commit()
        
        print("\n✅ Successfully updated organizational structure!")
        print("\nNew Structure:")
        print("=" * 60)
        print(f"Commandant: {new_org_structure['commandant']['name']}")
        print(f"\nAdditional Commandant: {new_org_structure['additional_commandant']['name']}")
        print(f"\nGroups under Additional Commandant:")
        for group in new_org_structure['additional_commandant']['groups']:
            if group['incharge']:
                print(f"  • {group['name']}: {group['incharge']}")
            else:
                print(f"  • {group['name']}: (Not assigned)")
        
        print(f"\nAssistant Commandants ({len(new_org_structure['assistant_commandants'])}):")
        for ac in new_org_structure['assistant_commandants']:
            print(f"  • {ac['name']}")
        
        print("\n" + "=" * 60)
        print("\n✅ Old data has been replaced with new data!")
        
    else:
        print("❌ Battalion 1 not found!")

print("\n=== Update Complete ===\n")
