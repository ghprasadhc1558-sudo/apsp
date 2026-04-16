# Important Announcements Management - User Guide

## Overview
The Important Announcements feature allows you to manage the scrolling marquee announcements that appear on the homepage through the admin dashboard.

## Features Added

### 1. **Database-Driven Announcements**
- Announcements are now stored in the database instead of being hardcoded
- Easy to add, edit, hide/show, and delete through admin panel
- Changes reflect immediately on the homepage

### 2. **Admin Dashboard Integration**
- New "Announcements" section in admin dashboard
- User-friendly interface to manage all announcements
- Real-time preview functionality

## How to Use

### Accessing Announcement Management

1. **Login to Admin Panel**
   - Go to `/admin/login`
   - Enter your admin credentials
   - You'll be redirected to the admin dashboard

2. **Navigate to Announcements**
   - Click on "Announcements" in the left sidebar
   - Or click the menu icon and select "Announcements"

### Adding New Announcements

1. In the "Add New Announcement" section, enter your announcement text
2. Keep it concise (examples below)
3. Click "Add Announcement"
4. The announcement will be added to the list and will appear on the homepage

**Examples of good announcements:**
- "Combined seniority list of ARSIs 01.01.2024"
- "DPC RSIs TO RIs 2024-25"
- "Commemoration Day 2024"
- "ID Parade Registration Open"
- "New Recruitment Notification 2026"

### Managing Existing Announcements

Each announcement has two action buttons:

1. **Hide/Show Button** (Orange/Green)
   - Click "Hide" to temporarily remove from homepage
   - Click "Show" to make it visible again
   - Hidden announcements are kept in the database

2. **Delete Button** (Red)
   - Permanently removes the announcement
   - Requires confirmation before deleting

### Preview Changes

Click the "Preview on Homepage" button to open the homepage in a new tab and see your announcements in action.

## Technical Details

### Files Modified/Created

1. **New Model**: `app/models/announcement.py`
   - Database table for storing announcements
   
2. **Updated Routes**: `app/routes.py`
   - Added API endpoints for CRUD operations:
     - `GET /admin/api/announcements` - Get all announcements
     - `POST /admin/api/announcements` - Add new announcement
     - `PUT /admin/api/announcements/<id>` - Update announcement
     - `DELETE /admin/api/announcements/<id>` - Delete announcement

3. **Updated Templates**:
   - `app/templates/index.html` - Now displays announcements from database
   - `app/templates/admin-dashboard.html` - Added announcement management UI

4. **Initialization Script**: `init_announcements.py`
   - Creates the database table
   - Populates with default announcements

### Database Schema

```python
class Announcement:
    id: Integer (Primary Key)
    content: Text (Required)
    is_active: Boolean (Default: True)
    order: Integer (For sorting)
    created_at: DateTime
    updated_at: DateTime
```

### API Endpoints

#### Get All Announcements
```
GET /admin/api/announcements
Response: [
    {
        "id": 1,
        "content": "Sample announcement",
        "is_active": true,
        "order": 1,
        "created_at": "2026-01-19T..."
    }
]
```

#### Add Announcement
```
POST /admin/api/announcements
Body: { "content": "New announcement text" }
Response: { "success": true, "announcement": {...} }
```

#### Update Announcement
```
PUT /admin/api/announcements/1
Body: { "is_active": false }
Response: { "success": true, "announcement": {...} }
```

#### Delete Announcement
```
DELETE /admin/api/announcements/1
Response: { "success": true, "message": "Deleted successfully" }
```

## Homepage Display

Announcements appear in the marquee at the top of the homepage:
- Active announcements are displayed in order
- Separated by " | " character
- Scrolls continuously from right to left
- If no announcements exist, shows default fallback text

## Best Practices

1. **Keep announcements concise** - They scroll on the homepage
2. **Use clear, informative text** - Avoid jargon
3. **Update regularly** - Remove outdated announcements
4. **Use Hide instead of Delete** - For temporary removal
5. **Test after adding** - Use preview to verify appearance

## Troubleshooting

### Announcements not showing on homepage?
- Check if announcements are marked as "Active" (green badge)
- Refresh the homepage
- Verify database connection

### Can't add announcements?
- Ensure you're logged in as admin
- Check if content field is not empty
- Check browser console for errors

### Need to reset to default announcements?
Run the initialization script again:
```bash
python init_announcements.py
```

## Future Enhancements (Possible)

- Drag-and-drop reordering
- Scheduled announcements (auto-publish/unpublish)
- Rich text formatting
- Announcement expiry dates
- Category/priority tags
- Announcement history/archive

## Support

If you encounter any issues or need help:
1. Check the browser console for errors
2. Verify database connectivity
3. Ensure all files are properly updated
4. Check server logs for detailed error messages

---

**Last Updated**: January 19, 2026
**Version**: 1.0.0
