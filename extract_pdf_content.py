import PyPDF2
import sys
import io

# Set UTF-8 encoding for output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')

pdf_path = r'app\static\aboutsdrf\sdrf 1 23.pdf'

try:
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        print(f"Total pages: {num_pages}\n")
        print("="*80)
        
        # Extract text from all pages
        full_text = ""
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            # Clean up the text a bit
            text = text.replace('\uf0d8', '•')  # Replace bullet character
            text = text.replace('\uf0a7', '•')
            text = text.replace('\uf0b7', '•')
            print(f"\n{'='*80}\n--- Page {page_num + 1} ---\n{'='*80}\n")
            print(text)
            full_text += text + "\n\n"
        
        # Save to file for reference
        with open('sdrf_extracted_content.txt', 'w', encoding='utf-8', errors='ignore') as f:
            f.write(full_text)
        print("\n\n" + "="*80)
        print("Content saved to sdrf_extracted_content.txt")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
