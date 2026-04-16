from PIL import Image
import os

def improve_commandant_photos():
    """
    Improve quality of all commandant photos
    - Resize to 400x400 (high quality display size)
    - Save with quality=95 (high quality JPEG)
    - Convert to square crop
    """
    commandant_dir = 'app/static/images/commandants'
    target_size = 400
    
    if not os.path.exists(commandant_dir):
        print(f"❌ Directory not found: {commandant_dir}")
        return
    
    print("🔄 Improving Commandant Photos Quality...")
    print("=" * 70)
    print(f"📏 Target: {target_size}x{target_size} square, Quality: 95%")
    print("=" * 70)
    
    processed = 0
    errors = 0
    
    for filename in os.listdir(commandant_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')):
            input_path = os.path.join(commandant_dir, filename)
            
            try:
                with Image.open(input_path) as img:
                    original_size = img.size
                    original_format = img.format
                    
                    # Convert to RGB if necessary
                    if img.mode in ('RGBA', 'LA', 'P'):
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        if 'A' in img.mode:
                            background.paste(img, mask=img.split()[-1])
                        else:
                            background.paste(img)
                        img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Make square crop (center)
                    width, height = img.size
                    if width > height:
                        left = (width - height) // 2
                        img = img.crop((left, 0, left + height, height))
                    elif height > width:
                        top = (height - width) // 2
                        img = img.crop((0, top, width, top + width))
                    
                    # Resize to target size with high quality
                    img = img.resize((target_size, target_size), Image.Resampling.LANCZOS)
                    
                    # Save with backup
                    backup_path = input_path + '.backup'
                    if not os.path.exists(backup_path):
                        original_img = Image.open(input_path)
                        original_img.save(backup_path, original_format if original_format else 'JPEG')
                    
                    # Change extension to .jpg for consistency
                    base_name = filename.rsplit('.', 1)[0]
                    new_filename = f"{base_name}.jpg"
                    output_path = os.path.join(commandant_dir, new_filename)
                    
                    # Save with high quality
                    img.save(output_path, 'JPEG', quality=95, optimize=True, subsampling=0)
                    
                    # Remove old file if extension changed
                    if new_filename != filename:
                        os.remove(input_path)
                    
                    processed += 1
                    print(f"✅ {filename} → {new_filename}")
                    print(f"   {original_size[0]}x{original_size[1]} → {target_size}x{target_size}")
                    
            except Exception as e:
                errors += 1
                print(f"❌ Error processing {filename}: {e}")
    
    print("=" * 70)
    print(f"✅ Processed: {processed} photos")
    if errors > 0:
        print(f"❌ Errors: {errors}")
    print("\n💡 Original photos backed up with .backup extension")
    print("🎯 All photos now: 400x400px, 95% quality, square crop")
    print("🔄 Refresh browser to see crystal clear photos!")

if __name__ == "__main__":
    improve_commandant_photos()
