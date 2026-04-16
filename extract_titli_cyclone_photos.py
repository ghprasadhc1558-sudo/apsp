"""Extract images from TitliCyclonePhotos.pdf and save to SDRF gallery"""
import os
from PIL import Image
import fitz  # PyMuPDF

# Paths
pdf_path = r"E:\apsp data\Website as on 08.09.2025\Events\TitliCyclonePhotos.pdf"
output_dir = r"E:\APSP_WEBSITE\app\static\images\sdrf"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Open the PDF
pdf_document = fitz.open(pdf_path)
print(f"PDF opened: {pdf_path}")
print(f"Total pages: {len(pdf_document)}")

image_count = 0

# Iterate through each page
for page_num in range(len(pdf_document)):
    page = pdf_document[page_num]
    print(f"\nProcessing page {page_num + 1}...")
    
    # Get images from the page
    image_list = page.get_images(full=True)
    print(f"Found {len(image_list)} images on page {page_num + 1}")
    
    # Extract each image
    for img_index, img_info in enumerate(image_list):
        xref = img_info[0]
        
        # Extract the image
        base_image = pdf_document.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        
        # Generate filename
        image_filename = f"titli_cyclone_{image_count + 1}.{image_ext}"
        image_path = os.path.join(output_dir, image_filename)
        
        # Save the image
        with open(image_path, "wb") as img_file:
            img_file.write(image_bytes)
        
        print(f"  Saved: {image_filename}")
        image_count += 1

pdf_document.close()
print(f"\n✓ Successfully extracted {image_count} images to {output_dir}")
