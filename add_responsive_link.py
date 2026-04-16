import os

TEMPLATES_DIR = r'e:\apsp-new-website\APSP_WEBSITE\app\templates'
RESPONSIVE_LINK = '    <link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/responsive.css\') }}">'

def process_files():
    count = 0
    for filename in os.listdir(TEMPLATES_DIR):
        if not filename.endswith('.html'):
            continue
            
        filepath = os.path.join(TEMPLATES_DIR, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'css/responsive.css' in content:
            print(f"Skipping {filename} (already present)")
            continue
            
        if "filename='css/style.css'" in content:
            # Pattern 1: Single quotes
            target = "filename='css/style.css') }}\">"
            if target in content:
                new_content = content.replace(target, target + '\n' + RESPONSIVE_LINK)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {filename}")
                count += 1
                continue

            # Pattern 2: Double quotes in filename (just in case)
            target_dq = 'filename="css/style.css") }}\">'
            if target_dq in content:
                new_content = content.replace(target_dq, target_dq + '\n' + RESPONSIVE_LINK)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {filename}")
                count += 1
                continue
                
            print(f"Warning: style.css found but pattern mismatch in {filename}")
        else:
            print(f"Skipping {filename} (style.css not found)")

    print(f"Total files updated: {count}")

if __name__ == '__main__':
    process_files()
