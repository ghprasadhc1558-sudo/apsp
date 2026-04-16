#!/usr/bin/env python3
"""Initialize gallery table in the database"""

from app import create_app, db
from app.models.gallery import GalleryImage

def init_gallery():
    """Create gallery table and add sample data"""
    app = create_app()
    
    with app.app_context():
        # Create gallery table
        db.create_all()
        print("✅ Gallery table created successfully!")
        
        # Check if sample data already exists
        existing_count = GalleryImage.query.count()
        if existing_count > 0:
            print(f"ℹ️  Database already has {existing_count} gallery images")
            return
        
        print("✅ Gallery system is ready!")
        print("\nYou can now:")
        print("1. Login to admin dashboard")
        print("2. Go to Gallery Management section")
        print("3. Add images with title, description, and category")
        print("4. Images will automatically appear on the gallery page")

if __name__ == '__main__':
    init_gallery()
