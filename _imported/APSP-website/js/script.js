// Mobile Menu Toggle
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('nav-menu');

if (hamburger) {
    hamburger.addEventListener('click', () => {
        navMenu.classList.toggle('active');
    });
}

// Dropdown menu for mobile
const dropdowns = document.querySelectorAll('.dropdown');
dropdowns.forEach(dropdown => {
    dropdown.addEventListener('click', (e) => {
        if (window.innerWidth <= 968) {
            e.preventDefault();
            dropdown.classList.toggle('active');
        }
    });
});

// Slider functionality
let currentSlide = 0;
const slides = document.querySelectorAll('.slide');

function showSlide(n) {
    slides.forEach(slide => slide.classList.remove('active'));
    
    if (n >= slides.length) currentSlide = 0;
    if (n < 0) currentSlide = slides.length - 1;
    
    slides[currentSlide].classList.add('active');
}

function changeSlide(n) {
    currentSlide += n;
    showSlide(currentSlide);
}

// Auto slide
setInterval(() => {
    currentSlide++;
    showSlide(currentSlide);
}, 5000);

// Font size adjustment
function adjustFontSize(size) {
    const body = document.body;
    body.classList.remove('font-small', 'font-large');
    
    if (size === 'decrease') {
        body.classList.add('font-small');
    } else if (size === 'increase') {
        body.classList.add('font-large');
    }
    
    localStorage.setItem('fontSize', size);
}

// Load saved font size
window.addEventListener('DOMContentLoaded', () => {
    const savedSize = localStorage.getItem('fontSize');
    if (savedSize) {
        adjustFontSize(savedSize);
    }
});

// Load dynamic content from localStorage
function loadDynamicContent() {
    const welcomeContent = localStorage.getItem('welcome-content');
    const announcementsContent = localStorage.getItem('announcements-content');
    const recentEventsContent = localStorage.getItem('recent-events-content');
    
    if (welcomeContent && document.getElementById('welcome-content')) {
        document.getElementById('welcome-content').innerHTML = welcomeContent;
    }
    
    if (announcementsContent && document.getElementById('announcements-content')) {
        document.getElementById('announcements-content').innerHTML = announcementsContent;
    }
    
    if (recentEventsContent && document.getElementById('recent-events-content')) {
        document.getElementById('recent-events-content').innerHTML = recentEventsContent;
    }
}

// Load content on page load
window.addEventListener('DOMContentLoaded', loadDynamicContent);