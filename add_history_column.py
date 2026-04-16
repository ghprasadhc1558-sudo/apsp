from app import create_app, db

app = create_app()

with app.app_context():
    try:
        # Add the history column to the battalion table
        with db.engine.connect() as conn:
            conn.execute(db.text("ALTER TABLE battalion ADD COLUMN history TEXT"))
            conn.commit()
        
        print("✓ Successfully added 'history' column to battalion table!")
        
    except Exception as e:
        print(f"Error: {e}")
        # If column already exists, that's fine
        if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
            print("Column already exists, skipping...")
        else:
            import traceback
            traceback.print_exc()
