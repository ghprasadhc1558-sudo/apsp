// Check if user is logged in
window.addEventListener('DOMContentLoaded', () => {
    if (sessionStorage.getItem('adminLoggedIn') !== 'true') {
        window.location.href = 'admin-login.html';
        return;
    }
    
    // Set admin username
    const username = sessionStorage.getItem('adminUsername');
    if (username) {
        document.getElementById('admin-username').textContent = username;
    }
    
    // Load saved content
    loadSavedContent();
});

// Toggle sidebar for mobile
function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('active');
}

// Show section
function showSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => section.style.display = 'none');
    
    // Show selected section
    document.getElementById(sectionId).style.display = 'block';
    
    // Update active menu item
    const menuItems = document.querySelectorAll('.sidebar-menu a');
    menuItems.forEach(item => item.classList.remove('active'));
    event.target.closest('a').classList.add('active');
    
    // Close sidebar on mobile
    if (window.innerWidth <= 968) {
        document.getElementById('sidebar').classList.remove('active');
    }
}

// Save content
function saveContent(section) {
    let successMessage;
    
    switch(section) {
        case 'home-welcome':
            const welcomeTitle = document.getElementById('welcome-title').value;
            const welcomeText = document.getElementById('welcome-text').value;
            
            const welcomeHTML = `
                <h2>${welcomeTitle}</h2>
                <p>${welcomeText}</p>
            `;
            
            localStorage.setItem('welcome-content', welcomeHTML);
            successMessage = document.getElementById('success-home-welcome');
            successMessage.textContent = 'Welcome section updated successfully!';
            break;
            
        case 'announcements':
            const announcementsText = document.getElementById('announcements-text').value;
            localStorage.setItem('announcements-content', announcementsText);
            successMessage = document.getElementById('success-announcements');
            successMessage.textContent = 'Announcements updated successfully!';
            break;
            
        case 'events':
            const eventTitle = document.getElementById('event-title').value;
            const eventImage = document.getElementById('event-image').value;
            const eventDescription = document.getElementById('event-description').value;
            
            if (eventTitle && eventDescription) {
                // Save event (in real app, would save to database)
                const events = JSON.parse(localStorage.getItem('events') || '[]');
                events.push({ title: eventTitle, image: eventImage, description: eventDescription });
                localStorage.setItem('events', JSON.stringify(events));
                
                // Clear form
                document.getElementById('event-title').value = '';
                document.getElementById('event-image').value = '';
                document.getElementById('event-description').value = '';
                
                successMessage = document.getElementById('success-events');
                successMessage.textContent = 'Event added successfully!';
            }
            break;
            
        case 'battalions':
            const battalionNumber = document.getElementById('battalion-number').value;
            const battalionLocation = document.getElementById('battalion-location').value;
            const battalionCommander = document.getElementById('battalion-commander').value;
            const battalionStrength = document.getElementById('battalion-strength').value;
            const battalionDescription = document.getElementById('battalion-description').value;
            
            if (battalionNumber) {
                const battalions = JSON.parse(localStorage.getItem('battalions') || '{}');
                battalions[battalionNumber] = {
                    location: battalionLocation,
                    commander: battalionCommander,
                    strength: battalionStrength,
                    description: battalionDescription
                };
                localStorage.setItem('battalions', JSON.stringify(battalions));
                
                successMessage = document.getElementById('success-battalions');
                successMessage.textContent = `Battalion ${battalionNumber} information updated successfully!`;
            }
            break;
            
        case 'gallery':
            const galleryImage = document.getElementById('gallery-image').value;
            const galleryTitle = document.getElementById('gallery-title').value;
            const galleryCategory = document.getElementById('gallery-category').value;
            
            if (galleryImage && galleryTitle) {
                const gallery = JSON.parse(localStorage.getItem('gallery') || '[]');
                gallery.push({ image: galleryImage, title: galleryTitle, category: galleryCategory });
                localStorage.setItem('gallery', JSON.stringify(gallery));
                
                // Clear form
                document.getElementById('gallery-image').value = '';
                document.getElementById('gallery-title').value = '';
                document.getElementById('gallery-category').value = '';
                
                successMessage = document.getElementById('success-gallery');
                successMessage.textContent = 'Image added to gallery successfully!';
            }
            break;
            
        case 'about':
            const aboutContent = document.getElementById('about-content').value;
            localStorage.setItem('about-content', aboutContent);
            successMessage = document.getElementById('success-about');
            successMessage.textContent = 'About page updated successfully!';
            break;
            
        case 'contacts':
            const contactPhone = document.getElementById('contact-phone').value;
            const contactEmail = document.getElementById('contact-email').value;
            const contactAddress = document.getElementById('contact-address').value;
            
            const contacts = {
                phone: contactPhone,
                email: contactEmail,
                address: contactAddress
            };
            localStorage.setItem('contacts', JSON.stringify(contacts));
            successMessage = document.getElementById('success-contacts');
            successMessage.textContent = 'Contact information updated successfully!';
            break;
    }
    
    if (successMessage) {
        successMessage.classList.add('show');
        setTimeout(() => {
            successMessage.classList.remove('show');
        }, 3000);
    }
}

// Load saved content
function loadSavedContent() {
    // Load welcome content
    const welcomeContent = localStorage.getItem('welcome-content');
    if (welcomeContent) {
        // Extract title and text from HTML (basic parsing)
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = welcomeContent;
        const h2 = tempDiv.querySelector('h2');
        const p = tempDiv.querySelector('p');
        if (h2) document.getElementById('welcome-title').value = h2.textContent;
        if (p) document.getElementById('welcome-text').value = p.textContent;
    }
    
    // Load announcements
    const announcements = localStorage.getItem('announcements-content');
    if (announcements) {
        document.getElementById('announcements-text').value = announcements;
    }
    
    // Load about content
    const aboutContent = localStorage.getItem('about-content');
    if (aboutContent) {
        document.getElementById('about-content').value = aboutContent;
    }
    
    // Load contacts
    const contacts = JSON.parse(localStorage.getItem('contacts') || '{}');
    if (contacts.phone) document.getElementById('contact-phone').value = contacts.phone;
    if (contacts.email) document.getElementById('contact-email').value = contacts.email;
    if (contacts.address) document.getElementById('contact-address').value = contacts.address;
}

// Handle logout
function handleLogout() {
    if (confirm('Are you sure you want to logout?')) {
        sessionStorage.removeItem('adminLoggedIn');
        sessionStorage.removeItem('adminUsername');
        window.location.href = 'admin-login.html';
    }
}