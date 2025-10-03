// EMMA Platform JavaScript

// Smooth scrolling for navigation links
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');

    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add animation to feature cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Animate cards on scroll
    const cards = document.querySelectorAll('.feature-card, .subject-card, .testimonial-card, .pricing-card, .topic-card');
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });

    // Notebook cell functionality
    const runButtons = document.querySelectorAll('.cell-controls .btn-primary');
    runButtons.forEach(button => {
        button.addEventListener('click', function() {
            const cell = this.closest('.notebook-cell');
            const input = cell.querySelector('textarea');
            const output = cell.querySelector('.cell-output');

            // Simulate computation
            output.innerHTML = '<p style="font-family: monospace; color: #0066CC;">Computing...</p>';

            setTimeout(() => {
                output.innerHTML = `
                    <p style="font-family: monospace; color: #212529;">
                        <strong>Output:</strong><br>
                        Result computed successfully for: ${input.value}
                    </p>
                `;
            }, 500);
        });
    });

    // Clear button functionality
    const clearButtons = document.querySelectorAll('.cell-controls .btn-outline:nth-child(2)');
    clearButtons.forEach(button => {
        button.addEventListener('click', function() {
            const cell = this.closest('.notebook-cell');
            const output = cell.querySelector('.cell-output');
            output.innerHTML = '';
        });
    });

    // Mobile menu toggle
    const navMenu = document.querySelector('.nav-menu');
    const navToggle = document.createElement('button');
    navToggle.className = 'nav-toggle';
    navToggle.innerHTML = '☰';
    navToggle.style.display = 'none';
    navToggle.style.background = 'none';
    navToggle.style.border = 'none';
    navToggle.style.fontSize = '1.5rem';
    navToggle.style.cursor = 'pointer';
    navToggle.style.color = '#0066CC';

    // Insert toggle button before nav menu
    if (navMenu) {
        navMenu.parentNode.insertBefore(navToggle, navMenu);

        navToggle.addEventListener('click', function() {
            navMenu.style.display = navMenu.style.display === 'flex' ? 'none' : 'flex';
        });
    }

    // Responsive menu handling
    function handleResize() {
        if (window.innerWidth <= 768) {
            navToggle.style.display = 'block';
            if (navMenu) {
                navMenu.style.flexDirection = 'column';
                navMenu.style.position = 'absolute';
                navMenu.style.top = '60px';
                navMenu.style.left = '0';
                navMenu.style.width = '100%';
                navMenu.style.background = 'white';
                navMenu.style.padding = '1rem';
                navMenu.style.boxShadow = '0 4px 12px rgba(0,0,0,0.1)';
                navMenu.style.display = 'none';
            }
        } else {
            navToggle.style.display = 'none';
            if (navMenu) {
                navMenu.style.display = 'flex';
                navMenu.style.flexDirection = 'row';
                navMenu.style.position = 'static';
                navMenu.style.background = 'transparent';
                navMenu.style.boxShadow = 'none';
            }
        }
    }

    window.addEventListener('resize', handleResize);
    handleResize();

    // Add interactive hover effects
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s ease';
        });
    });

    // Progress bar animations
    const progressBars = document.querySelectorAll('.progress-fill');
    const progressObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const width = entry.target.style.width;
                entry.target.style.width = '0';
                setTimeout(() => {
                    entry.target.style.width = width;
                }, 100);
            }
        });
    }, { threshold: 0.5 });

    progressBars.forEach(bar => {
        bar.style.transition = 'width 1s ease';
        progressObserver.observe(bar);
    });

    // Stat counter animation
    const statNumbers = document.querySelectorAll('.stat-number, .metric-value');
    statNumbers.forEach(stat => {
        const text = stat.textContent.trim();
        const hasNumber = /\d/.test(text);

        if (hasNumber) {
            const observer = new IntersectionObserver(function(entries) {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'scale(1)';
                    }
                });
            }, { threshold: 0.5 });

            stat.style.opacity = '0';
            stat.style.transform = 'scale(0.8)';
            stat.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(stat);
        }
    });

    // Show solution button functionality
    const solutionButtons = document.querySelectorAll('.dashboard-card .btn-primary');
    solutionButtons.forEach(button => {
        if (button.textContent.trim() === 'Show Solution') {
            button.addEventListener('click', function() {
                const card = this.closest('.dashboard-card');
                const problemText = card.querySelector('p[style*="Courier"]');

                if (this.textContent === 'Show Solution') {
                    const solutionDiv = document.createElement('div');
                    solutionDiv.className = 'solution-content';
                    solutionDiv.style.marginTop = '1rem';
                    solutionDiv.style.padding = '1rem';
                    solutionDiv.style.background = '#f8f9fa';
                    solutionDiv.style.borderRadius = '6px';
                    solutionDiv.style.borderLeft = '4px solid #0066CC';
                    solutionDiv.innerHTML = '<p style="color: #0066CC; font-weight: 600;">Solution:</p><p>Step-by-step solution would appear here with detailed mathematical reasoning and explanations.</p>';

                    card.insertBefore(solutionDiv, this);
                    this.textContent = 'Hide Solution';
                } else {
                    const solution = card.querySelector('.solution-content');
                    if (solution) solution.remove();
                    this.textContent = 'Show Solution';
                }
            });
        }
    });

    // Add loading state to workspace buttons
    const workspaceButtons = document.querySelectorAll('.workspace-main .btn, .workspace-sidebar .btn');
    workspaceButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.textContent.includes('New Notebook') || this.textContent.includes('Add New Cell')) {
                const originalText = this.textContent;
                this.textContent = 'Creating...';
                this.disabled = true;

                setTimeout(() => {
                    this.textContent = originalText;
                    this.disabled = false;
                }, 800);
            }
        });
    });

    // Dashboard metric animations
    const metricValues = document.querySelectorAll('.metric-value');
    metricValues.forEach(metric => {
        const finalValue = metric.textContent.trim();
        const hasNumber = /^\d+/.test(finalValue);

        if (hasNumber) {
            const number = parseInt(finalValue.match(/\d+/)[0]);

            const observer = new IntersectionObserver(function(entries) {
                entries.forEach(entry => {
                    if (entry.isIntersecting && !metric.dataset.animated) {
                        metric.dataset.animated = 'true';
                        let current = 0;
                        const increment = number / 30;
                        const timer = setInterval(() => {
                            current += increment;
                            if (current >= number) {
                                metric.textContent = finalValue;
                                clearInterval(timer);
                            } else {
                                metric.textContent = Math.floor(current) + finalValue.replace(/^\d+/, '');
                            }
                        }, 30);
                    }
                });
            }, { threshold: 0.5 });

            observer.observe(metric);
        }
    });

    console.log('EMMA Platform initialized successfully');
});

// Utility function for formatting numbers
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Utility function for smooth animations
function animateValue(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            element.textContent = formatNumber(Math.round(end));
            clearInterval(timer);
        } else {
            element.textContent = formatNumber(Math.round(current));
        }
    }, 16);
}

// Export for potential module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { formatNumber, animateValue };
}
