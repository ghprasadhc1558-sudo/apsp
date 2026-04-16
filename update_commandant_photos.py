from app import create_app, db
from app.models.battalion import Battalion

app = create_app()

# Updated commandant data with photo filenames
commandant_updates = {
    1: {'commandant_image': 'commandant_1.svg'},
    2: {'commandant_image': 'commandant_2.svg'},
    3: {'commandant_image': 'commandant_3.svg'},
    4: {'commandant_image': 'commandant_4.svg'},
    5: {'commandant_image': 'commandant_5.svg'},
    6: {'commandant_image': 'commandant_6.svg'},
    7: {'commandant_image': 'commandant_7.svg'},
    8: {'commandant_image': 'commandant_8.svg'},
    9: {'commandant_image': 'commandant_9.svg'},
    11: {'commandant_image': 'commandant_11.svg'},
    14: {'commandant_image': 'commandant_14.svg'},
    16: {'commandant_image': 'commandant_16.svg'}
}

with app.app_context():
    print("Updating commandant photos...")
    
    for bn_num, data in commandant_updates.items():
        battalion = Battalion.query.filter_by(battalion_number=bn_num).first()
        
        if battalion:
            battalion.commandant_image = data['commandant_image']
            print(f"✓ Updated {battalion.name} - Photo: {data['commandant_image']}")
    
    db.session.commit()
    print("\n✅ All commandant photos updated successfully!")
