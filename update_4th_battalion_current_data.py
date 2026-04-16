import sqlite3
import json

conn = sqlite3.connect('instance/apsp.db')
cursor = conn.cursor()

# New 4th Battalion organizational structure
org_structure = {
    "additional_commandant": {
        "name": "To be updated",
        "rank": "Additional Commandant"
    },
    "groups": [
        {"head": "Head Quarter Office", "incharge": "K.Narasimha Rao, RI, Cell No. 7331133838"},
        {"head": "Quarter Master Office", "incharge": "S Murali Krishna, RI, Cell No. 7331185252"},
        {"head": "Motor Transport Office", "incharge": "B.S.Naresh, RI, Cell No. 7331155757"},
        {"head": "Battalion Welfare Office", "incharge": "B.Kantha Rao, RI, Cell No. 7331185454"},
        {"head": "Training In Door", "incharge": "S Murali Krishna, Cell No. 9493762228"},
        {"head": "Training Out Door", "incharge": "A Ganesh, Cell No. 8331985615"},
        {"head": "JA", "incharge": "Sri Y. Kumar Naik Rathla, Cell No. 8328110352"}
    ],
    "assistant_commandants": [
        {
            "name": "LSKDV Prasad (Cell No. 7331110602)",
            "rank": "Assistant Commandant",
            "companies": []
        },
        {
            "name": "VVV.Satyanarayana (Cell No. 7331110604)",
            "rank": "Assistant Commandant",
            "companies": []
        },
        {
            "name": "T.Ravi (Cell No. 7331110605)",
            "rank": "Assistant Commandant",
            "companies": []
        }
    ]
}

# Convert to JSON string
org_structure_json = json.dumps(org_structure)

# Update the database
cursor.execute('''
    UPDATE battalion 
    SET organizational_structure = ?,
        commandant_name = ?,
        commandant_rank = ?
    WHERE battalion_number = 4
''', (org_structure_json, 'P. Satti Babu', 'Commandant'))

conn.commit()

print("✓ 4th Battalion data updated successfully!")
print("\nUpdated Information:")
print(f"Commandant: P. Satti Babu (Cell No. 7331110600)")
print(f"Additional Commandant: {org_structure['additional_commandant']['name']}")
print(f"Number of Groups: {len(org_structure['groups'])}")
print(f"Number of Assistant Commandants: {len(org_structure['assistant_commandants'])}")
print("\nGroups:")
for group in org_structure['groups']:
    print(f"  - {group['head']}: {group['incharge']}")
print("\nAssistant Commandants:")
for ac in org_structure['assistant_commandants']:
    print(f"  - {ac['name']}")
print("\nNote: Company assignments for Assistant Commandants can be added later.")

conn.close()
