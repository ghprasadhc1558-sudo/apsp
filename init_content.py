#!/usr/bin/env python3
"""Initialize content management data for all pages"""
from app import create_app, db
from app.models.content import Content

app = create_app()

default_content = {
    'home': {
        'title': 'Welcome to Andhra Pradesh Special Police',
        'content': 'Andhra Pradesh Special Police (APSP) is an armed police force serving the state of Andhra Pradesh, India. We are committed to maintaining law and order, and providing security services across the state.',
        'meta_description': 'Official website of Andhra Pradesh Special Police (APSP) - Dedicated to excellence in service and commitment to safety.'
    },
    'about': {
        'title': 'About Andhra Pradesh Special Police',
        'content': '''Andhra Pradesh Special Police (APSP) is a specialized armed police force established to maintain internal security, law and order in the state of Andhra Pradesh. 

Our force consists of multiple battalions strategically located across the state, trained and equipped to handle various security challenges including riot control, VIP security, disaster response, and counter-insurgency operations.

Mission: To serve the people of Andhra Pradesh with dedication, professionalism, and commitment to maintaining peace and security.

Vision: To be recognized as a premier police force known for excellence in service, integrity, and community engagement.''',
        'meta_description': 'Learn about Andhra Pradesh Special Police - our history, mission, vision, and commitment to serving the people.'
    },
    'sdrf': {
        'title': 'State Disaster Response Force (SDRF)',
        'content': '''The State Disaster Response Force (SDRF) is a specialized unit within APSP dedicated to disaster management and emergency response.

Our SDRF teams are trained in:
- Flood and cyclone rescue operations
- Earthquake response and building collapse rescue
- Fire fighting and hazardous material handling
- Medical emergency response
- Search and rescue operations

Available 24/7 for emergency response across Andhra Pradesh.''',
        'meta_description': 'APSP State Disaster Response Force - Professional disaster management and emergency response services.'
    },
    'gallery': {
        'title': 'Photo Gallery',
        'content': 'Explore our photo gallery showcasing training sessions, ceremonies, operations, and various events of Andhra Pradesh Special Police.',
        'meta_description': 'View photos from APSP events, training sessions, ceremonies and operations.'
    },
    'news': {
        'title': 'Latest News & Updates',
        'content': 'Stay updated with the latest news, announcements, and developments from Andhra Pradesh Special Police.',
        'meta_description': 'Latest news and updates from Andhra Pradesh Special Police.'
    },
    'events': {
        'title': 'Events & Activities',
        'content': 'Information about upcoming and past events, training programs, and activities organized by APSP.',
        'meta_description': 'APSP events, training programs and activities calendar.'
    },
    'contacts': {
        'title': 'Contact Us',
        'content': '''Get in touch with Andhra Pradesh Special Police for any queries, complaints, or information.

Headquarters:
APSP Headquarters, Mangalagiri
Guntur District, Andhra Pradesh

Emergency Helpline: 100
Control Room: +91-863-2340100''',
        'meta_description': 'Contact Andhra Pradesh Special Police - Phone numbers, email addresses and office locations.'
    }
}

with app.app_context():
    print("Initializing content management data...")
    
    # Create tables if they don't exist
    db.create_all()
    
    for page, data in default_content.items():
        existing = Content.query.filter_by(page=page).first()
        
        if not existing:
            content = Content(
                page=page,
                title=data['title'],
                content=data['content'],
                meta_description=data.get('meta_description', '')
            )
            db.session.add(content)
            print(f"✓ Added content for {page} page")
        else:
            print(f"- Content for {page} page already exists")
    
    db.session.commit()
    print("\n✅ Content management system initialized successfully!")
