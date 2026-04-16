// Mobile Menu Toggle
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('nav-menu');

// Only run menu code if elements exist
if (hamburger && navMenu) {
	// Click event for hamburger
	hamburger.addEventListener('click', (e) => {
		e.stopPropagation();
		navMenu.classList.toggle('active');
		hamburger.classList.toggle('active');
		console.log('Menu toggled:', navMenu.classList.contains('active'));
	});

	// Touch event for better mobile support
	hamburger.addEventListener('touchstart', (e) => {
		e.preventDefault();
		e.stopPropagation();
		navMenu.classList.toggle('active');
		hamburger.classList.toggle('active');
	});

	// Close menu when clicking outside
	document.addEventListener('click', (e) => {
		if (!navMenu.contains(e.target) && !hamburger.contains(e.target)) {
			navMenu.classList.remove('active');
			hamburger.classList.remove('active');
		}
	});

	// Prevent menu from closing when clicking inside
	navMenu.addEventListener('click', (e) => {
		e.stopPropagation();
	});

	// Handle window resize
	window.addEventListener('resize', () => {
		if (window.innerWidth > 968) {
			navMenu.classList.remove('active');
			hamburger.classList.remove('active');
		}
	});
}

// Dropdown menu for mobile
const dropdowns = document.querySelectorAll('.dropdown');
dropdowns.forEach(dropdown => {
	const dropdownLink = dropdown.querySelector('a');
	if (dropdownLink) {
		dropdownLink.addEventListener('click', (e) => {
			if (window.innerWidth <= 968) {
				e.preventDefault();
				// Close other dropdowns
				dropdowns.forEach(d => {
					if (d !== dropdown) {
						d.classList.remove('active');
					}
				});
				dropdown.classList.toggle('active');
			}
		});

		// Touch support for dropdowns
		dropdownLink.addEventListener('touchstart', (e) => {
			if (window.innerWidth <= 968) {
				e.preventDefault();
				dropdowns.forEach(d => {
					if (d !== dropdown) {
						d.classList.remove('active');
					}
				});
				dropdown.classList.toggle('active');
			}
		});
	}
});

// Slider functionality
const slides = document.querySelectorAll('.slide');

// Only run slider code if slides exist
if (slides && slides.length > 0) {
	let currentSlide = 0;

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
	let slideInterval;

	function startAutoSlide() {
		slideInterval = setInterval(() => {
			currentSlide++;
			showSlide(currentSlide);
		}, 5000);
	}

	function stopAutoSlide() {
		clearInterval(slideInterval);
	}

	startAutoSlide();

	const sliderSection = document.querySelector('.slider');
	if (sliderSection) {
		sliderSection.addEventListener('mouseenter', stopAutoSlide);
		sliderSection.addEventListener('mouseleave', startAutoSlide);
	}
}

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
    /* Temporarily disabled to prevent overwriting server-side data
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
    */
}

// Load content on page load
window.addEventListener('DOMContentLoaded', loadDynamicContent);