"""
Initialize the Events table in the database
"""
from app import create_app, db
from app.models.event import Event

def init_events():
    app = create_app()
    
    with app.app_context():
        # Create events table
        db.create_all()
        print("✓ Events table created successfully!")
        
        # Check if any events exist
        event_count = Event.query.count()
        print(f"✓ Current events count: {event_count}")
        
        if event_count == 0:
            print("You can now add events through the admin dashboard!")

if __name__ == '__main__':
    init_events()
