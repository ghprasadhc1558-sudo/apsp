import sqlite3
import os

# Database path
db_path = 'instance/apsp.db'

if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# tables to update
tables = {
    'battalion_events': ['image_file', 'pdf_file'],
    'battalion_announcements': ['image_file', 'pdf_file']
}

for table, columns in tables.items():
    print(f"Checking table: {table}")
    try:
        cursor.execute(f"PRAGMA table_info({table})")
        existing_columns = [info[1] for info in cursor.fetchall()]
        
        for col in columns:
            if col not in existing_columns:
                print(f"Adding column {col} to {table}...")
                try:
                    cursor.execute(f"ALTER TABLE {table} ADD COLUMN {col} VARCHAR(255)")
                    print(f"Successfully added {col}")
                except Exception as e:
                    print(f"Error adding {col}: {str(e)}")
            else:
                print(f"Column {col} already exists in {table}")
                
    except Exception as e:
        print(f"Error processing {table}: {str(e)}")

conn.commit()
conn.close()
print("Database schema update complete.")
