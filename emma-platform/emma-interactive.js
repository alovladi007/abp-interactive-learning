// Emma Platform - Interactive Features

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    setupNavigation();
    setupInputMethods();
    setupSolver();
    setupSubjects();
    setupButtons();
});

// Navigation setup
function setupNavigation() {
    // Update nav links to use anchors
    updateNavLinks();
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
}

function updateNavLinks() {
    const navMenu = document.querySelector('.nav-menu');
    if (navMenu) {
        navMenu.innerHTML = `
            <a href="#" class="nav-link active">Home</a>
            <a href="#subjects" class="nav-link">Subjects</a>
            <a href="#quick-input" class="nav-link">Solver</a>
            <a href="#features" class="nav-link">Study Tools</a>
            <a href="#demo-section" class="nav-link">Practice</a>
        `;
    }
}

// Input method switching
function setupInputMethods() {
    const inputTypes = document.querySelectorAll('.input-type');
    const inputField = document.querySelector('.input-field');
    
    inputTypes.forEach(type => {
        type.addEventListener('click', function() {
            inputTypes.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            const method = this.dataset.type || this.textContent.trim().toLowerCase();
            handleInputMethod(method, inputField);
        });
    });
}

function handleInputMethod(method, inputField) {
    switch(method) {
        case 'type':
        case 'text':
            inputField.placeholder = 'Enter your homework question...';
            inputField.disabled = false;
            break;
        case 'photo':
            inputField.placeholder = 'Click here to upload a photo...';
            inputField.disabled = true;
            inputField.addEventListener('click', uploadPhoto);
            break;
        case 'voice':
            inputField.placeholder = 'Click here to record audio...';
            inputField.disabled = true;
            inputField.addEventListener('click', startVoiceRecording);
            break;
        case 'draw':
            inputField.placeholder = 'Click here to open drawing pad...';
            inputField.disabled = true;
            inputField.addEventListener('click', openDrawingPad);
            break;
    }
}

// Solver functionality
function setupSolver() {
    const solveBtn = document.querySelector('.btn-solve');
    const inputField = document.querySelector('.input-field');
    
    if (solveBtn) {
        solveBtn.addEventListener('click', function() {
            const question = inputField.value.trim();
            if (question) {
                showSolution(question);
            } else {
                alert('Please enter a question first!');
            }
        });
    }
}

function showSolution(question) {
    alert(`Solution for: "${question}"\n\nStep 1: Analyze the problem\nStep 2: Apply relevant concepts\nStep 3: Calculate the answer\n\nDetailed solution coming soon!`);
}

// Subject selection
function setupSubjects() {
    const subjectTags = document.querySelectorAll('.subject-tags .tag');
    
    subjectTags.forEach(tag => {
        tag.addEventListener('click', function() {
            if (this.textContent === 'More...') {
                showAllSubjects();
            } else {
                this.classList.toggle('active');
            }
        });
    });
    
    // Subject cards
    const exploreButtons = document.querySelectorAll('.btn-explore');
    exploreButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const subjectCard = this.closest('.subject-card');
            const subjectName = subjectCard.querySelector('h3').textContent;
            showSubjectDetails(subjectName);
        });
    });
}

function showAllSubjects() {
    const subjects = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'History', 
                     'English', 'Computer Science', 'Economics', 'Psychology', 
                     'Geography', 'Art', 'Music', 'Philosophy', 'Engineering'];
    
    alert('All Available Subjects:\n\n' + subjects.join('\n'));
}

function showSubjectDetails(subject) {
    alert(`${subject} Resources:\n\n• Video Tutorials\n• Practice Problems\n• Study Guides\n• Expert Help\n\nClick "Start Learning ${subject}" to begin!`);
}

// Button handlers
function setupButtons() {
    // Start Learning Free button
    const startBtn = document.querySelector('.hero-actions .btn-gradient');
    if (startBtn) {
        startBtn.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector('.quick-input').scrollIntoView({ behavior: 'smooth' });
        });
    }
    
    // Watch Demo button
    const demoBtn = document.querySelector('.hero-actions .btn-outline');
    if (demoBtn) {
        demoBtn.addEventListener('click', function(e) {
            e.preventDefault();
            alert('Demo Video:\n\n1. Enter your homework question\n2. Select the subject\n3. Get instant step-by-step solution\n4. Practice with similar problems\n\nFull demo coming soon!');
        });
    }
}

// Helper functions
function uploadPhoto() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.onchange = (e) => {
        const file = e.target.files[0];
        if (file) {
            alert(`Photo uploaded: ${file.name}\n\nProcessing image for text extraction...`);
        }
    };
    input.click();
}

function startVoiceRecording() {
    alert('Voice Recording:\n\n🎤 Click "Allow" to use microphone\n📢 Speak your question clearly\n⏹️ Click stop when done\n\nVoice feature coming soon!');
}

function openDrawingPad() {
    alert('Drawing Pad:\n\n✏️ Draw math equations\n📐 Use shapes and symbols\n🔢 Write formulas\n\nDrawing feature coming soon!');
}

// Add section IDs for navigation
document.addEventListener('DOMContentLoaded', function() {
    // Add IDs to sections if they don't exist
    const quickInput = document.querySelector('.quick-input');
    if (quickInput && !quickInput.id) quickInput.id = 'quick-input';
    
    const demoSection = document.querySelector('.demo-section');
    if (demoSection && !demoSection.id) demoSection.id = 'demo-section';
});