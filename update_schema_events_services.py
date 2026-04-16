import sqlite3
import os

DB_PATH = os.path.join('instance', 'apsp.db')

def migrate():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 1. Add pdf_file column to events table
        print("Checking events table for pdf_file column...")
        cursor.execute("PRAGMA table_info(events)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'pdf_file' not in columns:
            print("Adding pdf_file column to events table...")
            cursor.execute("ALTER TABLE events ADD COLUMN pdf_file TEXT")
            print("pdf_file column added.")
        else:
            print("pdf_file column already exists.")

        # 2. Create services table
        print("Checking if services table exists...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='services'")
        if not cursor.fetchone():
            print("Creating services table...")
            cursor.execute("""
                CREATE TABLE services (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title VARCHAR(200) NOT NULL,
                    url VARCHAR(500) NOT NULL,
                    description TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("services table created.")
        else:
            print("services table already exists.")

        conn.commit()
        print("Migration completed successfully.")

    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
