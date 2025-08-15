// ========================================
// ABP Interactive Learning Platform - Main JavaScript
// Modern UI interactions and functionality
// ========================================

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeSearch();
    initializeAnimations();
    initializeVideoCards();
    initializeProductCards();
    initializeModals();
    initializeForms();
    initializeTooltips();
});

// ========== Navigation Functions ==========
function initializeNavigation() {
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Active nav link on scroll
    window.addEventListener('scroll', () => {
        const sections = document.querySelectorAll('section[id]');
        const scrollY = window.pageYOffset;

        sections.forEach(section => {
            const sectionHeight = section.offsetHeight;
            const sectionTop = section.offsetTop - 100;
            const sectionId = section.getAttribute('id');
            const navLink = document.querySelector(`.nav-link[href="#${sectionId}"]`);

            if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
                document.querySelectorAll('.nav-link').forEach(link => {
                    link.classList.remove('active');
                });
                if (navLink) navLink.classList.add('active');
            }
        });
    });

    // Mobile menu toggle
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger) {
        hamburger.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            hamburger.classList.toggle('active');
        });
    }
}

// ========== Search Functionality ==========
function initializeSearch() {
    const searchInput = document.querySelector('.search-bar input');
    const searchBar = document.querySelector('.search-bar');
    
    if (searchInput) {
        // Search suggestions
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            if (query.length > 2) {
                showSearchSuggestions(query);
            } else {
                hideSearchSuggestions();
            }
        });

        // Search on Enter
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch(this.value);
            }
        });

        // Focus effects
        searchInput.addEventListener('focus', () => {
            searchBar.classList.add('focused');
        });

        searchInput.addEventListener('blur', () => {
            searchBar.classList.remove('focused');
            setTimeout(hideSearchSuggestions, 200);
        });
    }
}

function showSearchSuggestions(query) {
    // Simulated search suggestions
    const suggestions = [
        'Python Programming',
        'JavaScript Basics',
        'Data Science',
        'Machine Learning',
        'Web Development',
        'AI Fundamentals'
    ].filter(item => item.toLowerCase().includes(query));

    // Create or update suggestions dropdown
    let dropdown = document.querySelector('.search-suggestions');
    if (!dropdown) {
        dropdown = document.createElement('div');
        dropdown.className = 'search-suggestions';
        document.querySelector('.search-bar').appendChild(dropdown);
    }

    dropdown.innerHTML = suggestions.map(item => 
        `<div class="suggestion-item" onclick="selectSuggestion('${item}')">${item}</div>`
    ).join('');
    dropdown.style.display = 'block';
}

function hideSearchSuggestions() {
    const dropdown = document.querySelector('.search-suggestions');
    if (dropdown) {
        dropdown.style.display = 'none';
    }
}

function selectSuggestion(value) {
    document.querySelector('.search-bar input').value = value;
    hideSearchSuggestions();
    performSearch(value);
}

function performSearch(query) {
    console.log('Searching for:', query);
    // Redirect to search results or filter content
    window.location.href = `#search?q=${encodeURIComponent(query)}`;
}

// ========== Animation Functions ==========
function initializeAnimations() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all elements with animation classes
    document.querySelectorAll('.fade-in, .scale-in, .slide-in-left, .slide-in-right').forEach(el => {
        observer.observe(el);
    });

    // Parallax effect for hero section
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const parallax = document.querySelector('.hero');
        if (parallax) {
            parallax.style.transform = `translateY(${scrolled * 0.5}px)`;
        }
    });
}

// ========== Video Card Interactions ==========
function initializeVideoCards() {
    const videoCards = document.querySelectorAll('.video-card');
    
    videoCards.forEach(card => {
        // Hover effect
        card.addEventListener('mouseenter', function() {
            this.querySelector('.video-thumbnail img').style.transform = 'scale(1.05)';
        });

        card.addEventListener('mouseleave', function() {
            this.querySelector('.video-thumbnail img').style.transform = 'scale(1)';
        });

        // Click to play
        card.addEventListener('click', function() {
            const videoTitle = this.querySelector('.video-title').textContent;
            playVideo(videoTitle);
        });
    });
}

function playVideo(title) {
    console.log('Playing video:', title);
    // Create and show video modal
    showVideoModal(title);
}

function playDemoVideo() {
    showVideoModal('ABP Learning Platform Demo');
}

function showVideoModal(title) {
    // Create video modal
    const modal = document.createElement('div');
    modal.className = 'modal active';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h2 class="modal-title">${title}</h2>
                <button class="modal-close" onclick="closeModal(this)">&times;</button>
            </div>
            <div class="modal-body">
                <div style="position: relative; padding-bottom: 56.25%; height: 0;">
                    <iframe 
                        src="https://www.youtube.com/embed/dQw4w9WgXcQ" 
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
                        frameborder="0" 
                        allowfullscreen>
                    </iframe>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
}

// ========== Product Card Interactions ==========
function initializeProductCards() {
    const productCards = document.querySelectorAll('.product-card');
    
    productCards.forEach(card => {
        const addToCartBtn = card.querySelector('.btn-primary');
        
        if (addToCartBtn) {
            addToCartBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                const productTitle = card.querySelector('.product-title').textContent;
                const productPrice = card.querySelector('.product-price').textContent;
                addToCart(productTitle, productPrice);
            });
        }

        // Quick view on card click
        card.addEventListener('click', function(e) {
            if (!e.target.closest('.btn')) {
                const productTitle = this.querySelector('.product-title').textContent;
                showProductDetails(productTitle);
            }
        });
    });
}

function addToCart(product, price) {
    // Animate cart icon
    const cartIcon = document.querySelector('.fa-cart-plus');
    if (cartIcon) {
        cartIcon.classList.add('bounce');
        setTimeout(() => cartIcon.classList.remove('bounce'), 500);
    }

    // Show notification
    showNotification(`${product} added to cart!`, 'success');

    // Update cart count
    updateCartCount();
}

function updateCartCount() {
    let cartCount = parseInt(localStorage.getItem('cartCount') || 0);
    cartCount++;
    localStorage.setItem('cartCount', cartCount);
    
    // Update UI
    let cartBadge = document.querySelector('.cart-badge');
    if (!cartBadge) {
        // Create cart badge if it doesn't exist
        const navActions = document.querySelector('.nav-actions');
        if (navActions) {
            cartBadge = document.createElement('span');
            cartBadge.className = 'cart-badge';
            navActions.appendChild(cartBadge);
        }
    }
    if (cartBadge) {
        cartBadge.textContent = cartCount;
        cartBadge.style.display = cartCount > 0 ? 'block' : 'none';
    }
}

function showProductDetails(productTitle) {
    console.log('Showing details for:', productTitle);
    // Would open product detail modal
}

// ========== Modal Functions ==========
function initializeModals() {
    // Close modal on background click
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            e.target.remove();
        }
    });

    // Close modal on ESC key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const modal = document.querySelector('.modal.active');
            if (modal) modal.remove();
        }
    });
}

function closeModal(button) {
    const modal = button.closest('.modal');
    if (modal) modal.remove();
}

// ========== Form Functions ==========
function initializeForms() {
    // Contact form
    const contactForm = document.querySelector('.contact-form form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            // Validate
            if (validateForm(data)) {
                // Submit form
                submitContactForm(data);
            }
        });
    }

    // Newsletter subscription
    const newsletterForms = document.querySelectorAll('.footer-section form, .newsletter-form');
    newsletterForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('input[type="email"]').value;
            subscribeNewsletter(email);
        });
    });
}

function validateForm(data) {
    // Basic validation
    for (const [key, value] of Object.entries(data)) {
        if (!value || value.trim() === '') {
            showNotification(`Please fill in all fields`, 'error');
            return false;
        }
    }
    return true;
}

function submitContactForm(data) {
    console.log('Submitting contact form:', data);
    showNotification('Message sent successfully! We\'ll get back to you soon.', 'success');
    
    // Reset form
    document.querySelector('.contact-form form').reset();
}

function subscribeNewsletter(email) {
    console.log('Subscribing:', email);
    showNotification('Successfully subscribed to newsletter!', 'success');
}

// ========== Notification System ==========
function showNotification(message, type = 'info') {
    // Remove existing notification
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();

    // Create new notification
    const notification = document.createElement('div');
    notification.className = `notification notification-${type} slide-in-right`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">&times;</button>
    `;

    document.body.appendChild(notification);

    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// ========== Tooltip Functions ==========
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltipText = this.getAttribute('data-tooltip');
            showTooltip(this, tooltipText);
        });

        element.addEventListener('mouseleave', function() {
            hideTooltip();
        });
    });
}

function showTooltip(element, text) {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip-popup';
    tooltip.textContent = text;
    
    document.body.appendChild(tooltip);
    
    const rect = element.getBoundingClientRect();
    tooltip.style.top = `${rect.top - tooltip.offsetHeight - 10}px`;
    tooltip.style.left = `${rect.left + (rect.width - tooltip.offsetWidth) / 2}px`;
}

function hideTooltip() {
    const tooltip = document.querySelector('.tooltip-popup');
    if (tooltip) tooltip.remove();
}

// ========== Dashboard Functions ==========
function initializeDashboard() {
    // Sidebar toggle
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('active');
        });
    }

    // Dashboard cards
    const dashboardCards = document.querySelectorAll('.dashboard-card');
    dashboardCards.forEach(card => {
        card.addEventListener('click', function() {
            const feature = this.dataset.feature;
            navigateToFeature(feature);
        });
    });
}

function navigateToFeature(feature) {
    console.log('Navigating to:', feature);
    // Navigate to feature page
    window.location.href = `${feature}.html`;
}

// ========== Utility Functions ==========
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// ========== Theme Toggle ==========
function initializeTheme() {
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }

    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.body.setAttribute('data-theme', savedTheme);
}

function toggleTheme() {
    const currentTheme = document.body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    showNotification(`Switched to ${newTheme} mode`, 'info');
}

// ========== Loading States ==========
function showLoading(element) {
    element.classList.add('skeleton');
    element.innerHTML = '<div class="spinner"></div>';
}

function hideLoading(element, content) {
    element.classList.remove('skeleton');
    element.innerHTML = content;
}

// ========== API Calls (Simulated) ==========
async function fetchCourses() {
    // Simulated API call
    return new Promise(resolve => {
        setTimeout(() => {
            resolve([
                { id: 1, title: 'Python Basics', price: 49.99 },
                { id: 2, title: 'JavaScript Advanced', price: 79.99 },
                { id: 3, title: 'Data Science', price: 99.99 }
            ]);
        }, 1000);
    });
}

async function fetchUserData() {
    // Simulated API call
    return new Promise(resolve => {
        setTimeout(() => {
            resolve({
                name: 'John Doe',
                courses: 5,
                certificates: 2,
                progress: 75
            });
        }, 500);
    });
}

// ========== Initialize on specific pages ==========
if (document.querySelector('.dashboard-container')) {
    initializeDashboard();
}

if (document.querySelector('.quiz-container')) {
    initializeQuiz();
}

function initializeQuiz() {
    const answerOptions = document.querySelectorAll('.answer-option');
    
    answerOptions.forEach(option => {
        option.addEventListener('click', function() {
            // Remove previous selection
            answerOptions.forEach(opt => opt.classList.remove('selected'));
            
            // Add selection to clicked option
            this.classList.add('selected');
            
            // Enable submit button
            const submitBtn = document.querySelector('.quiz-submit');
            if (submitBtn) submitBtn.disabled = false;
        });
    });
}

// ========== Export functions for global use ==========
window.playDemoVideo = playDemoVideo;
window.closeModal = closeModal;
window.selectSuggestion = selectSuggestion;
window.showNotification = showNotification;

// ========== Add custom styles for notifications ==========
const style = document.createElement('style');
style.textContent = `
    .notification {
        position: fixed;
        top: 80px;
        right: 20px;
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 1rem 1.5rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        z-index: 9999;
        min-width: 300px;
        box-shadow: var(--shadow-lg);
    }

    .notification-success {
        border-color: var(--success-color);
        background: rgba(76, 175, 80, 0.1);
    }

    .notification-error {
        border-color: var(--danger-color);
        background: rgba(244, 67, 54, 0.1);
    }

    .notification-info {
        border-color: var(--primary-accent);
        background: rgba(0, 212, 255, 0.1);
    }

    .notification button {
        background: none;
        border: none;
        color: var(--text-secondary);
        font-size: 1.5rem;
        cursor: pointer;
        margin-left: auto;
    }

    .search-suggestions {
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        margin-top: 0.5rem;
        max-height: 300px;
        overflow-y: auto;
        display: none;
        z-index: 100;
    }

    .suggestion-item {
        padding: 0.75rem 1rem;
        cursor: pointer;
        transition: var(--transition-fast);
    }

    .suggestion-item:hover {
        background: var(--hover-bg);
    }

    .cart-badge {
        position: absolute;
        top: -8px;
        right: -8px;
        background: var(--danger-color);
        color: white;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: bold;
    }

    .bounce {
        animation: bounce 0.5s ease;
    }

    @keyframes bounce {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.2); }
    }

    .hero-stats {
        display: flex;
        gap: 2rem;
        margin-top: 2rem;
    }

    .stat-item {
        text-align: center;
    }

    .stat-number {
        display: block;
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-accent);
    }

    .stat-label {
        display: block;
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin-top: 0.25rem;
    }

    .play-overlay {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 4rem;
        color: white;
        opacity: 0.8;
        transition: var(--transition-fast);
        pointer-events: none;
    }

    .video-preview:hover .play-overlay {
        opacity: 1;
        transform: translate(-50%, -50%) scale(1.1);
    }

    .tooltip-popup {
        position: fixed;
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 6px;
        padding: 0.5rem 0.75rem;
        font-size: 0.875rem;
        z-index: 10000;
        pointer-events: none;
        box-shadow: var(--shadow-md);
    }

    .search-bar.focused {
        box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.2);
        border-color: var(--primary-accent);
    }
`;
document.head.appendChild(style);

console.log('ABP Interactive Learning Platform initialized successfully!');
