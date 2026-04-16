# APSP Website - Andhra Pradesh Special Police

A modern, responsive website for the Andhra Pradesh Special Police with complete admin panel for content management.

## Features

### Public Website
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Home Page**: Welcome section, announcements, quick links, and recent events
- **Gallery Page**: Photo gallery with category filters (Events, Training, Ceremonies, Operations)
- **Battalions Page**: Complete information about all 12 active battalions (1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 14, 16)
- **Contact Us**: Contact information and location details
- **Dynamic Content**: All content can be managed through admin panel
- **Accessibility**: Font size adjustment options

### Admin Panel
- **Secure Login**: Admin authentication system (Username: admin, Password: admin123)
- **Content Management**: Dynamic content editing for all pages
- **Home Page Management**: Edit welcome section and announcements
- **Events Management**: Add and manage events
- **Battalions Management**: Update battalion information
- **Gallery Management**: Add images to gallery with categories
- **About Page Management**: Edit about page content
- **Contact Management**: Update contact information

## Active Battalions

The website features information about the following battalions:
- 1st Battalion - Vijayawada
- 2nd Battalion - Visakhapatnam
- 3rd Battalion - Tirupati
- 4th Battalion - Guntur
- 5th Battalion - Nellore
- 6th Battalion - Kadapa
- 7th Battalion - Anantapur
- 8th Battalion - Kurnool
- 9th Battalion - Eluru
- 11th Battalion - Rajahmundry
- 14th Battalion - Kakinada
- 16th Battalion - Srikakulam

## Technology Stack

- **HTML5**: Structure and content
- **CSS3**: Styling with modern features (Grid, Flexbox, Animations)
- **JavaScript**: Interactive functionality
- **Local Storage**: Dynamic content management
- **Session Storage**: Admin authentication
- **Font Awesome**: Icons
- **Responsive Design**: Mobile-first approach

## File Structure

```
APSP-website/
│
├── index.html              # Home page
├── gallery.html            # Photo gallery
├── battalions.html         # All battalions list
├── contacts.html           # Contact information
├── admin-login.html        # Admin login page
├── admin-dashboard.html    # Admin control panel
│
├── css/
│   ├── style.css          # Main stylesheet
│   ├── admin.css          # Admin panel styles
│   ├── gallery.css        # Gallery page styles
│   └── battalions.css     # Battalions page styles
│
├── js/
│   ├── script.js          # Main JavaScript
│   ├── admin-login.js     # Admin login functionality
│   ├── admin-dashboard.js # Admin dashboard functionality
│   └── gallery.js         # Gallery filtering
│
├── images/                # Images folder (logo, sliders, events, gallery)
│
└── README.md             # This file
```

## Getting Started

1. **Open the Website**: Simply open `index.html` in a web browser
2. **Navigate**: Use the menu bar to explore different pages
3. **Admin Access**: Click "Admin Login" in the top right corner
4. **Login Credentials**:
   - Username: `admin`
   - Password: `admin123`

## Admin Panel Usage

### Login
1. Click "Admin Login" in the header
2. Enter credentials (admin/admin123)
3. Access the admin dashboard

### Managing Content
1. **Home Content**: Update welcome section and announcements
2. **Events**: Add new events with title, image, and description
3. **Battalions**: Update battalion information including location, commander, and strength
4. **Gallery**: Add images with titles and categories
5. **About Page**: Edit about page content
6. **Contacts**: Update contact information

### Saving Changes
- Click "Save" button after making changes
- Changes are instantly reflected on the website
- Data is stored in browser's localStorage

## Menu Structure

The website includes the following menu items:
- **Home**: Main landing page
- **About Us**: Overview, History, Organization, Officers
- **Battalions**: All Battalions (with dropdown for individual battalions)
- **APSDRF**: About SDRF, Operations, Training
- **Gallery**: Photo gallery with filters
- **News & Events**: Latest News, Events, Announcements
- **Contact Us**: Contact information

## Features in Detail

### Image Slider
- Auto-rotating banner images
- Manual navigation with prev/next buttons
- Smooth transitions

### Announcements Bar
- Scrolling marquee with important updates
- Editable through admin panel

### Gallery Filters
- All images
- Events
- Training
- Ceremonies
- Operations

### Responsive Navigation
- Desktop: Horizontal menu with dropdowns
- Mobile: Hamburger menu

## Customization

### Adding Real Data
1. Login to admin panel
2. Replace dummy content with real information
3. Upload actual images (or provide URLs)
4. Update battalion details
5. Add real events and announcements

### Logo and Branding
- Replace placeholder logo in `images/logo.png`
- Update slider images in `images/` folder
- Modify colors in CSS variables (in `style.css`)

### Color Scheme
Current colors (can be changed in CSS):
- Primary: #003d82 (Blue)
- Secondary: #006644 (Green)
- Accent: #cc0000 (Red)

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers

## Notes

- All content is stored in browser's localStorage
- Images use placeholder SVGs if actual images are not available
- Admin session persists until logout
- Responsive design works on all screen sizes

## Future Enhancements

- Backend integration with database
- File upload functionality for images
- User management system
- More detailed battalion pages
- News and events archive
- Search functionality
- Multi-language support

## Credits

Developed for Andhra Pradesh Special Police
Based on the official APSP website structure

---

**Important**: This is a frontend-only implementation using localStorage. For production use, implement a proper backend with database and authentication system.

## Support

For technical support or queries, please contact the administrator.