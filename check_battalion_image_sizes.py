from PIL import Image
import os

battalion_images_dir = "app/static/images/battalions/"

print("Current Battalion Image Sizes:")
print("=" * 60)

for filename in sorted(os.listdir(battalion_images_dir)):
    if filename.endswith('.jpeg'):
        filepath = os.path.join(battalion_images_dir, filename)
        try:
            with Image.open(filepath) as img:
                width, height = img.size
                file_size = os.path.getsize(filepath) / 1024  # KB
                print(f"{filename:15} - {width:4}x{height:3} - {file_size:6.2f} KB")
        except Exception as e:
            print(f"{filename:15} - Error: {e}")

print("=" * 60)
