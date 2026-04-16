from app import create_app, db
from sqlalchemy import text

app = create_app()

def migrate():
    with app.app_context():
        # Check if column exists
        try:
            with db.engine.connect() as conn:
                # Add column
                try:
                    conn.execute(text("ALTER TABLE sdrf_content ADD COLUMN about_pdf VARCHAR(500)"))
                    print("Added about_pdf column")
                except Exception as e:
                    print(f"Column might already exist: {e}")

                # Update existing record with default PDF
                conn.execute(text("UPDATE sdrf_content SET about_pdf = 'aboutsdrf/sdrf 1 23.pdf'"))
                conn.commit()
                print("Updated existing records with default PDF")
                
        except Exception as e:
            print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate()
