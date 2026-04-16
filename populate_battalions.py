from app import create_app, db
from app.models.battalion import Battalion

app = create_app()

battalions_data = [
    {"battalion_number": 1, "name": "1st Battalion", "district": "Vijayawada", "commandant_name": "Shri A.K. Sharma", "commandant_rank": "Commandant", "commandant_image": "1st.jpg", "ri_1": "S. Ramesh", "ri_2": "P. Suresh", "ri_3": "K. Prasad", "description": "Elite battalion stationed in Vijayawada."},
    {"battalion_number": 2, "name": "2nd Battalion", "district": "Kurnool", "commandant_name": "Smt M. Deepika", "commandant_rank": "Commandant", "commandant_image": "2nd.jpg", "ri_1": "M.C. Shaikshavali", "ri_2": "K. Siva Sankar Rao", "ri_3": "P. Samba Siva Rao", "description": "Special operations battalion based in Kurnool."},
    {"battalion_number": 3, "name": "3rd Battalion", "district": "Kakinada", "commandant_name": "Shri B. Ramesh", "commandant_rank": "Commandant", "commandant_image": "3rd.jpg", "ri_1": "T. Srinivas", "ri_2": "D. Raju", "ri_3": "S. Prasad", "description": "Coastal security battalion in Kakinada."},
    {"battalion_number": 4, "name": "4th Battalion", "district": "Mangalagiri", "commandant_name": "Shri C. Srinivas", "commandant_rank": "Commandant", "commandant_image": "4th.jpg", "ri_1": "K. Suresh", "ri_2": "M. Raju", "ri_3": "P. Ramesh", "description": "Strategic battalion in Mangalagiri."},
    {"battalion_number": 5, "name": "5th Battalion", "district": "Vizianagaram", "commandant_name": "Shri D. Prasad", "commandant_rank": "Commandant", "commandant_image": "5th.jpg", "ri_1": "S. Naveen", "ri_2": "L. Rakesh", "ri_3": "G. Sandeep", "description": "Northern region battalion in Vizianagaram."},
    {"battalion_number": 6, "name": "6th Battalion", "district": "Anantapur", "commandant_name": "Shri E. Suresh", "commandant_rank": "Commandant", "commandant_image": "6th.jpg", "ri_1": "J. Naveen", "ri_2": "K. Suresh", "ri_3": "S. Praveen", "description": "Border security battalion in Anantapur."},
    {"battalion_number": 7, "name": "7th Battalion", "district": "Guntur", "commandant_name": "Shri F. Rajesh", "commandant_rank": "Commandant", "commandant_image": "7th.jpg", "ri_1": "D. Raju", "ri_2": "S. Mahesh", "ri_3": "K. Praveen", "description": "Central region battalion in Guntur."},
    {"battalion_number": 8, "name": "8th Battalion", "district": "Eluru", "commandant_name": "Shri G. Sandeep", "commandant_rank": "Commandant", "commandant_image": "8th.jpg", "ri_1": "S. Raju", "ri_2": "M. Prasad", "ri_3": "L. Suresh", "description": "Rapid response battalion in Eluru."},
    {"battalion_number": 9, "name": "9th Battalion", "district": "Ongole", "commandant_name": "Shri H. Praveen", "commandant_rank": "Commandant", "commandant_image": "9th.jpg", "ri_1": "K. Naveen", "ri_2": "S. Ramesh", "ri_3": "P. Suresh", "description": "Coastal operations battalion in Ongole."},
    {"battalion_number": 11, "name": "11th Battalion", "district": "Kadapa", "commandant_name": "Shri J. Naveen", "commandant_rank": "Commandant", "commandant_image": "11th.jpg", "ri_1": "S. Prasad", "ri_2": "L. Rakesh", "ri_3": "G. Sandeep", "description": "Southern region battalion in Kadapa."},
    {"battalion_number": 14, "name": "14th Battalion", "district": "Srikakulam", "commandant_name": "Shri K. Suresh", "commandant_rank": "Commandant", "commandant_image": "14th.jpg", "ri_1": "S. Naveen", "ri_2": "L. Rakesh", "ri_3": "G. Sandeep", "description": "Specialized battalion in Srikakulam."},
    {"battalion_number": 16, "name": "16th Battalion", "district": "Tirupati", "commandant_name": "Shri L. Rakesh", "commandant_rank": "Commandant", "commandant_image": "16th.jpg", "ri_1": "S. Prasad", "ri_2": "L. Suresh", "ri_3": "K. Praveen", "description": "VIP security battalion in Tirupati."},
]

with app.app_context():
    # Create all tables first
    db.create_all()
    
    # Clear existing battalions
    Battalion.query.delete()
    
    # Add all battalions
    for data in battalions_data:
        battalion = Battalion(**data)
        db.session.add(battalion)
    
    db.session.commit()
    print(f'Successfully added {len(battalions_data)} battalions to the database!')
