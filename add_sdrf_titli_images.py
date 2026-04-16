"""Add Titli Cyclone SDRF images to the gallery database"""
from app import create_app, db
from app.models.gallery import GalleryImage
import os

app = create_app()

with app.app_context():
    # SDRF images directory
    sdrf_dir = "sdrf"
    
    # Get all titli cyclone images
    image_files = [f"titli_cyclone_{i}.jpeg" for i in range(1, 15)]
    
    print(f"Adding {len(image_files)} Titli Cyclone SDRF images to gallery...")
    
    added_count = 0
    for image_file in image_files:
        full_path = os.path.join(sdrf_dir, image_file)
        
        # Check if image already exists in database
        existing = GalleryImage.query.filter_by(filename=full_path).first()
        
        if not existing:
            gallery_image = GalleryImage(
                filename=full_path,
                title=f"Titli Cyclone SDRF Response - {image_file.split('_')[-1].split('.')[0]}",
                description="APSP SDRF team's response during Titli Cyclone disaster operations",
                category="SDRF Operations",
                image_path=full_path,
                is_active=True
            )
            db.session.add(gallery_image)
            added_count += 1
            print(f"  ✓ Added: {image_file}")
        else:
            print(f"  - Skipped (already exists): {image_file}")
    
    db.session.commit()
    print(f"\n✓ Successfully added {added_count} new images to the gallery!")
    print(f"Total SDRF Titli Cyclone images in gallery: {GalleryImage.query.filter(GalleryImage.filename.like('sdrf/titli_cyclone%')).count()}")
