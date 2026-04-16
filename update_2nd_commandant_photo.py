"""
INSTRUCTIONS TO ADD REAL PHOTO FOR 2ND BATTALION COMMANDANT:

1. Save the image file Smt. M.DEEPIKA's photo to:
   e:\APSP_WEBSITE\app\static\images\commandants\commandant_2_deepika.jpg

2. Then run this script:
   .venv\Scripts\python.exe update_2nd_commandant_photo.py

This will update the database to use the real photo instead of the SVG placeholder.
"""

from app import create_app, db
from app.models.battalion import Battalion
import os

app = create_app()

with app.app_context():
    # Check if the image file exists
    image_path = "app/static/images/commandants/commandant_2_deepika.jpg"
    
    if not os.path.exists(image_path):
        print("\n❌ ERROR: Image file not found!")
        print(f"Please save Smt. M.DEEPIKA's photo to:")
        print(f"   {os.path.abspath(image_path)}")
        print("\nThen run this script again.")
    else:
        # Update 2nd Battalion commandant image
        battalion = Battalion.query.filter_by(battalion_number=2).first()
        
        if battalion:
            battalion.commandant_image = 'commandant_2_deepika.jpg'
            db.session.commit()
            print("\n✅ SUCCESS!")
            print(f"Updated 2nd Battalion commandant image to real photo")
            print(f"Commandant: {battalion.commandant_name}")
            print(f"Image: {battalion.commandant_image}")
            print("\nThe real photo will now appear on the website!")
        else:
            print("\n❌ ERROR: 2nd Battalion not found in database")
