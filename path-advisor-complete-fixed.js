// Complete AI Path Advisor with Full Course Integration - Fixed Version

// State management
let currentStep = 1;
let selectedCategory = null;
let selectedMajor = null;
let selectedCareer = null;
let selectedCourses = [];
let availableCourses = [];
let userPreferences = {};

// Backend API base URL
const API_BASE_URL = 'http://localhost:8000';

// Complete major data by category
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
        { id: 'criminal-justice', name: 'Criminal Justice', icon: 'shield-alt', description: 'Law enforcement, corrections, courts' }
    ]
};

// Career paths for all majors
const careerPaths = {
    cs: [
        { id: 'software-engineer', name: 'Software Engineer', description: 'Build scalable applications', icon: 'code' },
        { id: 'ml-engineer', name: 'ML Engineer', description: 'Develop AI systems', icon: 'robot' },
        { id: 'data-engineer', name: 'Data Engineer', description: 'Build data pipelines', icon: 'database' }
    ],
    'data-science': [
        { id: 'data-scientist', name: 'Data Scientist', description: 'Analyze complex data', icon: 'chart-line' },
        { id: 'ml-engineer', name: 'ML Engineer', description: 'Build ML models', icon: 'brain' },
        { id: 'bi-analyst', name: 'Business Intelligence Analyst', description: 'Drive business insights', icon: 'chart-pie' }
    ],
    ee: [
        { id: 'embedded-engineer', name: 'Embedded Systems Engineer', description: 'Design firmware', icon: 'microchip' },
        { id: 'rf-engineer', name: 'RF Engineer', description: 'Design wireless systems', icon: 'wifi' },
        { id: 'power-engineer', name: 'Power Systems Engineer', description: 'Design power grids', icon: 'plug' }
    ],
    physics: [
        { id: 'research-physicist', name: 'Research Physicist', description: 'Conduct experiments', icon: 'atom' },
        { id: 'computational-physicist', name: 'Computational Physicist', description: 'Simulate systems', icon: 'calculator' },
        { id: 'applied-physicist', name: 'Applied Physicist', description: 'Develop technologies', icon: 'cogs' }
    ],
    // Default career paths for majors without specific paths
    default: [
        { id: 'researcher', name: 'Researcher', description: 'Conduct research in the field', icon: 'microscope' },
        { id: 'educator', name: 'Educator', description: 'Teach and mentor', icon: 'chalkboard-teacher' },
        { id: 'consultant', name: 'Consultant', description: 'Provide expert advice', icon: 'user-tie' }
    ]
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Initializing AI Path Advisor with Complete Course Integration...');
    
    // Show first step
    showStep(1);
    
    // Set up navigation buttons
    setupNavigationButtons();
    
    // Set up field cards
    setupFieldCards();
    
    // Set up preference inputs
    setupPreferenceInputs();
});

function setupNavigationButtons() {
    console.log('Setting up navigation buttons...');
    
    const nextBtn = document.getElementById('next-btn');
    const prevBtn = document.getElementById('prev-btn');
    
    if (nextBtn) {
        // Remove any existing listeners
        nextBtn.replaceWith(nextBtn.cloneNode(true));
        const newNextBtn = document.getElementById('next-btn');
        newNextBtn.addEventListener('click', handleNext);
        console.log('✅ Next button listener attached');
    }
    
    if (prevBtn) {
        // Remove any existing listeners
        prevBtn.replaceWith(prevBtn.cloneNode(true));
        const newPrevBtn = document.getElementById('prev-btn');
        newPrevBtn.addEventListener('click', handlePrevious);
        console.log('✅ Previous button listener attached');
    }
}

function setupFieldCards() {
    console.log('Setting up field cards...');
    
    // Add click handlers to all field cards
    document.querySelectorAll('.field-card').forEach(card => {
        card.style.cursor = 'pointer';
        card.addEventListener('click', function(e) {
            e.preventDefault();
            const category = this.dataset.category;
            console.log('Field card clicked:', category);
            selectField(category);
        });
    });
    
    console.log(`✅ Set up ${document.querySelectorAll('.field-card').length} field cards`);
}

function setupPreferenceInputs() {
    const hoursSlider = document.getElementById('hours-slider');
    if (hoursSlider) {
        hoursSlider.addEventListener('input', function() {
            const valueDisplay = document.getElementById('hours-value');
            if (valueDisplay) {
                valueDisplay.textContent = this.value + ' hours/week';
            }
        });
    }
}

function selectField(category) {
    console.log('📍 Selected field:', category);
    selectedCategory = category;
    
    // Update UI - highlight selected field
    document.querySelectorAll('.field-card').forEach(card => {
        if (card.dataset.category === category) {
            card.style.borderColor = 'var(--primary-accent, #667eea)';
            card.style.transform = 'translateY(-4px)';
            card.style.boxShadow = '0 8px 24px rgba(102, 126, 234, 0.2)';
        } else {
            card.style.borderColor = '';
            card.style.transform = '';
            card.style.boxShadow = '';
        }
    });
    
    // Enable next button
    enableNextButton();
}

function showMajors() {
    console.log('📚 Showing majors for category:', selectedCategory);
    
    const majorGrid = document.getElementById('major-grid');
    if (!majorGrid) {
        console.error('Major grid not found!');
        return;
    }
    
    const majors = majorsByCategory[selectedCategory] || [];
    console.log(`Found ${majors.length} majors for ${selectedCategory}`);
    
    majorGrid.innerHTML = '';
    
    for (const major of majors) {
        const majorCard = document.createElement('div');
        majorCard.className = 'major-card';
        majorCard.dataset.major = major.id;
        majorCard.style.cursor = 'pointer';
        
        majorCard.innerHTML = `
            <div class="major-icon" style="font-size: 2rem; color: var(--primary-accent, #667eea); margin-bottom: 1rem;">
                <i class="fas fa-${major.icon}"></i>
            </div>
            <h3 style="margin-bottom: 0.5rem;">${major.name}</h3>
            <p style="color: var(--text-secondary); font-size: 0.9rem;">${major.description}</p>
            <div class="course-status" id="status-${major.id}" style="margin-top: 1rem;">
                <span class="badge" style="background: var(--secondary-bg); color: var(--text-primary);">Click to select</span>
            </div>
        `;
        
        majorCard.addEventListener('click', () => selectMajor(major));
        majorGrid.appendChild(majorCard);
    }
    
    // Try to fetch course counts from backend (but don't block)
    majors.forEach(major => {
        fetchCourseCount(major.id);
    });
}

async function fetchCourseCount(majorId) {
    // Only fetch for majors that have courses in backend
    const backendMajors = ['cs', 'ee', 'physics'];
    if (!backendMajors.includes(majorId)) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/courses/major/${majorId}`);
        if (response.ok) {
            const courses = await response.json();
            const statusElement = document.getElementById(`status-${majorId}`);
            if (statusElement) {
                statusElement.innerHTML = `<span class="badge" style="background: var(--primary-accent, #667eea); color: white;">${courses.length} courses available</span>`;
            }
        }
    } catch (error) {
        console.log(`Could not fetch courses for ${majorId} - backend may be offline`);
    }
}

function selectMajor(major) {
    console.log('🎓 Selected major:', major.name, '(', major.id, ')');
    selectedMajor = major.id;
    
    // Update UI
    document.querySelectorAll('.major-card').forEach(card => {
        if (card.dataset.major === major.id) {
            card.style.borderColor = 'var(--primary-accent, #667eea)';
            card.style.background = 'linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)';
        } else {
            card.style.borderColor = '';
            card.style.background = '';
        }
    });
    
    // Try to fetch courses if backend is available
    fetchCoursesForMajor(major.id);
    
    // Enable next button
    enableNextButton();
}

async function fetchCoursesForMajor(majorId) {
    // Only fetch for majors that have courses in backend
    const backendMajors = ['cs', 'ee', 'physics'];
    if (!backendMajors.includes(majorId)) {
        console.log(`No backend courses for ${majorId}, using mock data`);
        availableCourses = generateMockCourses(majorId);
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/courses/major/${majorId}`);
        if (response.ok) {
            availableCourses = await response.json();
            console.log(`✅ Loaded ${availableCourses.length} courses from backend for ${majorId}`);
        } else {
            availableCourses = generateMockCourses(majorId);
        }
    } catch (error) {
        console.log('Backend offline, using mock courses');
        availableCourses = generateMockCourses(majorId);
    }
}

function generateMockCourses(majorId) {
    // Generate mock courses for majors without backend data
    const mockCourses = {
        'data-science': [
            { id: 'DS101', name: 'Introduction to Data Science', credits: 3, prerequisites: [], description: 'Fundamentals of data analysis' },
            { id: 'DS201', name: 'Statistical Methods', credits: 4, prerequisites: ['DS101'], description: 'Statistical analysis techniques' },
            { id: 'DS301', name: 'Machine Learning', credits: 4, prerequisites: ['DS201'], description: 'ML algorithms and applications' }
        ],
        'me': [
            { id: 'ME101', name: 'Engineering Mechanics', credits: 4, prerequisites: [], description: 'Statics and dynamics' },
            { id: 'ME201', name: 'Thermodynamics', credits: 4, prerequisites: ['ME101'], description: 'Heat and energy systems' },
            { id: 'ME301', name: 'Fluid Mechanics', credits: 4, prerequisites: ['ME201'], description: 'Fluid flow and applications' }
        ],
        default: [
            { id: 'CORE101', name: 'Introduction to Field', credits: 3, prerequisites: [], description: 'Foundation course' },
            { id: 'CORE201', name: 'Intermediate Studies', credits: 4, prerequisites: ['CORE101'], description: 'Core concepts' },
            { id: 'CORE301', name: 'Advanced Topics', credits: 4, prerequisites: ['CORE201'], description: 'Specialized knowledge' }
        ]
    };
    
    return mockCourses[majorId] || mockCourses.default;
}

function showCareerPaths() {
    console.log('💼 Showing career paths for major:', selectedMajor);
    
    const careerGrid = document.querySelector('.career-grid');
    if (!careerGrid) {
        console.error('Career grid not found!');
        return;
    }
    
    // If we have courses to select and they haven't been selected yet, show course selection
    if (availableCourses.length > 0 && selectedCourses.length === 0) {
        showCourseSelection();
        return;
    }
    
    // Otherwise show career paths
    const paths = careerPaths[selectedMajor] || careerPaths.default;
    
    careerGrid.innerHTML = '<h3 style="width: 100%; margin-bottom: 1rem;">Choose Your Career Path</h3>';
    
    for (const career of paths) {
        const careerCard = document.createElement('div');
        careerCard.className = 'career-card';
        careerCard.dataset.career = career.id;
        careerCard.style.cssText = `
            background: var(--card-bg);
            border: 2px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            cursor: pointer;
            transition: all 0.3s ease;
        `;
        
        careerCard.innerHTML = `
            <div style="font-size: 2rem; color: var(--primary-accent, #667eea); margin-bottom: 1rem;">
                <i class="fas fa-${career.icon}"></i>
            </div>
            <h4 style="margin-bottom: 0.5rem;">${career.name}</h4>
            <p style="color: var(--text-secondary); font-size: 0.9rem;">${career.description}</p>
        `;
        
        careerCard.addEventListener('click', () => selectCareer(career.id));
        careerGrid.appendChild(careerCard);
    }
}

function showCourseSelection() {
    console.log('📚 Showing course selection for', availableCourses.length, 'courses');
    
    const careerGrid = document.querySelector('.career-grid');
    if (!careerGrid) return;
    
    let html = `
        <div style="width: 100%;">
            <h3 style="margin-bottom: 1rem;">Select Your Courses</h3>
            <p style="margin-bottom: 1rem; color: var(--text-secondary);">
                Choose the courses you want to include in your learning path
            </p>
            <div style="margin-bottom: 1rem;">
                <input type="text" id="course-search" placeholder="Search courses..." 
                       style="width: 100%; padding: 0.75rem; border: 1px solid var(--border-color); 
                              border-radius: 8px; background: var(--secondary-bg);">
            </div>
            <div style="max-height: 400px; overflow-y: auto; margin-bottom: 1rem;">
    `;
    
    for (const course of availableCourses) {
        html += `
            <div class="course-item" data-course-id="${course.id}" 
                 style="background: var(--card-bg); border: 1px solid var(--border-color); 
                        border-radius: 8px; padding: 1rem; margin-bottom: 0.75rem;">
                <div style="display: flex; align-items: start;">
                    <input type="checkbox" class="course-checkbox" value="${course.id}" 
                           id="course-${course.id}" style="margin-right: 1rem; margin-top: 0.25rem;">
                    <div style="flex: 1;">
                        <label for="course-${course.id}" style="cursor: pointer; display: block;">
                            <strong>${course.id}: ${course.name}</strong>
                            <span class="badge" style="margin-left: 0.5rem; background: var(--secondary-bg); 
                                                       padding: 0.25rem 0.5rem; border-radius: 4px;">
                                ${course.credits} credits
                            </span>
                        </label>
                        <p style="margin: 0.5rem 0; color: var(--text-secondary); font-size: 0.9rem;">
                            ${course.description}
                        </p>
                        ${course.prerequisites && course.prerequisites.length > 0 ? 
                            `<small style="color: #ff9800;">Prerequisites: ${course.prerequisites.join(', ')}</small>` : 
                            '<small style="color: #4caf50;">No prerequisites</small>'}
                    </div>
                </div>
            </div>
        `;
    }
    
    html += `
            </div>
            <div style="padding: 1rem; background: var(--secondary-bg); border-radius: 8px;">
                <strong>Selected: <span id="selected-count">0</span> courses</strong>
                <div id="selected-list" style="margin-top: 0.5rem;"></div>
            </div>
            <div style="margin-top: 1rem;">
                <button onclick="skipCourseSelection()" class="btn btn-secondary" 
                        style="padding: 0.5rem 1rem; background: var(--secondary-bg); 
                               border: 1px solid var(--border-color); border-radius: 8px; cursor: pointer;">
                    Skip Course Selection
                </button>
            </div>
        </div>
    `;
    
    careerGrid.innerHTML = html;
    
    // Add event listeners
    document.querySelectorAll('.course-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', updateCourseSelection);
    });
    
    // Add search functionality
    const searchInput = document.getElementById('course-search');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            document.querySelectorAll('.course-item').forEach(item => {
                const text = item.textContent.toLowerCase();
                item.style.display = text.includes(searchTerm) ? 'block' : 'none';
            });
        });
    }
}

function updateCourseSelection() {
    selectedCourses = [];
    document.querySelectorAll('.course-checkbox:checked').forEach(checkbox => {
        selectedCourses.push(checkbox.value);
    });
    
    console.log('📝 Selected courses:', selectedCourses);
    
    document.getElementById('selected-count').textContent = selectedCourses.length;
    
    const selectedList = document.getElementById('selected-list');
    if (selectedCourses.length > 0) {
        const courseNames = selectedCourses.map(id => {
            const course = availableCourses.find(c => c.id === id);
            return course ? course.name : id;
        });
        selectedList.innerHTML = courseNames.map(name => 
            `<span class="badge" style="background: var(--primary-accent, #667eea); color: white; 
                                        margin: 0.25rem; padding: 0.25rem 0.5rem; 
                                        display: inline-block; border-radius: 4px;">
                ${name}
            </span>`
        ).join('');
        
        enableNextButton();
    } else {
        selectedList.innerHTML = '<span style="color: var(--text-secondary);">No courses selected</span>';
    }
}

function skipCourseSelection() {
    console.log('Skipping course selection');
    selectedCourses = [];
    
    // Show career paths instead
    const paths = careerPaths[selectedMajor] || careerPaths.default;
    const careerGrid = document.querySelector('.career-grid');
    
    careerGrid.innerHTML = '';
    for (const career of paths) {
        const careerCard = document.createElement('div');
        careerCard.className = 'career-card';
        careerCard.dataset.career = career.id;
        careerCard.style.cssText = `
            background: var(--card-bg);
            border: 2px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            cursor: pointer;
            transition: all 0.3s ease;
        `;
        
        careerCard.innerHTML = `
            <div style="font-size: 2rem; color: var(--primary-accent, #667eea); margin-bottom: 1rem;">
                <i class="fas fa-${career.icon}"></i>
            </div>
            <h4 style="margin-bottom: 0.5rem;">${career.name}</h4>
            <p style="color: var(--text-secondary); font-size: 0.9rem;">${career.description}</p>
        `;
        
        careerCard.addEventListener('click', () => selectCareer(career.id));
        careerGrid.appendChild(careerCard);
    }
}

function selectCareer(careerId) {
    console.log('🎯 Selected career:', careerId);
    selectedCareer = careerId;
    
    // Update UI
    document.querySelectorAll('.career-card').forEach(card => {
        if (card.dataset.career === careerId) {
            card.style.borderColor = 'var(--primary-accent, #667eea)';
            card.style.background = 'linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)';
        } else {
            card.style.borderColor = '';
            card.style.background = '';
        }
    });
    
    enableNextButton();
}

function handleNext() {
    console.log('➡️ Next clicked, current step:', currentStep);
    
    if (currentStep === 1 && selectedCategory) {
        currentStep = 2;
        showStep(2);
        showMajors();
    } else if (currentStep === 2 && selectedMajor) {
        currentStep = 3;
        showStep(3);
        showCareerPaths();
    } else if (currentStep === 3 && (selectedCareer || selectedCourses.length > 0)) {
        currentStep = 4;
        showStep(4);
        // Preferences step is already in HTML
    } else if (currentStep === 4) {
        currentStep = 5;
        showStep(5);
        generateRoadmap();
    } else {
        console.log('Cannot proceed - missing selection');
    }
}

function handlePrevious() {
    console.log('⬅️ Previous clicked, current step:', currentStep);
    
    if (currentStep > 1) {
        currentStep--;
        showStep(currentStep);
        
        if (currentStep === 2) {
            showMajors();
        } else if (currentStep === 3) {
            showCareerPaths();
        }
    }
}

function showStep(step) {
    console.log('📍 Showing step:', step);
    
    // Hide all steps
    for (let i = 1; i <= 5; i++) {
        const stepElement = document.getElementById(`step-${i}`);
        if (stepElement) {
            stepElement.style.display = 'none';
        }
    }
    
    // Show current step
    const currentStepElement = document.getElementById(`step-${step}`);
    if (currentStepElement) {
        currentStepElement.style.display = 'block';
    }
    
    // Update progress
    updateProgress(step);
    
    // Update navigation buttons
    updateNavButtons(step);
}

function updateProgress(step) {
    // Update all progress indicators
    for (let i = 1; i <= 5; i++) {
        const progressStep = document.getElementById(`step-${i}-progress`);
        if (progressStep) {
            progressStep.classList.remove('active', 'completed');
            
            if (i < step) {
                progressStep.classList.add('completed');
                const circle = progressStep.querySelector('.step-circle');
                if (circle) {
                    circle.style.background = 'var(--success-color, #4caf50)';
                    circle.style.color = 'white';
                }
            } else if (i === step) {
                progressStep.classList.add('active');
                const circle = progressStep.querySelector('.step-circle');
                if (circle) {
                    circle.style.background = 'var(--primary-accent, #667eea)';
                    circle.style.color = 'white';
                }
            } else {
                const circle = progressStep.querySelector('.step-circle');
                if (circle) {
                    circle.style.background = '';
                    circle.style.color = '';
                }
            }
        }
    }
}

function updateNavButtons(step) {
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    
    if (prevBtn) {
        prevBtn.style.display = step > 1 ? 'inline-block' : 'none';
    }
    
    if (nextBtn) {
        if (step === 5) {
            nextBtn.style.display = 'none';
        } else {
            nextBtn.style.display = 'inline-block';
            nextBtn.textContent = step === 4 ? 'Generate Roadmap' : 'Next';
            // Don't auto-disable - let selection handlers control it
        }
    }
}

function enableNextButton() {
    const nextBtn = document.getElementById('next-btn');
    if (nextBtn) {
        nextBtn.disabled = false;
        nextBtn.style.opacity = '1';
        nextBtn.style.cursor = 'pointer';
        console.log('✅ Next button enabled');
    }
}

function disableNextButton() {
    const nextBtn = document.getElementById('next-btn');
    if (nextBtn) {
        nextBtn.disabled = true;
        nextBtn.style.opacity = '0.5';
        nextBtn.style.cursor = 'not-allowed';
    }
}

async function generateRoadmap() {
    console.log('🚀 Generating roadmap...');
    console.log('Selected:', {
        category: selectedCategory,
        major: selectedMajor,
        career: selectedCareer,
        courses: selectedCourses
    });
    
    // Collect preferences
    userPreferences = {
        field: selectedCategory,
        major: selectedMajor,
        career: selectedCareer,
        courses: selectedCourses,
        hours: document.getElementById('hours-slider')?.value || 15,
        budget: document.getElementById('budget-select')?.value || 'free',
        style: document.getElementById('style-select')?.value || 'visual',
        level: document.getElementById('level-select')?.value || 'beginner'
    };
    
    const roadmapResult = document.getElementById('roadmap-result');
    if (!roadmapResult) {
        console.error('Roadmap result element not found');
        return;
    }
    
    // Show loading state
    roadmapResult.innerHTML = `
        <div style="text-align: center; padding: 3rem;">
            <div class="loading">
                <div class="spinner"></div>
            </div>
            <p style="margin-top: 1rem;">Generating your personalized learning roadmap...</p>
        </div>
    `;
    
    // Simulate processing
    setTimeout(() => {
        displayRoadmap();
    }, 2000);
}

function displayRoadmap() {
    const roadmapResult = document.getElementById('roadmap-result');
    
    // Get major name
    const majorData = Object.values(majorsByCategory).flat().find(m => m.id === selectedMajor);
    const majorName = majorData ? majorData.name : selectedMajor;
    
    // Get career name
    const careerData = (careerPaths[selectedMajor] || careerPaths.default).find(c => c.id === selectedCareer);
    const careerName = careerData ? careerData.name : selectedCareer || 'General Path';
    
    let html = `
        <div style="padding: 2rem;">
            <h2 style="margin-bottom: 1.5rem; color: var(--primary-accent, #667eea);">
                🎯 Your Personalized Learning Roadmap
            </h2>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                        gap: 1rem; margin-bottom: 2rem;">
                <div style="padding: 1rem; background: var(--secondary-bg); border-radius: 8px;">
                    <strong>Field:</strong><br>${selectedCategory}
                </div>
                <div style="padding: 1rem; background: var(--secondary-bg); border-radius: 8px;">
                    <strong>Major:</strong><br>${majorName}
                </div>
                <div style="padding: 1rem; background: var(--secondary-bg); border-radius: 8px;">
                    <strong>Career Path:</strong><br>${careerName}
                </div>
                <div style="padding: 1rem; background: var(--secondary-bg); border-radius: 8px;">
                    <strong>Study Hours:</strong><br>${userPreferences.hours} hrs/week
                </div>
            </div>
    `;
    
    // Display selected courses if any
    if (selectedCourses.length > 0) {
        html += `
            <div style="margin-bottom: 2rem;">
                <h3 style="margin-bottom: 1rem;">📚 Selected Courses</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 1rem;">
        `;
        
        for (const courseId of selectedCourses) {
            const course = availableCourses.find(c => c.id === courseId);
            html += `
                <div style="padding: 1rem; background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                            border: 1px solid var(--primary-accent, #667eea); border-radius: 8px;">
                    <strong>${courseId}</strong><br>
                    <span style="color: var(--text-secondary); font-size: 0.9rem;">
                        ${course ? course.name : 'Course'}
                    </span>
                </div>
            `;
        }
        
        html += `
                </div>
            </div>
        `;
    }
    
    // Add learning milestones
    html += `
        <div style="margin-bottom: 2rem;">
            <h3 style="margin-bottom: 1rem;">🏆 Learning Milestones</h3>
            <div style="position: relative; padding-left: 2rem;">
    `;
    
    const milestones = [
        { month: 1, title: 'Foundation', description: 'Core concepts and fundamentals' },
        { month: 3, title: 'Intermediate', description: 'Advanced topics and practical applications' },
        { month: 6, title: 'Advanced', description: 'Specialization and real-world projects' },
        { month: 12, title: 'Expert', description: 'Industry-ready skills and portfolio' }
    ];
    
    for (const milestone of milestones) {
        html += `
            <div style="margin-bottom: 1.5rem; padding: 1rem; background: var(--card-bg); 
                        border-left: 4px solid var(--primary-accent, #667eea); border-radius: 8px;">
                <strong>Month ${milestone.month}: ${milestone.title}</strong><br>
                <span style="color: var(--text-secondary);">${milestone.description}</span>
            </div>
        `;
    }
    
    html += `
            </div>
        </div>
        
        <div style="margin-top: 2rem; display: flex; gap: 1rem; flex-wrap: wrap;">
            <button class="btn btn-primary" onclick="saveRoadmap()" 
                    style="padding: 0.75rem 1.5rem; background: var(--primary-accent, #667eea); 
                           color: white; border: none; border-radius: 8px; cursor: pointer;">
                💾 Save Roadmap
            </button>
            <button class="btn btn-secondary" onclick="downloadRoadmap()"
                    style="padding: 0.75rem 1.5rem; background: var(--secondary-bg); 
                           border: 1px solid var(--border-color); border-radius: 8px; cursor: pointer;">
                📥 Download PDF
            </button>
            <button class="btn btn-outline" onclick="location.reload()"
                    style="padding: 0.75rem 1.5rem; background: transparent; 
                           border: 1px solid var(--border-color); border-radius: 8px; cursor: pointer;">
                🔄 Start Over
            </button>
        </div>
    </div>
    `;
    
    roadmapResult.innerHTML = html;
}

// Global functions
window.skipCourseSelection = skipCourseSelection;
window.saveRoadmap = function() {
    alert('✅ Roadmap saved to your profile! You can access it from your dashboard.');
};
window.downloadRoadmap = function() {
    alert('📥 Downloading roadmap as PDF... (Feature coming soon!)');
};

console.log('✅ AI Path Advisor script loaded successfully!');