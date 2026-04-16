import sqlite3
import json

conn = sqlite3.connect('instance/apsp.db')
cursor = conn.cursor()

# New 6th Battalion organizational structure
org_structure = {
    "additional_commandant": {
        "name": "D.Aseervadam",
        "rank": "Additional Commandant"
    },
    "groups": [
        {"head": "Head Quarters Office", "incharge": "M.Venkata Rao, RI"},
        {"head": "Quarter Master Office", "incharge": "A.Simhardri Naidu, RI"},
        {"head": "Motor Transport Office", "incharge": "S.Srinivasa Rao, RI"},
        {"head": "Training", "incharge": "K.Satya Narayana, RI"},
        {"head": "Band", "incharge": "S.Srinivasulu, ARSI"},
        {"head": "JA", "incharge": "P.Ibrahim Khan, RSI"},
        {"head": "Command And Control", "incharge": ""},
        {"head": "BATTALION Welfare Office", "incharge": "G.Suresh, RI"}
    ],
    "assistant_commandants": [
        {
            "name": "P.V.Hanumanthu",
            "rank": "Assistant Commandant",
            "companies": [
                {"name": "C Company", "incharge": "B.Ramulu, RI"}
            ]
        },
        {
            "name": "Sri U.Ravi",
            "rank": "Assistant Commandant",
            "companies": [
                {"name": "D Company", "incharge": "P.T.Prasad, RI"},
                {"name": "E Company", "incharge": "A.Ganapathi, RI"},
                {"name": "G Company", "incharge": "A.Ganapathi, RI (i/c OC)"}
            ]
        },
        {
            "name": "K.Venkateswara Rao",
            "rank": "Assistant Commandant",
            "companies": [
                {"name": "A Company", "incharge": "G.Nagendra, RI"},
                {"name": "K Company", "incharge": "M.Guru Naidu, RI"}
            ]
        },
        {
            "name": "K.Krishna Murthy",
            "rank": "Assistant Commandant",
            "companies": [
                {"name": "B Company", "incharge": "V.L.Chandra Sekhar, RI"},
                {"name": "H Company", "incharge": "K.Yesu Dasu, RI"}
            ]
        },
        {
            "name": "D.Venkateswara Rao",
            "rank": "Assistant Commandant",
            "companies": [
                {"name": "F Company/SDRF", "incharge": "K.Venkateswarlu, RI"}
            ]
        }
    ]
}

# Convert to JSON string
org_structure_json = json.dumps(org_structure)

# Update the database
cursor.execute('''
    UPDATE battalion 
    SET organizational_structure = ?,
        commandant_name = ?
    WHERE battalion_number = 6
''', (org_structure_json, 'K. Nagesh Babu'))

conn.commit()

print("✓ 6th Battalion data updated successfully!")
print("\nUpdated Information:")
print(f"Commandant: K. Nagesh Babu")
print(f"Additional Commandant: {org_structure['additional_commandant']['name']}")
print(f"Number of Groups: {len(org_structure['groups'])}")
print(f"Number of Assistant Commandants: {len(org_structure['assistant_commandants'])}")
print("\nGroups:")
for group in org_structure['groups']:
    print(f"  - {group['head']}: {group['incharge']}")
print("\nAssistant Commandants:")
for ac in org_structure['assistant_commandants']:
    print(f"  - {ac['name']}: {len(ac['companies'])} companies")

conn.close()
