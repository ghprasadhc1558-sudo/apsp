from PIL import Image
import os

def convert_and_resize_specific_battalions():
    """
    Convert PNG to JPEG and resize battalions 1, 4, 7, 8 to match 2nd battalion size
    """
    battalion_dir = 'app/static/images/battalions'
    target_width = 1200  # Standard width matching 2nd battalion
    target_quality = 85  # Good quality JPEG
    
    # Battalions to fix
    battalions_to_fix = [
        ('1th-bn.png', '1st-bn.jpeg'),
        ('8th-bn.png', '8th-bn.jpeg')
    ]
    
    # Create missing battalion placeholders
    missing_battalions = ['4th-bn.jpeg', '7th-bn.jpeg']
    
    print("🔄 Converting and resizing battalion images...")
    print("=" * 60)
    
    # Convert PNG to JPEG and resize
    for old_name, new_name in battalions_to_fix:
        old_path = os.path.join(battalion_dir, old_name)
        new_path = os.path.join(battalion_dir, new_name)
        
        if os.path.exists(old_path):
            try:
                with Image.open(old_path) as img:
                    # Convert RGBA to RGB if needed
                    if img.mode in ('RGBA', 'LA', 'P'):
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    original_size = img.size
                    
                    # Calculate new height maintaining aspect ratio
                    width_percent = (target_width / float(img.size[0]))
                    target_height = int((float(img.size[1]) * float(width_percent)))
                    
                    # Resize image
                    resized_img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                    
                    # Save as JPEG
                    resized_img.save(new_path, 'JPEG', quality=target_quality, optimize=True)
                    
                    new_size = os.path.getsize(new_path)
                    print(f"✅ Converted: {old_name} → {new_name}")
                    print(f"   Size: {original_size[0]}x{original_size[1]} → {target_width}x{target_height}")
                    print(f"   File: {os.path.getsize(old_path) // 1024}KB → {new_size // 1024}KB")
                    print()
                    
            except Exception as e:
                print(f"❌ Error converting {old_name}: {e}")
                print()
    
    # Check for missing battalions
    print("📋 Checking for missing battalion images...")
    print("-" * 60)
    
    for filename in missing_battalions:
        filepath = os.path.join(battalion_dir, filename)
        if not os.path.exists(filepath):
            print(f"⚠️  Missing: {filename}")
            print(f"   Please add this image to: {battalion_dir}")
        else:
            size = os.path.getsize(filepath)
            with Image.open(filepath) as img:
                print(f"✅ Found: {filename} - {img.size[0]}x{img.size[1]} ({size // 1024}KB)")
    
    print()
    print("=" * 60)
    print("✅ Image conversion completed!")
    print("📝 Summary:")
    print("   - Converted PNG to JPEG format")
    print("   - Resized to 1200px width (standard size)")
    print("   - Reduced file size for faster loading")
    print()
    print("🔄 Next steps:")
    print("   1. Refresh browser to see changes")
    print("   2. Upload images for 4th and 7th battalions if missing")
    print("   3. All images will now match 2nd battalion format")

if __name__ == "__main__":
    convert_and_resize_specific_battalions()
