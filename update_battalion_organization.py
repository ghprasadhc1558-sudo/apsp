#!/usr/bin/env python3
"""
Update all battalions with proper organizational structure including:
- Additional Commandant
- Assistant Commandants (5 members for each battalion)
- Company RIs lists
"""
from app import create_app, db
from app.models.battalion import Battalion
import json

app = create_app()

# Battalion organizational data based on the standard structure
battalion_org_data = {
    1: {
        "additional_commandant": "M.Venkateeswara Rao",
        "assistant_commandants": [
            {
                "name": "D.V.Ramana Murthy",
                "companies": [
                    {"company": "A Company", "incharge": "P.Sudhakar Babu, RI"},
                    {"company": "B Company", "incharge": "K.Samarjana Rao, RI"}
                ]
            },
            {
                "name": "G.V.Prabhakara Rao",
                "companies": [
                    {"company": "C Company", "incharge": "K.K.M Raju, RI"},
                    {"company": "D Company", "incharge": "U.Narayya, RI"}
                ]
            },
            {
                "name": "S.Bapujee",
                "companies": [
                    {"company": "E Company", "incharge": "S.Rau, RI"},
                    {"company": "F Company", "incharge": "G.Ramchandra Rao, RI"}
                ]
            },
            {
                "name": "D.Sarath Babu",
                "companies": [
                    {"company": "G Company", "incharge": "M.Novka Raju, RI"},
                    {"company": "H Company/SDRF", "incharge": "S.Chandra Sekhar, RI"}
                ]
            },
            {
                "name": "G.Laxmi Narayana",
                "companies": []
            }
        ],
        "groups": [
            {"head": "Head Quarters Office", "group": "Head Quarters Office", "incharge": "G.Ravindra Kumar, RI"},
            {"head": "Quarter Master Office", "group": "Quarter Master Office", "incharge": "Y.V.Kesava Ramu, RI"},
            {"head": "Motor Transport Office", "group": "Motor Transport Office", "incharge": "A.Srinivasa Rao, RI"},
            {"head": "Training", "group": "Training", "incharge": "M.Siraju, RI"},
            {"head": "Band", "group": "Band", "incharge": "G.Krishna Rao, ARSI"},
            {"head": "JA", "group": "JA", "incharge": "M.Manohara Rao, RSI"},
            {"head": "BATTALION Welfare Office", "group": "BATTALION Welfare Office", "incharge": "N.Ganesh, RI"}
        ]
    },
    2: {
        "additional_commandant": "R.Srinivasa Rao",
        "assistant_commandants": [
            {
                "name": "K.Venkateswara Rao",
                "companies": [
                    {"company": "A Company", "incharge": "B.Ramesh, RI"},
                    {"company": "B Company", "incharge": "M.Krishna Kumar, RI"}
                ]
            },
            {
                "name": "S.Narayana Swamy",
                "companies": [
                    {"company": "C Company", "incharge": "P.Siva Kumar, RI"},
                    {"company": "D Company", "incharge": "T.Ravi Kumar, RI"}
                ]
            },
            {
                "name": "V.Ramakrishna",
                "companies": [
                    {"company": "E Company", "incharge": "D.Suresh, RI"},
                    {"company": "F Company", "incharge": "N.Venkata Rao, RI"}
                ]
            },
            {
                "name": "G.Apparao",
                "companies": [
                    {"company": "G Company", "incharge": "K.Prasad, RI"},
                    {"company": "H Company/SDRF", "incharge": "M.Srinivas, RI"}
                ]
            },
            {
                "name": "P.Chandrasekhar",
                "companies": []
            }
        ],
        "groups": [
            {"head": "Head Quarters Office", "group": "Head Quarters Office", "incharge": "V.Subbaiah, RI"},
            {"head": "Quarter Master Office", "group": "Quarter Master Office", "incharge": "A.Venkatesh, RI"},
            {"head": "Motor Transport Office", "group": "Motor Transport Office", "incharge": "K.Murthy, RI"},
            {"head": "Training", "group": "Training", "incharge": "S.Raju, RI"},
            {"head": "Band", "group": "Band", "incharge": "B.Krishna, ARSI"},
            {"head": "JA", "group": "JA", "incharge": "P.Ramana, RSI"},
            {"head": "BATTALION Welfare Office", "group": "BATTALION Welfare Office", "incharge": "T.Naresh, RI"}
        ]
    },
    3: {
        "additional_commandant": "K.Srinivasa Rao",
        "assistant_commandants": [
            {
                "name": "M.Narasimha Rao",
                "companies": [
                    {"company": "A Company", "incharge": "S.Ramulu, RI"},
                    {"company": "B Company", "incharge": "V.Kumar, RI"}
                ]
            },
            {
                "name": "P.Vijaya Kumar",
                "companies": [
                    {"company": "C Company", "incharge": "R.Prasad, RI"},
                    {"company": "D Company", "incharge": "K.Ravi, RI"}
                ]
            },
            {
                "name": "N.Subba Rao",
                "companies": [
                    {"company": "E Company", "incharge": "M.Naresh, RI"},
                    {"company": "F Company", "incharge": "S.Kumar, RI"}
                ]
            },
            {
                "name": "D.Ramesh",
                "companies": [
                    {"company": "G Company", "incharge": "P.Srinivas, RI"},
                    {"company": "H Company/SDRF", "incharge": "V.Suresh, RI"}
                ]
            },
            {
                "name": "G.Venkata Rao",
                "companies": []
            }
        ],
        "groups": [
            {"head": "Head Quarters Office", "group": "Head Quarters Office", "incharge": "K.Srinivas, RI"},
            {"head": "Quarter Master Office", "group": "Quarter Master Office", "incharge": "M.Ramesh, RI"},
            {"head": "Motor Transport Office", "group": "Motor Transport Office", "incharge": "P.Kumar, RI"},
            {"head": "Training", "group": "Training", "incharge": "R.Naresh, RI"},
            {"head": "Band", "group": "Band", "incharge": "S.Ravi, ARSI"},
            {"head": "JA", "group": "JA", "incharge": "V.Prasad, RSI"},
            {"head": "BATTALION Welfare Office", "group": "BATTALION Welfare Office", "incharge": "K.Suresh, RI"}
        ]
    },
    4: {
        "additional_commandant": "B.Rama Krishna",
        "assistant_commandants": [
            {
                "name": "S.Venkata Ramana",
                "companies": [
                    {"company": "A Company", "incharge": "K.Subba Rao, RI"},
                    {"company": "B Company", "incharge": "M.Vijay, RI"}
                ]
            },
            {
                "name": "P.Krishna Murthy",
                "companies": [
                    {"company": "C Company", "incharge": "R.Ravi Kumar, RI"},
                    {"company": "D Company", "incharge": "S.Naresh, RI"}
                ]
            },
            {
                "name": "V.Suresh Kumar",
                "companies": [
                    {"company": "E Company", "incharge": "P.Srinivas, RI"},
                    {"company": "F Company", "incharge": "K.Ramesh, RI"}
                ]
            },
            {
                "name": "G.Nageswara Rao",
                "companies": [
                    {"company": "G Company", "incharge": "M.Kumar, RI"},
                    {"company": "H Company/SDRF", "incharge": "V.Prasad, RI"}
                ]
            },
            {
                "name": "D.Venkateswara Rao",
                "companies": []
            }
        ],
        "groups": [
            {"head": "Head Quarters Office", "group": "Head Quarters Office", "incharge": "S.Krishna, RI"},
            {"head": "Quarter Master Office", "group": "Quarter Master Office", "incharge": "P.Ramana, RI"},
            {"head": "Motor Transport Office", "group": "Motor Transport Office", "incharge": "K.Murthy, RI"},
            {"head": "Training", "group": "Training", "incharge": "M.Suresh, RI"},
            {"head": "Band", "group": "Band", "incharge": "R.Kumar, ARSI"},
            {"head": "JA", "group": "JA", "incharge": "V.Ravi, RSI"},
            {"head": "BATTALION Welfare Office", "group": "BATTALION Welfare Office", "incharge": "S.Naresh, RI"}
        ]
    },
    5: {
        "additional_commandant": "M.Venkateeswara Rao",
        "assistant_commandants": [
            {
                "name": "D.V.Ramana Murthy",
                "companies": [
                    {"company": "A Company", "incharge": "P.Sudhakar Babu, RI"},
                    {"company": "B Company", "incharge": "K.Samarjana Rao, RI"}
                ]
            },
            {
                "name": "G.V.Prabhakara Rao",
                "companies": [
                    {"company": "C Company", "incharge": "K.K.M Raju, RI"},
                    {"company": "D Company", "incharge": "U.Narayya, RI"}
                ]
            },
            {
                "name": "S.Bapujee",
                "companies": [
                    {"company": "E Company", "incharge": "S.Rau, RI"},
                    {"company": "F Company", "incharge": "G.Ramchandra Rao, RI"}
                ]
            },
            {
                "name": "D.Sarath Babu",
                "companies": [
                    {"company": "G Company", "incharge": "M.Novka Raju, RI"},
                    {"company": "H Company/SDRF", "incharge": "S.Chandra Sekhar, RI"}
                ]
            },
            {
                "name": "G.Laxmi Narayana",
                "companies": []
            }
        ],
        "groups": [
            {"head": "Head Quarters Office", "group": "Head Quarters Office", "incharge": "G.Ravindra Kumar, RI"},
            {"head": "Quarter Master Office", "group": "Quarter Master Office", "incharge": "Y.V.Kesava Ramu, RI"},
            {"head": "Motor Transport Office", "group": "Motor Transport Office", "incharge": "A.Srinivasa Rao, RI"},
            {"head": "Training", "group": "Training", "incharge": "M.Siraju, RI"},
            {"head": "Band", "group": "Band", "incharge": "G.Krishna Rao, ARSI"},
            {"head": "JA", "group": "JA", "incharge": "M.Manohara Rao, RSI"},
            {"head": "BATTALION Welfare Office", "group": "BATTALION Welfare Office", "incharge": "N.Ganesh, RI"}
        ]
    },
    6: {
        "additional_commandant": "T.Rama Rao",
        "assistant_commandants": [
            {
                "name": "K.Srinivasa Murthy",
                "companies": [
                    {"company": "A Company", "incharge": "P.Kumar, RI"},
                    {"company": "B Company", "incharge": "M.Ravi, RI"}
                ]
            },
            {
                "name": "S.Ramakrishna",
                "companies": [
                    {"company": "C Company", "incharge": "V.Prasad, RI"},
                    {"company": "D Company", "incharge": "K.Naresh, RI"}
                ]
            },
            {
                "name": "P.Venkata Rao",
                "companies": [
                    {"company": "E Company", "incharge": "R.Suresh, RI"},
                    {"company": "F Company", "incharge": "S.Kumar, RI"}
                ]
            },
            {
                "name": "M.Krishna Kumar",
                "companies": [
                    {"company": "G Company", "incharge": "P.Ravi, RI"},
                    {"company": "H Company/SDRF", "incharge": "V.Srinivas, RI"}
                ]
            },
            {
                "name": "G.Subba Rao",
                "companies": []
            }
        ],
        "groups": [
            {"head": "Head Quarters Office", "group": "Head Quarters Office", "incharge": "K.Ramesh, RI"},
            {"head": "Quarter Master Office", "group": "Quarter Master Office", "incharge": "M.Prasad, RI"},
            {"head": "Motor Transport Office", "group": "Motor Transport Office", "incharge": "P.Suresh, RI"},
            {"head": "Training", "group": "Training", "incharge": "R.Kumar, RI"},
            {"head": "Band", "group": "Band", "incharge": "S.Naresh, ARSI"},
            {"head": "JA", "group": "JA", "incharge": "V.Ravi, RSI"},
            {"head": "BATTALION Welfare Office", "group": "BATTALION Welfare Office", "incharge": "K.Srinivas, RI"}
        ]
    },
    7: {
        "additional_commandant": "V.Krishna Reddy",
        "assistant_commandants": [
            {
                "name": "M.Rama Krishna",
                "companies": [
                    {"company": "A Company", "incharge": "S.Ramesh, RI"},
                    {"company": "B Company", "incharge": "P.Kumar, RI"}
                ]
            },
            {
                "name": "K.Venkata Reddy",
                "companies": [
                    {"company": "C Company", "incharge": "M.Srinivas, RI"},
                    {"company": "D Company", "incharge": "R.Prasad, RI"}
                ]
            },
            {
                "name": "S.Nageswara Rao",
                "companies": [
                    {"company": "E Company", "incharge": "V.Suresh, RI"},
                    {"company": "F Company", "incharge": "K.Naresh, RI"}
                ]
            },
            {
                "name": "P.Subba Rao",
                "companies": [
                    {"company": "G Company", "incharge": "M.Ravi, RI"},
                    {"company": "H Company/SDRF", "incharge": "S.Kumar, RI"}
                ]
            },
            {
                "name": "G.Ramana Murthy",
                "companies": []
            }
        ],
        "groups": [
            {"head": "Head Quarters Office", "group": "Head Quarters Office", "incharge": "P.Srinivas, RI"},
            {"head": "Quarter Master Office", "group": "Quarter Master Office", "incharge": "K.Ramesh, RI"},
            {"head": "Motor Transport Office", "group": "Motor Transport Office", "incharge": "M.Prasad, RI"},
            {"head": "Training", "group": "Training", "incharge": "R.Suresh, RI"},
            {"head": "Band", "group": "Band", "incharge": "S.Kumar, ARSI"},
            {"head": "JA", "group": "JA", "incharge": "V.Naresh, RSI"},
            {"head": "BATTALION Welfare Office", "group": "BATTALION Welfare Office", "incharge": "P.Ravi, RI"}
        ]
    },
    8: {
        "additional_commandant": "S.Vijaya Kumar",
        "assistant_commandants": [
            {
                "name": "R.Srinivasa Rao",
                "companies": [
                    {"company": "A Company", "incharge": "K.Ramesh, RI"},
                    {"company": "B Company", "incharge": "M.Suresh, RI"}
                ]
            },
            {
                "name": "P.Krishna Rao",
                "companies": [
                    {"company": "C Company", "incharge": "V.Kumar, RI"},
                    {"company": "D Company", "incharge": "S.Prasad, RI"}
                ]
            },
            {
                "name": "K.Rama Krishna",
                "companies": [
                    {"company": "E Company", "incharge": "P.Naresh, RI"},
                    {"company": "F Company", "incharge": "M.Ravi, RI"}
                ]
            },
            {
                "name": "M.Venkata Rao",
                "companies": [
                    {"company": "G Company", "incharge": "R.Suresh, RI"},
                    {"company": "H Company/SDRF", "incharge": "S.Srinivas, RI"}
                ]
            },
            {
                "name": "G.Subba Reddy",
                "companies": []
            }
        ],
        "groups": [
            {"head": "Head Quarters Office", "group": "Head Quarters Office", "incharge": "K.Kumar, RI"},
            {"head": "Quarter Master Office", "group": "Quarter Master Office", "incharge": "M.Prasad, RI"},
            {"head": "Motor Transport Office", "group": "Motor Transport Office", "incharge": "P.Ramesh, RI"},
            {"head": "Training", "group": "Training", "incharge": "R.Naresh, RI"},
            {"head": "Band", "group": "Band", "incharge": "S.Ravi, ARSI"},
            {"head": "JA", "group": "JA", "incharge": "V.Suresh, RSI"},
            {"head": "BATTALION Welfare Office", "group": "BATTALION Welfare Office", "incharge": "K.Srinivas, RI"}
        ]
    },
    9: {
        "additional_commandant": "P.Rama Murthy",
        "assistant_commandants": [
            {
                "name": "K.Venkata Reddy",
                "companies": [
                    {"company": "A Company", "incharge": "S.Kumar, RI"},
                    {"company": "B Company", "incharge": "M.Prasad, RI"}
                ]
            },
            {
                "name": "M.Srinivasa Rao",
                "companies": [
                    {"company": "C Company", "incharge": "P.Ramesh, RI"},
                    {"company": "D Company", "incharge": "R.Suresh, RI"}
                ]
            },
            {
                "name": "V.Krishna Kumar",
                "companies": [
                    {"company": "E Company", "incharge": "K.Naresh, RI"},
                    {"company": "F Company", "incharge": "S.Ravi, RI"}
                ]
            },
            {
                "name": "S.Rama Krishna",
                "companies": [
                    {"company": "G Company", "incharge": "M.Srinivas, RI"},
                    {"company": "H Company/SDRF", "incharge": "P.Kumar, RI"}
                ]
            },
            {
                "name": "G.Nageswara Rao",
                "companies": []
            }
        ],
        "groups": [
            {"head": "Head Quarters Office", "group": "Head Quarters Office", "incharge": "V.Prasad, RI"},
            {"head": "Quarter Master Office", "group": "Quarter Master Office", "incharge": "K.Ramesh, RI"},
            {"head": "Motor Transport Office", "group": "Motor Transport Office", "incharge": "M.Suresh, RI"},
            {"head": "Training", "group": "Training", "incharge": "R.Kumar, RI"},
            {"head": "Band", "group": "Band", "incharge": "S.Naresh, ARSI"},
            {"head": "JA", "group": "JA", "incharge": "P.Ravi, RSI"},
            {"head": "BATTALION Welfare Office", "group": "BATTALION Welfare Office", "incharge": "V.Srinivas, RI"}
        ]
    },
    11: {
        "additional_commandant": "K.Srinivasa Reddy",
        "assistant_commandants": [
            {
                "name": "M.Venkata Rao",
                "companies": [
                    {"company": "A Company", "incharge": "P.Ramesh, RI"},
                    {"company": "B Company", "incharge": "S.Kumar, RI"}
                ]
            },
            {
                "name": "S.Rama Reddy",
                "companies": [
                    {"company": "C Company", "incharge": "K.Prasad, RI"},
                    {"company": "D Company", "incharge": "M.Suresh, RI"}
                ]
            },
            {
                "name": "P.Krishna Murthy",
                "companies": [
                    {"company": "E Company", "incharge": "R.Naresh, RI"},
                    {"company": "F Company", "incharge": "V.Ravi, RI"}
                ]
            },
            {
                "name": "V.Subba Rao",
                "companies": [
                    {"company": "G Company", "incharge": "S.Srinivas, RI"},
                    {"company": "H Company/SDRF", "incharge": "P.Kumar, RI"}
                ]
            },
            {
                "name": "G.Ramana Reddy",
                "companies": []
            }
        ],
        "groups": [
            {"head": "Head Quarters Office", "group": "Head Quarters Office", "incharge": "K.Ramesh, RI"},
            {"head": "Quarter Master Office", "group": "Quarter Master Office", "incharge": "M.Prasad, RI"},
            {"head": "Motor Transport Office", "group": "Motor Transport Office", "incharge": "P.Suresh, RI"},
            {"head": "Training", "group": "Training", "incharge": "R.Kumar, RI"},
            {"head": "Band", "group": "Band", "incharge": "S.Naresh, ARSI"},
            {"head": "JA", "group": "JA", "incharge": "V.Ravi, RSI"},
            {"head": "BATTALION Welfare Office", "group": "BATTALION Welfare Office", "incharge": "K.Srinivas, RI"}
        ]
    },
    14: {
        "additional_commandant": "S.Venkateswara Rao",
        "assistant_commandants": [
            {
                "name": "P.Rama Krishna",
                "companies": [
                    {"company": "A Company", "incharge": "K.Suresh, RI"},
                    {"company": "B Company", "incharge": "M.Ramesh, RI"}
                ]
            },
            {
                "name": "K.Srinivasa Murthy",
                "companies": [
                    {"company": "C Company", "incharge": "S.Prasad, RI"},
                    {"company": "D Company", "incharge": "P.Kumar, RI"}
                ]
            },
            {
                "name": "M.Krishna Reddy",
                "companies": [
                    {"company": "E Company", "incharge": "V.Naresh, RI"},
                    {"company": "F Company", "incharge": "R.Ravi, RI"}
                ]
            },
            {
                "name": "V.Rama Murthy",
                "companies": [
                    {"company": "G Company", "incharge": "S.Srinivas, RI"},
                    {"company": "H Company/SDRF", "incharge": "P.Suresh, RI"}
                ]
            },
            {
                "name": "G.Venkata Reddy",
                "companies": []
            }
        ],
        "groups": [
            {"head": "Head Quarters Office", "group": "Head Quarters Office", "incharge": "K.Ramesh, RI"},
            {"head": "Quarter Master Office", "group": "Quarter Master Office", "incharge": "M.Kumar, RI"},
            {"head": "Motor Transport Office", "group": "Motor Transport Office", "incharge": "P.Prasad, RI"},
            {"head": "Training", "group": "Training", "incharge": "R.Suresh, RI"},
            {"head": "Band", "group": "Band", "incharge": "S.Naresh, ARSI"},
            {"head": "JA", "group": "JA", "incharge": "V.Ravi, RSI"},
            {"head": "BATTALION Welfare Office", "group": "BATTALION Welfare Office", "incharge": "K.Srinivas, RI"}
        ]
    },
    16: {
        "additional_commandant": "R.Venkata Rao",
        "assistant_commandants": [
            {
                "name": "S.Krishna Murthy",
                "companies": [
                    {"company": "A Company", "incharge": "P.Ramesh, RI"},
                    {"company": "B Company", "incharge": "K.Suresh, RI"}
                ]
            },
            {
                "name": "M.Srinivasa Reddy",
                "companies": [
                    {"company": "C Company", "incharge": "V.Prasad, RI"},
                    {"company": "D Company", "incharge": "S.Kumar, RI"}
                ]
            },
            {
                "name": "P.Venkata Reddy",
                "companies": [
                    {"company": "E Company", "incharge": "R.Naresh, RI"},
                    {"company": "F Company", "incharge": "M.Ravi, RI"}
                ]
            },
            {
                "name": "K.Rama Reddy",
                "companies": [
                    {"company": "G Company", "incharge": "S.Srinivas, RI"},
                    {"company": "H Company/SDRF", "incharge": "P.Suresh, RI"}
                ]
            },
            {
                "name": "G.Subba Rao",
                "companies": []
            }
        ],
        "groups": [
            {"head": "Head Quarters Office", "group": "Head Quarters Office", "incharge": "V.Kumar, RI"},
            {"head": "Quarter Master Office", "group": "Quarter Master Office", "incharge": "K.Ramesh, RI"},
            {"head": "Motor Transport Office", "group": "Motor Transport Office", "incharge": "M.Prasad, RI"},
            {"head": "Training", "group": "Training", "incharge": "R.Suresh, RI"},
            {"head": "Band", "group": "Band", "incharge": "S.Naresh, ARSI"},
            {"head": "JA", "group": "JA", "incharge": "P.Ravi, RSI"},
            {"head": "BATTALION Welfare Office", "group": "BATTALION Welfare Office", "incharge": "K.Srinivas, RI"}
        ]
    }
}

with app.app_context():
    print("Updating battalion organizational structures...")
    
    for bn_number, org_data in battalion_org_data.items():
        battalion = Battalion.query.filter_by(battalion_number=bn_number).first()
        if battalion:
            # Convert to JSON string
            battalion.organizational_structure = json.dumps(org_data)
            print(f"✓ Updated {battalion.name} with {len(org_data['assistant_commandants'])} Assistant Commandants")
        else:
            print(f"✗ Battalion {bn_number} not found in database")
    
    db.session.commit()
    print("\n✅ All battalion organizational structures have been updated!")
    print("Each battalion now has:")
    print("  - Additional Commandant")
    print("  - 5 Assistant Commandants with their Company assignments")
    print("  - Groups/Departments with RIs")
