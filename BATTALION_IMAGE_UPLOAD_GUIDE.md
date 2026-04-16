"""
Instructions for Uploading Battalion Building Photos
=====================================================

For battalions 1, 4, 7, 8 (and all battalions):

1. Image Size Requirements:
   - Recommended Width: 1200-1600 pixels
   - Recommended Height: 600-900 pixels
   - Aspect Ratio: 16:9 or 4:3 works best
   - Format: JPEG (.jpg or .jpeg)
   - File Size: Keep under 2MB for faster loading

2. Image Location:
   Place your image file in: app/static/images/battalions/
   
3. Naming Convention:
   - 1st Battalion: 1st-bn.jpeg
   - 2nd Battalion: 2nd-bn.jpeg
   - 3rd Battalion: 3rd-bn.jpeg
   - 4th Battalion: 4th-bn.jpeg
   - 5th Battalion: 5th-bn.jpeg
   - 6th Battalion: 6th-bn.jpeg
   - 7th Battalion: 7th-bn.jpeg
   - 8th Battalion: 8th-bn.jpeg
   - 9th Battalion: 9th-bn.jpeg
   - 10th Battalion: 10th-bn.jpeg
   - 11th Battalion: 11th-bn.jpeg
   - 12th Battalion: 12th-bn.jpeg
   - 13th Battalion: 13th-bn.jpeg
   - 14th Battalion: 14th-bn.jpeg
   - 15th Battalion: 15th-bn.jpeg
   - 16th Battalion: 16th-bn.jpeg

4. Steps to Upload:
   a) Prepare your image with the recommended size
   b) Name it correctly (e.g., 1st-bn.jpeg for 1st Battalion)
   c) Copy the file to: E:\APSP_WEBSITE\app\static\images\battalions\
   d) Refresh the battalion page to see the new image

5. Image Processing Tips:
   - Use tools like Paint, Photoshop, or online tools to resize
   - Maintain good quality while keeping file size reasonable
   - Crop to show the important parts of the building
   - Ensure good lighting and clarity

6. Current Display Settings:
   - Images now display in full width with original aspect ratio
   - No sides will be cut off
   - object-fit: contain ensures entire image is visible
   - Background color: light gray (#f8f9fa)

7. If Image Doesn't Appear:
   - Check file name is exactly correct (case-sensitive)
   - Verify file is in correct folder
   - Clear browser cache (Ctrl+Shift+R)
   - Check file permissions

Example Python Script to Resize Images:
"""

from PIL import Image
import os

def resize_battalion_image(input_path, output_path, target_width=1400):
    """
    Resize battalion image to target width while maintaining aspect ratio
    """
    try:
        with Image.open(input_path) as img:
            # Calculate new height maintaining aspect ratio
            width_percent = (target_width / float(img.size[0]))
            target_height = int((float(img.size[1]) * float(width_percent)))
            
            # Resize image
            resized_img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
            # Save with good quality
            resized_img.save(output_path, 'JPEG', quality=85, optimize=True)
            print(f"✅ Successfully resized: {output_path}")
            print(f"   Original: {img.size[0]}x{img.size[1]}")
            print(f"   Resized: {target_width}x{target_height}")
            
    except Exception as e:
        print(f"❌ Error resizing image: {e}")

# Example usage:
# resize_battalion_image('original_image.jpg', 'app/static/images/battalions/1st-bn.jpeg')
