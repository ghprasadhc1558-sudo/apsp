// Filter gallery items
function filterGallery(category) {
    const items = document.querySelectorAll('.gallery-item');
    const buttons = document.querySelectorAll('.filter-btn');
    
    // Update active button
    buttons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Filter items
    items.forEach(item => {
        if (category === 'all') {
            item.classList.remove('hidden');
        } else {
            if (item.dataset.category === category) {
                item.classList.remove('hidden');
            } else {
                item.classList.add('hidden');
            }
        }
    });
}

// Load gallery from localStorage (admin added images)
window.addEventListener('DOMContentLoaded', () => {
    const galleryData = JSON.parse(localStorage.getItem('gallery') || '[]');
    const galleryGrid = document.getElementById('gallery-grid');
    
    galleryData.forEach(item => {
        const galleryItem = document.createElement('div');
        galleryItem.className = 'gallery-item';
        galleryItem.dataset.category = item.category.toLowerCase();
        
        galleryItem.innerHTML = `
            <img src="${item.image}" alt="${item.title}" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22400%22 height=%22300%22%3E%3Crect fill=%22%23e0e0e0%22 width=%22400%22 height=%22300%22/%3E%3Ctext x=%2250%25%22 y=%2250%25%22 dominant-baseline=%22middle%22 text-anchor=%22middle%22 fill=%22%23666%22 font-size=%2218%22%3E${item.title}%3C/text%3E%3C/svg%3E'">
            <div class="gallery-overlay">
                <h3>${item.title}</h3>
                <p>${item.category}</p>
            </div>
        `;
        
        galleryGrid.appendChild(galleryItem);
    });
});