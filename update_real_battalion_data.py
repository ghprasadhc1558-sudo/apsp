from app import create_app, db
from app.models.battalion import Battalion

app = create_app()

# Real battalion data from official sources
battalion_updates = {
    3: {
        'name': '3rd Battalion',
        'district': 'Kakinada',
        'commandant_name': 'Sri M. Nagendra Rao',
        'commandant_rank': 'I/C Commandant',
        'commandant_image': 'commandant_3.svg',
        'organizational_structure': '''ADDITIONAL COMMANDANT
NAME: S.Devananda Rao

ASSISTANT COMMANDANTS
- B.Chandra Shekararao
- S.Manmadha Rao
- Sri M.Mohana Rao

GROUP HEAD - GROUP - GROUP INCHARGE
Head Quarters Office - K.Ajay Kumar, RI
Quarter Master Office - B.Vitalleswara Rao, RI
Motor Transport Office - D.G.V.B.S.V.Prasad, RI
Band - Phara rao, ARSI
JA - A.Manikanta, RSI
Command And Control - Emai Id
BATTALION Welfare Office - K.Ravishankar, RI

COMPANY HEAD - COMPANY - COMPANY INCHARGE
C Company - D.G.V.B.S.V.Prasad, RI
B Company - D.Srinivasa Rao, RSI
F Company - D.G.V.B.S.V.Prasad, RI
H Company - K.Satyanarayana, RI
Training - K.Ajay Kumar, RI
E Company - K.Satyanarayana, RI
A Company - K.Satyanarayana, RI
D Company - K.Babu Rao, RI
K/SDRF Company - V.Ramu, RI'''
    },
    5: {
        'name': '5th Battalion',
        'district': 'Vizianagaram',
        'commandant_name': 'Smt. Malika Garg',
        'commandant_rank': 'Commandant, IPS',
        'commandant_image': 'commandant_5.svg',
        'organizational_structure': '''ADDITIONAL COMMANDANT
NAME: M.Venkateswara Rao

ASSISTANT COMMANDANTS
- D.V.Ramana Murthy
- G.V.Prabhakara Rao
- S.Bapujee
- P.Sarath Babu
- G.Laxmi Narayana

GROUP HEAD - GROUP - GROUP INCHARGE
Head Quarters Office - G.Ravindra Kumar, RI
Quarter Master Office - Y.V.Kesava Ramu, RI
Motor Transport Office - A.Srinivasa Rao, RI
Training - M.Srinu, RI
Band - G.Krishna Rao, ARSI
JA - M.Manohara Rao, RSI
Command And Control - 
BATTALION Welfare Office - N.Ganesh, RI

COMPANY HEAD - COMPANY - COMPANY INCHARGE
A Company - P.Sudhakara Babu, RI
G Company - M.Nooka Raju, RI
C Company - K.K.M.Raju, RI
E Company - S.Raju, RI
B Company - K.Samarjana Rao, RI
D Company - U.Danayya, RI
F Company - G.Damodara Rao, RI
H Company/SDRF - S.Chandra Sekhar, RI'''
    },
    6: {
        'name': '6th Battalion',
        'district': 'Mangalagiri',
        'commandant_name': 'K. Nagesh Babu',
        'commandant_rank': 'Commandant',
        'commandant_image': 'commandant_6.svg',
        'organizational_structure': '''ADDITIONAL COMMANDANT
NAME: D.Aseervadam

ASSISTANT COMMANDANTS
- P.V.Hanumanthu
- Sri U.Ravi
- K.Venkateswara Rao
- D.Venkateswara Rao

GROUP HEAD - GROUP - GROUP INCHARGE
Head Quarters Office - M.Venkata Rao, RI
Quarter Master Office - S.Srinivasa Rao, RI
Motor Transport Office - B.Venkata Rao, RI
Training - A.Simhardri Naidu, RI
Band - S.Srinivasulu, ARSI
JA - P.Ibrahim Khan, RSI
Command And Control - 
BATTALION Welfare Office - G.Suresh, RI

COMPANY HEAD - COMPANY - COMPANY INCHARGE
A Company - K.Yesu Dasu, RI
C Company - B. Ramulu, RI
E Company - Y.Venkateswarlu, RI
D Company - B.Rajasekharani, RI
H Company - A.Sateesh, RI
K Company - M.Girish Naidu, RI
B Company - V.L.C'Indra Sekhar, RI
G Company - K.P.Das, RI
F Company/SDRF - K.Venkateswarlu, RI'''
    },
    9: {
        'name': '9th Battalion',
        'district': 'Venkatagiri',
        'commandant_name': 'Commandant',
        'commandant_rank': 'Commandant',
        'commandant_image': 'commandant_9.svg',
        'organizational_structure': '''ADDITIONAL COMMANDANT
NAME: M.Arun Bose

ASSISTANT COMMANDANTS
- N.H. Vijayanand
- B.Anand Kanna

GROUP HEAD - GROUP - GROUP INCHARGE
Head Quarters Office - U.Swaiah,RI
Quarter Master Office - P.Venkateswarlu, RI
Motor Transport Office - S.Govindaraju, RI
Training - P.Venkateswarlu, RI
Band - G.R.Ramanaiah, ARSI
JA - K.Dhileep, RSI
Command And Control - 
BATTALION Welfare Office - J.N.V.Satyanarayana, RI

COMPANY HEAD - COMPANY - COMPANY INCHARGE
A Company - Y.Jalaiah, RI
B Company - V.Rajasekhar, RI
C Company - G.Lakshmaiah, RI
D Company - M. Durvasulu, RI
E Company - B.Bhasker, RI
F Company - N. Madana Mohan, RI
G Company/SDRF - Ch.Srinivasa Reddy, RI'''
    },
    11: {
        'name': '11th Battalion',
        'district': 'Kadapa',
        'commandant_name': 'K. Ananda Reddy',
        'commandant_rank': 'Commandant',
        'commandant_image': 'commandant_11.svg',
        'organizational_structure': '''ADDITIONAL COMMANDANT
NAME: D. Nageswarappa

ASSISTANT COMMANDANTS
- M.Theophilus
- K.Venkat Reddy
- P.N.D.Prasad
- B.Venkata Sruudu

GROUP HEAD - GROUP - GROUP INCHARGE
Head Quarters Office - K.Nagaraju, RI
Quarter Master Office - S. Ali Basha, RI
Motor Transport Office - M. Anjaneyulu, RI
Training - K. Nagaraju, RI
Band - T.V.Ramana, ARSI
JA - S.V.Ramana, RSI
Command And Control - 
BATTALION Welfare Office - S.Ali Basha, RI

COMPANY HEAD - COMPANY - COMPANY INCHARGE
B Company - M. Anjaneyulu, RI
C Company - KVB Varma RI
G Company - K.Nagaraju RI
A Company - M.Anjaneyulu, RI
BTC Training - K.Nagaraju RI
D Company - V.Krishnaiah, RI
F Company - P.T.Prasad RI
E Company - KV Ramana, RI'''
    },
    14: {
        'name': '14th Battalion',
        'district': 'Anantapuramu',
        'commandant_name': 'Sri K. Prabhu Kumar',
        'commandant_rank': 'Commandant',
        'commandant_image': 'commandant_14.svg',
        'organizational_structure': '''ADDITIONAL COMMANDANT
NAME: V.Kesava Reddy

ASSISTANT COMMANDANTS
- Sri S.Mahaboob Basha
- Sri G.Prasad Reddy
- Sri B.Suneel
- Sri B.Venkata Siva Reddy
- Sri R.Wilson Care
- S.Mahaboob Basha

GROUP HEAD - GROUP - GROUP INCHARGE
Head Quarters Office - S.Nagendra, RI
Quarter Master Office - A.NarayanaSwamy, RSI
Motor Transport Office - M.Nagendra Babu, RI
Training - B.Krishna Naik, RSI
Band - K.Aadinarayana, ARSI
JA - M. Ramanjaneyulu, RSI
Command And Control - 
BATTALION Welfare Office - V.Sreedhar, RSI

COMPANY HEAD - COMPANY - COMPANY INCHARGE
A Company - G.Pradeepkumar RI
B Company - Sri S.Koteswara Rao, RI
C Company - P.Khaleel Hussain, RSI
D Company - N. Maruthi Kumar, RI
E Company - B.krishna Naik, RSI
F Company - K.Laxma Naik, RI
G Company - S.Nagendra, RI'''
    },
    16: {
        'name': '16th Battalion',
        'district': 'Visakhapatnam',
        'commandant_name': 'K.V. Murali Krishna',
        'commandant_rank': 'Commandant, IPS',
        'commandant_image': 'commandant_16.svg',
        'organizational_structure': '''ADDITIONAL COMMANDANT
NAME: CH.V.S.PADMANABHA RAJU

ASSISTANT COMMANDANTS
- P.SATYAM
- G.ELIA SAGAR
- V.NARAYANA RAO
- N.MURALIDHAR
- B.RAMAKRISHNA

GROUP HEAD - GROUP - GROUP INCHARGE
Head Quarters Office - K.TULASI RAO, RI
Quarter Master Office - T.RAVI KUMAR, RI
Motor Transport Office - J.CHENNAKESAVA RAO, RI
Training - B.M.MOHANA RAO, RI
Band - K. PANDU RANGA RAO, HC 259
JA - P.Satyamarrayana, RSI
Command And Control - 
BATTALION Welfare Office - G.Narayana, RI

COMPANY HEAD - COMPANY - COMPANY INCHARGE
C Company - P.Duryodhana Rao, RI
Training - B.M.MOHANA RAO, RI
G Company - K.V Ranga Rao,RI
D/SDRF Company - T.Ramakrishna, RI
E Company - B.Narayana Rao, RI
F Company - D.Madhu sudhana Rao, RI
A Company - J.SRINIVAS RAO, RI
B Company - S.V.RAMANA, RI'''
    }
}

with app.app_context():
    print("Updating battalion data with real information...\n")
    
    for bn_num, data in battalion_updates.items():
        battalion = Battalion.query.filter_by(battalion_number=bn_num).first()
        
        if battalion:
            battalion.name = data['name']
            battalion.district = data['district']
            battalion.commandant_name = data['commandant_name']
            battalion.commandant_rank = data['commandant_rank']
            battalion.commandant_image = data['commandant_image']
            battalion.organizational_structure = data['organizational_structure']
            
            print(f"✓ Updated {data['name']}")
            print(f"  Location: {data['district']}")
            print(f"  Commandant: {data['commandant_name']}")
            print(f"  Rank: {data['commandant_rank']}")
            print()
    
    db.session.commit()
    print("✅ All battalion data updated successfully with real information!")
