from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, current_app, make_response
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from .models.user import User
from .models.battalion import Battalion
from .models.gallery import GalleryImage
from .models.event import Event
from .models.banner import Banner
from .models.announcement import Announcement
from .models.contact import ContactInfo
from .models.sdrf_content import SDRFContent
from .models.officer import Officer
from .models.service import Service
from . import db, login_manager
import os
import json

bp = Blueprint('main', __name__)

@bp.app_context_processor
def inject_nav_data():
    from .models.service import Service
    from .models.event import Event
    nav_services = Service.query.order_by(Service.created_at.desc()).limit(5).all()
    nav_events = Event.query.order_by(Event.created_at.desc()).limit(10).all()
    return dict(nav_services=nav_services, nav_events=nav_events)

@bp.route('/battalion/<int:battalion_id>')
def battalion_detail(battalion_id):
    battalion = Battalion.query.filter_by(battalion_number=battalion_id).first()
    if not battalion:
        return "Battalion not found", 404
    
    # Parse organizational structure
    org_data = None
    if battalion.organizational_structure:
        try:
            # Try to parse as JSON first (new format)
            import json
            org_data = json.loads(battalion.organizational_structure)
        except (json.JSONDecodeError, ValueError):
            # Fall back to text parsing (old format)
            org_data = parse_org_structure(battalion.organizational_structure)
    
    response = make_response(render_template('battalion_detail.html', battalion=battalion, org_data=org_data))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@bp.route('/battalion/<int:battalion_id>/login', methods=['POST'])
def battalion_detail_login(battalion_id):
    username = request.form.get('username')
    password = request.form.get('password')
    
    battalion = Battalion.query.filter_by(battalion_number=battalion_id).first()
    if not battalion:
        return "Battalion not found", 404
        
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password, password):
        # Check if user is assigned to this battalion OR is a super admin
        if (user.is_battalion_admin and user.battalion_id == battalion.id) or user.is_admin:
            login_user(user)
            flash('Login Successful!', 'success')
            return redirect(url_for('main.battalion_detail', battalion_id=battalion_id))
        else:
             flash('Unauthorized access for this battalion', 'error')
    else:
        flash('Invalid username or password', 'error')
        
    return redirect(url_for('main.battalion_detail', battalion_id=battalion_id))

def parse_org_structure(org_text):
    """Parse organizational structure text into structured data"""
    lines = org_text.strip().split('\n')
    data = {
        'additional_commandant': '',
        'assistant_commandants': [],
        'groups': [],
        'companies': []
    }
    
    current_section = None
    current_ac = {'name': '', 'companies': []}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if 'ADDITIONAL COMMANDANT' in line:
            current_section = 'additional'
            continue
        elif 'ASSISTANT COMMANDANT' in line and 'NAME' not in line:
            if current_ac and current_ac.get('companies'):
                data['assistant_commandants'].append(current_ac)  # type: ignore
            current_ac = {'name': '', 'companies': []}
            current_section = 'assistant'
            continue
        elif line.startswith('NAME'):
            name = line.split(':', 1)[1].strip() if ':' in line else ''
            if current_section == 'additional':
                data['additional_commandant'] = name
            elif current_section == 'assistant':
                current_ac['name'] = name
        elif 'GROUP HEAD' in line or 'GROUP - GROUP INCHARGE' in line:
            current_section = 'groups'
            continue
        elif 'COMPANY HEAD' in line or 'COMPANY - COMPANY INCHARGE' in line:
            current_section = 'companies'
            continue
        elif ' - ' in line:
            parts = line.split(' - ', 1)
            if len(parts) == 2:
                group_or_company = parts[0].strip()
                incharge = parts[1].strip()
                
                if current_section == 'groups':
                    data['groups'].append({  # type: ignore
                        'head': group_or_company,
                        'group': group_or_company,
                        'incharge': incharge
                    })
                elif current_section == 'companies' and current_ac:
                    current_ac['companies'].append({  # type: ignore
                        'company': group_or_company,
                        'incharge': incharge
                    })
    
    # Add last assistant commandant
    if current_ac and current_ac.get('companies'):
        data['assistant_commandants'].append(current_ac)  # type: ignore
    
    return data

@bp.route('/battalion/<int:battalion_id>/history')
def battalion_history(battalion_id):
    battalion = Battalion.query.filter_by(battalion_number=battalion_id).first()
    if not battalion:
        return "Battalion not found", 404
    response = make_response(render_template('battalion_history.html', battalion=battalion))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@bp.route('/battalion/<int:battalion_id>/events')
def battalion_events(battalion_id):
    from .models.battalion_content import BattalionEvent, BattalionAnnouncement
    battalion = Battalion.query.filter_by(battalion_number=battalion_id).first()
    if not battalion:
        return "Battalion not found", 404
    events = BattalionEvent.query.filter_by(battalion_id=battalion.id).order_by(BattalionEvent.created_at.desc()).all()
    announcements = BattalionAnnouncement.query.filter_by(battalion_id=battalion.id).order_by(BattalionAnnouncement.created_at.desc()).all()
    
    # Calculate permission
    can_edit = current_user.is_authenticated and (current_user.is_admin or (current_user.is_battalion_admin and current_user.battalion_id == battalion.id))
    
    response = make_response(render_template('battalion_events.html', battalion=battalion, events=events, announcements=announcements, can_edit=can_edit))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@bp.route('/battalion/<int:battalion_id>/announcements')
def battalion_announcements(battalion_id):
    from .models.battalion_content import BattalionAnnouncement
    battalion = Battalion.query.filter_by(battalion_number=battalion_id).first()
    if not battalion:
        return "Battalion not found", 404
    announcements = BattalionAnnouncement.query.filter_by(battalion_id=battalion.id).order_by(BattalionAnnouncement.created_at.desc()).all()
    response = make_response(render_template('battalion_announcements.html', battalion=battalion, announcements=announcements))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@bp.route('/battalion/<int:battalion_id>/gallery')
def battalion_gallery(battalion_id):
    from .models.battalion_content import BattalionGallery
    battalion = Battalion.query.filter_by(battalion_number=battalion_id).first()
    if not battalion:
        return "Battalion not found", 404
    gallery_items = BattalionGallery.query.filter_by(battalion_id=battalion.id).order_by(BattalionGallery.created_at.desc()).all()
    
    # Calculate permission
    can_edit = current_user.is_authenticated and (current_user.is_admin or (current_user.is_battalion_admin and current_user.battalion_id == battalion.id))
    
    response = make_response(render_template('battalion_gallery.html', battalion=battalion, gallery_items=gallery_items, can_edit=can_edit))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@bp.route('/')
def index():
    # Get banners from database
    banners = Banner.query.filter_by(is_active=True).order_by(Banner.order).all()
    
    # Fallback to battalion images if no banners
    if not banners:
        battalion_images = [
            '2nd-bn.jpeg', '3rd-bn.jpeg', '5th-bn.jpeg', '6th-bn.jpeg',
            '9th-bn.jpeg', '11th-bn.jpeg', '14th-bn.jpeg', '16th-bn.jpeg'
        ]
    else:
        battalion_images = []
    
    # Get recent events (latest 12)
    recent_events = Event.query.order_by(Event.created_at.desc()).limit(12).all()
    
    # Get active announcements
    announcements = Announcement.query.filter_by(is_active=True).order_by(Announcement.order).all()
    
    return render_template('index.html', banners=banners, battalion_images=battalion_images, events=recent_events, announcements=announcements)

@bp.route('/battalions')
def battalions():
    all_battalions = Battalion.query.order_by(Battalion.battalion_number).all()
    return render_template('battalions.html', battalions=all_battalions)

@bp.route('/contacts')
def contacts():
    return render_template('contacts.html')

@bp.route('/api/contacts')
def api_get_contacts():
    """Public API to get contact information"""
    contact_info = ContactInfo.query.first()
    
    if not contact_info:
        return jsonify({
            'phone_numbers': ['+91-866-2434567', '+91-866-2434890', '100 (Emergency)'],
            'email_addresses': ['info@apsp.ap.gov.in', 'dgapsp@ap.gov.in', 'complaints@apsp.ap.gov.in'],
            'office_address': 'APSP Headquarters\nVijayawada, Andhra Pradesh\nPIN: 520001'
        })
    
    return jsonify({
        'phone_numbers': contact_info.get_phone_numbers(),
        'email_addresses': contact_info.get_email_addresses(),
        'office_address': contact_info.office_address or ''
    })

@bp.route('/about')
def about():
    # Create Officer table if not exists (temporary check)
    try:
        db.create_all()
    except:
        pass
        
    officers = Officer.query.order_by(Officer.priority.asc()).all()
    return render_template('about.html', officers=officers)

@bp.route('/sdrf')
def sdrf():
    sdrf_content = SDRFContent.query.first()
    return render_template('sdrf.html', sdrf_content=sdrf_content)

@bp.route('/sdrf/operations')
def sdrf_operations():
    sdrf_content = SDRFContent.query.first()
    pdf_path = sdrf_content.operations_pdf if sdrf_content else 'aboutsdrf/about-sdrf.pdf'
    return render_template('sdrf_operations.html', pdf_path=pdf_path)

@bp.route('/sdrf/training')
def sdrf_training():
    sdrf_content = SDRFContent.query.first()
    pdf_path = sdrf_content.training_pdf if sdrf_content else 'aboutsdrf/about-sdrf.pdf'
    return render_template('sdrf_training.html', pdf_path=pdf_path)


@bp.route('/events')
def events():
    all_events = Event.query.order_by(Event.created_at.desc()).all()
    return render_template('events.html', events=all_events)

@bp.route('/services')
def services():
    services = Service.query.order_by(Service.created_at.desc()).all()
    return render_template('services.html', services=services)

@bp.route('/announcements')
def announcements():
    return render_template('announcements.html')





@bp.route('/gallery')
def gallery():
    # Fetch all active images from database
    gallery_images = GalleryImage.query.filter_by(is_active=True).order_by(GalleryImage.uploaded_at.desc()).all()
    
    # Static battalion images (fallback)
    battalion_images = [
        '2nd-bn.jpeg', '3rd-bn.jpeg', '5th-bn.jpeg', '6th-bn.jpeg',
        '9th-bn.jpeg', '11th-bn.jpeg', '14th-bn.jpeg', '16th-bn.jpeg'
    ]
    return render_template('gallery.html', gallery_images=gallery_images, battalion_images=battalion_images)

@bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, is_admin=True).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.admin_dashboard'))
        else:
            error = 'Invalid username or password.'
    return render_template('admin-login.html', error=error)

@bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('main.admin_login'))
    return render_template('admin-dashboard.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/admin/change-password', methods=['POST'])
@login_required
def change_password():
    """Change admin password"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')
    
    # Validate inputs
    if not all([current_password, new_password, confirm_password]):
        return jsonify({'error': 'All fields are required'}), 400
    
    if new_password != confirm_password:
        return jsonify({'error': 'New passwords do not match'}), 400
    
    if len(new_password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters long'}), 400
    
    # Check current password
    if not check_password_hash(current_user.password, current_password):
        return jsonify({'error': 'Current password is incorrect'}), 400
        
    try:
        # Update password
        current_user.password = generate_password_hash(new_password)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Password changed successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/admin/change-password-login', methods=['POST'])
def change_password_login():
    """Change password from login page"""
    data = request.get_json()
    username = data.get('username')
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    # Validate inputs
    if not all([username, current_password, new_password]):
        return jsonify({'error': 'All fields are required'}), 400
    
    if len(new_password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters long'}), 400
    
    # Find user
    user = User.query.filter_by(username=username, is_admin=True).first()
    if not user:
        return jsonify({'error': 'Invalid username'}), 400
    
    # Check current password
    if not check_password_hash(user.password, current_password):
        return jsonify({'error': 'Current password is incorrect'}), 400
    
    try:
        # Update password
        user.password = generate_password_hash(new_password)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Password changed successfully! You can now login.'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while changing password'}), 500
    
    try:
        # Update password
        current_user.password = generate_password_hash(new_password)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Password changed successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# API Routes for Admin Dashboard
@bp.route('/admin/api/battalion/<int:battalion_id>', methods=['GET'])
@login_required
def get_battalion_data(battalion_id):
    """API endpoint to get battalion data for editing"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    battalion = Battalion.query.filter_by(battalion_number=battalion_id).first()
    if not battalion:
        return jsonify({'error': 'Battalion not found'}), 404
    
    return jsonify({
        'battalion_number': battalion.battalion_number,
        'name': battalion.name,
        'district': battalion.district,
        'commandant_name': battalion.commandant_name,
        'commandant_rank': battalion.commandant_rank,
        'ri_1': battalion.ri_1,
        'ri_2': battalion.ri_2,
        'ri_3': battalion.ri_3,
        'description': battalion.description,
        'commandant_speech': battalion.commandant_speech,
        'organizational_structure': battalion.organizational_structure
    })

@bp.route('/admin/api/battalion/<int:battalion_id>', methods=['POST'])
@login_required
def update_battalion_data(battalion_id):
    """API endpoint to update battalion data"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    battalion = Battalion.query.filter_by(battalion_number=battalion_id).first()
    if not battalion:
        return jsonify({'error': 'Battalion not found'}), 404
    
    data = request.get_json()
    
    # Update battalion fields
    if 'district' in data:
        battalion.district = data['district']
    if 'commandant_name' in data:
        battalion.commandant_name = data['commandant_name']
    if 'commandant_rank' in data:
        battalion.commandant_rank = data['commandant_rank']
    if 'ri_1' in data:
        battalion.ri_1 = data['ri_1']
    if 'ri_2' in data:
        battalion.ri_2 = data['ri_2']
    if 'ri_3' in data:
        battalion.ri_3 = data['ri_3']
    if 'description' in data:
        battalion.description = data['description']
    if 'commandant_speech' in data:
        battalion.commandant_speech = data['commandant_speech']
    if 'organizational_structure' in data:
        battalion.organizational_structure = data['organizational_structure']
    
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': 'Battalion data updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/api/battalion/<int:battalion_number>/update', methods=['POST'])
@login_required
def api_update_battalion_details(battalion_number):
    """API endpoint to update battalion data from battalion detail page"""
    battalion = Battalion.query.filter_by(battalion_number=battalion_number).first()
    if not battalion:
        return jsonify({'error': 'Battalion not found'}), 404
        
    # Check permissions: Admin or Battalion Admin for this specific battalion
    if not (current_user.is_admin or (current_user.is_battalion_admin and current_user.battalion_id == battalion.id)):
        return jsonify({'error': 'Unauthorized access'}), 403
    
    data = request.get_json()
    
    try:
        if 'district' in data:
            battalion.district = data['district']
        if 'commandant_name' in data:
            battalion.commandant_name = data['commandant_name']
        if 'commandant_rank' in data:
            battalion.commandant_rank = data['commandant_rank']
        if 'commandant_speech' in data:
            battalion.commandant_speech = data['commandant_speech']
        if 'organizational_structure' in data:
            # Validate JSON structure if needed
            battalion.organizational_structure = data['organizational_structure']
            
        db.session.commit()
        return jsonify({'success': True, 'message': 'Battalion details updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# Gallery API Routes
@bp.route('/admin/api/gallery', methods=['GET'])
@login_required
def get_gallery_images():
    """Get all gallery images"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    category = request.args.get('category', 'all')
    
    if category == 'all':
        images = GalleryImage.query.filter_by(is_active=True).order_by(GalleryImage.uploaded_at.desc()).all()
    else:
        images = GalleryImage.query.filter_by(category=category, is_active=True).order_by(GalleryImage.uploaded_at.desc()).all()
    
    return jsonify([img.to_dict() for img in images])

@bp.route('/admin/api/gallery', methods=['POST'])
@login_required
def add_gallery_image():
    """Add new gallery image with file upload"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Check if file is present
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        if file_ext not in allowed_extensions:
            return jsonify({'error': 'Invalid file type. Only PNG, JPG, JPEG, GIF allowed'}), 400
        
        # Create gallery folder if it doesn't exist
        gallery_folder = os.path.join(current_app.static_folder, 'images', 'gallery')
        os.makedirs(gallery_folder, exist_ok=True)
        
        # Generate unique filename
        import uuid
        unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
        file_path = os.path.join(gallery_folder, unique_filename)
        
        # Save file
        file.save(file_path)
        
        # Save to database
        image_path = f"images/gallery/{unique_filename}"
        new_image = GalleryImage(
            filename=file.filename,
            title=request.form.get('title'),
            description=request.form.get('description'),
            category=request.form.get('category'),
            image_path=image_path
        )
        
        db.session.add(new_image)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Image uploaded successfully',
            'image': new_image.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/admin/api/gallery/<int:image_id>', methods=['PUT'])
@login_required
def update_gallery_image(image_id):
    """Update gallery image"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    image = GalleryImage.query.get(image_id)
    if not image:
        return jsonify({'error': 'Image not found'}), 404
    
    try:
        data = request.get_json()
        
        if 'title' in data:
            image.title = data['title']
        if 'description' in data:
            image.description = data['description']
        if 'category' in data:
            image.category = data['category']
        if 'image_path' in data:
            image.image_path = data['image_path']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Image updated successfully',
            'image': image.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/admin/api/gallery/<int:image_id>', methods=['DELETE'])
@login_required
def delete_gallery_image(image_id):
    """Delete gallery image (soft delete)"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    image = GalleryImage.query.get(image_id)
    if not image:
        return jsonify({'error': 'Image not found'}), 404
    
    try:
        # Soft delete - just mark as inactive
        image.is_active = False
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Image deleted successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Service (Useful Links) Management Routes
@bp.route('/admin/api/services', methods=['GET'])
@login_required
def get_services():
    """Get all services"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    services = Service.query.order_by(Service.created_at.desc()).all()
    return jsonify({
        'success': True,
        'services': [service.to_dict() for service in services]
    })

@bp.route('/admin/api/services', methods=['POST'])
@login_required
def add_service():
    """Add new service"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        data = request.get_json()
        
        if not data.get('title') or not data.get('url'):
            return jsonify({'error': 'Title and URL are required'}), 400
        
        service = Service(
            title=data['title'],
            url=data['url'],
            description=data.get('description', '')
        )
        
        db.session.add(service)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Service added successfully',
            'service': service.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/admin/api/services/<int:service_id>', methods=['PUT'])
@login_required
def update_service(service_id):
    """Update service"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    service = Service.query.get(service_id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404
    
    try:
        data = request.get_json()
        
        if 'title' in data:
            service.title = data['title']
        if 'url' in data:
            service.url = data['url']
        if 'description' in data:
            service.description = data['description']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Service updated successfully',
            'service': service.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/admin/api/services/<int:service_id>', methods=['DELETE'])
@login_required
def delete_service(service_id):
    """Delete service"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    service = Service.query.get(service_id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404
    
    try:
        db.session.delete(service)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Service deleted successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Event Management Routes
@bp.route('/admin/api/events', methods=['GET'])
@login_required
def get_events():
    """Get all events"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    events = Event.query.order_by(Event.created_at.desc()).all()
    return jsonify({
        'success': True,
        'events': [event.to_dict() for event in events]
    })

@bp.route('/admin/api/events', methods=['POST'])
@login_required
def add_event():
    """Add new event"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Handle form data primarily for file upload
        data = request.form
        
        if not data.get('title'):
            return jsonify({'error': 'Event title is required'}), 400
            
        pdf_filename = None
        if 'pdf' in request.files:
            file = request.files['pdf']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                from datetime import datetime
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                pdf_filename = f"event_{timestamp}_{filename}"
                upload_path = os.path.join(current_app.static_folder, 'pdfs', pdf_filename)
                os.makedirs(os.path.dirname(upload_path), exist_ok=True)
                file.save(upload_path)
        
        event = Event(
            title=data['title'],
            description=data.get('description', ''),
            image_url=data.get('image_url', ''),
            pdf_file=pdf_filename
        )
        
        db.session.add(event)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Event added successfully',
            'event': event.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/admin/api/events/<int:event_id>', methods=['PUT'])
@login_required
def update_event(event_id):
    """Update event"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    try:
        # Check if json or form data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        if 'title' in data:
            event.title = data['title']
        if 'description' in data:
            event.description = data['description']
        if 'image_url' in data:
            event.image_url = data['image_url']
            
        if 'pdf' in request.files:
            file = request.files['pdf']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                from datetime import datetime
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                pdf_filename = f"event_{timestamp}_{filename}"
                upload_path = os.path.join(current_app.static_folder, 'pdfs', pdf_filename)
                os.makedirs(os.path.dirname(upload_path), exist_ok=True)
                file.save(upload_path)
                event.pdf_file = pdf_filename
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Event updated successfully',
            'event': event.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/admin/api/events/<int:event_id>', methods=['DELETE'])
@login_required
def delete_event(event_id):
    """Delete event"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    try:
        # Delete PDF if exists
        if event.pdf_file:
            path = os.path.join(current_app.static_folder, 'pdfs', event.pdf_file)
            if os.path.exists(path):
                os.remove(path)
                
        db.session.delete(event)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Event deleted successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Banner Management Routes
@bp.route('/admin/api/banners', methods=['GET'])
@login_required
def get_banners():
    """Get all banners"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    banners = Banner.query.filter_by(is_active=True).order_by(Banner.order).all()
    return jsonify([banner.to_dict() for banner in banners])

@bp.route('/admin/api/banners', methods=['POST'])
@login_required
def add_banner():
    """Add new banner"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    caption = request.form.get('caption', '')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        # Add timestamp to avoid filename conflicts
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        name, ext = os.path.splitext(filename)
        filename = f"banner_{timestamp}{ext}"
        
        # Save to static/images directory
        upload_path = os.path.join(current_app.root_path, 'static', 'images', filename)
        file.save(upload_path)
        
        # Get the highest order number
        max_order = db.session.query(db.func.max(Banner.order)).scalar() or 0
        
        # Create new banner record
        banner = Banner(
            filename=filename,
            caption=caption,
            order=max_order + 1
        )
        
        try:
            db.session.add(banner)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Banner added successfully',
                'banner': banner.to_dict()
            })
        except Exception as e:
            db.session.rollback()
            # Delete uploaded file if database insert fails
            if os.path.exists(upload_path):
                os.remove(upload_path)
            return jsonify({'error': str(e)}), 500

@bp.route('/admin/api/banners/<int:banner_id>', methods=['DELETE'])
@login_required
def delete_banner(banner_id):
    """Delete banner"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    banner = Banner.query.get(banner_id)
    if not banner:
        return jsonify({'error': 'Banner not found'}), 404
    
    try:
        # Delete the file
        file_path = os.path.join(current_app.root_path, 'static', 'images', banner.filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Delete the database record
        db.session.delete(banner)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Banner deleted successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/admin/api/banners/<int:banner_id>/move', methods=['POST'])
@login_required
def move_banner(banner_id):
    """Move banner up or down in order"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    direction = data.get('direction')
    
    if direction not in ['up', 'down']:
        return jsonify({'error': 'Invalid direction'}), 400
    
    banner = Banner.query.get(banner_id)
    if not banner:
        return jsonify({'error': 'Banner not found'}), 404
    
    try:
        if direction == 'up' and banner.order > 1:
            # Find banner with order one less
            other_banner = Banner.query.filter_by(order=banner.order - 1).first()
            if other_banner:
                # Swap orders
                banner.order, other_banner.order = other_banner.order, banner.order
        elif direction == 'down':
            # Find banner with order one more
            other_banner = Banner.query.filter_by(order=banner.order + 1).first()
            if other_banner:
                # Swap orders
                banner.order, other_banner.order = other_banner.order, banner.order
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Banner order updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Announcement API Routes
@bp.route('/admin/api/announcements', methods=['GET'])
@login_required
def get_announcements():
    """Get all announcements"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Return all announcements for admin management, not just active ones
    announcements = Announcement.query.order_by(Announcement.order).all()
    return jsonify([announcement.to_dict() for announcement in announcements])

@bp.route('/admin/api/announcements/<int:announcement_id>', methods=['PUT'])
@login_required
def update_announcement_status(announcement_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    announcement = Announcement.query.get(announcement_id)
    if not announcement:
        return jsonify({'error': 'Announcement not found'}), 404
    
    data = request.get_json()
    if 'is_active' in data:
        announcement.is_active = data['is_active']
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Announcement updated successfully',
            'announcement': announcement.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/admin/api/announcements', methods=['POST'])
@login_required
def add_announcement():
    """Add new announcement"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    content = data.get('content')
    
    if not content:
        return jsonify({'error': 'Content is required'}), 400
    
    # Get the highest order number
    max_order = db.session.query(db.func.max(Announcement.order)).scalar() or 0
    
    announcement = Announcement(
        content=content,
        order=max_order + 1
    )
    
    try:
        db.session.add(announcement)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Announcement added successfully',
            'announcement': announcement.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/admin/api/announcements/<int:announcement_id>', methods=['DELETE'])
@login_required
def delete_announcement(announcement_id):
    """Delete announcement"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    announcement = Announcement.query.get(announcement_id)
    if not announcement:
        return jsonify({'error': 'Announcement not found'}), 404
    
    try:
        db.session.delete(announcement)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Announcement deleted successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/api/battalion/announcements/update', methods=['POST'])
@login_required
def api_update_battalion_announcement():
    """API endpoint to update a battalion announcement"""
    if not current_user.is_battalion_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        from app.models.battalion_content import BattalionAnnouncement
        data = request.get_json()
        announcement_id = data.get('announcement_id')
        
        announcement = BattalionAnnouncement.query.get(announcement_id)
        if not announcement or announcement.battalion_id != current_user.battalion_id:
            return jsonify({'success': False, 'message': 'Announcement not found'}), 404
        
        announcement.title = data.get('title', announcement.title)
        announcement.date = data.get('date', announcement.date)
        announcement.content = data.get('content', announcement.content)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Announcement updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400


@bp.route('/api/battalion/gallery/update', methods=['POST'])
@login_required
def api_update_battalion_gallery():
    """API endpoint to update battalion gallery image caption"""
    if not current_user.is_battalion_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        from app.models.battalion_content import BattalionGallery
        data = request.get_json()
        image_id = data.get('image_id')
        
        image = BattalionGallery.query.get(image_id)
        if not image or image.battalion_id != current_user.battalion_id:
            return jsonify({'success': False, 'message': 'Image not found'}), 404
        
        image.caption = data.get('caption', image.caption)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Caption updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400


# API Routes for Edit Battalion Information Page
@bp.route('/api/battalion/history/update', methods=['POST'])
@login_required
def api_update_battalion_history():
    """API endpoint to update battalion history"""
    if not current_user.is_battalion_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        data = request.get_json()
        battalion = Battalion.query.get(current_user.battalion_id)
        
        if not battalion:
            return jsonify({'success': False, 'message': 'Battalion not found'}), 404
        
        battalion.history = data.get('history', '')
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'History updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400


@bp.route('/api/battalion/events/list', methods=['GET'])
@login_required
def api_list_battalion_events():
    """API endpoint to list battalion events"""
    if not current_user.is_battalion_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        from app.models.battalion_content import BattalionEvent
        battalion_id = request.args.get('battalion_id', type=int)
        
        if battalion_id != current_user.battalion_id:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        events = BattalionEvent.query.filter_by(battalion_id=battalion_id).order_by(BattalionEvent.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'events': [event.to_dict() for event in events]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400


@bp.route('/admin/api/sdrf/upload-about-pdf', methods=['POST'])
@login_required
def upload_about_sdrf_pdf():
    """Upload About SDRF PDF"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'}), 400
        
    if file and file.filename.lower().endswith('.pdf'):
        try:
            filename = secure_filename(file.filename)
            # Use specific folder for about sdrf
            folder_path = os.path.join(current_app.static_folder, 'aboutsdrf')
            os.makedirs(folder_path, exist_ok=True)
            
            # Save file
            file_path = os.path.join(folder_path, filename)
            file.save(file_path)
            
            # Update database
            sdrf_content = SDRFContent.query.first()
            if not sdrf_content:
                sdrf_content = SDRFContent()
                db.session.add(sdrf_content)
            
            # Store relative path
            relative_path = f'aboutsdrf/{filename}'
            sdrf_content.about_pdf = relative_path
            db.session.commit()
            
            return jsonify({
                'success': True, 
                'message': 'About SDRF PDF uploaded successfully',
                'filepath': relative_path
            })
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    else:
        return jsonify({'success': False, 'message': 'Invalid file type. Only PDF allowed'}), 400

@bp.route('/admin/api/sdrf/delete-about-pdf', methods=['POST'])
@login_required
def delete_about_sdrf_pdf():
    """Delete About SDRF PDF"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        sdrf_content = SDRFContent.query.first()
        if sdrf_content:
            sdrf_content.about_pdf = None
            db.session.commit()
        return jsonify({'success': True, 'message': 'About SDRF PDF deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/admin/api/sdrf/status', methods=['GET'])
@login_required
def get_sdrf_status():
    """Get status of SDRF PDFs"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
    sdrf_content = SDRFContent.query.first()
    return jsonify({
        'success': True,
        'about_pdf': sdrf_content.about_pdf if sdrf_content else None,
        'operations_pdf': sdrf_content.operations_pdf if sdrf_content else None,
        'training_pdf': sdrf_content.training_pdf if sdrf_content else None
    })

@bp.route('/api/battalion/announcements/list', methods=['GET'])
@login_required
def api_list_battalion_announcements():
    """API endpoint to list battalion announcements"""
    if not current_user.is_battalion_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        from app.models.battalion_content import BattalionAnnouncement
        battalion_id = request.args.get('battalion_id', type=int)
        
        if battalion_id != current_user.battalion_id:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        announcements = BattalionAnnouncement.query.filter_by(battalion_id=battalion_id).order_by(BattalionAnnouncement.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'announcements': [announcement.to_dict() for announcement in announcements]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400


@bp.route('/api/battalion/gallery/list', methods=['GET'])
@login_required
def api_list_battalion_gallery():
    """API endpoint to list battalion gallery images"""
    if not current_user.is_battalion_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        from app.models.battalion_content import BattalionGallery
        battalion_id = request.args.get('battalion_id', type=int)
        
        if battalion_id != current_user.battalion_id:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        images = BattalionGallery.query.filter_by(battalion_id=battalion_id).order_by(BattalionGallery.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'gallery': [image.to_dict() for image in images]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

# Officer Management API Routes
@bp.route('/admin/api/officers', methods=['GET'])
@login_required
def get_officers():
    """Get all officers"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    officers = Officer.query.order_by(Officer.priority.asc()).all()
    return jsonify({
        'success': True,
        'officers': [officer.to_dict() for officer in officers]
    })

@bp.route('/admin/api/officers', methods=['POST'])
@login_required
def add_officer():
    """Add new officer"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        data = request.form
        file = request.files.get('image')
        
        image_filename = 'default.jpg'
        if file:
            filename = secure_filename(file.filename)
            # Create folder if not exists
            officers_folder = os.path.join(current_app.static_folder, 'images', 'officers')
            os.makedirs(officers_folder, exist_ok=True)
            
            import uuid
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file.save(os.path.join(officers_folder, unique_filename))
            image_filename = unique_filename

        officer = Officer(
            name=data.get('name'),
            designation=data.get('designation'),
            phone=data.get('phone'),
            email=data.get('email'),
            image_file=image_filename,
            priority=int(data.get('priority', 0))
        )
        
        db.session.add(officer)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Officer added successfully',
            'officer': officer.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/admin/api/officers/<int:id>', methods=['PUT'])
@login_required
def update_officer(id):
    """Update officer"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    officer = Officer.query.get_or_404(id)
    
    try:
        data = request.form
        file = request.files.get('image')
        
        if file:
            filename = secure_filename(file.filename)
            officers_folder = os.path.join(current_app.static_folder, 'images', 'officers')
            os.makedirs(officers_folder, exist_ok=True)
            
            import uuid
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file.save(os.path.join(officers_folder, unique_filename))
            officer.image_file = unique_filename

        if 'name' in data: officer.name = data['name']
        if 'designation' in data: officer.designation = data['designation']
        if 'phone' in data: officer.phone = data['phone']
        if 'email' in data: officer.email = data['email']
        if 'priority' in data: officer.priority = int(data['priority'])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Officer updated successfully',
            'officer': officer.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/admin/api/officers/<int:id>', methods=['DELETE'])
@login_required
def delete_officer(id):
    """Delete officer"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    officer = Officer.query.get_or_404(id)
    
    try:
        db.session.delete(officer)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Officer deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Battalion Event Management API
@bp.route('/api/battalion/events/add', methods=['POST'])
@login_required
def add_battalion_event():
    if not current_user.is_battalion_admin and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
        
    try:
        from app.models.battalion_content import BattalionEvent
        # Handle FormData
        battalion_id = request.form.get('battalion_id')
        title = request.form.get('title')
        description = request.form.get('description')
        date = request.form.get('date')
        location = request.form.get('location')
        
        # Verify permission
        if not current_user.is_admin and current_user.battalion_id != int(battalion_id):
             return jsonify({'error': 'Unauthorized for this battalion'}), 403

        image_file = request.files.get('image')
        pdf_file = request.files.get('pdf')
        
        image_filename = None
        pdf_filename = None
        import uuid
        
        if image_file:
            filename = secure_filename(image_file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            folder = os.path.join(current_app.static_folder, 'images', 'battalion_events')
            os.makedirs(folder, exist_ok=True)
            image_file.save(os.path.join(folder, unique_filename))
            image_filename = unique_filename
            
        if pdf_file:
            filename = secure_filename(pdf_file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            folder = os.path.join(current_app.static_folder, 'files', 'battalion_events')
            os.makedirs(folder, exist_ok=True)
            pdf_file.save(os.path.join(folder, unique_filename))
            pdf_filename = unique_filename
             
        event = BattalionEvent(
            battalion_id=battalion_id,
            title=title,
            description=description,
            date=date,
            location=location,
            image_file=image_filename,
            pdf_file=pdf_filename
        )
        
        db.session.add(event)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Event added successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/api/battalion/events/<int:event_id>', methods=['DELETE'])
@login_required
def delete_battalion_event(event_id):
    if not current_user.is_battalion_admin and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
        
    try:
        from app.models.battalion_content import BattalionEvent
        event = BattalionEvent.query.get_or_404(event_id)
        
        # Verify permission
        if not current_user.is_admin and current_user.battalion_id != event.battalion_id:
             return jsonify({'error': 'Unauthorized for this battalion'}), 403
        
        # Delete files
        try:
            if event.image_file:
                path = os.path.join(current_app.static_folder, 'images', 'battalion_events', event.image_file)
                if os.path.exists(path): os.remove(path)
            if event.pdf_file:
                path = os.path.join(current_app.static_folder, 'files', 'battalion_events', event.pdf_file)
                if os.path.exists(path): os.remove(path)
        except:
            pass
             
        db.session.delete(event)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Event deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Battalion Announcement Management API
@bp.route('/api/battalion/announcements/add', methods=['POST'])
@login_required
def add_battalion_announcement():
    if not current_user.is_battalion_admin and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
        
    try:
        from app.models.battalion_content import BattalionAnnouncement
        # Handle FormData
        battalion_id = request.form.get('battalion_id')
        title = request.form.get('title')
        content = request.form.get('content')
        date = request.form.get('date')
        
        # Verify permission
        if not current_user.is_admin and current_user.battalion_id != int(battalion_id):
             return jsonify({'error': 'Unauthorized for this battalion'}), 403
             
        image_file = request.files.get('image')
        pdf_file = request.files.get('pdf')
        
        image_filename = None
        pdf_filename = None
        import uuid
        
        if image_file:
            filename = secure_filename(image_file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            folder = os.path.join(current_app.static_folder, 'images', 'battalion_announcements')
            os.makedirs(folder, exist_ok=True)
            image_file.save(os.path.join(folder, unique_filename))
            image_filename = unique_filename
            
        if pdf_file:
            filename = secure_filename(pdf_file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            folder = os.path.join(current_app.static_folder, 'files', 'battalion_announcements')
            os.makedirs(folder, exist_ok=True)
            pdf_file.save(os.path.join(folder, unique_filename))
            pdf_filename = unique_filename

        announcement = BattalionAnnouncement(
            battalion_id=battalion_id,
            title=title,
            content=content,
            date=date,
            image_file=image_filename,
            pdf_file=pdf_filename
        )
        
        db.session.add(announcement)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Announcement added successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/api/battalion/announcements/<int:announcement_id>', methods=['DELETE'])
@login_required
def delete_battalion_announcement(announcement_id):
    if not current_user.is_battalion_admin and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
        
    try:
        from app.models.battalion_content import BattalionAnnouncement
        announcement = BattalionAnnouncement.query.get_or_404(announcement_id)
        
        # Verify permission
        if not current_user.is_admin and current_user.battalion_id != announcement.battalion_id:
             return jsonify({'error': 'Unauthorized for this battalion'}), 403
        
        # Delete files
        try:
            if announcement.image_file:
                path = os.path.join(current_app.static_folder, 'images', 'battalion_announcements', announcement.image_file)
                if os.path.exists(path): os.remove(path)
            if announcement.pdf_file:
                path = os.path.join(current_app.static_folder, 'files', 'battalion_announcements', announcement.pdf_file)
                if os.path.exists(path): os.remove(path)
        except:
            pass
             
        db.session.delete(announcement)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Announcement deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Battalion Gallery Management API

# Battalion Gallery Management API
@bp.route('/api/battalion/gallery/add', methods=['POST'])
@login_required
def add_battalion_gallery_image():
    if not current_user.is_battalion_admin and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
        
    try:
        from app.models.battalion_content import BattalionGallery
        
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
            
        file = request.files['image']
        battalion_id = request.form.get('battalion_id')
        caption = request.form.get('caption')
        
        # Verify permission
        if not current_user.is_admin and current_user.battalion_id != int(battalion_id):
             return jsonify({'error': 'Unauthorized for this battalion'}), 403
             
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
            
        if file:
            filename = secure_filename(file.filename)
            import uuid
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            
            # Create directory
            gallery_folder = os.path.join(current_app.static_folder, 'images', 'battalion_gallery')
            os.makedirs(gallery_folder, exist_ok=True)
            
            file.save(os.path.join(gallery_folder, unique_filename))
            
            image = BattalionGallery(
                battalion_id=battalion_id,
                image_path=unique_filename,
                caption=caption
            )
            
            db.session.add(image)
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'Image uploaded successfully'})
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/api/battalion/gallery/<int:image_id>', methods=['DELETE'])
@login_required
def delete_battalion_gallery_image(image_id):
    if not current_user.is_battalion_admin and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
        
    try:
        from app.models.battalion_content import BattalionGallery
        image = BattalionGallery.query.get_or_404(image_id)
        
        # Verify permission
        if not current_user.is_admin and current_user.battalion_id != image.battalion_id:
             return jsonify({'error': 'Unauthorized for this battalion'}), 403
        
        # Delete file
        try:
            file_path = os.path.join(current_app.static_folder, 'images', 'battalion_gallery', image.image_path)
            if os.path.exists(file_path):
                os.remove(file_path)
        except:
            pass
            
        db.session.delete(image)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Image deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/api/battalion-admin/change-password', methods=['POST'])
@login_required
def change_battalion_admin_password():
    """Change battalion admin password"""
    if not current_user.is_battalion_admin and not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
             return jsonify({'success': False, 'message': 'All fields are required'}), 400
             
        # Verify current password
        if not check_password_hash(current_user.password, current_password):
            return jsonify({'success': False, 'message': 'Incorrect current password'}), 400
            
        # Update password
        current_user.password = generate_password_hash(new_password)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Password changed successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/admin/api/contacts', methods=['POST'])
@login_required
def save_contact_info():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        data = request.get_json()
        
        contact_info = ContactInfo.query.first()
        if not contact_info:
            contact_info = ContactInfo()
            db.session.add(contact_info)
        
        # Update fields
        contact_info.office_address = data.get('office_address', '')
        contact_info.set_phone_numbers(data.get('phone_numbers', []))
        contact_info.set_email_addresses(data.get('email_addresses', []))
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Contact information updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/admin/api/contacts', methods=['GET'])
@login_required
def get_admin_contacts():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    contact_info = ContactInfo.query.first()
    
    if not contact_info:
        return jsonify({
            'phone_numbers': [],
            'email_addresses': [],
            'office_address': ''
        })
    
    return jsonify({
        'phone_numbers': contact_info.get_phone_numbers(),
        'email_addresses': contact_info.get_email_addresses(),
        'office_address': contact_info.office_address or ''
    })

# Battalion Image Upload Routes
@bp.route('/api/battalion/upload-commandant-photo', methods=['POST'])
@login_required
def upload_commandant_photo():
    """Upload commandant photo"""
    if not current_user.is_battalion_admin and not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        if 'photo' not in request.files:
            return jsonify({'success': False, 'message': 'No file part'}), 400
            
        file = request.files['photo']
        battalion_number = request.form.get('battalion_number')
        
        # Verify permission
        if not current_user.is_admin:
             # Get battalion_number from current_user.battalion_id
             user_battalion = Battalion.query.get(current_user.battalion_id)
             if not user_battalion or str(user_battalion.battalion_number) != str(battalion_number):
                 return jsonify({'success': False, 'message': 'Unauthorized for this battalion'}), 403

        if file.filename == '':
            return jsonify({'success': False, 'message': 'No selected file'}), 400
            
        if file:
            filename = secure_filename(file.filename)
            import uuid
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            
            # Create directory
            folder = os.path.join(current_app.static_folder, 'images', 'commandants')
            os.makedirs(folder, exist_ok=True)
            
            file.save(os.path.join(folder, unique_filename))
            
            # Update database
            battalion = Battalion.query.filter_by(battalion_number=battalion_number).first()
            if not battalion:
                 return jsonify({'success': False, 'message': 'Battalion not found'}), 404
            
            # Delete old image if exists and not default
            if battalion.commandant_image and 'default' not in battalion.commandant_image:
                try:
                    old_path = os.path.join(folder, battalion.commandant_image)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                except:
                    pass
            
            battalion.commandant_image = unique_filename
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'Commandant photo uploaded successfully'})
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/api/battalion/delete-commandant-photo', methods=['POST'])
@login_required
def delete_commandant_photo():
    """Delete commandant photo"""
    if not current_user.is_battalion_admin and not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        data = request.get_json()
        battalion_number = data.get('battalion_number')
        
        # Verify permission
        if not current_user.is_admin:
             user_battalion = Battalion.query.get(current_user.battalion_id)
             if not user_battalion or str(user_battalion.battalion_number) != str(battalion_number):
                 return jsonify({'success': False, 'message': 'Unauthorized for this battalion'}), 403
        
        battalion = Battalion.query.filter_by(battalion_number=battalion_number).first()
        if not battalion:
             return jsonify({'success': False, 'message': 'Battalion not found'}), 404
             
        if battalion.commandant_image:
            # Try to delete file
            try:
                folder = os.path.join(current_app.static_folder, 'images', 'commandants')
                path = os.path.join(folder, battalion.commandant_image)
                if os.path.exists(path):
                    os.remove(path)
            except:
                pass
            
            battalion.commandant_image = None
            db.session.commit()
            
        return jsonify({'success': True, 'message': 'Commandant photo deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/api/battalion/upload-battalion-image', methods=['POST'])
@login_required
def upload_battalion_image():
    """Upload battalion building image"""
    if not current_user.is_battalion_admin and not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'message': 'No file part'}), 400
            
        file = request.files['image']
        battalion_number = request.form.get('battalion_number')
        
        # Verify permission
        if not current_user.is_admin:
             user_battalion = Battalion.query.get(current_user.battalion_id)
             if not user_battalion or str(user_battalion.battalion_number) != str(battalion_number):
                 return jsonify({'success': False, 'message': 'Unauthorized for this battalion'}), 403

        if file.filename == '':
            return jsonify({'success': False, 'message': 'No selected file'}), 400
            
        if file:
            filename = secure_filename(file.filename)
            import uuid
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            
            # Create directory
            folder = os.path.join(current_app.static_folder, 'images', 'battalions')
            os.makedirs(folder, exist_ok=True)
            
            file.save(os.path.join(folder, unique_filename))
            
            # Update database
            battalion = Battalion.query.filter_by(battalion_number=battalion_number).first()
            if not battalion:
                 return jsonify({'success': False, 'message': 'Battalion not found'}), 404
            
            # Delete old image if exists and not default
            if battalion.image and 'default' not in battalion.image:
                try:
                    old_path = os.path.join(folder, battalion.image)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                except:
                    pass
            
            battalion.image = unique_filename
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'Battalion image uploaded successfully'})
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/api/battalion/delete-battalion-image', methods=['POST'])
@login_required
def delete_battalion_image():
    """Delete battalion image"""
    if not current_user.is_battalion_admin and not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        data = request.get_json()
        battalion_number = data.get('battalion_number')
        
        # Verify permission
        if not current_user.is_admin:
             user_battalion = Battalion.query.get(current_user.battalion_id)
             if not user_battalion or str(user_battalion.battalion_number) != str(battalion_number):
                 return jsonify({'success': False, 'message': 'Unauthorized for this battalion'}), 403
        
        battalion = Battalion.query.filter_by(battalion_number=battalion_number).first()
        if not battalion:
             return jsonify({'success': False, 'message': 'Battalion not found'}), 404
             
        if battalion.image:
            # Try to delete file
            try:
                folder = os.path.join(current_app.static_folder, 'images', 'battalions')
                path = os.path.join(folder, battalion.image)
                if os.path.exists(path):
                    os.remove(path)
            except:
                pass
            
            battalion.image = None
            db.session.commit()
            
        return jsonify({'success': True, 'message': 'Battalion image deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500