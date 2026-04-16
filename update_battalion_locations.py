from app import create_app, db
from app.models.battalion import Battalion
import os

app = create_app()

# Battalion data with correct locations
battalion_data = {
    1: {'district': 'Srikakulam', 'name': '1st Battalion'},
    2: {'district': 'Kurnool', 'name': '2nd Battalion'},
    3: {'district': 'Kakinada', 'name': '3rd Battalion'},
    4: {'district': 'Rajamahendravaram', 'name': '4th Battalion'},
    5: {'district': 'Vizianagaram', 'name': '5th Battalion'},
    6: {'district': 'Mangalagiri', 'name': '6th Battalion'},
    7: {'district': 'Ongole', 'name': '7th Battalion'},
    8: {'district': 'Chittoor', 'name': '8th Battalion'},
    9: {'district': 'Venkatagiri', 'name': '9th Battalion'},
    11: {'district': 'Kadapa', 'name': '11th Battalion'},
    14: {'district': 'Anantapuramu', 'name': '14th Battalion'},
    16: {'district': 'Visakhapatnam', 'name': '16th Battalion'}
}

with app.app_context():
    print("Updating battalion locations...")
    
    for bn_num, data in battalion_data.items():
        battalion = Battalion.query.filter_by(battalion_number=bn_num).first()
        
        if battalion:
            battalion.district = data['district']
            battalion.name = data['name']
            print(f"✓ Updated {data['name']} - Location: {data['district']}")
        else:
            # Create new battalion if it doesn't exist
            new_battalion = Battalion(
                battalion_number=bn_num,
                name=data['name'],
                district=data['district'],
                commandant_name=f"Commandant {bn_num}",
                commandant_rank="Commandant",
                commandant_image="default_commandant.png",
                description=f"The {data['name']} APSP is stationed at {data['district']}."
            )
            db.session.add(new_battalion)
            print(f"✓ Created {data['name']} - Location: {data['district']}")
    
    db.session.commit()
    print("\n✅ All battalion locations updated successfully!")
