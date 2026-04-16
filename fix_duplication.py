
import os

file_path = r'e:\apsp-new-website\APSP_WEBSITE\app\templates\battalion_detail.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = '<!-- Battalion Admin Section - Reverted to Original Style & Location -->'
end_marker = '<!-- Battalion Admin Section -->'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
    print(f"Found duplicate block start at {start_idx} and end at {end_idx}")
    # Keep the end_marker (the start of the second block)
    new_content = content[:start_idx] + content[end_idx:]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully removed duplicate block.")
else:
    print("Could not find both markers or order is wrong.")
    print(f"Start index: {start_idx}")
    print(f"End index: {end_idx}")
