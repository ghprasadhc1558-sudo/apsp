import sqlite3

conn = sqlite3.connect('instance/apsp.db')
cursor = conn.cursor()

# Get all battalions
cursor.execute('SELECT battalion_number, commandant_image FROM battalion')
battalions = cursor.fetchall()

print("Fixing commandant image paths...")

for bn_num, img_path in battalions:
    if img_path and img_path.startswith('commandants/'):
        # Remove the 'commandants/' prefix
        new_path = img_path.replace('commandants/', '')
        cursor.execute('UPDATE battalion SET commandant_image = ? WHERE battalion_number = ?', (new_path, bn_num))
        print(f"Battalion {bn_num}: {img_path} -> {new_path}")

conn.commit()
print("\n✓ All image paths fixed!")

# Verify
cursor.execute('SELECT battalion_number, commandant_image FROM battalion ORDER BY battalion_number')
results = cursor.fetchall()
print("\nVerification:")
for bn_num, img_path in results:
    print(f"Battalion {bn_num}: {img_path}")

conn.close()
