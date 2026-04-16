from PIL import Image
import os

battalion_images_dir = "app/static/images/battalions/"

# Target dimensions based on 2nd battalion (1475x549)
TARGET_WIDTH = 1475
TARGET_HEIGHT = 549

# Images to resize: 1st, 4th, 7th, 8th
images_to_resize = ['1th-bn.jpeg', '7th-bn.jpeg', '8th-bn.jpeg']

print("Resizing Battalion Images to Match Others:")
print("=" * 70)

for filename in images_to_resize:
    filepath = os.path.join(battalion_images_dir, filename)
    
    if not os.path.exists(filepath):
        print(f"⚠️  {filename} not found, skipping...")
        continue
    
    try:
        # Open image
        with Image.open(filepath) as img:
            old_width, old_height = img.size
            old_size = os.path.getsize(filepath) / 1024  # KB
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize to target dimensions
            img_resized = img.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
            
            # Save with high quality
            img_resized.save(filepath, 'JPEG', quality=90, optimize=True)
        
        # Check new size
        new_size = os.path.getsize(filepath) / 1024  # KB
        
        print(f"✅ {filename}")
        print(f"   Old: {old_width}x{old_height} ({old_size:.2f} KB)")
        print(f"   New: {TARGET_WIDTH}x{TARGET_HEIGHT} ({new_size:.2f} KB)")
        print()
        
    except Exception as e:
        print(f"❌ {filename} - Error: {e}")
        print()

print("=" * 70)
print("✨ All battalion images resized to uniform size!")
print(f"Standard size: {TARGET_WIDTH}x{TARGET_HEIGHT}")
