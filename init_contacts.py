"""
Initialize Contact Information
This script creates the ContactInfo table and adds default contact data
"""
from app import create_app, db
from app.models.contact import ContactInfo

app = create_app()

with app.app_context():
    print("Initializing Contact Information...")
    
    # Create tables if they don't exist
    db.create_all()
    print("✓ Database tables created/verified")
    
    # Check if contact info already exists
    existing = ContactInfo.query.first()
    
    if not existing:
        # Create default contact information
        contact_info = ContactInfo()
        
        # Set default phone numbers
        default_phones = [
            "+91-866-2434567",
            "+91-866-2434890",
            "100 (Emergency)"
        ]
        contact_info.set_phone_numbers(default_phones)
        
        # Set default email addresses
        default_emails = [
            "info@apsp.ap.gov.in",
            "dgapsp@ap.gov.in",
            "complaints@apsp.ap.gov.in"
        ]
        contact_info.set_email_addresses(default_emails)
        
        # Set default office address
        contact_info.office_address = """APSP Headquarters
Vijayawada, Andhra Pradesh
PIN: 520001"""
        
        db.session.add(contact_info)
        db.session.commit()
        
        print("\n✅ Contact information initialized successfully!")
        print("\nDefault Contact Information:")
        print(f"Phone Numbers: {', '.join(default_phones)}")
        print(f"Email Addresses: {', '.join(default_emails)}")
        print(f"Office Address:\n{contact_info.office_address}")
    else:
        print("\n⚠️  Contact information already exists in database")
        print("\nCurrent Contact Information:")
        print(f"Phone Numbers: {', '.join(existing.get_phone_numbers())}")
        print(f"Email Addresses: {', '.join(existing.get_email_addresses())}")
        print(f"Office Address:\n{existing.office_address}")
    
    print("\n" + "="*60)
    print("You can now manage contact information from the admin dashboard!")
    print("URL: http://localhost:5000/admin/dashboard")
    print("="*60)
