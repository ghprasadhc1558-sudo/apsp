import os

# Create commandants directory if it doesn't exist
commandants_dir = "app/static/images/commandants"
os.makedirs(commandants_dir, exist_ok=True)

# Battalion commandants data
commandants = {
    1: {"name": "Shri A.K. Sharma", "initials": "AKS"},
    2: {"name": "Smt. M.DEEPIKA", "initials": "MD"},
    3: {"name": "Shri B. Ramesh", "initials": "BR"},
    4: {"name": "Shri C. Srinivas", "initials": "CS"},
    5: {"name": "Shri D. Prasad", "initials": "DP"},
    6: {"name": "Shri Srilina Prasad", "initials": "SP"},
    7: {"name": "Shri F. Rajesh", "initials": "FR"},
    8: {"name": "Shri G. Sandeep", "initials": "GS"},
    9: {"name": "Shri H. Praveen", "initials": "HP"},
    11: {"name": "Shri J. Naveen", "initials": "JN"},
    14: {"name": "Shri K. Suresh", "initials": "KS"},
    16: {"name": "Shri L. Rakesh", "initials": "LR"}
}

# Color schemes for different battalions
colors = [
    "#003d82", "#0056b3", "#1976d2", "#2196f3",
    "#004d40", "#00796b", "#009688", "#26a69a",
    "#6a1b9a", "#7b1fa2", "#8e24aa", "#9c27b0"
]

# Create SVG placeholder images for each commandant
for idx, (bn_num, data) in enumerate(commandants.items()):
    color = colors[idx % len(colors)]
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300" viewBox="0 0 300 300">
  <defs>
    <linearGradient id="grad{bn_num}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{color};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{color}cc;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="300" height="300" fill="url(#grad{bn_num})"/>
  <text x="150" y="130" font-family="Arial, sans-serif" font-size="80" font-weight="bold" 
        fill="white" text-anchor="middle">{data['initials']}</text>
  <text x="150" y="200" font-family="Arial, sans-serif" font-size="20" font-weight="600" 
        fill="rgba(255,255,255,0.9)" text-anchor="middle">{bn_num}th Bn</text>
</svg>'''
    
    filename = f"commandant_{bn_num}.svg"
    filepath = os.path.join(commandants_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print(f"✓ Created {filename} for {data['name']}")

print(f"\n✅ All {len(commandants)} commandant photos created successfully in {commandants_dir}/")
