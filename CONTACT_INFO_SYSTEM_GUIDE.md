# Contact Information Management System

## Overview
The Contact Information Management System allows admin users to manage multiple phone numbers, email addresses, and office address information that is displayed on the public Contact Us page.

## Features
✅ **Multiple Phone Numbers**: Add unlimited phone numbers with remove buttons
✅ **Multiple Email Addresses**: Add unlimited email addresses with remove buttons
✅ **Office Address**: Single text area for full office address
✅ **Dynamic Loading**: Contact page automatically loads latest information
✅ **Auto-Save**: Save all contact information with one click
✅ **Database Backed**: All data stored in SQLite database

## Files Modified/Created

### New Files:
1. `init_contacts.py` - Initialization script for contact info database
2. `CONTACT_INFO_SYSTEM_GUIDE.md` - This documentation file

### Modified Files:
1. `app/models/contact.py` - Added `ContactInfo` model with JSON storage
2. `app/models/__init__.py` - Exported `ContactInfo` model
3. `app/routes.py` - Added admin and public API endpoints:
   - `GET /admin/api/contacts` - Get contact info (admin only)
   - `POST /admin/api/contacts` - Save contact info (admin only)
   - `GET /api/contacts` - Public API for contact page
4. `app/templates/admin-dashboard.html` - Updated contacts section with:
   - Dynamic phone number fields
   - Dynamic email address fields
   - Add/Remove buttons
   - Save functionality
5. `app/templates/contacts.html` - Updated to dynamically load contact data

## Database Schema

### ContactInfo Model
```python
class ContactInfo(db.Model):
    id: Integer (Primary Key)
    phone_numbers: Text (JSON array)
    email_addresses: Text (JSON array)
    office_address: Text
    updated_at: DateTime (auto-updated)
```

## How to Use

### For Admin Users:

1. **Login to Admin Dashboard**:
   - URL: `http://localhost:5000/admin/login`
   - Username: `admin`
   - Password: `admin123`

2. **Navigate to Contacts Section**:
   - Click "Contacts" in the sidebar menu

3. **Add Multiple Phone Numbers**:
   - Enter phone number in existing field
   - Click "+ Add Another Phone Number" for more fields
   - Click X button to remove unwanted fields

4. **Add Multiple Email Addresses**:
   - Enter email in existing field
   - Click "+ Add Another Email Address" for more fields
   - Click X button to remove unwanted fields

5. **Update Office Address**:
   - Enter complete address in the text area
   - Use line breaks for formatting

6. **Save Changes**:
   - Click "Save Contact Info" button
   - Success message will appear
   - Changes are immediately visible on public contact page

### For Public Users:

- Visit: `http://localhost:5000/contacts`
- Contact information automatically updates from database
- No page refresh needed after admin updates

## API Endpoints

### Admin Endpoints (Login Required)

#### Get Contact Info
```
GET /admin/api/contacts
Response: {
    "phone_numbers": ["phone1", "phone2", ...],
    "email_addresses": ["email1", "email2", ...],
    "office_address": "address text"
}
```

#### Save Contact Info
```
POST /admin/api/contacts
Content-Type: application/json

Body: {
    "phone_numbers": ["phone1", "phone2", ...],
    "email_addresses": ["email1", "email2", ...],
    "office_address": "address text"
}

Response: {
    "success": true,
    "message": "Contact information saved successfully"
}
```

### Public Endpoint

#### Get Contact Info (Public)
```
GET /api/contacts
Response: {
    "phone_numbers": ["phone1", "phone2", ...],
    "email_addresses": ["email1", "email2", ...],
    "office_address": "address text"
}
```

## Initialization

Run the initialization script once to create the database table and add default contact data:

```bash
cd E:\apsp-new-website\APSP_WEBSITE
E:/apsp-new-website/.venv/Scripts/python.exe init_contacts.py
```

### Default Data Created:
- **Phone Numbers**: 
  - +91-866-2434567
  - +91-866-2434890
  - 100 (Emergency)
- **Email Addresses**:
  - info@apsp.ap.gov.in
  - dgapsp@ap.gov.in
  - complaints@apsp.ap.gov.in
- **Office Address**:
  ```
  APSP Headquarters
  Vijayawada, Andhra Pradesh
  PIN: 520001
  ```

## Technical Details

### Data Storage
- Phone numbers and emails stored as JSON arrays in database
- Helper methods for serialization/deserialization:
  - `set_phone_numbers(list)` - Convert list to JSON
  - `get_phone_numbers()` - Convert JSON to list
  - `set_email_addresses(list)` - Convert list to JSON
  - `get_email_addresses()` - Convert JSON to list

### Frontend Features
- Dynamic field addition/removal without page reload
- Show remove button only when multiple fields exist
- Auto-load data on page load
- Success/error messages with auto-hide
- Real-time updates on contacts page

### Security
- Admin endpoints require login authentication
- Only admin users can modify contact information
- Public endpoint is read-only
- Input validation and error handling

## Troubleshooting

### Contact Info Not Saving
1. Check if logged in as admin
2. Verify network calls in browser console
3. Check Flask server logs for errors

### Contact Page Not Updating
1. Clear browser cache
2. Check API endpoint: `/api/contacts`
3. Verify data exists in database

### Database Errors
1. Re-run initialization script
2. Check database file exists: `instance/apsp.db`
3. Verify all migrations completed

## Future Enhancements (Optional)

- Social media links management
- Emergency contact numbers section
- Map integration for office location
- Contact form submissions management
- Email notification on contact form submissions
- Multi-language support for contact information

---

**Status**: ✅ Fully Implemented and Operational
**Version**: 1.0
**Last Updated**: February 6, 2026
