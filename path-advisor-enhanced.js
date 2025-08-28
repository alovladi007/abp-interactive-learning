// Enhanced AI Path Advisor JavaScript with all majors

// Major definitions by category
const majorsByCategory = {
    technology: [
        {
            id: 'cs',
            name: 'Computer Science',
            icon: 'laptop-code',
            color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            description: 'Programming, algorithms, AI/ML, systems',
            careers: 6,
            duration: '6-36 months'
        },
        {
            id: 'data-science',
            name: 'Data Science',
            icon: 'chart-bar',
            color: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
            description: 'Statistics, ML, data engineering, analytics',
            careers: 5,
            duration: '6-24 months'
        }
    ],
    engineering: [
        {
            id: 'ee',
            name: 'Electrical Engineering',
            icon: 'bolt',
            color: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            description: 'Circuits, signals, power systems, embedded',
            careers: 5,
            duration: '10-36 months'
        },
        {
            id: 'me',
            name: 'Mechanical Engineering',
            icon: 'cogs',
            color: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
            description: 'Mechanics, thermodynamics, design, manufacturing',
            careers: 5,
            duration: '12-36 months'
        },
        {
            id: 'civil',
            name: 'Civil Engineering',
            icon: 'building',
            color: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
            description: 'Structures, transportation, water, geotechnical',
            careers: 5,
            duration: '12-36 months'
        },
        {
            id: 'chemeng',
            name: 'Chemical Engineering',
            icon: 'flask',
            color: 'linear-gradient(135deg, #f857a6 0%, #ff5858 100%)',
            description: 'Process design, reactions, transport, control',
            careers: 5,
            duration: '12-36 months'
        },
        {
            id: 'bme',
            name: 'Biomedical Engineering',
            icon: 'dna',
            color: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
            description: 'Medical devices, imaging, biomechanics, tissue',
            careers: 5,
            duration: '12-36 months'
        }
    ],
    sciences: [
        {
            id: 'physics',
            name: 'Physics',
            icon: 'atom',
            color: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
            description: 'Mechanics, E&M, quantum, thermodynamics',
            careers: 4,
            duration: '12-36 months'
        },
        {
            id: 'materials',
            name: 'Materials Science',
            icon: 'cubes',
            color: 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)',
            description: 'Polymers, semiconductors, nanomaterials',
            careers: 5,
            duration: '10-36 months'
        },
        {
            id: 'environment',
            name: 'Environmental Science',
            icon: 'leaf',
            color: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
            description: 'Climate, air quality, water treatment',
            careers: 4,
            duration: '10-30 months'
        },
        {
            id: 'chemistry',
            name: 'Chemistry',
            icon: 'vial',
            color: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            description: 'Organic, inorganic, physical, analytical',
            careers: 4,
            duration: '12-36 months'
        }
    ],
    health: [
        {
            id: 'medicine',
            name: 'Medicine (Pre-Med)',
            icon: 'stethoscope',
            color: 'linear-gradient(135deg, #f857a6 0%, #ff5858 100%)',
            description: 'Anatomy, physiology, pathology, pharmacology',
            careers: 6,
            duration: '24-48 months'
        },
        {
            id: 'nursing',
            name: 'Nursing',
            icon: 'user-nurse',
            color: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
            description: 'Patient care, pharmacology, clinical practice',
            careers: 4,
            duration: '18-36 months'
        },
        {
            id: 'pharmacy',
            name: 'Pharmacy',
            icon: 'pills',
            color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            description: 'Drug design, pharmacology, clinical pharmacy',
            careers: 4,
            duration: '24-48 months'
        },
        {
            id: 'public-health',
            name: 'Public Health',
            icon: 'globe',
            color: 'linear-gradient(135deg, #30cfd0 0%, #330867 100%)',
            description: 'Epidemiology, biostatistics, health policy',
            careers: 5,
            duration: '10-30 months'
        },
        {
            id: 'nutrition',
            name: 'Nutrition & Dietetics',
            icon: 'apple-alt',
            color: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
            description: 'Clinical nutrition, food science, metabolism',
            careers: 4,
            duration: '12-24 months'
        }
    ],
    business: [
        {
            id: 'economics',
            name: 'Economics',
            icon: 'chart-line',
            color: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
            description: 'Micro, macro, econometrics, policy analysis',
            careers: 5,
            duration: '12-36 months'
        },
        {
            id: 'finance',
            name: 'Finance',
            icon: 'dollar-sign',
            color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            description: 'Corporate finance, investments, banking',
            careers: 6,
            duration: '12-30 months'
        }
    ],
    social: [
        {
            id: 'policy',
            name: 'Political Science',
            icon: 'landmark',
            color: 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)',
            description: 'Comparative politics, policy analysis, IR',
            careers: 4,
            duration: '12-30 months'
        },
        {
            id: 'education',
            name: 'Education',
            icon: 'graduation-cap',
            color: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
            description: 'Learning theories, curriculum, assessment',
            careers: 4,
            duration: '12-24 months'
        },
        {
            id: 'psychology',
            name: 'Psychology',
            icon: 'brain',
            color: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            description: 'Clinical, cognitive, social, developmental',
            careers: 5,
            duration: '18-36 months'
        }
    ],
    arts: [
        {
            id: 'architecture',
            name: 'Architecture',
            icon: 'drafting-compass',
            color: 'linear-gradient(135deg, #30cfd0 0%, #330867 100%)',
            description: 'Design studios, sustainability, urban planning',
            careers: 4,
            duration: '24-48 months'
        },
        {
            id: 'communications',
            name: 'Communications',
            icon: 'newspaper',
            color: 'linear-gradient(135deg, #f857a6 0%, #ff5858 100%)',
            description: 'Writing, reporting, media, data journalism',
            careers: 4,
            duration: '12-24 months'
        }
    ],
    law: [
        {
            id: 'law',
            name: 'Law (Pre-Law)',
            icon: 'gavel',
            color: 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)',
            description: 'Contracts, torts, constitutional, criminal law',
            careers: 5,
            duration: '24-36 months'
        },
        {
            id: 'criminal-justice',
            name: 'Criminal Justice',
            icon: 'shield-alt',
            color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            description: 'Law enforcement, corrections, forensics',
            careers: 4,
            duration: '12-24 months'
        }
    ]
};

// Career paths for each major
const careerPaths = {
    'cs': [
        { id: 'full-cs', name: 'Full Computer Science Degree', duration: '24-36 months', icon: 'graduation-cap' },
        { id: 'ml-engineer', name: 'Machine Learning Engineer', duration: '12-18 months', icon: 'brain' },
        { id: 'full-stack', name: 'Full Stack Developer', duration: '6-10 months', icon: 'code' },
        { id: 'data-engineer', name: 'Data Engineer', duration: '8-12 months', icon: 'database' },
        { id: 'security-engineer', name: 'Security Engineer', duration: '10-14 months', icon: 'shield-alt' },
        { id: 'devops', name: 'DevOps Engineer', duration: '8-12 months', icon: 'server' }
    ],
    'ee': [
        { id: 'full-ee', name: 'Full Electrical Engineering', duration: '24-36 months', icon: 'graduation-cap' },
        { id: 'embedded', name: 'Embedded Systems Engineer', duration: '10-14 months', icon: 'microchip' },
        { id: 'power', name: 'Power Systems Engineer', duration: '12-18 months', icon: 'bolt' },
        { id: 'control', name: 'Control Systems Engineer', duration: '12-16 months', icon: 'sliders-h' },
        { id: 'rf', name: 'RF/Communications Engineer', duration: '14-18 months', icon: 'satellite' }
    ],
    'me': [
        { id: 'full-me', name: 'Full Mechanical Engineering', duration: '24-36 months', icon: 'graduation-cap' },
        { id: 'design', name: 'Design Engineer', duration: '12-18 months', icon: 'drafting-compass' },
        { id: 'manufacturing', name: 'Manufacturing Engineer', duration: '10-14 months', icon: 'industry' },
        { id: 'thermal', name: 'Thermal Systems Engineer', duration: '12-16 months', icon: 'temperature-high' },
        { id: 'robotics', name: 'Robotics Engineer', duration: '14-18 months', icon: 'robot' }
    ],
    'medicine': [
        { id: 'full-med', name: 'Pre-Medical Curriculum', duration: '36-48 months', icon: 'graduation-cap' },
        { id: 'clinical', name: 'Clinical Research', duration: '18-24 months', icon: 'microscope' },
        { id: 'surgery', name: 'Surgical Preparation', duration: '24-30 months', icon: 'procedures' },
        { id: 'primary', name: 'Primary Care Track', duration: '24-30 months', icon: 'stethoscope' },
        { id: 'specialist', name: 'Medical Specialist', duration: '30-36 months', icon: 'user-md' },
        { id: 'research', name: 'Medical Research', duration: '24-30 months', icon: 'flask' }
    ],
    'public-health': [
        { id: 'full-ph', name: 'Full Public Health', duration: '24-30 months', icon: 'graduation-cap' },
        { id: 'epidemiologist', name: 'Epidemiologist', duration: '12-18 months', icon: 'virus' },
        { id: 'health-policy', name: 'Health Policy Analyst', duration: '10-14 months', icon: 'file-medical' },
        { id: 'global-health', name: 'Global Health Specialist', duration: '12-16 months', icon: 'globe' },
        { id: 'biostatistician', name: 'Biostatistician', duration: '10-14 months', icon: 'chart-line' }
    ],
    'default': [
        { id: 'full', name: 'Full Curriculum', duration: '24-36 months', icon: 'graduation-cap' },
        { id: 'specialist', name: 'Domain Specialist', duration: '12-18 months', icon: 'user-tie' },
        { id: 'practitioner', name: 'Professional Track', duration: '12-24 months', icon: 'briefcase' },
        { id: 'research', name: 'Research Focus', duration: '18-30 months', icon: 'microscope' }
    ]
};

// State management
let currentStep = 1;
let selectedCategory = null;
let selectedMajor = null;
let selectedCareer = null;
let userPreferences = {};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    setupCategoryHandlers();
    setupSliders();
});

function setupCategoryHandlers() {
    document.querySelectorAll('.category-card').forEach(card => {
        card.addEventListener('click', function() {
            // Remove previous selection
            document.querySelectorAll('.category-card').forEach(c => c.classList.remove('active'));
            
            // Add selection to clicked card
            this.classList.add('active');
            selectedCategory = this.dataset.category;
            
            // Show majors for this category
            showMajors(selectedCategory);
        });
    });
}

function showMajors(category) {
    const majors = majorsByCategory[category] || [];
    const majorGrid = document.getElementById('major-grid');
    const categoryTitle = document.getElementById('category-title');
    
    // Update title
    const categoryCard = document.querySelector(`[data-category="${category}"]`);
    categoryTitle.textContent = `Select Your Major in ${categoryCard.querySelector('h3').textContent}`;
    
    // Populate majors
    majorGrid.innerHTML = majors.map(major => `
        <div class="major-card" data-major="${major.id}">
            <div class="major-icon" style="background: ${major.color};">
                <i class="fas fa-${major.icon}"></i>
            </div>
            <h3 style="margin: 0 0 0.5rem 0;">${major.name}</h3>
            <p style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 1rem;">
                ${major.description}
            </p>
            <div style="display: flex; gap: 1rem; font-size: 0.85rem; color: var(--text-secondary);">
                <span><i class="fas fa-route"></i> ${major.careers} paths</span>
                <span><i class="fas fa-clock"></i> ${major.duration}</span>
            </div>
        </div>
    `).join('');
    
    // Show major selection section
    document.getElementById('step-1').style.display = 'none';
    document.getElementById('major-selection').style.display = 'block';
    
    // Add click handlers to major cards
    document.querySelectorAll('.major-card').forEach(card => {
        card.addEventListener('click', function() {
            document.querySelectorAll('.major-card').forEach(c => c.classList.remove('selected'));
            this.classList.add('selected');
            selectedMajor = this.dataset.major;
            
            // Show career paths after a short delay
            setTimeout(() => {
                showCareerPaths(selectedMajor);
            }, 300);
        });
    });
}

function backToCategories() {
    document.getElementById('major-selection').style.display = 'none';
    document.getElementById('step-1').style.display = 'block';
    selectedMajor = null;
}

function showCareerPaths(major) {
    const careerGrid = document.getElementById('career-grid');
    const careers = careerPaths[major] || careerPaths['default'];
    
    careerGrid.innerHTML = careers.map(career => `
        <div class="career-card" data-career="${career.id}">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <div style="width: 50px; height: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center;">
                    <i class="fas fa-${career.icon}" style="color: white; font-size: 1.5rem;"></i>
                </div>
                <div>
                    <h3 style="margin: 0;">${career.name}</h3>
                    <p style="margin: 0; color: var(--text-secondary); font-size: 0.9rem;">${career.duration}</p>
                </div>
            </div>
        </div>
    `).join('');
    
    // Hide major selection and show career selection
    document.getElementById('major-selection').style.display = 'none';
    document.getElementById('step-2').style.display = 'block';
    document.getElementById('main-nav').style.display = 'flex';
    updateProgress(2);
    
    // Add click handlers to career cards
    document.querySelectorAll('.career-card').forEach(card => {
        card.addEventListener('click', function() {
            document.querySelectorAll('.career-card').forEach(c => c.classList.remove('selected'));
            this.classList.add('selected');
            selectedCareer = this.dataset.career;
        });
    });
}

function setupSliders() {
    const hoursSlider = document.getElementById('hours-slider');
    if (hoursSlider) {
        hoursSlider.addEventListener('input', function() {
            document.getElementById('hours-value').textContent = `${this.value} hours/week`;
        });
    }
}

function updateProgress(step) {
    currentStep = step;
    
    // Update progress indicators
    for (let i = 1; i <= 5; i++) {
        const progressStep = document.getElementById(`step-${i}-progress`);
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

function nextStep() {
    if (currentStep === 2 && !selectedCareer) {
        alert('Please select a career path');
        return;
    }
    
    if (currentStep === 2) {
        document.getElementById('step-2').style.display = 'none';
        document.getElementById('step-3').style.display = 'block';
        updateProgress(3);
    } else if (currentStep === 3) {
        // Collect preferences
        userPreferences = {
            hours: document.getElementById('hours-slider').value,
            budget: document.getElementById('budget-select').value,
            style: document.getElementById('style-select').value,
            level: document.getElementById('level-select')?.value || 'beginner'
        };
        
        document.getElementById('step-3').style.display = 'none';
        document.getElementById('step-4').style.display = 'block';
        updateProgress(4);
    } else if (currentStep === 4) {
        generateRoadmap();
    }
    
    currentStep++;
}

function previousStep() {
    if (currentStep === 2) {
        document.getElementById('step-2').style.display = 'none';
        document.getElementById('major-selection').style.display = 'block';
        document.getElementById('main-nav').style.display = 'none';
        updateProgress(1);
    } else if (currentStep === 3) {
        document.getElementById('step-3').style.display = 'none';
        document.getElementById('step-2').style.display = 'block';
        updateProgress(2);
    } else if (currentStep === 4) {
        document.getElementById('step-4').style.display = 'none';
        document.getElementById('step-3').style.display = 'block';
        updateProgress(3);
    }
    
    currentStep--;
}

function startQuiz() {
    alert('Quiz feature coming soon! For now, we\'ll use your preferences.');
    skipQuiz();
}

function skipQuiz() {
    generateRoadmap();
}

function generateRoadmap() {
    // Hide step 4
    document.getElementById('step-4').style.display = 'none';
    document.getElementById('main-nav').style.display = 'none';
    
    // Show loading state
    document.getElementById('step-5').style.display = 'block';
    updateProgress(5);
    
    // Simulate API call and generate roadmap
    setTimeout(() => {
        displayRoadmap();
    }, 2000);
}

function displayRoadmap() {
    // Generate sample roadmap based on selection
    const roadmapData = generateRoadmapData(selectedMajor, selectedCareer, userPreferences);
    
    const roadmapHTML = `
        <h2>Your Personalized Learning Roadmap</h2>
        <p style="color: var(--text-secondary); margin-bottom: 2rem;">
            ${selectedMajor.toUpperCase()} - ${selectedCareer} Path
        </p>
        
        <div style="display: flex; gap: 2rem; margin-bottom: 2rem;">
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: bold; color: var(--primary-accent);">
                    ${roadmapData.weeks}
                </div>
                <div style="font-size: 0.9rem; color: var(--text-secondary);">Total Weeks</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: bold; color: var(--primary-accent);">
                    ${roadmapData.hours}
                </div>
                <div style="font-size: 0.9rem; color: var(--text-secondary);">Total Hours</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: bold; color: var(--primary-accent);">
                    ${roadmapData.modules.length}
                </div>
                <div style="font-size: 0.9rem; color: var(--text-secondary);">Modules</div>
            </div>
        </div>
        
        <div class="roadmap-timeline">
            ${roadmapData.modules.map((module, index) => `
                <div class="roadmap-item">
                    <h3>${module.name}</h3>
                    <p style="color: var(--text-secondary); margin: 0.5rem 0;">
                        ${module.description}
                    </p>
                    <p style="font-size: 0.9rem; color: var(--text-secondary);">
                        <i class="fas fa-clock"></i> ${module.duration} weeks | 
                        <i class="fas fa-book"></i> ${module.resources} resources
                    </p>
                </div>
            `).join('')}
        </div>
        
        <div class="nav-buttons">
            <button class="btn btn-secondary" onclick="location.reload()">
                <i class="fas fa-redo"></i> Start Over
            </button>
            <button class="btn btn-primary" onclick="startLearning()">
                <i class="fas fa-rocket"></i> Start Learning
            </button>
        </div>
    `;
    
    document.getElementById('step-5').innerHTML = roadmapHTML;
}

function generateRoadmapData(major, career, preferences) {
    // Generate realistic roadmap data based on selections
    const modules = [];
    const hoursPerWeek = parseInt(preferences.hours) || 15;
    
    // Add foundation module
    modules.push({
        name: 'Foundation & Prerequisites',
        description: 'Core concepts and mathematical foundations',
        duration: 4,
        resources: 12
    });
    
    // Add core modules based on major
    if (major === 'cs' || major === 'data-science') {
        modules.push({
            name: 'Programming & Data Structures',
            description: 'Master programming languages and fundamental data structures',
            duration: 6,
            resources: 18
        });
        modules.push({
            name: 'Algorithms & Systems',
            description: 'Algorithm design, analysis, and system architecture',
            duration: 6,
            resources: 15
        });
    } else if (major === 'medicine' || major === 'nursing') {
        modules.push({
            name: 'Anatomy & Physiology',
            description: 'Human body systems and functions',
            duration: 8,
            resources: 20
        });
        modules.push({
            name: 'Clinical Sciences',
            description: 'Pathology, pharmacology, and clinical practice',
            duration: 8,
            resources: 22
        });
    } else {
        modules.push({
            name: 'Core Theory',
            description: 'Fundamental theories and principles of the field',
            duration: 6,
            resources: 16
        });
        modules.push({
            name: 'Applied Practice',
            description: 'Hands-on application and practical skills',
            duration: 6,
            resources: 14
        });
    }
    
    // Add specialization module
    modules.push({
        name: 'Specialization & Capstone',
        description: 'Advanced topics and final project',
        duration: 4,
        resources: 10
    });
    
    const totalWeeks = modules.reduce((sum, m) => sum + m.duration, 0);
    const totalHours = totalWeeks * hoursPerWeek;
    
    return {
        weeks: totalWeeks,
        hours: totalHours,
        modules: modules
    };
}

function startLearning() {
    alert('Great! Your learning journey begins now. You\'ll be redirected to your dashboard.');
    window.location.href = 'dashboard.html';
}