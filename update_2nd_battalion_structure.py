from app import create_app, db
from app.models.battalion import Battalion
import json

app = create_app()

with app.app_context():
    # Find 2nd Battalion
    battalion = Battalion.query.filter_by(battalion_number=2).first()
    
    if battalion:
        # Update Commandant
        battalion.commandant_name = "Smt M.DEEPIKA"
        battalion.commandant_rank = "Commandant"
        
        # New Organizational Structure
        org_structure = {
            "additional_commandant": {
                "name": "V.Nagendra Rao",
                "rank": "Additional Commandant"
            },
            "groups": [
                {
                    "head": "Quarter Master Office",
                    "incharge": "M.C.Shailkshavali, RI"
                },
                {
                    "head": "Head Quarters Office",
                    "incharge": "K.Siva Sankar Rao, RI"
                },
                {
                    "head": "Motor Transport Office",
                    "incharge": "P.Samba Siva Rao, RI"
                },
                {
                    "head": "Band",
                    "incharge": "J.Obulesu, RSI"
                },
                {
                    "head": "JA",
                    "incharge": "J.Obulesu, RSI"
                },
                {
                    "head": "Training",
                    "incharge": "D.Raju, RI"
                },
                {
                    "head": "Command And Control",
                    "incharge": ""
                },
                {
                    "head": "BATTALION Welfare Office",
                    "incharge": "R.Prabhakar Rao, RI"
                }
            ],
            "assistant_commandants": [
                {
                    "name": "D.Venkataramana",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {
                            "name": "C Company",
                            "incharge": "L.Srinivasa Reddy, RI"
                        },
                        {
                            "name": "K Company",
                            "incharge": "L.Srinivasa Reddy, RI"
                        }
                    ]
                },
                {
                    "name": "P. Ravi Kiran",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {
                            "name": "E Company",
                            "incharge": "T.Rama Rao, RI"
                        },
                        {
                            "name": "F Company",
                            "incharge": "G.V.Rami Reddy, RI"
                        }
                    ]
                },
                {
                    "name": "V.Keshava Reddy",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {
                            "name": "D/SDRF Company",
                            "incharge": "S.Praveen Kumar, RI"
                        }
                    ]
                },
                {
                    "name": "S.Sharfuddin",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {
                            "name": "G Company",
                            "incharge": "M.Surya Rao, RI"
                        },
                        {
                            "name": "H Company",
                            "incharge": "S.Ramakotalaiah, RI"
                        }
                    ]
                },
                {
                    "name": "S.Mahaboob Basha",
                    "rank": "Assistant Commandant",
                    "companies": [
                        {
                            "name": "A Company",
                            "incharge": "A.Ganapathi, RI"
                        },
                        {
                            "name": "B Company",
                            "incharge": "D.Raju, RI"
                        }
                    ]
                }
            ]
        }
        
        battalion.organizational_structure = json.dumps(org_structure)
        
        db.session.commit()
        print("✅ 2nd Battalion organizational structure updated successfully!")
        print(f"Commandant: {battalion.commandant_name}")
        print(f"Additional Commandant: V.Nagendra Rao")
        print(f"Total Assistant Commandants: 5")
        print(f"Total Groups: 8")
    else:
        print("❌ 2nd Battalion not found in database!")
