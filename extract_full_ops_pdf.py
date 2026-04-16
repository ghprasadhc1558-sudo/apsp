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
        
        # Extract text from ALL pages to understand structure
        full_text = ""
        
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            # Clean up the text
            text = text.replace('\uf0d8', '•')
            text = text.replace('\uf0a7', '•')
            text = text.replace('\uf0b7', '•')
            print(f"\n{'='*80}\n--- Page {page_num + 1} ---\n{'='*80}\n")
            print(text if text.strip() else "[IMAGE/NO TEXT CONTENT]")
            full_text += f"\n\n=== PAGE {page_num + 1} ===\n\n" + (text if text.strip() else "[IMAGE/NO TEXT CONTENT]")
        
        # Save to file for reference
        with open('sdrf_operations_full.txt', 'w', encoding='utf-8', errors='ignore') as f:
            f.write(full_text)
        print("\n\n" + "="*80)
        print("Full operations content saved to sdrf_operations_full.txt")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
