// Complete AI Path Advisor JavaScript

// State management
let currentStep = 1;
let selectedCategory = null;
let selectedMajor = null;
let selectedCareer = null;
let userPreferences = {};

// Major data by category
const majorsByCategory = {
    technology: [
        { id: 'cs', name: 'Computer Science', icon: 'laptop-code', description: 'Programming, algorithms, AI/ML, systems' },
        { id: 'data-science', name: 'Data Science', icon: 'chart-bar', description: 'Statistics, ML, data engineering' }
    ],
    engineering: [
        { id: 'ee', name: 'Electrical Engineering', icon: 'bolt', description: 'Circuits, signals, power systems' },
        { id: 'me', name: 'Mechanical Engineering', icon: 'cogs', description: 'Mechanics, thermodynamics, design' },
        { id: 'civil', name: 'Civil Engineering', icon: 'building', description: 'Structures, transportation, water' },
        { id: 'chemeng', name: 'Chemical Engineering', icon: 'flask', description: 'Process design, reactions, transport' },
        { id: 'bme', name: 'Biomedical Engineering', icon: 'dna', description: 'Medical devices, imaging, biomechanics' }
    ],
    sciences: [
        { id: 'physics', name: 'Physics', icon: 'atom', description: 'Mechanics, E&M, quantum, thermo' },
        { id: 'chemistry', name: 'Chemistry', icon: 'vial', description: 'Organic, inorganic, physical, analytical' },
        { id: 'materials', name: 'Materials Science', icon: 'cubes', description: 'Polymers, semiconductors, nanomaterials' },
        { id: 'environment', name: 'Environmental Science', icon: 'leaf', description: 'Climate, air quality, water treatment' }
    ],
    health: [
        { id: 'medicine', name: 'Medicine (Pre-Med)', icon: 'stethoscope', description: 'Anatomy, physiology, pathology' },
        { id: 'nursing', name: 'Nursing', icon: 'user-nurse', description: 'Patient care, pharmacology, clinical' },
        { id: 'pharmacy', name: 'Pharmacy', icon: 'pills', description: 'Drug design, pharmacology, clinical' },
        { id: 'public-health', name: 'Public Health', icon: 'globe', description: 'Epidemiology, biostatistics, policy' },
        { id: 'nutrition', name: 'Nutrition & Dietetics', icon: 'apple-alt', description: 'Clinical nutrition, food science' }
    ],
    business: [
        { id: 'economics', name: 'Economics', icon: 'chart-line', description: 'Micro, macro, econometrics, policy' },
        { id: 'finance', name: 'Finance', icon: 'dollar-sign', description: 'Corporate finance, investments, banking' }
    ],
    social: [
        { id: 'policy', name: 'Political Science', icon: 'landmark', description: 'Comparative politics, policy analysis' },
        { id: 'education', name: 'Education', icon: 'graduation-cap', description: 'Learning theories, curriculum, assessment' },
        { id: 'psychology', name: 'Psychology', icon: 'brain', description: 'Clinical, cognitive, social, developmental' }
    ],
    arts: [
        { id: 'architecture', name: 'Architecture', icon: 'drafting-compass', description: 'Design studios, sustainability, urban' },
        { id: 'communications', name: 'Communications', icon: 'newspaper', description: 'Writing, reporting, media, journalism' }
    ],
    law: [
        { id: 'law', name: 'Law (Pre-Law)', icon: 'gavel', description: 'Contracts, torts, constitutional, criminal' },
        { id: 'criminal-justice', name: 'Criminal Justice', icon: 'shield-alt', description: 'Law enforcement, corrections, forensics' }
    ]
};

// Career paths for each major
const careerPaths = {
    'cs': [
        { id: 'full-cs', name: 'Full Computer Science Degree', duration: '24-36 months', icon: 'graduation-cap' },
        { id: 'ml-engineer', name: 'Machine Learning Engineer', duration: '12-18 months', icon: 'brain' },
        { id: 'full-stack', name: 'Full Stack Developer', duration: '6-10 months', icon: 'code' },
        { id: 'data-engineer', name: 'Data Engineer', duration: '8-12 months', icon: 'database' }
    ],
    'data-science': [
        { id: 'data-scientist', name: 'Data Scientist', duration: '12-18 months', icon: 'chart-line' },
        { id: 'ml-engineer', name: 'Machine Learning Engineer', duration: '12-18 months', icon: 'brain' },
        { id: 'data-analyst', name: 'Data Analyst', duration: '6-9 months', icon: 'chart-bar' }
    ],
    'ee': [
        { id: 'full-ee', name: 'Full Electrical Engineering', duration: '24-36 months', icon: 'graduation-cap' },
        { id: 'embedded', name: 'Embedded Systems Engineer', duration: '10-14 months', icon: 'microchip' },
        { id: 'power', name: 'Power Systems Engineer', duration: '12-18 months', icon: 'bolt' }
    ],
    'medicine': [
        { id: 'pre-med', name: 'Pre-Medical Curriculum', duration: '36-48 months', icon: 'graduation-cap' },
        { id: 'clinical-research', name: 'Clinical Research', duration: '18-24 months', icon: 'microscope' },
        { id: 'medical-prep', name: 'MCAT Preparation Track', duration: '6-12 months', icon: 'book-medical' }
    ],
    'default': [
        { id: 'full', name: 'Full Curriculum', duration: '24-36 months', icon: 'graduation-cap' },
        { id: 'specialist', name: 'Domain Specialist', duration: '12-18 months', icon: 'user-tie' },
        { id: 'practitioner', name: 'Professional Track', duration: '12-24 months', icon: 'briefcase' },
        { id: 'certification', name: 'Certification Path', duration: '6-12 months', icon: 'certificate' }
    ]
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    setupFieldSelection();
    setupSlider();
    
    // Initially hide navigation buttons
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    if (prevBtn) prevBtn.style.display = 'none';
    if (nextBtn) nextBtn.style.display = 'none';
});

function setupFieldSelection() {
    // Add click handlers to field cards
    document.querySelectorAll('.field-card').forEach(card => {
        card.addEventListener('click', function() {
            selectField(this.dataset.category);
        });
    });
}

function setupSlider() {
    const slider = document.getElementById('hours-slider');
    if (slider) {
        slider.addEventListener('input', function() {
            document.getElementById('hours-value').textContent = this.value;
        });
    }
}

function selectField(category) {
    selectedCategory = category;
    
    // Update UI
    document.querySelectorAll('.field-card').forEach(c => c.classList.remove('selected'));
    document.querySelector(`[data-category="${category}"]`).classList.add('selected');
    
    // Show next button
    document.getElementById('next-btn').style.display = 'block';
}

function showMajors() {
    const majors = majorsByCategory[selectedCategory] || [];
    const majorGrid = document.getElementById('major-grid');
    
    majorGrid.innerHTML = majors.map(major => `
        <div class="goal-card" onclick="selectMajor('${major.id}')" style="cursor: pointer; transition: all 0.3s ease;">
            <div class="goal-icon" style="background: linear-gradient(135deg, var(--primary-accent) 0%, var(--secondary-accent) 100%);">
                <i class="fas fa-${major.icon}"></i>
            </div>
            <h3 style="margin: 0 0 0.5rem 0; color: var(--text-primary);">${major.name}</h3>
            <p class="text-secondary" style="font-size: 0.9rem; margin: 0;">
                ${major.description}
            </p>
        </div>
    `).join('');
    
    // Hide step 1, show step 2
    document.getElementById('step-1').style.display = 'none';
    document.getElementById('step-2').style.display = 'block';
    updateProgress(2);
    currentStep = 2;
    
    // Update navigation
    document.getElementById('prev-btn').style.display = 'block';
}

function selectMajor(majorId) {
    selectedMajor = majorId;
    
    // Highlight selected major
    event.currentTarget.style.border = '2px solid var(--primary-accent)';
    event.currentTarget.style.background = 'linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%)';
    
    // Auto-advance after short delay
    setTimeout(() => showCareerPaths(), 300);
}

function showCareerPaths() {
    const careers = careerPaths[selectedMajor] || careerPaths['default'];
    const careerGrid = document.getElementById('career-grid');
    
    careerGrid.innerHTML = careers.map(career => `
        <div class="goal-card" onclick="selectCareer('${career.id}')" style="cursor: pointer; transition: all 0.3s ease;">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div class="goal-icon" style="background: linear-gradient(135deg, var(--primary-accent) 0%, var(--secondary-accent) 100%);">
                    <i class="fas fa-${career.icon}"></i>
                </div>
                <div>
                    <h3 style="margin: 0; color: var(--text-primary);">${career.name}</h3>
                    <p class="text-secondary" style="margin: 0; font-size: 0.9rem;">
                        <i class="fas fa-clock" style="margin-right: 0.5rem;"></i>${career.duration}
                    </p>
                </div>
            </div>
        </div>
    `).join('');
    
    // Hide step 2, show step 3
    document.getElementById('step-2').style.display = 'none';
    document.getElementById('step-3').style.display = 'block';
    updateProgress(3);
    currentStep = 3;
}

function selectCareer(careerId) {
    selectedCareer = careerId;
    
    // Highlight selected career
    event.currentTarget.style.border = '2px solid var(--primary-accent)';
    event.currentTarget.style.background = 'linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%)';
    
    // Auto-advance after short delay
    setTimeout(() => {
        document.getElementById('step-3').style.display = 'none';
        document.getElementById('step-4').style.display = 'block';
        updateProgress(4);
        currentStep = 4;
    }, 300);
}

function backToFields() {
    document.getElementById('step-2').style.display = 'none';
    document.getElementById('step-1').style.display = 'block';
    updateProgress(1);
    currentStep = 1;
    document.getElementById('prev-btn').style.display = 'none';
}

function updateProgress(step) {
    // Update progress indicators
    for (let i = 1; i <= 5; i++) {
        const progressStep = document.getElementById(`step-${i}-progress`);
        if (progressStep) {
            if (i < step) {
                progressStep.classList.add('completed');
                progressStep.classList.remove('active');
            } else if (i === step) {
                progressStep.classList.add('active');
                progressStep.classList.remove('completed');
            } else {
                progressStep.classList.remove('active', 'completed');
            }
        }
    }
}

function nextStep() {
    if (currentStep === 1) {
        if (!selectedCategory) {
            alert('Please select a field of study');
            return;
        }
        showMajors();
    } else if (currentStep === 2) {
        if (!selectedMajor) {
            alert('Please select a major');
            return;
        }
        showCareerPaths();
    } else if (currentStep === 3) {
        if (!selectedCareer) {
            alert('Please select a career path');
            return;
        }
        document.getElementById('step-3').style.display = 'none';
        document.getElementById('step-4').style.display = 'block';
        updateProgress(4);
        currentStep = 4;
    } else if (currentStep === 4) {
        generateRoadmap();
    }
}

function previousStep() {
    if (currentStep === 2) {
        backToFields();
    } else if (currentStep === 3) {
        document.getElementById('step-3').style.display = 'none';
        document.getElementById('step-2').style.display = 'block';
        updateProgress(2);
        currentStep = 2;
    } else if (currentStep === 4) {
        document.getElementById('step-4').style.display = 'none';
        document.getElementById('step-3').style.display = 'block';
        updateProgress(3);
        currentStep = 3;
    } else if (currentStep === 5) {
        document.getElementById('step-5').style.display = 'none';
        document.getElementById('step-4').style.display = 'block';
        updateProgress(4);
        currentStep = 4;
        document.getElementById('next-btn').style.display = 'block';
    }
}

function startQuiz() {
    alert('Quiz feature coming soon! We\'ll use your selected experience level for now.');
    generateRoadmap();
}

function skipQuiz() {
    generateRoadmap();
}

function generateRoadmap() {
    // Collect preferences
    userPreferences = {
        field: selectedCategory,
        major: selectedMajor,
        career: selectedCareer,
        hours: document.getElementById('hours-slider').value,
        budget: document.getElementById('budget-select').value,
        style: document.getElementById('style-select').value,
        level: document.getElementById('level-select').value
    };
    
    // Hide step 4, show step 5
    document.getElementById('step-4').style.display = 'none';
    document.getElementById('step-5').style.display = 'block';
    document.getElementById('next-btn').style.display = 'none';
    updateProgress(5);
    currentStep = 5;
    
    // Simulate loading
    setTimeout(() => {
        displayRoadmap();
    }, 2500);
}

function displayRoadmap() {
    const majorName = majorsByCategory[selectedCategory]?.find(m => m.id === selectedMajor)?.name || selectedMajor;
    const totalWeeks = Math.ceil(180 / parseInt(userPreferences.hours));
    const totalHours = totalWeeks * parseInt(userPreferences.hours);
    
    const roadmapHTML = `
        <div class="card-header">
            <h2>Your Personalized Learning Roadmap</h2>
            <span class="badge" style="background: var(--success-color); color: white; padding: 0.5rem 1rem;">
                <i class="fas fa-check-circle"></i> Ready to Start
            </span>
        </div>
        
        <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); padding: 1.5rem; border-radius: 12px; margin: 2rem 0;">
            <h3 style="margin: 0 0 0.5rem 0; color: var(--text-primary);">
                <i class="fas fa-graduation-cap" style="color: var(--primary-accent); margin-right: 0.5rem;"></i>
                ${majorName} - ${selectedCareer}
            </h3>
            <p class="text-secondary" style="margin: 0;">
                Customized for ${userPreferences.level} level • ${userPreferences.style} learning style • ${userPreferences.hours} hours/week
            </p>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin: 2rem 0;">
            <div class="stat-card" style="text-align: center; padding: 1.5rem;">
                <div class="stat-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0 auto 1rem;">
                    <i class="fas fa-calendar-alt"></i>
                </div>
                <div class="stat-value">${totalWeeks}</div>
                <div class="stat-label">Total Weeks</div>
            </div>
            <div class="stat-card" style="text-align: center; padding: 1.5rem;">
                <div class="stat-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); margin: 0 auto 1rem;">
                    <i class="fas fa-clock"></i>
                </div>
                <div class="stat-value">${totalHours}</div>
                <div class="stat-label">Total Hours</div>
            </div>
            <div class="stat-card" style="text-align: center; padding: 1.5rem;">
                <div class="stat-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); margin: 0 auto 1rem;">
                    <i class="fas fa-book"></i>
                </div>
                <div class="stat-value">6</div>
                <div class="stat-label">Core Modules</div>
            </div>
            <div class="stat-card" style="text-align: center; padding: 1.5rem;">
                <div class="stat-icon" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); margin: 0 auto 1rem;">
                    <i class="fas fa-project-diagram"></i>
                </div>
                <div class="stat-value">3</div>
                <div class="stat-label">Projects</div>
            </div>
        </div>
        
        <h3 style="margin: 2rem 0 1rem 0;">
            <i class="fas fa-route" style="color: var(--primary-accent); margin-right: 0.5rem;"></i>
            Your Learning Path
        </h3>
        
        <div style="position: relative; padding-left: 2rem;">
            ${generateModules()}
        </div>
        
        <div style="margin-top: 3rem; padding: 2rem; background: var(--info-bg, #f0f9ff); border-radius: 12px; text-align: center;">
            <h3 style="margin: 0 0 1rem 0; color: var(--text-primary);">Ready to Begin?</h3>
            <p class="text-secondary" style="margin-bottom: 1.5rem;">
                Your personalized roadmap is ready. Start with Module 1 and track your progress along the way.
            </p>
            <button class="btn btn-primary btn-lg" onclick="startLearning()" style="padding: 1rem 2rem;">
                <i class="fas fa-rocket"></i> Start Learning Journey
            </button>
            <button class="btn btn-outline btn-lg" onclick="downloadRoadmap()" style="margin-left: 1rem; padding: 1rem 2rem;">
                <i class="fas fa-download"></i> Download Plan
            </button>
        </div>
    `;
    
    document.getElementById('loading-state').style.display = 'none';
    document.getElementById('roadmap-result').innerHTML = roadmapHTML;
    document.getElementById('roadmap-result').style.display = 'block';
}

function generateModules() {
    const modules = [
        { name: 'Foundation & Prerequisites', weeks: '1-3', description: 'Core concepts and mathematical foundations', resources: ['Textbook', 'Video Course', 'Practice Sets'] },
        { name: 'Core Fundamentals', weeks: '4-7', description: 'Essential theories and principles', resources: ['Interactive Labs', 'Case Studies', 'Quizzes'] },
        { name: 'Applied Concepts', weeks: '8-10', description: 'Practical applications and real-world scenarios', resources: ['Projects', 'Simulations', 'Workshops'] },
        { name: 'Advanced Topics', weeks: '11-13', description: 'Specialized knowledge and cutting-edge concepts', resources: ['Research Papers', 'Expert Talks', 'Forums'] },
        { name: 'Integration & Synthesis', weeks: '14-15', description: 'Connecting concepts and building expertise', resources: ['Capstone Project', 'Peer Review', 'Mentorship'] },
        { name: 'Portfolio & Career Prep', weeks: '16+', description: 'Building your professional portfolio', resources: ['Portfolio Guide', 'Interview Prep', 'Networking'] }
    ];
    
    return modules.map((module, index) => `
        <div class="goal-card" style="margin-bottom: 1.5rem; position: relative; padding-left: 2rem;">
            <div style="position: absolute; left: -1rem; top: 1.5rem; width: 30px; height: 30px; background: ${index === 0 ? 'var(--primary-accent)' : 'var(--border-color)'}; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">
                ${index + 1}
            </div>
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div style="flex: 1;">
                    <h4 style="margin: 0 0 0.5rem 0; color: var(--text-primary);">${module.name}</h4>
                    <p class="text-secondary" style="margin: 0 0 0.75rem 0; font-size: 0.9rem;">
                        ${module.description}
                    </p>
                    <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                        ${module.resources.map(r => `
                            <span class="badge" style="background: var(--secondary-bg); color: var(--text-secondary); padding: 0.25rem 0.75rem;">
                                ${r}
                            </span>
                        `).join('')}
                    </div>
                </div>
                <div style="text-align: right;">
                    <span class="badge" style="background: var(--primary-accent); color: white; padding: 0.5rem 1rem;">
                        Weeks ${module.weeks}
                    </span>
                </div>
            </div>
        </div>
    `).join('');
}

function startLearning() {
    alert('Great! Redirecting to your dashboard where you can track your progress...');
    window.location.href = 'dashboard.html';
}

function downloadRoadmap() {
    alert('Your roadmap PDF will be generated and downloaded shortly...');
}