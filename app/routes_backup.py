from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, current_app
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
from . import db, login_manager
import os
import json

bp = Blueprint('main', __name__)

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
    
    return render_template('battalion_detail.html', battalion=battalion, org_data=org_data)

def parse_org_structure(org_text):
    """Parse organizational structure text into structured data"""
    lines = org_text.strip().split('\n')
    data = {
        'additional_commandant': None,
        'assistant_commandants': [],
        'groups': [],
        'companies': []
    }
    
    current_section = None
    current_ac = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if 'ADDITIONAL COMMANDANT' in line:
            current_section = 'additional'
            continue
        elif 'ASSISTANT COMMANDANT' in line and 'NAME' not in line:
            if current_ac and current_ac.get('companies'):
                data['assistant_commandants'].append(current_ac) # type: ignore
            current_ac = {'name': '', 'companies': []}
            current_section = 'assistant'
            continue
        elif line.startswith('NAME'):
            name = line.split(':', 1)[1].strip() if ':' in line else ''
            if current_section == 'additional':
                data['additional_commandant'] = name # type: ignore
            elif current_section == 'assistant' and current_ac is not None:
                current_ac['name'] = name # type: ignore
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
                    data['groups'].append({ # type: ignore
                        'head': group_or_company,
                        'group': group_or_company,
                        'incharge': incharge
                    })
                elif current_section == 'companies' and current_ac:
                    current_ac['companies'].append({ # type: ignore
                        'company': group_or_company,
                        'incharge': incharge
                    })
    
    # Add last assistant commandant
    if current_ac and current_ac.get('companies'):
        data['assistant_commandants'].append(current_ac) # type: ignore
    
    return data

@bp.route('/battalion/<int:battalion_id>/history')
def battalion_history(battalion_id):
    battalion = Battalion.query.filter_by(battalion_number=battalion_id).first()
    if not battalion:
        return "Battalion not found", 404
    return render_template('battalion_history.html', battalion=battalion)

@bp.route('/battalion/<int:battalion_id>/events')
def battalion_events(battalion_id):
    from .models.battalion_content import BattalionEvent, BattalionAnnouncement
    battalion = Battalion.query.filter_by(battalion_number=battalion_id).first()
    if not battalion:
        return "Battalion not found", 404
    events = BattalionEvent.query.filter_by(battalion_id=battalion.id).order_by(BattalionEvent.created_at.desc()).all()
    announcements = BattalionAnnouncement.query.filter_by(battalion_id=battalion.id).order_by(BattalionAnnouncement.created_at.desc()).all()
    return render_template('battalion_events.html', battalion=battalion, events=events, announcements=announcements)

@bp.route('/battalion/<int:battalion_id>/announcements')
def battalion_announcements(battalion_id):
    from .models.battalion_content import BattalionAnnouncement
    battalion = Battalion.query.filter_by(battalion_number=battalion_id).first()
    if not battalion:
        return "Battalion not found", 404
    announcements = BattalionAnnouncement.query.filter_by(battalion_id=battalion.id).order_by(BattalionAnnouncement.created_at.desc()).all()
    return render_template('battalion_announcements.html', battalion=battalion, announcements=announcements)

@bp.route('/battalion/<int:battalion_id>/gallery')
def battalion_gallery(battalion_id):
    from .models.battalion_content import BattalionGallery
    battalion = Battalion.query.filter_by(battalion_number=battalion_id).first()
    if not battalion:
        return "Battalion not found", 404
    gallery_items = BattalionGallery.query.filter_by(battalion_id=battalion.id).order_by(BattalionGallery.created_at.desc()).all()
    return render_template('battalion_gallery.html', battalion=battalion, gallery_items=gallery_items)

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
    
    # Get recent events (latest 4)
    recent_events = Event.query.order_by(Event.created_at.desc()).limit(4).all()
    
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

@bp.route('/news')
def news():
    return render_template('news.html')

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
        data = request.get_json()
        
        if not data.get('title'):
            return jsonify({'error': 'Event title is required'}), 400
        
        event = Event(
            title=data['title'],
            description=data.get('description', ''),
            image_url=data.get('image_url', '')
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
        data = request.get_json()
        
        if 'title' in data:
            event.title = data['title']
        if 'description' in data:
            event.description = data['description']
        if 'image_url' in data:
            event.image_url = data['image_url']
        
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
    
    announcements = Announcement.query.order_by(Announcement.order).all()
    return jsonify([{
        'id': a.id,
        'content': a.content,
        'is_active': a.is_active,
        'order': a.order,
        'created_at': a.created_at.isoformat() if a.created_at else None
    } for a in announcements])

@bp.route('/admin/api/announcements', methods=['POST'])
@login_required
def add_announcement():
    """Add new announcement"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    content = data.get('content', '').strip()
    
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
            'announcement': {
                'id': announcement.id,
                'content': announcement.content,
                'is_active': announcement.is_active,
                'order': announcement.order
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/admin/api/announcements/<int:announcement_id>', methods=['PUT'])
@login_required
def update_announcement(announcement_id):
    """Update announcement"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    announcement = Announcement.query.get(announcement_id)
    if not announcement:
        return jsonify({'error': 'Announcement not found'}), 404
    
    data = request.get_json()
    
    if 'content' in data:
        announcement.content = data['content'].strip()
    if 'is_active' in data:
        announcement.is_active = data['is_active']
    
    try:
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Announcement updated successfully',
            'announcement': {
                'id': announcement.id,
                'content': announcement.content,
                'is_active': announcement.is_active,
                'order': announcement.order
            }
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


# Contact Information Management
@bp.route('/admin/api/contacts', methods=['GET'])
@login_required
def get_contacts():
    """Get contact information"""
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


@bp.route('/admin/api/contacts', methods=['POST'])
@login_required
def save_contacts():
    """Save contact information"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        data = request.json
        phone_numbers = data.get('phone_numbers', [])
        email_addresses = data.get('email_addresses', [])
        office_address = data.get('office_address', '')
        
        contact_info = ContactInfo.query.first()
        
        if not contact_info:
            contact_info = ContactInfo()
            db.session.add(contact_info)
        
        contact_info.set_phone_numbers(phone_numbers)
        contact_info.set_email_addresses(email_addresses)
        contact_info.office_address = office_address
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Contact information saved successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# SDRF Content Management
@bp.route('/admin/api/sdrf', methods=['GET'])
@login_required
def get_sdrf_content():
    """Get SDRF content"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    sdrf_content = SDRFContent.query.first()
    
    if not sdrf_content:
        return jsonify({
            'about_content': '',
            'operations_pdf': '',
            'training_pdf': ''
        })
    
    return jsonify({
        'about_content': sdrf_content.about_content or '',
        'operations_pdf': sdrf_content.operations_pdf or '',
        'training_pdf': sdrf_content.training_pdf or ''
    })


@bp.route('/admin/api/sdrf/about', methods=['POST'])
@login_required
def save_sdrf_about():
    """Save About SDRF content"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        data = request.json
        about_content = data.get('about_content', '')
        
        sdrf_content = SDRFContent.query.first()
        
        if not sdrf_content:
            sdrf_content = SDRFContent()
            db.session.add(sdrf_content)
        
        sdrf_content.about_content = about_content
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'About SDRF content saved successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/admin/api/sdrf/operations-pdf', methods=['POST'])
@login_required
def upload_operations_pdf():
    """Upload Operations PDF"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF file provided'}), 400
    
    file = request.files['pdf']
    
    if not file or file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are allowed'}), 400
    
    try:
        # Secure filename
        filename = secure_filename('sdrf_operations.pdf')
        
        # Save to static/pdfs directory
        pdf_dir = os.path.join(current_app.root_path, 'static', 'pdfs')
        os.makedirs(pdf_dir, exist_ok=True)
        
        file_path = os.path.join(pdf_dir, filename)
        
        # Delete old file if exists
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Save new file
        file.save(file_path)
        
        # Update database
        sdrf_content = SDRFContent.query.first()
        if not sdrf_content:
            sdrf_content = SDRFContent()
            db.session.add(sdrf_content)
        
        sdrf_content.operations_pdf = f'pdfs/{filename}'
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Operations PDF uploaded successfully',
            'filename': filename
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/admin/api/sdrf/operations-pdf', methods=['DELETE'])
@login_required
def delete_operations_pdf():
    """Delete Operations PDF"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        sdrf_content = SDRFContent.query.first()
        
        if sdrf_content and sdrf_content.operations_pdf:
            # Delete file from filesystem
            file_path = os.path.join(current_app.root_path, 'static', sdrf_content.operations_pdf)
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # Update database
            sdrf_content.operations_pdf = None
            db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Operations PDF deleted successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/admin/api/sdrf/training-pdf', methods=['POST'])
@login_required
def upload_training_pdf():
    """Upload Training PDF"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF file provided'}), 400
    
    file = request.files['pdf']
    
    if not file or file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are allowed'}), 400
    
    try:
        # Secure filename
        filename = secure_filename('sdrf_training.pdf')
        
        # Save to static/pdfs directory
        pdf_dir = os.path.join(current_app.root_path, 'static', 'pdfs')
        os.makedirs(pdf_dir, exist_ok=True)
        
        file_path = os.path.join(pdf_dir, filename)
        
        # Delete old file if exists
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Save new file
        file.save(file_path)
        
        # Update database
        sdrf_content = SDRFContent.query.first()
        if not sdrf_content:
            sdrf_content = SDRFContent()
            db.session.add(sdrf_content)
        
        sdrf_content.training_pdf = f'pdfs/{filename}'
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Training PDF uploaded successfully',
            'filename': filename
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/admin/api/sdrf/training-pdf', methods=['DELETE'])
@login_required
def delete_training_pdf():
    """Delete Training PDF"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        sdrf_content = SDRFContent.query.first()
        
        if sdrf_content and sdrf_content.training_pdf:
            # Delete file from filesystem
            file_path = os.path.join(current_app.root_path, 'static', sdrf_content.training_pdf)
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # Update database
            sdrf_content.training_pdf = None
            db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Training PDF deleted successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/api/battalion/upload-commandant-photo', methods=['POST'])
def upload_commandant_photo():
    """Upload commandant photo for a battalion"""
    try:
        print(f"Upload request received. Files: {list(request.files.keys())}")
        print(f"Form data: {dict(request.form)}")
        
        if 'photo' not in request.files:
            return jsonify({'success': False, 'message': 'No photo provided'}), 400
        
        file = request.files['photo']
        battalion_number = request.form.get('battalion_number')
        
        print(f"File: {file.filename}, Battalion: {battalion_number}")
        
        if not battalion_number:
            return jsonify({'success': False, 'message': 'Battalion number required'}), 400
        
        try:
            battalion_number = int(battalion_number)
        except ValueError:
            return jsonify({'success': False, 'message': 'Invalid battalion number'}), 400
        
        if not file or file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'}), 400
        
        # Check file type - allow common image formats
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}
        if '.' not in file.filename:
            return jsonify({'success': False, 'message': 'Invalid file type. Please upload an image file.'}), 400
            
        ext = file.filename.rsplit('.', 1)[1].lower()
        if ext not in allowed_extensions:
            return jsonify({'success': False, 'message': f'Invalid file type "{ext}". Allowed: JPEG, JPG, PNG, GIF, WEBP, BMP'}), 400
        
        # Get battalion
        battalion = Battalion.query.filter_by(battalion_number=battalion_number).first()
        if not battalion:
            return jsonify({'success': False, 'message': f'Battalion {battalion_number} not found'}), 404
        
        # Generate filename - use JPEG for best quality/size ratio
        filename = f'commandant_{battalion_number}.jpg'
        
        # Save file with quality optimization
        upload_folder = os.path.join(current_app.root_path, 'static', 'images', 'commandants')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        
        print(f"Saving file to: {filepath}")
        
        # Use PIL to process image for better quality
        try:
            from PIL import Image # type: ignore
            import io
            
            # Read uploaded file
            img_data = file.read()
            img = Image.open(io.BytesIO(img_data))
            
            # Convert to RGB if necessary (for PNG with transparency)
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                if 'A' in img.mode:
                    background.paste(img, mask=img.split()[-1])
                else:
                    background.paste(img)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize to optimal size for display (400x400 for high quality)
            target_size = 400
            if img.size[0] != target_size or img.size[1] != target_size:
                # Calculate crop box for center square
                width, height = img.size
                if width > height:
                    left = (width - height) // 2
                    img = img.crop((left, 0, left + height, height))
                elif height > width:
                    top = (height - width) // 2
                    img = img.crop((0, top, width, top + width))
                
                # Resize with high quality
                img = img.resize((target_size, target_size), Image.Resampling.LANCZOS)
            
            # Save with high quality settings
            img.save(filepath, 'JPEG', quality=95, optimize=True, subsampling=0)
            print(f"Photo processed and saved with high quality: {filename}")
            
        except ImportError:
            # Fallback: save directly if PIL not available
            file.seek(0)
            file.save(filepath)
            print(f"Photo saved directly (PIL not available): {filename}")
        
        # Update database - store only filename
        battalion.commandant_image = filename
        db.session.commit()
        
        print(f"Photo uploaded successfully: {filename}")
        
        return jsonify({
            'success': True,
            'message': 'Commandant photo uploaded successfully!',
            'photo_url': url_for('static', filename=f'images/commandants/{filename}')
        })
    except Exception as e:
        print(f"Error uploading photo: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Upload error: {str(e)}'}), 500

@bp.route('/api/battalion/delete-commandant-photo', methods=['POST'])
def delete_commandant_photo():
    """Delete commandant photo for a battalion"""
    try:
        data = request.get_json()
        battalion_number = data.get('battalion_number')
        
        if not battalion_number:
            return jsonify({'success': False, 'message': 'Battalion number required'}), 400
        
        battalion_number = int(battalion_number)
        
        battalion = Battalion.query.filter_by(battalion_number=battalion_number).first()
        if not battalion:
            return jsonify({'success': False, 'message': 'Battalion not found'}), 404
        
        # Delete photo file if exists
        if battalion.commandant_image and battalion.commandant_image != 'default_commandant.svg':
            filepath = os.path.join(current_app.root_path, 'static', 'images', 'commandants', battalion.commandant_image)
            if os.path.exists(filepath):
                os.remove(filepath)
        
        # Update database to use default
        battalion.commandant_image = 'default_commandant.svg'
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Photo deleted successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/api/battalion/upload-battalion-image', methods=['POST'])
def upload_battalion_image():
    """Upload battalion headquarters building image"""
    try:
        print(f"Battalion image upload request. Files: {list(request.files.keys())}")
        print(f"Form data: {dict(request.form)}")
        
        if 'image' not in request.files:
            return jsonify({'success': False, 'message': 'No image provided'}), 400
        
        file = request.files['image']
        battalion_number = request.form.get('battalion_number')
        
        print(f"File: {file.filename}, Battalion: {battalion_number}")
        
        if not battalion_number:
            return jsonify({'success': False, 'message': 'Battalion number required'}), 400
        
        try:
            battalion_number = int(battalion_number)
        except ValueError:
            return jsonify({'success': False, 'message': 'Invalid battalion number'}), 400
        
        if not file or file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'}), 400
        
        # Check file type - allow common image formats
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}
        if '.' not in file.filename:
            return jsonify({'success': False, 'message': 'Invalid file type. Please upload an image file.'}), 400
            
        ext = file.filename.rsplit('.', 1)[1].lower()
        if ext not in allowed_extensions:
            return jsonify({'success': False, 'message': f'Invalid file type "{ext}". Allowed: JPEG, JPG, PNG, GIF, WEBP, BMP'}), 400
        
        # Get battalion
        battalion = Battalion.query.filter_by(battalion_number=battalion_number).first()
        if not battalion:
            return jsonify({'success': False, 'message': f'Battalion {battalion_number} not found'}), 404
        
        # Generate filename
        filename = f'{battalion_number}th-bn.{ext}'
        
        # Save file
        upload_folder = os.path.join(current_app.root_path, 'static', 'images', 'battalions')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        
        print(f"Saving battalion image to: {filepath}")
        file.save(filepath)
        
        # Update database - store only filename
        battalion.image = filename
        db.session.commit()
        
        print(f"Battalion image uploaded successfully: {filename}")
        
        return jsonify({
            'success': True,
            'message': 'Battalion image uploaded successfully!',
            'image_url': url_for('static', filename=f'images/battalions/{filename}')
        })
    except Exception as e:
        print(f"Error uploading battalion image: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Upload error: {str(e)}'}), 500

@bp.route('/api/battalion/delete-battalion-image', methods=['POST'])
def delete_battalion_image():
    """Delete battalion headquarters building image"""
    try:
        data = request.get_json()
        battalion_number = data.get('battalion_number')
        
        if not battalion_number:
            return jsonify({'success': False, 'message': 'Battalion number required'}), 400
        
        battalion_number = int(battalion_number)
        
        battalion = Battalion.query.filter_by(battalion_number=battalion_number).first()
        if not battalion:
            return jsonify({'success': False, 'message': 'Battalion not found'}), 404
        
        # Delete image file if exists (try all extensions)
        upload_folder = os.path.join(current_app.root_path, 'static', 'images', 'battalions')
        extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp']
        
        deleted = False
        for ext in extensions:
            filename = f'{battalion_number}th-bn.{ext}'
            filepath = os.path.join(upload_folder, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                deleted = True
        
        # Update database to clear image field
        battalion.image = None
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Battalion image deleted successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


# ==================== BATTALION ADMIN ROUTES ====================

@bp.route('/battalion-admin/login', methods=['GET', 'POST'])
def battalion_admin_login():
    """Battalion admin login"""
    error = None
    battalion_number = request.args.get('battalion') or request.form.get('battalion_number')
    redirect_url = request.form.get('redirect_url')  # Get redirect URL if provided
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, is_battalion_admin=True).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.battalion_admin_dashboard'))
        else:
            error = 'Invalid username or password.'
            # If login failed and redirect_url exists, redirect back to battalion page with error
            if redirect_url:
                flash(error, 'danger')
                return redirect(redirect_url)
    
    return render_template('battalion-admin-login.html', error=error, battalion_number=battalion_number)

@bp.route('/battalion/<int:battalion_id>/admin-login', methods=['POST'])
def battalion_detail_login(battalion_id):
    """Handle login from battalion detail page"""
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = User.query.filter_by(username=username, is_battalion_admin=True).first()
    
    if user and check_password_hash(user.password, password):
        # Check if user's battalion matches the page they're logging in from
        battalion = Battalion.query.filter_by(battalion_number=battalion_id).first()
        if battalion and user.battalion_id == battalion.id:
            login_user(user)
            # Redirect back to same battalion page to show edit interface inline
            return redirect(url_for('main.battalion_detail', battalion_id=battalion_id))
        else:
            flash('You are not authorized for this battalion', 'error')
    else:
        flash('Invalid username or password', 'error')
    
    return redirect(url_for('main.battalion_detail', battalion_id=battalion_id))

@bp.route('/api/battalion/<int:battalion_number>/update', methods=['POST'])
@login_required
def api_update_battalion(battalion_number):
    """API endpoint to update battalion data inline"""
    if not current_user.is_battalion_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    data = request.json
    battalion = Battalion.query.filter_by(battalion_number=battalion_number).first()
    
    if not battalion:
        return jsonify({'success': False, 'message': 'Battalion not found'}), 404
    
    # Check if current user is admin of this battalion
    if current_user.battalion_id != battalion.id:
        return jsonify({'success': False, 'message': 'Unauthorized for this battalion'}), 403
    
    try:
        battalion.district = data.get('district', battalion.district)
        battalion.commandant_name = data.get('commandant_name', battalion.commandant_name)
        battalion.commandant_rank = data.get('commandant_rank', battalion.commandant_rank)
        battalion.commandant_speech = data.get('commandant_speech', battalion.commandant_speech)
        battalion.organizational_structure = data.get('organizational_structure', battalion.organizational_structure)
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Battalion updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/api/battalion-admin/change-password', methods=['POST'])
def api_battalion_admin_change_password():
    """Change password for battalion admin

    Note: this endpoint must return JSON for XHR requests. We avoid using
    @login_required which would redirect to an HTML login page when the
    client is not authenticated (causing JSON.parse errors). Instead perform
    explicit checks and return JSON responses with proper status codes.
    """
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    if not current_user.is_battalion_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    data = request.json
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    if not check_password_hash(current_user.password, current_password):
        return jsonify({'success': False, 'message': 'Current password is incorrect'})
    
    try:
        current_user.password = generate_password_hash(new_password)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Password updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/api/battalion-admin/login-change-password', methods=['POST'])
def api_battalion_admin_login_change_password():
    """Change password for battalion admin without being logged in"""
    data = request.json
    username = data.get('username')
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    user = User.query.filter_by(username=username, is_battalion_admin=True).first()
    
    if not user:
        return jsonify({'success': False, 'message': 'User not found'})
    
    if not check_password_hash(user.password, current_password):
        return jsonify({'success': False, 'message': 'Current password is incorrect'})
    
    try:
        user.password = generate_password_hash(new_password)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Password updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/battalion-admin/dashboard')
@login_required
def battalion_admin_dashboard():
    """Battalion admin dashboard"""
    if not current_user.is_battalion_admin:
        return redirect(url_for('main.battalion_admin_login'))
    
    battalion = Battalion.query.get(current_user.battalion_id)
    if not battalion:
        flash('Battalion not found', 'danger')
        return redirect(url_for('main.index'))
    
    return render_template('battalion-admin-dashboard.html', battalion=battalion)

@bp.route('/battalion-admin/edit', methods=['GET', 'POST'])
@login_required
def battalion_admin_edit():
    """Edit battalion basic information"""
    if not current_user.is_battalion_admin:
        return redirect(url_for('main.battalion_admin_login'))
    
    battalion = Battalion.query.get(current_user.battalion_id)
    if not battalion:
        flash('Battalion not found', 'danger')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        try:
            battalion.name = request.form.get('name', battalion.name)
            battalion.district = request.form.get('district', battalion.district)
            battalion.description = request.form.get('description', battalion.description)
            
            # Handle battalion image upload
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename:
                    filename = secure_filename(f"{battalion.battalion_number}th-bn.jpg")
                    upload_folder = os.path.join(current_app.root_path, 'static', 'images', 'battalions')
                    os.makedirs(upload_folder, exist_ok=True)
                    file.save(os.path.join(upload_folder, filename))
                    battalion.image = filename
            
            db.session.commit()
            flash('Battalion information updated successfully!', 'success')
            return redirect(url_for('main.battalion_admin_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating battalion: {str(e)}', 'danger')
    
    return render_template('battalion-admin-edit.html', battalion=battalion)

@bp.route('/battalion-admin/commandant', methods=['GET', 'POST'])
@login_required
def battalion_admin_commandant():
    """Manage commandant information"""
    if not current_user.is_battalion_admin:
        return redirect(url_for('main.battalion_admin_login'))
    
    battalion = Battalion.query.get(current_user.battalion_id)
    if not battalion:
        flash('Battalion not found', 'danger')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        try:
            battalion.commandant_name = request.form.get('commandant_name', battalion.commandant_name)
            battalion.commandant_rank = request.form.get('commandant_rank', battalion.commandant_rank)
            battalion.commandant_speech = request.form.get('commandant_speech', battalion.commandant_speech)
            battalion.ri_1 = request.form.get('ri_1', battalion.ri_1)
            battalion.ri_2 = request.form.get('ri_2', battalion.ri_2)
            battalion.ri_3 = request.form.get('ri_3', battalion.ri_3)
            
            # Handle commandant image upload
            if 'commandant_image' in request.files:
                file = request.files['commandant_image']
                if file and file.filename:
                    filename = secure_filename(f"commandant-{battalion.battalion_number}.jpg")
                    upload_folder = os.path.join(current_app.root_path, 'static', 'images', 'commandants')
                    os.makedirs(upload_folder, exist_ok=True)
                    file.save(os.path.join(upload_folder, filename))
                    battalion.commandant_image = filename
            
            db.session.commit()
            flash('Commandant information updated successfully!', 'success')
            return redirect(url_for('main.battalion_admin_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating commandant: {str(e)}', 'danger')
    
    return render_template('battalion-admin-commandant.html', battalion=battalion)

@bp.route('/battalion-admin/organization', methods=['GET', 'POST'])
@login_required
def battalion_admin_organization():
    """Manage organizational structure"""
    if not current_user.is_battalion_admin:
        return redirect(url_for('main.battalion_admin_login'))
    
    battalion = Battalion.query.get(current_user.battalion_id)
    if not battalion:
        flash('Battalion not found', 'danger')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        try:
            org_structure = request.form.get('organizational_structure', battalion.organizational_structure)
            battalion.organizational_structure = org_structure
            
            db.session.commit()
            flash('Organizational structure updated successfully!', 'success')
            return redirect(url_for('main.battalion_admin_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating organization: {str(e)}', 'danger')
    
    return render_template('battalion-admin-organization.html', battalion=battalion)

@bp.route('/battalion-admin/history', methods=['GET', 'POST'])
@login_required
def battalion_admin_history():
    """Manage battalion history"""
    if not current_user.is_battalion_admin:
        return redirect(url_for('main.battalion_admin_login'))
    
    battalion = Battalion.query.get(current_user.battalion_id)
    if not battalion:
        flash('Battalion not found', 'danger')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        try:
            battalion.history = request.form.get('history', battalion.history)
            
            db.session.commit()
            flash('Battalion history updated successfully!', 'success')
            return redirect(url_for('main.battalion_admin_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating history: {str(e)}', 'danger')
    
    return render_template('battalion-admin-history.html', battalion=battalion)

@bp.route('/battalion-admin/change-password', methods=['GET', 'POST'])
@login_required
def battalion_admin_change_password():
    """Change battalion admin password"""
    if not current_user.is_battalion_admin:
        return redirect(url_for('main.battalion_admin_login'))
    
    battalion = Battalion.query.get(current_user.battalion_id)
    if not battalion:
        flash('Battalion not found', 'danger')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate inputs
        if not all([current_password, new_password, confirm_password]):
            flash('All fields are required', 'danger')
            return render_template('battalion-admin-change-password.html', battalion=battalion)
        
        if new_password != confirm_password:
            flash('New passwords do not match', 'danger')
            return render_template('battalion-admin-change-password.html', battalion=battalion)
        
        if len(new_password) < 8:
            flash('Password must be at least 8 characters long', 'danger')
            return render_template('battalion-admin-change-password.html', battalion=battalion)
        
        # Check current password
        if not check_password_hash(current_user.password, current_password):
            flash('Current password is incorrect', 'danger')
            return render_template('battalion-admin-change-password.html', battalion=battalion)
        
        try:
            # Update password
            current_user.password = generate_password_hash(new_password)
            db.session.commit()
            flash('Password changed successfully!', 'success')
            return redirect(url_for('main.battalion_admin_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error changing password: {str(e)}', 'danger')
    
    return render_template('battalion-admin-change-password.html', battalion=battalion)


# Battalion Admin - Events Management
@bp.route('/battalion-admin/events', methods=['GET'])
@login_required
def battalion_admin_events():
    """Manage battalion events"""
    if not current_user.is_battalion_admin:
        return redirect(url_for('main.battalion_admin_login'))
    
    battalion = Battalion.query.get(current_user.battalion_id)
    if not battalion:
        flash('Battalion not found', 'danger')
        return redirect(url_for('main.index'))
    
    from app.models.battalion_content import BattalionEvent
    events = BattalionEvent.query.filter_by(battalion_id=battalion.id).order_by(BattalionEvent.date.desc()).all()
    
    return render_template('battalion-admin-events.html', battalion=battalion, events=events)


@bp.route('/api/battalion/events/add', methods=['POST'])
@login_required
def api_add_battalion_event():
    """API endpoint to add a battalion event"""
    if not current_user.is_battalion_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        from app.models.battalion_content import BattalionEvent
        data = request.get_json()
        
        event = BattalionEvent(
            battalion_id=data['battalion_id'],
            title=data['title'],
            date=data['date'],
            location=data.get('location', ''),
            description=data.get('description', '')
        )
        
        db.session.add(event)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Event added successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400


@bp.route('/api/battalion/events/delete', methods=['POST'])
@login_required
def api_delete_battalion_event():
    """API endpoint to delete a battalion event"""
    if not current_user.is_battalion_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        from app.models.battalion_content import BattalionEvent
        data = request.get_json()
        event_id = data['event_id']
        
        event = BattalionEvent.query.get(event_id)
        if not event or event.battalion_id != current_user.battalion_id:
            return jsonify({'success': False, 'message': 'Event not found'}), 404
        
        db.session.delete(event)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Event deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400


# Battalion Admin - Announcements Management
@bp.route('/battalion-admin/announcements', methods=['GET'])
@login_required
def battalion_admin_announcements():
    """Manage battalion announcements"""
    if not current_user.is_battalion_admin:
        return redirect(url_for('main.battalion_admin_login'))
    
    battalion = Battalion.query.get(current_user.battalion_id)
    if not battalion:
        flash('Battalion not found', 'danger')
        return redirect(url_for('main.index'))
    
    from app.models.battalion_content import BattalionAnnouncement
    announcements = BattalionAnnouncement.query.filter_by(battalion_id=battalion.id).order_by(BattalionAnnouncement.date.desc()).all()
    
    return render_template('battalion-admin-announcements.html', battalion=battalion, announcements=announcements)


@bp.route('/api/battalion/announcements/add', methods=['POST'])
@login_required
def api_add_battalion_announcement():
    """API endpoint to add a battalion announcement"""
    if not current_user.is_battalion_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        from app.models.battalion_content import BattalionAnnouncement
        data = request.get_json()
        
        announcement = BattalionAnnouncement(
            battalion_id=data['battalion_id'],
            title=data['title'],
            date=data['date'],
            content=data.get('content', '')
        )
        
        db.session.add(announcement)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Announcement added successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400


@bp.route('/api/battalion/announcements/delete', methods=['POST'])
@login_required
def api_delete_battalion_announcement():
    """API endpoint to delete a battalion announcement"""
    if not current_user.is_battalion_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        from app.models.battalion_content import BattalionAnnouncement
        data = request.get_json()
        announcement_id = data['announcement_id']
        
        announcement = BattalionAnnouncement.query.get(announcement_id)
        if not announcement or announcement.battalion_id != current_user.battalion_id:
            return jsonify({'success': False, 'message': 'Announcement not found'}), 404
        
        db.session.delete(announcement)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Announcement deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400


# Battalion Admin - Gallery Management
@bp.route('/battalion-admin/gallery', methods=['GET'])
@login_required
def battalion_admin_gallery():
    """Manage battalion gallery"""
    if not current_user.is_battalion_admin:
        return redirect(url_for('main.battalion_admin_login'))
    
    battalion = Battalion.query.get(current_user.battalion_id)
    if not battalion:
        flash('Battalion not found', 'danger')
        return redirect(url_for('main.index'))
    
    from app.models.battalion_content import BattalionGallery
    gallery_images = BattalionGallery.query.filter_by(battalion_id=battalion.id).order_by(BattalionGallery.created_at.desc()).all()
    
    return render_template('battalion-admin-gallery.html', battalion=battalion, gallery_images=gallery_images)


@bp.route('/api/battalion/gallery/upload', methods=['POST'])
@login_required
def api_upload_battalion_gallery():
    """API endpoint to upload a battalion gallery image"""
    if not current_user.is_battalion_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        from app.models.battalion_content import BattalionGallery
        import os
        from werkzeug.utils import secure_filename
        
        if 'image' not in request.files:
            return jsonify({'success': False, 'message': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'}), 400
        
        # Check file extension
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        filename = secure_filename(file.filename)
        if not '.' in filename or filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({'success': False, 'message': 'Invalid file type. Use PNG, JPG, JPEG, GIF, or WEBP'}), 400
        
        # Create directory if it doesn't exist
        upload_dir = os.path.join('app', 'static', 'images', 'battalion_gallery')
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate unique filename
        import uuid
        ext = filename.rsplit('.', 1)[1].lower()
        new_filename = f"battalion_{current_user.battalion_id}_{uuid.uuid4().hex[:8]}.{ext}"
        filepath = os.path.join(upload_dir, new_filename)
        
        # Save file
        file.save(filepath)
        
        # Create database entry
        caption = request.form.get('caption', '')
        gallery_image = BattalionGallery(
            battalion_id=current_user.battalion_id,
            image_path=new_filename,
            caption=caption
        )
        
        db.session.add(gallery_image)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Image uploaded successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400


@bp.route('/api/battalion/gallery/delete', methods=['POST'])
@login_required
def api_delete_battalion_gallery():
    """API endpoint to delete a battalion gallery image"""
    if not current_user.is_battalion_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        from app.models.battalion_content import BattalionGallery
        import os
        
        data = request.get_json()
        image_id = data['image_id']
        
        image = BattalionGallery.query.get(image_id)
        if not image or image.battalion_id != current_user.battalion_id:
            return jsonify({'success': False, 'message': 'Image not found'}), 404
        
        # Delete file from filesystem
        try:
            filepath = os.path.join('app', 'static', 'images', 'battalion_gallery', image.image_path)
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            print(f"Error deleting file: {e}")
        
        # Delete from database
        db.session.delete(image)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Image deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400


@bp.route('/api/battalion/events/update', methods=['POST'])
@login_required
def api_update_battalion_event():
    """API endpoint to update a battalion event"""
    if not current_user.is_battalion_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        from app.models.battalion_content import BattalionEvent
        data = request.get_json()
        event_id = data.get('event_id')
        
        event = BattalionEvent.query.get(event_id)
        if not event or event.battalion_id != current_user.battalion_id:
            return jsonify({'success': False, 'message': 'Event not found'}), 404
        
        event.title = data.get('title', event.title)
        event.date = data.get('date', event.date)
        event.location = data.get('location', event.location)
        event.description = data.get('description', event.description)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Event updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400


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



 
 #   O f f i c e r   M a n a g e m e n t   A P I   R o u t e s 
 
 @ b p . r o u t e ( ' / a d m i n / a p i / o f f i c e r s ' ,   m e t h o d s = [ ' G E T ' ] ) 
 
 @ l o g i n _ r e q u i r e d 
 
 d e f   g e t _ o f f i c e r s ( ) : 
 
         " " " G e t   a l l   o f f i c e r s " " " 
 
         i f   n o t   c u r r e n t _ u s e r . i s _ a d m i n : 
 
                 r e t u r n   j s o n i f y ( { ' e r r o r ' :   ' U n a u t h o r i z e d ' } ) ,   4 0 3 
 
         
 
         o f f i c e r s   =   O f f i c e r . q u e r y . o r d e r _ b y ( O f f i c e r . p r i o r i t y . a s c ( ) ) . a l l ( ) 
 
         r e t u r n   j s o n i f y ( { 
 
                 ' s u c c e s s ' :   T r u e , 
 
                 ' o f f i c e r s ' :   [ o f f i c e r . t o _ d i c t ( )   f o r   o f f i c e r   i n   o f f i c e r s ] 
 
         } ) 
 
 
 
 @ b p . r o u t e ( ' / a d m i n / a p i / o f f i c e r s ' ,   m e t h o d s = [ ' P O S T ' ] ) 
 
 @ l o g i n _ r e q u i r e d 
 
 d e f   a d d _ o f f i c e r ( ) : 
 
         " " " A d d   n e w   o f f i c e r " " " 
 
         i f   n o t   c u r r e n t _ u s e r . i s _ a d m i n : 
 
                 r e t u r n   j s o n i f y ( { ' e r r o r ' :   ' U n a u t h o r i z e d ' } ) ,   4 0 3 
 
         
 
         t r y : 
 
                 d a t a   =   r e q u e s t . f o r m 
 
                 f i l e   =   r e q u e s t . f i l e s . g e t ( ' i m a g e ' ) 
 
                 
 
                 i m a g e _ f i l e n a m e   =   ' d e f a u l t . j p g ' 
 
                 i f   f i l e : 
 
                         f i l e n a m e   =   s e c u r e _ f i l e n a m e ( f i l e . f i l e n a m e ) 
 
                         #   C r e a t e   f o l d e r   i f   n o t   e x i s t s 
 
                         o f f i c e r s _ f o l d e r   =   o s . p a t h . j o i n ( c u r r e n t _ a p p . s t a t i c _ f o l d e r ,   ' i m a g e s ' ,   ' o f f i c e r s ' ) 
 
                         o s . m a k e d i r s ( o f f i c e r s _ f o l d e r ,   e x i s t _ o k = T r u e ) 
 
                         
 
                         i m p o r t   u u i d 
 
                         u n i q u e _ f i l e n a m e   =   f " { u u i d . u u i d 4 ( ) . h e x } _ { f i l e n a m e } " 
 
                         f i l e . s a v e ( o s . p a t h . j o i n ( o f f i c e r s _ f o l d e r ,   u n i q u e _ f i l e n a m e ) ) 
 
                         i m a g e _ f i l e n a m e   =   u n i q u e _ f i l e n a m e 
 
 
 
                 o f f i c e r   =   O f f i c e r ( 
 
                         n a m e = d a t a . g e t ( ' n a m e ' ) , 
 
                         r a n k = d a t a . g e t ( ' r a n k ' ) , 
 
                         d e s i g n a t i o n = d a t a . g e t ( ' d e s i g n a t i o n ' ) , 
 
                         p h o n e = d a t a . g e t ( ' p h o n e ' ) , 
 
                         e m a i l = d a t a . g e t ( ' e m a i l ' ) , 
 
                         l o c a t i o n = d a t a . g e t ( ' l o c a t i o n ' ) , 
 
                         i m a g e _ f i l e = i m a g e _ f i l e n a m e , 
 
                         p r i o r i t y = i n t ( d a t a . g e t ( ' p r i o r i t y ' ,   0 ) ) 
 
                 ) 
 
                 
 
                 d b . s e s s i o n . a d d ( o f f i c e r ) 
 
                 d b . s e s s i o n . c o m m i t ( ) 
 
                 
 
                 r e t u r n   j s o n i f y ( { 
 
                         ' s u c c e s s ' :   T r u e , 
 
                         ' m e s s a g e ' :   ' O f f i c e r   a d d e d   s u c c e s s f u l l y ' , 
 
                         ' o f f i c e r ' :   o f f i c e r . t o _ d i c t ( ) 
 
                 } ) 
 
         e x c e p t   E x c e p t i o n   a s   e : 
 
                 d b . s e s s i o n . r o l l b a c k ( ) 
 
                 r e t u r n   j s o n i f y ( { ' e r r o r ' :   s t r ( e ) } ) ,   5 0 0 
 
 
 
 @ b p . r o u t e ( ' / a d m i n / a p i / o f f i c e r s / < i n t : i d > ' ,   m e t h o d s = [ ' P U T ' ] ) 
 
 @ l o g i n _ r e q u i r e d 
 
 d e f   u p d a t e _ o f f i c e r ( i d ) : 
 
         " " " U p d a t e   o f f i c e r " " " 
 
         i f   n o t   c u r r e n t _ u s e r . i s _ a d m i n : 
 
                 r e t u r n   j s o n i f y ( { ' e r r o r ' :   ' U n a u t h o r i z e d ' } ) ,   4 0 3 
 
         
 
         o f f i c e r   =   O f f i c e r . q u e r y . g e t _ o r _ 4 0 4 ( i d ) 
 
         
 
         t r y : 
 
                 d a t a   =   r e q u e s t . f o r m 
 
                 f i l e   =   r e q u e s t . f i l e s . g e t ( ' i m a g e ' ) 
 
                 
 
                 i f   f i l e : 
 
                         f i l e n a m e   =   s e c u r e _ f i l e n a m e ( f i l e . f i l e n a m e ) 
 
                         o f f i c e r s _ f o l d e r   =   o s . p a t h . j o i n ( c u r r e n t _ a p p . s t a t i c _ f o l d e r ,   ' i m a g e s ' ,   ' o f f i c e r s ' ) 
 
                         o s . m a k e d i r s ( o f f i c e r s _ f o l d e r ,   e x i s t _ o k = T r u e ) 
 
                         
 
                         i m p o r t   u u i d 
 
                         u n i q u e _ f i l e n a m e   =   f " { u u i d . u u i d 4 ( ) . h e x } _ { f i l e n a m e } " 
 
                         f i l e . s a v e ( o s . p a t h . j o i n ( o f f i c e r s _ f o l d e r ,   u n i q u e _ f i l e n a m e ) ) 
 
                         o f f i c e r . i m a g e _ f i l e   =   u n i q u e _ f i l e n a m e 
 
 
 
                 i f   ' n a m e '   i n   d a t a :   o f f i c e r . n a m e   =   d a t a [ ' n a m e ' ] 
 
                 i f   ' r a n k '   i n   d a t a :   o f f i c e r . r a n k   =   d a t a [ ' r a n k ' ] 
 
                 i f   ' d e s i g n a t i o n '   i n   d a t a :   o f f i c e r . d e s i g n a t i o n   =   d a t a [ ' d e s i g n a t i o n ' ] 
 
                 i f   ' p h o n e '   i n   d a t a :   o f f i c e r . p h o n e   =   d a t a [ ' p h o n e ' ] 
 
                 i f   ' e m a i l '   i n   d a t a :   o f f i c e r . e m a i l   =   d a t a [ ' e m a i l ' ] 
 
                 i f   ' l o c a t i o n '   i n   d a t a :   o f f i c e r . l o c a t i o n   =   d a t a [ ' l o c a t i o n ' ] 
 
                 i f   ' p r i o r i t y '   i n   d a t a :   o f f i c e r . p r i o r i t y   =   i n t ( d a t a [ ' p r i o r i t y ' ] ) 
 
                 
 
                 d b . s e s s i o n . c o m m i t ( ) 
 
                 
 
                 r e t u r n   j s o n i f y ( { 
 
                         ' s u c c e s s ' :   T r u e , 
 
                         ' m e s s a g e ' :   ' O f f i c e r   u p d a t e d   s u c c e s s f u l l y ' , 
 
                         ' o f f i c e r ' :   o f f i c e r . t o _ d i c t ( ) 
 
                 } ) 
 
         e x c e p t   E x c e p t i o n   a s   e : 
 
                 d b . s e s s i o n . r o l l b a c k ( ) 
 
                 r e t u r n   j s o n i f y ( { ' e r r o r ' :   s t r ( e ) } ) ,   5 0 0 
 
 
 
 @ b p . r o u t e ( ' / a d m i n / a p i / o f f i c e r s / < i n t : i d > ' ,   m e t h o d s = [ ' D E L E T E ' ] ) 
 
 @ l o g i n _ r e q u i r e d 
 
 d e f   d e l e t e _ o f f i c e r ( i d ) : 
 
         " " " D e l e t e   o f f i c e r " " " 
 
         i f   n o t   c u r r e n t _ u s e r . i s _ a d m i n : 
 
                 r e t u r n   j s o n i f y ( { ' e r r o r ' :   ' U n a u t h o r i z e d ' } ) ,   4 0 3 
 
         
 
         o f f i c e r   =   O f f i c e r . q u e r y . g e t _ o r _ 4 0 4 ( i d ) 
 
         
 
         t r y : 
 
                 d b . s e s s i o n . d e l e t e ( o f f i c e r ) 
 
                 d b . s e s s i o n . c o m m i t ( ) 
 
                 r e t u r n   j s o n i f y ( { ' s u c c e s s ' :   T r u e ,   ' m e s s a g e ' :   ' O f f i c e r   d e l e t e d   s u c c e s s f u l l y ' } ) 
 
         e x c e p t   E x c e p t i o n   a s   e : 
 
                 d b . s e s s i o n . r o l l b a c k ( ) 
 
                 r e t u r n   j s o n i f y ( { ' e r r o r ' :   s t r ( e ) } ) ,   5 0 0 
 
 
