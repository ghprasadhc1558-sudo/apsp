# Battalion Admin System - Complete Documentation

## Overview
The APSP website now has a comprehensive battalion-level admin system where each of the 12 battalions has its own admin login. Battalion admins can manage their battalion's information independently.

## Features Implemented

### 1. **Battalion Admin Authentication**
- Separate login page for battalion admins: `/battalion-admin/login`
- Each battalion has its own admin account
- Secure password-based authentication
- Sessions are maintained separately from main admin

### 2. **Battalion Admin Dashboard**
Each battalion admin gets access to a personalized dashboard with:
- Battalion statistics and quick overview
- Quick action cards for common tasks
- Navigation sidebar with all management options
- Direct link to view their battalion's public page

### 3. **Management Capabilities**
Battalion admins can manage:

#### a) **Basic Battalion Information**
- Battalion name
- District/Location
- Description
- Battalion headquarters image upload

#### b) **Commandant Details**
- Commandant name and rank
- Commandant photo upload
- Commandant speech/message
- Reserve Inspector details (RI-1, RI-2, RI-3)

#### c) **Organizational Structure**
- Edit organizational hierarchy
- JSON-based structure management
- Add/update officers and companies

#### d) **Battalion History**
- Update and maintain battalion historical information
- Rich text editing capabilities

#### e) **Security**
- Change own password
- Password requirements enforcement
- Secure password storage

## Battalion Admin Accounts

All 12 battalions now have admin accounts:

| Battalion | Username | Default Password | Login URL |
|-----------|----------|------------------|-----------|
| 1st Battalion | battalion1_admin | Bn1@APSP2024 | /battalion-admin/login |
| 2nd Battalion | battalion2_admin | Bn2@APSP2024 | /battalion-admin/login |
| 3rd Battalion | battalion3_admin | Bn3@APSP2024 | /battalion-admin/login |
| 4th Battalion | battalion4_admin | Bn4@APSP2024 | /battalion-admin/login |
| 5th Battalion | battalion5_admin | Bn5@APSP2024 | /battalion-admin/login |
| 6th Battalion | battalion6_admin | Bn6@APSP2024 | /battalion-admin/login |
| 7th Battalion | battalion7_admin | Bn7@APSP2024 | /battalion-admin/login |
| 8th Battalion | battalion8_admin | Bn8@APSP2024 | /battalion-admin/login |
| 9th Battalion | battalion9_admin | Bn9@APSP2024 | /battalion-admin/login |
| 11th Battalion | battalion11_admin | Bn11@APSP2024 | /battalion-admin/login |
| 14th Battalion | battalion14_admin | Bn14@APSP2024 | /battalion-admin/login |
| 16th Battalion | battalion16_admin | Bn16@APSP2024 | /battalion-admin/login |

## Security Features

### 1. **Access Control**
- Battalion admins can ONLY access their own battalion data
- Cannot view or edit other battalions
- Separate authentication system from main admin

### 2. **Password Security**
- Passwords are hashed using Werkzeug's security functions
- Minimum 8 character requirement
- Change password functionality available
- Password confirmation during changes

### 3. **Session Management**
- Flask-Login handles user sessions
- Automatic logout on browser close (can be configured)
- Login required decorators protect all admin routes

## File Structure

### New Files Created:
```
app/
├── templates/
│   ├── battalion-admin-login.html          # Battalion admin login page
│   ├── battalion-admin-dashboard.html      # Battalion admin dashboard
│   ├── battalion-admin-edit.html           # Edit battalion info
│   ├── battalion-admin-commandant.html     # Manage commandant
│   ├── battalion-admin-organization.html   # Edit org structure
│   ├── battalion-admin-history.html        # Edit battalion history
│   └── battalion-admin-change-password.html # Change password page

Scripts:
├── migrate_user_table.py                   # Database migration script
└── init_battalion_admins.py                # Initialize battalion admin users
```

### Modified Files:
```
app/
├── models/
│   └── user.py                             # Added battalion admin fields
└── routes.py                               # Added battalion admin routes
```

## Routes Added

### Public Routes:
- `GET/POST /battalion-admin/login` - Battalion admin login

### Protected Routes (Login Required):
- `GET /battalion-admin/dashboard` - Battalion admin dashboard
- `GET/POST /battalion-admin/edit` - Edit battalion information
- `GET/POST /battalion-admin/commandant` - Manage commandant details
- `GET/POST /battalion-admin/organization` - Update org structure
- `GET/POST /battalion-admin/history` - Update battalion history
- `GET/POST /battalion-admin/change-password` - Change password

## Database Schema Changes

### User Model Updates:
```python
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_battalion_admin = db.Column(db.Boolean, default=False)  # NEW
    battalion_id = db.Column(db.Integer, db.ForeignKey('battalion.id'))  # NEW
```

## Usage Instructions

### For Battalion Admins:

1. **First Login**:
   - Go to: `http://your-domain.com/battalion-admin/login`
   - Use your battalion username and default password
   - Example: `battalion2_admin` / `Bn2@APSP2024`

2. **Change Password** (Recommended):
   - After first login, go to "Change Password" in the sidebar
   - Enter current password and new password
   - Confirm new password
   - Click "Update Password"

3. **Edit Battalion Information**:
   - Click "Edit Battalion Info" from dashboard
   - Update name, district, description
   - Upload battalion headquarters image
   - Click "Save Changes"

4. **Manage Commandant**:
   - Click "Manage Commandant" from dashboard
   - Update commandant name, rank, photo
   - Add commandant speech/message
   - Update Reserve Inspector details
   - Click "Save Changes"

5. **Update Organization**:
   - Click "Organization Structure"
   - Edit JSON structure or use the form
   - Click "Save Changes"

6. **Update History**:
   - Click "Battalion History"
   - Use rich text editor to update history
   - Click "Save Changes"

### For Main Admin:

The main admin login remains unchanged at `/admin/login` and maintains full system access.

## Maintenance Scripts

### Re-initialize Battalion Admins:
```bash
python init_battalion_admins.py
```
This will:
- Create new battalion admin accounts if they don't exist
- Update existing accounts (without changing passwords)
- Display all credentials

### Database Migration (if needed):
```bash
python migrate_user_table.py
```
This adds the battalion admin columns to the user table.

## Important Security Notes

1. **Change Default Passwords**: All battalion admins should change their passwords after first login
2. **Secure Credential Distribution**: Share credentials securely with battalion commandants
3. **Regular Password Updates**: Encourage periodic password changes
4. **Access Monitoring**: Main admin should monitor battalion admin activities
5. **Data Isolation**: Each battalion admin can only access their own data

## Future Enhancements (Optional)

Consider implementing:
1. Activity logging for battalion admin actions
2. Email notifications for important changes
3. Two-factor authentication (2FA)
4. Password reset via email
5. Bulk image upload capabilities
6. Rich text editor for descriptions
7. Preview mode before publishing changes
8. Version history for content changes

## Troubleshooting

### Battalion Admin Can't Login:
- Verify username format: `battalion[NUMBER]_admin`
- Check if password was changed from default
- Ensure user exists in database
- Check if `is_battalion_admin` flag is set

### Can't See Battalion Data:
- Verify `battalion_id` is correctly set in user table
- Check if battalion exists with that ID
- Verify user is logged in

### Permission Errors:
- Ensure login_required decorator is present
- Check if user has `is_battalion_admin = True`
- Verify session is active

## Support

For technical support or issues:
1. Check application logs for errors
2. Verify database integrity
3. Ensure all dependencies are installed
4. Contact system administrator

---

**System Status**: ✅ Fully Operational
**Last Updated**: January 21, 2026
**Version**: 1.0
