from app import create_app, db
from app.models.battalion import Battalion

app = create_app()

# Complete battalion data for all battalions
all_battalion_data = {
    1: {
        'name': '1st Battalion',
        'district': 'Srikakulam',
        'commandant_name': 'Shri A.K. Sharma',
        'commandant_rank': 'Commandant',
        'commandant_image': 'commandant_1.svg',
        'description': 'The 1st Battalion APSP is stationed at Srikakulam and serves the northern coastal region.',
        'organizational_structure': '''ADDITIONAL COMMANDANT
NAME: S. Ramesh

ASSISTANT COMMANDANTS
- P. Suresh
- K. Prasad

GROUP HEAD - GROUP - GROUP INCHARGE
Head Quarters Office - K.Ajay Kumar, RI
Quarter Master Office - S.Ramesh Kumar, RI
Motor Transport Office - P.Kumar Rao, RI
Training - D.Srinivas, RI
Band - K.Ravi Kumar, ARSI
JA - M.Prasad, RSI
Command And Control - L.Naidu, RI
BATTALION Welfare Office - S.Kumar Reddy, RI

COMPANY HEAD - COMPANY - COMPANY INCHARGE
A Company - K.Ramesh, RI
B Company - P.Suresh Kumar, RI
C Company - D.Prasad, RI
D Company - M.Ravi, RI
E Company - S.Kumar, RI
F Company - K.Naidu, RI'''
    },
    2: {
        'name': '2nd Battalion',
        'district': 'Kurnool',
        'commandant_name': 'Smt. M.DEEPIKA',
        'commandant_rank': 'Commandant',
        'commandant_image': 'commandant_2.svg',
        'description': 'The 2nd Battalion APSP is a special operations battalion based in Kurnool.',
        'organizational_structure': '''ADDITIONAL COMMANDANT
NAME: V.Nagendra Rao

ASSISTANT COMMANDANTS
- D.Venkataramana
- P. Ravi Kiran
- V.Keshava Reddy
- S.Sharfuddin
- S.Mahabboob Basha

GROUP HEAD - GROUP - GROUP INCHARGE
Quarter Master Office - M.C.Shaikshavail, RI
Head Quarters Office - K.Siva Sankar Rao, RI
Motor Transport Office - P.Samba Siva Rao, RI
Band - J.Obulesi, RSI
JA - J.Obulesi, RSI
Training - D.Raju, RI
Command And Control - 
BATTALION Welfare Office - R.Prabhakar Rao, RI

COMPANY HEAD - COMPANY - COMPANY INCHARGE
C Company - L.Srinivasa Reddy, RI
K Company - L.Srinivasa Reddy, RI
E Company - T.Rama Rao, RI
F Company - G.V.Saini Reddy, RI
D/SDRF Company - S.Praveen Kumar, RI
G Company - M.Surya Rao, RI
H Company - S.Ramakrishna RI
A Company - A.Ganapathi RI
B Company - D.Raju RI'''
    },
    4: {
        'name': '4th Battalion',
        'district': 'Rajamahendravaram',
        'commandant_name': 'Shri C. Srinivas',
        'commandant_rank': 'Commandant',
        'commandant_image': 'commandant_4.svg',
        'description': 'The 4th Battalion APSP is stationed at Rajamahendravaram (Rajahmundry).',
        'organizational_structure': '''ADDITIONAL COMMANDANT
NAME: K. Suresh

ASSISTANT COMMANDANTS
- M. Raju
- P. Ramesh

GROUP HEAD - GROUP - GROUP INCHARGE
Head Quarters Office - K.Suresh, RI
Quarter Master Office - M.Raju, RI
Motor Transport Office - P.Ramesh Kumar, RI
Training - D.Prasad, RI
Band - S.Kumar, ARSI
JA - K.Ravi, RSI
Command And Control - M.Naidu, RI
BATTALION Welfare Office - P.Reddy, RI

COMPANY HEAD - COMPANY - COMPANY INCHARGE
A Company - K.Suresh Kumar, RI
B Company - M.Prasad, RI
C Company - P.Kumar, RI
D Company - D.Ravi, RI
E Company - S.Ramesh, RI
F Company - K.Naidu, RI'''
    },
    7: {
        'name': '7th Battalion',
        'district': 'Ongole',
        'commandant_name': 'Shri F. Rajesh',
        'commandant_rank': 'Commandant',
        'commandant_image': 'commandant_7.svg',
        'description': 'The 7th Battalion APSP is stationed at Ongole, serving the Prakasam district.',
        'organizational_structure': '''ADDITIONAL COMMANDANT
NAME: S. Mahesh

ASSISTANT COMMANDANTS
- K. Praveen

GROUP HEAD - GROUP - GROUP INCHARGE
Head Quarters Office - D.Raju, RI
Quarter Master Office - S.Mahesh, RI
Motor Transport Office - K.Praveen Kumar, RI
Training - P.Kumar, RI
Band - M.Ramesh, ARSI
JA - S.Prasad, RSI
Command And Control - K.Suresh, RI
BATTALION Welfare Office - D.Naidu, RI

COMPANY HEAD - COMPANY - COMPANY INCHARGE
A Company - P.Ramesh, RI
B Company - K.Kumar, RI
C Company - M.Prasad, RI
D Company - S.Ravi, RI
E Company - D.Suresh, RI
F Company - P.Naidu, RI'''
    },
    8: {
        'name': '8th Battalion',
        'district': 'Chittoor',
        'commandant_name': 'Shri G. Sandeep',
        'commandant_rank': 'Commandant',
        'commandant_image': 'commandant_8.svg',
        'description': 'The 8th Battalion APSP is stationed at Chittoor district.',
        'organizational_structure': '''ADDITIONAL COMMANDANT
NAME: L. Suresh

ASSISTANT COMMANDANTS
- M. Prasad

GROUP HEAD - GROUP - GROUP INCHARGE
Head Quarters Office - S.Raju, RI
Quarter Master Office - M.Prasad, RI
Motor Transport Office - L.Suresh Kumar, RI
Training - K.Ramesh, RI
Band - P.Kumar, ARSI
JA - D.Ravi, RSI
Command And Control - S.Naidu, RI
BATTALION Welfare Office - M.Reddy, RI

COMPANY HEAD - COMPANY - COMPANY INCHARGE
A Company - K.Suresh, RI
B Company - P.Prasad, RI
C Company - M.Kumar, RI
D Company - S.Ravi, RI
E Company - D.Ramesh, RI
F Company - L.Naidu, RI'''
    }
}

with app.app_context():
    print("Updating all battalion data...\n")
    
    for bn_num, data in all_battalion_data.items():
        battalion = Battalion.query.filter_by(battalion_number=bn_num).first()
        
        if battalion:
            battalion.name = data['name']
            battalion.district = data['district']
            battalion.commandant_name = data['commandant_name']
            battalion.commandant_rank = data['commandant_rank']
            battalion.commandant_image = data['commandant_image']
            battalion.description = data['description']
            battalion.organizational_structure = data['organizational_structure']
            
            print(f"✓ Updated {data['name']}")
            print(f"  Location: {data['district']}")
            print(f"  Commandant: {data['commandant_name']}")
            print(f"  Rank: {data['commandant_rank']}")
            print()
    
    db.session.commit()
    print("✅ All battalion data updated successfully!")
