import PyPDF2
import sys
import io

# Set UTF-8 encoding for output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')

pdf_path = r'app\static\operation-sdrf\sdrf-operations.pdf'

try:
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        print(f"Total pages in PDF: {num_pages}\n")
        print("="*80)
        
        # Extract text from pages 25 to 63 (index 24 to 62)
        full_text = ""
        start_page = 24  # Page 25 (0-indexed)
        end_page = min(62, num_pages - 1)  # Page 63 or last page
        
        for page_num in range(start_page, end_page + 1):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            # Clean up the text
            text = text.replace('\uf0d8', '•')
            text = text.replace('\uf0a7', '•')
            text = text.replace('\uf0b7', '•')
            print(f"\n{'='*80}\n--- Page {page_num + 1} ---\n{'='*80}\n")
            print(text)
            full_text += f"\n\n=== PAGE {page_num + 1} ===\n\n" + text
        
        # Save to file for reference
        with open('sdrf_operations_extracted.txt', 'w', encoding='utf-8', errors='ignore') as f:
            f.write(full_text)
        print("\n\n" + "="*80)
        print("Operations content saved to sdrf_operations_extracted.txt")
        print(f"Extracted pages {start_page + 1} to {end_page + 1}")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
