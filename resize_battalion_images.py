from PIL import Image
import os

def resize_all_battalion_images():
    """
    Resize all battalion images to standard size
    Target: 1400px width with maintained aspect ratio
    """
    battalion_dir = 'app/static/images/battalions'
    target_width = 1400
    
    if not os.path.exists(battalion_dir):
        print(f"❌ Directory not found: {battalion_dir}")
        return
    
    print("🔄 Starting batch resize of battalion images...")
    print(f"📏 Target width: {target_width}px (height auto-calculated)")
    print("-" * 60)
    
    processed = 0
    errors = 0
    
    # Process all jpeg/jpg files in the directory
    for filename in os.listdir(battalion_dir):
        if filename.endswith(('.jpeg', '.jpg', '.JPEG', '.JPG')):
            input_path = os.path.join(battalion_dir, filename)
            
            try:
                with Image.open(input_path) as img:
                    original_size = img.size
                    
                    # Skip if already correct size
                    if img.size[0] == target_width:
                        print(f"⏭️  Skipped {filename} (already {target_width}px)")
                        continue
                    
                    # Calculate new height maintaining aspect ratio
                    width_percent = (target_width / float(img.size[0]))
                    target_height = int((float(img.size[1]) * float(width_percent)))
                    
                    # Resize image
                    resized_img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                    
                    # Save with backup
                    backup_path = input_path + '.backup'
                    if not os.path.exists(backup_path):
                        img.save(backup_path, 'JPEG', quality=95)
                    
                    # Save resized version
                    resized_img.save(input_path, 'JPEG', quality=85, optimize=True)
                    
                    processed += 1
                    print(f"✅ {filename}")
                    print(f"   {original_size[0]}x{original_size[1]} → {target_width}x{target_height}")
                    
            except Exception as e:
                errors += 1
                print(f"❌ Error processing {filename}: {e}")
    
    print("-" * 60)
    print(f"✅ Processed: {processed} images")
    if errors > 0:
        print(f"❌ Errors: {errors}")
    print("\n💡 Original images backed up with .backup extension")
    print("🔄 Refresh browser to see changes")

if __name__ == "__main__":
    resize_all_battalion_images()
