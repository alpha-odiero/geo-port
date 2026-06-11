/**
 * GeoPort Logistics - Category Grid Filter & Image Lightbox Modal
 */

document.addEventListener('DOMContentLoaded', () => {
  initGalleryFilter();
  initLightbox();
});

// Expose globally for dynamic DOM injection tracking
window.initGalleryFilter = initGalleryFilter;
window.initLightbox = initLightbox;

/* ==========================================================================
   Category Grid Filtering (Supports Gallery & Projects)
   ========================================================================== */
function initGalleryFilter() {
  const filterBtns = document.querySelectorAll('.filter-btn');
  const galleryItems = document.querySelectorAll('.gallery-item, .project-card-wrapper');

  if (filterBtns.length === 0 || galleryItems.length === 0) return;

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      // Remove active class from all buttons
      filterBtns.forEach(b => b.classList.remove('active'));
      // Add to clicked button
      btn.classList.add('active');

      const filterValue = btn.getAttribute('data-filter');

      galleryItems.forEach(item => {
        // Support either direct layout categories or wrapper categories
        const itemCategory = item.getAttribute('data-category') || '';
        
        if (filterValue === 'all') {
          item.style.display = 'block';
        } else if (itemCategory === filterValue) {
          item.style.display = 'block';
        } else {
          item.style.display = 'none';
        }
      });
    });
  });
}

/* ==========================================================================
   Image Lightbox Popup Modals (With Next/Prev Controls)
   ========================================================================== */
function initLightbox() {
  const galleryImages = document.querySelectorAll('.gallery-item img, .project-card img');
  const lightbox = document.createElement('div');
  lightbox.className = 'lightbox-modal';
  
  // HTML layout structure
  lightbox.innerHTML = `
    <button class="lightbox-arrow lightbox-prev" aria-label="Previous">&lsaquo;</button>
    <div class="lightbox-image-container">
      <button class="lightbox-close" aria-label="Close">&times;</button>
      <img src="" alt="GeoPort Logistics Portfolio Closeup">
    </div>
    <button class="lightbox-arrow lightbox-next" aria-label="Next">&rsaquo;</button>
  `;
  
  document.body.appendChild(lightbox);

  const lightboxImg = lightbox.querySelector('img');
  const closeBtn = lightbox.querySelector('.lightbox-close');
  const prevBtn = lightbox.querySelector('.lightbox-prev');
  const nextBtn = lightbox.querySelector('.lightbox-next');

  let activeImagesList = [];
  let currentImageIdx = 0;

  if (galleryImages.length === 0) return;

  // Open Lightbox
  galleryImages.forEach(img => {
    img.parentElement.addEventListener('click', (e) => {
      e.preventDefault();
      
      // Rebuild list of active visible images to support fluid next/prev on active filter category
      activeImagesList = [];
      const allVisibleParents = Array.from(galleryImages).filter(gImg => {
        // Find if parent or grand parent is visible (not set to display none)
        let parent = gImg.closest('.gallery-item, .project-card-wrapper, .project-card');
        return parent ? parent.style.display !== 'none' : true;
      });

      allVisibleParents.forEach(gImg => activeImagesList.push(gImg.src));

      currentImageIdx = activeImagesList.indexOf(img.src);
      if (currentImageIdx === -1) {
        activeImagesList = [img.src];
        currentImageIdx = 0;
      }

      showLightboxImage();
      lightbox.classList.add('active');
    });
  });

  const showLightboxImage = () => {
    if (activeImagesList.length > 0) {
      lightboxImg.src = activeImagesList[currentImageIdx];
    }
  };

  const nextLightboxImage = () => {
    currentImageIdx = (currentImageIdx + 1) % activeImagesList.length;
    showLightboxImage();
  };

  const prevLightboxImage = () => {
    currentImageIdx = (currentImageIdx - 1 + activeImagesList.length) % activeImagesList.length;
    showLightboxImage();
  };

  // Click interactions
  closeBtn.addEventListener('click', () => {
    lightbox.classList.remove('active');
  });

  nextBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    nextLightboxImage();
  });

  prevBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    prevLightboxImage();
  });

  // Close lightbox on clicking background
  lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox || e.target.classList.contains('lightbox-image-container')) {
      lightbox.classList.remove('active');
    }
  });

  // Keyboard navigation support
  document.addEventListener('keydown', (e) => {
    if (!lightbox.classList.contains('active')) return;
    
    if (e.key === 'Escape') {
      lightbox.classList.remove('active');
    } else if (e.key === 'ArrowRight') {
      nextLightboxImage();
    } else if (e.key === 'ArrowLeft') {
      prevLightboxImage();
    }
  });
}
