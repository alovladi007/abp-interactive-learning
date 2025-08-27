// Dashboard JavaScript for ABP Interactive Learning

document.addEventListener('DOMContentLoaded', function() {
    // Tab switching functionality
    const navItems = document.querySelectorAll('.sidebar-nav .nav-item');
    const tabContents = document.querySelectorAll('.tab-content');

    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all nav items
            navItems.forEach(nav => nav.classList.remove('active'));
            
            // Add active class to clicked item
            this.classList.add('active');
            
            // Hide all tab contents
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Show selected tab content
            const targetTab = this.getAttribute('data-tab');
            const targetContent = document.getElementById(targetTab);
            if (targetContent) {
                targetContent.classList.add('active');
            }
        });
    });

    // File upload functionality
    const uploadAreas = document.querySelectorAll('.upload-area');
    uploadAreas.forEach(area => {
        const fileInput = area.querySelector('input[type="file"]');
        
        area.addEventListener('click', () => {
            if (fileInput) fileInput.click();
        });
        
        area.addEventListener('dragover', (e) => {
            e.preventDefault();
            area.style.borderColor = '#667eea';
            area.style.backgroundColor = '#f8f9ff';
        });
        
        area.addEventListener('dragleave', (e) => {
            e.preventDefault();
            area.style.borderColor = '#ddd';
            area.style.backgroundColor = 'transparent';
        });
        
        area.addEventListener('drop', (e) => {
            e.preventDefault();
            area.style.borderColor = '#ddd';
            area.style.backgroundColor = 'transparent';
            
            const files = e.dataTransfer.files;
            if (files.length > 0 && fileInput) {
                fileInput.files = files;
                handleFileUpload(files[0], area);
            }
        });
        
        if (fileInput) {
            fileInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    handleFileUpload(e.target.files[0], area);
                }
            });
        }
    });

    // Handle file upload
    function handleFileUpload(file, uploadArea) {
        const fileName = file.name;
        const fileSize = (file.size / 1024 / 1024).toFixed(2) + ' MB';
        
        // Update upload area to show file info
        uploadArea.innerHTML = `
            <i class="fas fa-check-circle" style="color: #28a745;"></i>
            <h4>File Uploaded Successfully</h4>
            <p><strong>${fileName}</strong> (${fileSize})</p>
            <button class="btn btn-outline" onclick="this.parentElement.innerHTML = this.parentElement.getAttribute('data-original')">Upload Another</button>
        `;
        
        // Store original content for reset
        if (!uploadArea.getAttribute('data-original')) {
            uploadArea.setAttribute('data-original', uploadArea.innerHTML);
        }
    }

    // Search functionality
    const searchInputs = document.querySelectorAll('.search-input');
    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const cards = this.closest('.tab-content').querySelectorAll('.book-card, .item-card, .partner-card');
            
            cards.forEach(card => {
                const text = card.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // Filter functionality
    const filterSelects = document.querySelectorAll('.filter-select');
    filterSelects.forEach(select => {
        select.addEventListener('change', function() {
            const filterValue = this.value.toLowerCase();
            const cards = this.closest('.tab-content').querySelectorAll('.book-card, .item-card');
            
            cards.forEach(card => {
                if (filterValue === 'all categories' || filterValue === '') {
                    card.style.display = 'block';
                } else {
                    // This is a simplified filter - in a real app, you'd have data attributes
                    const cardText = card.textContent.toLowerCase();
                    if (cardText.includes(filterValue)) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                }
            });
        });
    });

    // Button click handlers
    document.addEventListener('click', function(e) {
        // Quiz start buttons
        if (e.target.textContent === 'Start Quiz') {
            e.preventDefault();
            const quizName = e.target.closest('.quiz-item').querySelector('h4').textContent;
            showNotification(`Starting ${quizName}...`, 'info');
            // In a real app, this would redirect to the quiz page
        }

        // Certification enrollment buttons
        if (e.target.textContent === 'Enroll Now') {
            e.preventDefault();
            const certName = e.target.closest('.cert-card').querySelector('h4').textContent;
            showNotification(`Enrollment for ${certName} initiated!`, 'success');
        }

        // Video generation buttons
        if (e.target.textContent.includes('Generate')) {
            e.preventDefault();
            showNotification('AI video generation started! This may take a few minutes.', 'info');
            // Simulate progress
            simulateProgress(e.target);
        }

        // Add to cart buttons
        if (e.target.textContent === 'Add to Cart') {
            e.preventDefault();
            const itemName = e.target.closest('.item-card').querySelector('h4').textContent;
            showNotification(`${itemName} added to cart!`, 'success');
        }

        // Continue reading buttons
        if (e.target.textContent === 'Continue Reading') {
            e.preventDefault();
            const bookName = e.target.closest('.book-card').querySelector('h4').textContent;
            showNotification(`Opening ${bookName}...`, 'info');
        }

        // Video play buttons (tutoring videos)
        if (e.target.closest('.video-card')) {
            const videoCard = e.target.closest('.video-card');
            if (videoCard && e.target.classList.contains('fa-play-circle')) {
                e.preventDefault();
                const videoTitle = videoCard.querySelector('h4').textContent;
                showNotification(`Playing: ${videoTitle}`, 'info');
                // In a real app, this would open a video player
            }
        }
    });

    // Simulate progress for long-running operations
    function simulateProgress(button) {
        const originalText = button.textContent;
        button.disabled = true;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        
        setTimeout(() => {
            button.innerHTML = '<i class="fas fa-check"></i> Complete!';
            button.style.backgroundColor = '#28a745';
            
            setTimeout(() => {
                button.textContent = originalText;
                button.disabled = false;
                button.style.backgroundColor = '';
            }, 2000);
        }, 3000);
    }

    // Notification system
    function showNotification(message, type = 'info') {
        // Remove existing notifications
        const existingNotifications = document.querySelectorAll('.notification');
        existingNotifications.forEach(notif => notif.remove());

        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas ${getNotificationIcon(type)}"></i>
                <span>${message}</span>
                <button class="notification-close">&times;</button>
            </div>
        `;

        // Add styles
        notification.style.cssText = `
            position: fixed;
            top: 90px;
            right: 20px;
            background: ${getNotificationColor(type)};
            color: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1000;
            min-width: 300px;
            animation: slideIn 0.3s ease;
        `;

        // Add to page
        document.body.appendChild(notification);

        // Close button functionality
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.addEventListener('click', () => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        });

        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => notification.remove(), 300);
            }
        }, 5000);
    }

    function getNotificationIcon(type) {
        switch(type) {
            case 'success': return 'fa-check-circle';
            case 'error': return 'fa-exclamation-circle';
            case 'warning': return 'fa-exclamation-triangle';
            default: return 'fa-info-circle';
        }
    }

    function getNotificationColor(type) {
        switch(type) {
            case 'success': return '#28a745';
            case 'error': return '#dc3545';
            case 'warning': return '#ffc107';
            default: return '#667eea';
        }
    }

    // Add CSS animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
        
        .notification-content {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .notification-close {
            background: none;
            border: none;
            color: white;
            font-size: 1.2rem;
            cursor: pointer;
            margin-left: auto;
            padding: 0;
            width: 20px;
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .notification-close:hover {
            opacity: 0.7;
        }
    `;
    document.head.appendChild(style);

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Basic validation
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#dc3545';
                } else {
                    field.style.borderColor = '#ddd';
                }
            });
            
            if (isValid) {
                showNotification('Form submitted successfully!', 'success');
            } else {
                showNotification('Please fill in all required fields.', 'error');
            }
        });
    });

    // Progress bar animations
    const progressBars = document.querySelectorAll('.progress-fill');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = width;
        }, 500);
    });

    // Responsive sidebar toggle for mobile
    function createMobileToggle() {
        if (window.innerWidth <= 768) {
            const sidebar = document.querySelector('.sidebar');
            const mainContent = document.querySelector('.main-content');
            
            if (!document.querySelector('.mobile-toggle')) {
                const toggleBtn = document.createElement('button');
                toggleBtn.className = 'mobile-toggle';
                toggleBtn.innerHTML = '<i class="fas fa-bars"></i>';
                toggleBtn.style.cssText = `
                    position: fixed;
                    top: 15px;
                    left: 15px;
                    z-index: 1001;
                    background: #667eea;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 5px;
                    cursor: pointer;
                `;
                
                toggleBtn.addEventListener('click', () => {
                    sidebar.style.display = sidebar.style.display === 'none' ? 'block' : 'none';
                });
                
                document.body.appendChild(toggleBtn);
            }
        }
    }

    // Initialize mobile toggle
    createMobileToggle();
    window.addEventListener('resize', createMobileToggle);

    // Initialize tooltips (simple implementation)
    const elementsWithTooltips = document.querySelectorAll('[title]');
    elementsWithTooltips.forEach(element => {
        element.addEventListener('mouseenter', function(e) {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.getAttribute('title');
            tooltip.style.cssText = `
                position: absolute;
                background: #333;
                color: white;
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 12px;
                z-index: 1000;
                pointer-events: none;
            `;
            
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + 'px';
            tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
            
            this.addEventListener('mouseleave', () => {
                tooltip.remove();
            }, { once: true });
        });
    });

    // AI Advisor Functionality
    const setupAIAdvisorHandlers = () => {
        // Handle Start Chat button click
        const startChatButtons = document.querySelectorAll('.ai-advisor-card button');
        startChatButtons.forEach(button => {
            if (button.innerHTML.includes('Start Chat')) {
                button.addEventListener('click', () => {
                    openAIAdvisorChat('Louis');
                });
            } else if (button.innerHTML.includes('fa-cog')) {
                button.addEventListener('click', () => {
                    openAIAdvisorSettings('Louis');
                });
            }
        });

        // Handle Add AI Advisor card click
        const addAdvisorCard = document.querySelector('[style*="border: 2px dashed"]');
        if (addAdvisorCard) {
            addAdvisorCard.addEventListener('click', () => {
                openAIAdvisorMarketplace();
            });
        }
    };

    // Open AI Advisor Chat Modal
    const openAIAdvisorChat = (advisorName) => {
        const modal = document.createElement('div');
        modal.className = 'ai-chat-modal';
        modal.innerHTML = `
            <div class="modal-overlay" onclick="this.parentElement.remove()"></div>
            <div class="modal-content" style="max-width: 600px; height: 70vh; display: flex; flex-direction: column;">
                <div class="modal-header" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem;">
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <div style="display: flex; align-items: center; gap: 1rem;">
                            <i class="fas fa-graduation-cap" style="font-size: 1.5rem;"></i>
                            <div>
                                <h2 style="margin: 0;">${advisorName} - AI Advisor</h2>
                                <p style="margin: 0; opacity: 0.9; font-size: 0.9rem;">Online • Ready to advise</p>
                            </div>
                        </div>
                        <button onclick="this.closest('.ai-chat-modal').remove()" style="background: none; border: none; color: white; font-size: 1.5rem; cursor: pointer;">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>
                <div class="chat-messages" style="flex: 1; overflow-y: auto; padding: 1.5rem; background: #f8f9fa;">
                    <div class="message ai-message" style="display: flex; gap: 1rem; margin-bottom: 1rem;">
                        <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white;">
                            <i class="fas fa-graduation-cap"></i>
                        </div>
                        <div style="flex: 1;">
                            <p style="background: white; padding: 1rem; border-radius: 8px; margin: 0;">
                                Hello! I'm ${advisorName}, your AI Academic Advisor. I specialize in Mathematics, Computer Science, and Physics. 
                                I'm here to guide your academic journey. Feel free to ask me about:
                                <ul style="margin-top: 0.5rem;">
                                    <li>Course planning and selection</li>
                                    <li>Homework assistance</li>
                                    <li>Concept explanations</li>
                                    <li>Study strategies</li>
                                    <li>Career guidance</li>
                                    <li>Research opportunities</li>
                                </ul>
                            </p>
                        </div>
                    </div>
                </div>
                <div class="chat-input" style="padding: 1rem; background: white; border-top: 1px solid #e5e7eb;">
                    <div style="display: flex; gap: 0.5rem;">
                        <input type="text" placeholder="Type your question..." style="flex: 1; padding: 0.75rem; border: 1px solid #e5e7eb; border-radius: 8px; font-size: 1rem;">
                        <button style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 0.75rem 1.5rem; border: none; border-radius: 8px; cursor: pointer; font-weight: 600;">
                            <i class="fas fa-paper-plane"></i> Send
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Add chat functionality
        const input = modal.querySelector('input');
        const sendButton = modal.querySelector('button[style*="gradient"]');
        const messagesContainer = modal.querySelector('.chat-messages');
        
        const sendMessage = () => {
            const message = input.value.trim();
            if (message) {
                // Add user message
                const userMessageHTML = `
                    <div class="message user-message" style="display: flex; gap: 1rem; margin-bottom: 1rem; justify-content: flex-end;">
                        <div style="flex: 1; text-align: right;">
                            <p style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem; border-radius: 8px; margin: 0; display: inline-block; max-width: 80%;">
                                ${message}
                            </p>
                        </div>
                        <div style="width: 40px; height: 40px; background: #e5e7eb; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                            <i class="fas fa-user"></i>
                        </div>
                    </div>
                `;
                messagesContainer.insertAdjacentHTML('beforeend', userMessageHTML);
                
                // Simulate AI response
                setTimeout(() => {
                    const aiResponseHTML = `
                        <div class="message ai-message" style="display: flex; gap: 1rem; margin-bottom: 1rem;">
                            <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white;">
                                <i class="fas fa-graduation-cap"></i>
                            </div>
                            <div style="flex: 1;">
                                <p style="background: white; padding: 1rem; border-radius: 8px; margin: 0;">
                                    I understand you're asking about "${message}". Let me help you with that...
                                    <br><br>
                                    [This is a simulated response. In a real implementation, this would connect to an AI service to provide actual academic advisory assistance.]
                                </p>
                            </div>
                        </div>
                    `;
                    messagesContainer.insertAdjacentHTML('beforeend', aiResponseHTML);
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                }, 1000);
                
                input.value = '';
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }
        };
        
        sendButton.addEventListener('click', sendMessage);
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    };

    // Open AI Advisor Settings
    const openAIAdvisorSettings = (advisorName) => {
        alert(`Opening settings for ${advisorName}. This feature will allow you to customize the AI advisor's behavior, advisory style, and subject focus.`);
    };

    // Open AI Advisor Marketplace
    const openAIAdvisorMarketplace = () => {
        alert('Opening AI Advisor Marketplace. Here you can browse and add more specialized AI advisors for different subjects like Chemistry, Biology, Literature, History, and more.');
    };

    // Initialize AI Advisor handlers if on academic setup page
    if (window.location.pathname.includes('academic-setup')) {
        setupAIAdvisorHandlers();
    }

    console.log('ABP Interactive Learning Dashboard initialized successfully!');
});
