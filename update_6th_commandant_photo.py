import sqlite3
import shutil
from pathlib import Path

# Connect to database
conn = sqlite3.connect('instance/apsp.db')
cursor = conn.cursor()

# Update the 6th Battalion commandant image
cursor.execute("""
    UPDATE battalion 
    SET commandant_image = 'commandants/commandant_6.jpg'
    WHERE battalion_number = 6
""")

conn.commit()
print(f"✓ Updated 6th Battalion commandant image to 'commandants/commandant_6.jpg'")

# Verify the update
cursor.execute("SELECT battalion_number, name, commandant_name, commandant_image FROM battalion WHERE battalion_number = 6")
result = cursor.fetchone()
print(f"\nVerification:")
print(f"Battalion: {result[1]}")
print(f"Commandant: {result[2]}")
print(f"Image path: {result[3]}")

conn.close()
