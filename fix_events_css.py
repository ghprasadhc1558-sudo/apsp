import re

path = r"d:\APSP-WEBSITE\APSP_WEBSITE\app\static\css\style.css"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

new_styles = """
.important-docs-section {
	padding: 20px 0;
	background: #f1f5f9;
}

.important-docs-section .section-title {
	color: #003d82 !important;
	font-size: 20px !important;
	font-weight: 800 !important;
	text-align: center !important;
	margin-bottom: 25px !important;
	text-transform: uppercase;
	letter-spacing: 1px;
	position: relative;
	padding-bottom: 15px;
	border: none !important;
	background: transparent !important;
	display: block !important;
	width: 100% !important;
}

.important-docs-section .section-title::after {
	content: '';
	position: absolute;
	bottom: 0;
	left: 50%;
	transform: translateX(-50%);
	width: 60px;
	height: 3px;
	background: #003d82;
	border-radius: 2px;
}
"""

# Replace the block from .important-docs-section up to the end of .section-title
pattern = re.compile(r'\.important-docs-section\s*\{.*?\.important-docs-section\s+\.section-title\s*\{.*?\}', re.DOTALL)
new_content = pattern.sub(new_styles.strip(), content)

if new_content != content:
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully updated style.css")
else:
    print("Pattern not found in style.css")
