"""
Initialize SDRF Content Management System
This script creates the SDRFContent table and initializes default content
"""
from app import create_app, db
from app.models.sdrf_content import SDRFContent
import os

app = create_app()

with app.app_context():
    print("Initializing SDRF Content Management System...")
    
    # Create tables if they don't exist
    db.create_all()
    print("✓ Database tables created/verified")
    
    # Check if SDRF content already exists
    existing = SDRFContent.query.first()
    
    if not existing:
        # Create default SDRF content
        sdrf_content = SDRFContent()
        
        # Set default About SDRF content (empty - will be filled by admin)
        sdrf_content.about_content = """<h2>About Andhra Pradesh State Disaster Response Force (APSDRF)</h2>
<p>The Andhra Pradesh State Disaster Response Force (APSDRF) is a specialized force constituted under the Disaster Management Act, 2005. It is trained and equipped to respond to natural and man-made disasters including floods, cyclones, earthquakes, building collapses, chemical emergencies, and other disasters.</p>

<h3>Formation and Legal Framework</h3>
<p>APSDRF was officially established in 2006 as part of the National Disaster Management framework. The force operates under the guidance of the State Disaster Management Authority (SDMA) and works in coordination with the National Disaster Response Force (NDRF).</p>

<h3>Units and Deployment</h3>
<p>APSDRF currently comprises multiple battalions strategically located across Andhra Pradesh to ensure rapid response:</p>
<ul>
    <li>1st Battalion APSP - Anantapur (100 personnel)</li>
    <li>3rd Battalion APSP - Kakinada (100 personnel)</li>
    <li>5th Battalion APSP - Vizianagaram (100 personnel)</li>
    <li>6th Battalion APSP - Mangalagiri (100 personnel)</li>
    <li>9th Battalion APSP - Tirupati (100 personnel)</li>
    <li>14th Battalion APSP - Visakhapatnam (100 personnel)</li>
</ul>

<h3>Key Capabilities</h3>
<p>APSDRF teams are trained and equipped for:</p>
<ul>
    <li>Flood and Water Rescue Operations</li>
    <li>Cyclone Response and Relief</li>
    <li>Urban Search and Rescue (USAR)</li>
    <li>Building Collapse Rescue</li>
    <li>HAZMAT Response</li>
    <li>High-Angle Rescue</li>
    <li>Medical First Response</li>
</ul>

<p><strong>Note:</strong> This content can be edited from the admin panel. Go to Admin Dashboard → SDRF Content to modify this text.</p>"""
        
        # Check if default PDFs exist and set paths
        ops_pdf_exists = os.path.exists(os.path.join(app.root_path, 'static', 'operation-sdrf', 'sdrf-operations.pdf'))
        train_pdf_exists = os.path.exists(os.path.join(app.root_path, 'static', 'training-sdrf', 'Advanced Trainings.pdf'))
        
        if ops_pdf_exists:
            sdrf_content.operations_pdf = 'operation-sdrf/sdrf-operations.pdf'
            print("✓ Found existing Operations PDF")
        else:
            sdrf_content.operations_pdf = None
            print("⚠️  No Operations PDF found - Upload from admin panel")
        
        if train_pdf_exists:
            sdrf_content.training_pdf = 'training-sdrf/Advanced Trainings.pdf'
            print("✓ Found existing Training PDF")
        else:
            sdrf_content.training_pdf = None
            print("⚠️  No Training PDF found - Upload from admin panel")
        
        db.session.add(sdrf_content)
        db.session.commit()
        
        print("\n✅ SDRF Content Management System initialized successfully!")
        print("\n" + "="*70)
        print("SDRF Content Configuration:")
        print("="*70)
        print(f"About SDRF Content: {len(sdrf_content.about_content)} characters loaded")
        print(f"Operations PDF: {sdrf_content.operations_pdf or 'Not set'}")
        print(f"Training PDF: {sdrf_content.training_pdf or 'Not set'}")
        print("\n" + "="*70)
        print("Admin Panel Access:")
        print("="*70)
        print("URL: http://localhost:5000/admin/dashboard")
        print("Navigate to 'SDRF Content' section to manage:")
        print("  • Edit About SDRF content (text/HTML)")
        print("  • Upload Operations PDF")
        print("  • Upload Training PDF")
        print("  • Delete and replace PDFs")
        print("="*70)
    else:
        print("\n⚠️  SDRF content already exists in database")
        print("\nCurrent SDRF Configuration:")
        print(f"About SDRF Content: {len(existing.about_content) if existing.about_content else 0} characters")
        print(f"Operations PDF: {existing.operations_pdf or 'Not set'}")
        print(f"Training PDF: {existing.training_pdf or 'Not set'}")
        print("\n✓ No changes made - Database already initialized")
