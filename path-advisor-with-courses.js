// Enhanced AI Path Advisor with Course Integration

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

// Major data by category (simplified for course integration)
const majorsByCategory = {
    technology: [
        { id: 'cs', name: 'Computer Science', icon: 'laptop-code', description: 'Programming, algorithms, AI/ML, systems' }
    ],
    engineering: [
        { id: 'ee', name: 'Electrical Engineering', icon: 'bolt', description: 'Circuits, signals, power systems' }
    ],
    sciences: [
        { id: 'physics', name: 'Physics', icon: 'atom', description: 'Mechanics, E&M, quantum, thermo' }
    ]
};

// Career paths (simplified)
const careerPaths = {
    cs: [
        { id: 'software-engineer', name: 'Software Engineer', description: 'Build scalable applications', icon: 'code' },
        { id: 'ml-engineer', name: 'ML Engineer', description: 'Develop AI systems', icon: 'robot' },
        { id: 'data-engineer', name: 'Data Engineer', description: 'Build data pipelines', icon: 'database' }
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
    ]
};

// Fetch courses from backend
async function fetchCourses(major) {
    try {
        const response = await fetch(`${API_BASE_URL}/courses/major/${major}`);
        if (!response.ok) throw new Error('Failed to fetch courses');
        return await response.json();
    } catch (error) {
        console.error('Error fetching courses:', error);
        // Fallback to empty array if backend is not available
        return [];
    }
}

// Fetch course details
async function fetchCourseDetails(major, courseId) {
    try {
        const response = await fetch(`${API_BASE_URL}/courses/major/${major}/course/${courseId}`);
        if (!response.ok) throw new Error('Failed to fetch course details');
        return await response.json();
    } catch (error) {
        console.error('Error fetching course details:', error);
        return null;
    }
}

// Generate course roadmap
async function fetchCourseRoadmap(major) {
    try {
        const response = await fetch(`${API_BASE_URL}/courses/major/${major}/roadmap`);
        if (!response.ok) throw new Error('Failed to fetch roadmap');
        return await response.json();
    } catch (error) {
        console.error('Error fetching roadmap:', error);
        return null;
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Show first step
    showStep(1);
    
    // Set up event listeners
    setupEventListeners();
    
    // Populate categories
    populateCategories();
});

function setupEventListeners() {
    // Navigation buttons
    const nextBtn = document.getElementById('next-btn');
    const prevBtn = document.getElementById('prev-btn');
    
    if (nextBtn) {
        nextBtn.addEventListener('click', nextStep);
    }
    
    if (prevBtn) {
        prevBtn.addEventListener('click', previousStep);
    }
    
    // Preference inputs
    const hoursSlider = document.getElementById('hours-slider');
    if (hoursSlider) {
        hoursSlider.addEventListener('input', function() {
            document.getElementById('hours-value').textContent = this.value + ' hours/week';
        });
    }
}

function populateCategories() {
    const categoryGrid = document.querySelector('.category-grid');
    if (!categoryGrid) return;
    
    categoryGrid.innerHTML = '';
    
    for (const [key, majors] of Object.entries(majorsByCategory)) {
        const categoryCard = document.createElement('div');
        categoryCard.className = 'category-card';
        categoryCard.dataset.category = key;
        
        // Simple icon based on category
        const iconMap = {
            technology: '💻',
            engineering: '⚙️',
            sciences: '🔬'
        };
        
        categoryCard.innerHTML = `
            <div class="category-icon" style="font-size: 2rem;">${iconMap[key] || '📚'}</div>
            <h3 style="text-transform: capitalize;">${key}</h3>
            <p>${majors.length} majors</p>
        `;
        
        categoryCard.addEventListener('click', () => selectCategory(key));
        categoryGrid.appendChild(categoryCard);
    }
}

function selectCategory(category) {
    selectedCategory = category;
    
    // Update UI
    document.querySelectorAll('.category-card').forEach(card => {
        card.classList.toggle('active', card.dataset.category === category);
    });
    
    // Enable next button
    document.getElementById('next-btn').disabled = false;
}

async function showMajors() {
    const majorGrid = document.querySelector('.major-grid');
    if (!majorGrid) return;
    
    majorGrid.innerHTML = '';
    
    const majors = majorsByCategory[selectedCategory] || [];
    
    for (const major of majors) {
        const majorCard = document.createElement('div');
        majorCard.className = 'major-card';
        majorCard.dataset.major = major.id;
        
        majorCard.innerHTML = `
            <div class="major-icon" style="font-size: 2rem;">
                <i class="fas fa-${major.icon}"></i>
            </div>
            <h3>${major.name}</h3>
            <p>${major.description}</p>
            <div class="course-count" id="course-count-${major.id}">
                <span class="loading-text">Loading courses...</span>
            </div>
        `;
        
        majorCard.addEventListener('click', () => selectMajor(major.id));
        majorGrid.appendChild(majorCard);
        
        // Fetch course count for this major
        fetchCourses(major.id).then(courses => {
            const countElement = document.getElementById(`course-count-${major.id}`);
            if (countElement && courses.length > 0) {
                countElement.innerHTML = `<span class="badge">${courses.length} courses available</span>`;
            } else if (countElement) {
                countElement.innerHTML = '<span class="text-muted">Course data unavailable</span>';
            }
        });
    }
}

async function selectMajor(majorId) {
    selectedMajor = majorId;
    
    // Update UI
    document.querySelectorAll('.major-card').forEach(card => {
        card.classList.toggle('selected', card.dataset.major === majorId);
    });
    
    // Fetch courses for selected major
    availableCourses = await fetchCourses(majorId);
    
    // Enable next button
    document.getElementById('next-btn').disabled = false;
}

async function showCourses() {
    const courseContainer = document.getElementById('step-3');
    if (!courseContainer) return;
    
    // Update step title
    const stepTitle = courseContainer.querySelector('h2');
    if (stepTitle) {
        stepTitle.textContent = 'Step 3: Select Your Courses';
    }
    
    // Create course selection UI
    let courseHTML = `
        <div class="course-selection">
            <p class="mb-3">Select the courses you want to include in your learning path:</p>
            <div class="course-filter mb-3">
                <input type="text" id="course-search" class="form-control" placeholder="Search courses...">
            </div>
            <div class="course-list" style="max-height: 400px; overflow-y: auto;">
    `;
    
    if (availableCourses.length > 0) {
        for (const course of availableCourses) {
            courseHTML += `
                <div class="course-item" data-course-id="${course.id}">
                    <div class="form-check">
                        <input class="form-check-input course-checkbox" type="checkbox" 
                               value="${course.id}" id="course-${course.id}">
                        <label class="form-check-label" for="course-${course.id}">
                            <div class="course-info">
                                <strong>${course.id}: ${course.name}</strong>
                                <span class="badge badge-secondary ml-2">${course.credits} credits</span>
                                <p class="mb-1 text-muted">${course.description}</p>
                                ${course.prerequisites.length > 0 ? 
                                    `<small class="text-warning">Prerequisites: ${course.prerequisites.join(', ')}</small>` : 
                                    '<small class="text-success">No prerequisites</small>'}
                            </div>
                        </label>
                    </div>
                    <button class="btn btn-sm btn-outline-info mt-2" onclick="showCourseDetails('${selectedMajor}', '${course.id}')">
                        View Syllabus
                    </button>
                </div>
            `;
        }
    } else {
        courseHTML += '<p class="text-muted">No courses available for this major.</p>';
    }
    
    courseHTML += `
            </div>
            <div class="selected-courses mt-3">
                <strong>Selected Courses: <span id="selected-count">0</span></strong>
                <div id="selected-list" class="mt-2"></div>
            </div>
        </div>
    `;
    
    // Find or create course content div
    let courseContent = courseContainer.querySelector('.course-content');
    if (!courseContent) {
        courseContent = document.createElement('div');
        courseContent.className = 'course-content';
        courseContainer.appendChild(courseContent);
    }
    courseContent.innerHTML = courseHTML;
    
    // Add event listeners for course selection
    document.querySelectorAll('.course-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', updateSelectedCourses);
    });
    
    // Add search functionality
    const searchInput = document.getElementById('course-search');
    if (searchInput) {
        searchInput.addEventListener('input', filterCourses);
    }
}

function updateSelectedCourses() {
    selectedCourses = [];
    const checkboxes = document.querySelectorAll('.course-checkbox:checked');
    
    checkboxes.forEach(checkbox => {
        selectedCourses.push(checkbox.value);
    });
    
    // Update UI
    document.getElementById('selected-count').textContent = selectedCourses.length;
    
    const selectedList = document.getElementById('selected-list');
    if (selectedCourses.length > 0) {
        selectedList.innerHTML = selectedCourses.map(id => {
            const course = availableCourses.find(c => c.id === id);
            return `<span class="badge badge-primary mr-1">${course ? course.name : id}</span>`;
        }).join('');
    } else {
        selectedList.innerHTML = '<span class="text-muted">No courses selected</span>';
    }
    
    // Enable/disable next button
    document.getElementById('next-btn').disabled = selectedCourses.length === 0;
}

function filterCourses() {
    const searchTerm = document.getElementById('course-search').value.toLowerCase();
    
    document.querySelectorAll('.course-item').forEach(item => {
        const courseInfo = item.querySelector('.course-info').textContent.toLowerCase();
        item.style.display = courseInfo.includes(searchTerm) ? 'block' : 'none';
    });
}

async function showCourseDetails(major, courseId) {
    const details = await fetchCourseDetails(major, courseId);
    if (!details) {
        alert('Could not load course details');
        return;
    }
    
    // Create modal for course details
    const modal = document.createElement('div');
    modal.className = 'modal fade show';
    modal.style.display = 'block';
    modal.style.backgroundColor = 'rgba(0,0,0,0.5)';
    
    modal.innerHTML = `
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">${details.id}: ${details.name}</h5>
                    <button type="button" class="close" onclick="this.closest('.modal').remove()">
                        <span>&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <h6>Learning Objectives:</h6>
                    <ul>
                        ${details.syllabus.objectives.map(obj => `<li>${obj}</li>`).join('')}
                    </ul>
                    
                    <h6>Weekly Topics:</h6>
                    <div class="accordion">
                        ${details.syllabus.topics.map((topic, i) => `
                            <div class="card mb-1">
                                <div class="card-header">
                                    <strong>Week ${topic.week}:</strong> ${topic.topic}
                                </div>
                                <div class="card-body">
                                    <p>${topic.content}</p>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                    
                    <h6 class="mt-3">Assessment:</h6>
                    <ul>
                        ${details.syllabus.assessments.map(a => 
                            `<li>${a.type}: ${a.weight} - ${a.description}</li>`
                        ).join('')}
                    </ul>
                    
                    <h6>Textbooks:</h6>
                    <ul>
                        ${details.syllabus.textbooks.map(book => `<li>${book}</li>`).join('')}
                    </ul>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
}

function showCareerPaths() {
    const careerGrid = document.querySelector('.career-grid');
    if (!careerGrid) return;
    
    careerGrid.innerHTML = '';
    
    const paths = careerPaths[selectedMajor] || [];
    
    for (const career of paths) {
        const careerCard = document.createElement('div');
        careerCard.className = 'career-card';
        careerCard.dataset.career = career.id;
        
        careerCard.innerHTML = `
            <div class="career-icon">
                <i class="fas fa-${career.icon}"></i>
            </div>
            <h3>${career.name}</h3>
            <p>${career.description}</p>
            ${selectedCourses.length > 0 ? 
                `<small class="text-info">Tailored for ${selectedCourses.length} selected courses</small>` : 
                ''}
        `;
        
        careerCard.addEventListener('click', () => selectCareer(career.id));
        careerGrid.appendChild(careerCard);
    }
}

function selectCareer(careerId) {
    selectedCareer = careerId;
    
    // Update UI
    document.querySelectorAll('.career-card').forEach(card => {
        card.classList.toggle('selected', card.dataset.career === careerId);
    });
    
    // Enable next button
    document.getElementById('next-btn').disabled = false;
}

async function generateRoadmap() {
    // Collect preferences
    userPreferences = {
        field: selectedCategory,
        major: selectedMajor,
        career: selectedCareer,
        courses: selectedCourses,
        hours: document.getElementById('hours-slider').value,
        budget: document.getElementById('budget-select').value,
        style: document.getElementById('style-select').value,
        level: document.getElementById('level-select').value
    };
    
    // Show loading state
    const roadmapResult = document.getElementById('roadmap-result');
    roadmapResult.innerHTML = '<div class="text-center"><div class="spinner-border"></div><p>Generating your personalized roadmap...</p></div>';
    
    // Fetch course roadmap from backend
    const roadmap = await fetchCourseRoadmap(selectedMajor);
    
    // Display roadmap with courses
    setTimeout(() => {
        displayRoadmapWithCourses(roadmap);
    }, 1500);
}

function displayRoadmapWithCourses(roadmap) {
    const roadmapResult = document.getElementById('roadmap-result');
    
    let html = `
        <div class="roadmap-header">
            <h3>Your Personalized Learning Path</h3>
            <p>Major: <strong>${selectedMajor.toUpperCase()}</strong> | 
               Career: <strong>${selectedCareer}</strong> | 
               Courses: <strong>${selectedCourses.length} selected</strong></p>
        </div>
        
        <div class="roadmap-timeline">
    `;
    
    if (roadmap && roadmap.roadmap) {
        // Display semester-based roadmap
        for (const semester of roadmap.roadmap) {
            html += `
                <div class="semester-block">
                    <h4>Semester ${semester.semester}</h4>
                    <p class="text-muted">${semester.total_credits} credits</p>
                    <div class="course-cards">
            `;
            
            for (const courseId of semester.courses) {
                const course = availableCourses.find(c => c.id === courseId);
                const isSelected = selectedCourses.includes(courseId);
                
                html += `
                    <div class="course-card ${isSelected ? 'selected-course' : ''}">
                        <h5>${courseId}</h5>
                        <p>${course ? course.name : 'Course Details'}</p>
                        ${isSelected ? '<span class="badge badge-success">Selected</span>' : ''}
                    </div>
                `;
            }
            
            html += `
                    </div>
                </div>
            `;
        }
    } else {
        // Fallback display if no roadmap from backend
        html += `
            <div class="roadmap-item">
                <h4>Foundation Courses</h4>
                ${selectedCourses.slice(0, 3).map(id => {
                    const course = availableCourses.find(c => c.id === id);
                    return `<p>• ${course ? course.name : id}</p>`;
                }).join('')}
            </div>
            <div class="roadmap-item">
                <h4>Core Courses</h4>
                ${selectedCourses.slice(3, 6).map(id => {
                    const course = availableCourses.find(c => c.id === id);
                    return `<p>• ${course ? course.name : id}</p>`;
                }).join('')}
            </div>
            <div class="roadmap-item">
                <h4>Advanced Courses</h4>
                ${selectedCourses.slice(6).map(id => {
                    const course = availableCourses.find(c => c.id === id);
                    return `<p>• ${course ? course.name : id}</p>`;
                }).join('')}
            </div>
        `;
    }
    
    html += `
        </div>
        <div class="roadmap-actions mt-4">
            <button class="btn btn-primary" onclick="downloadRoadmap()">Download Roadmap</button>
            <button class="btn btn-secondary" onclick="startLearning()">Start Learning</button>
        </div>
    `;
    
    roadmapResult.innerHTML = html;
}

function downloadRoadmap() {
    // Create downloadable roadmap
    const roadmapData = {
        major: selectedMajor,
        career: selectedCareer,
        courses: selectedCourses,
        preferences: userPreferences,
        generated: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(roadmapData, null, 2)], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `roadmap-${selectedMajor}-${Date.now()}.json`;
    a.click();
}

function startLearning() {
    alert('Your learning journey begins! The first course materials will be available in your dashboard.');
}

// Navigation functions
function nextStep() {
    if (currentStep === 1 && selectedCategory) {
        currentStep = 2;
        showStep(2);
        showMajors();
    } else if (currentStep === 2 && selectedMajor) {
        currentStep = 3;
        showStep(3);
        showCourses();
    } else if (currentStep === 3 && selectedCourses.length > 0) {
        currentStep = 4;
        showStep(4);
        showCareerPaths();
    } else if (currentStep === 4 && selectedCareer) {
        currentStep = 5;
        showStep(5);
    } else if (currentStep === 5) {
        currentStep = 6;
        showStep(6);
        generateRoadmap();
    }
}

function previousStep() {
    if (currentStep > 1) {
        currentStep--;
        showStep(currentStep);
        
        // Re-populate data for the previous step
        if (currentStep === 2) showMajors();
        else if (currentStep === 3) showCourses();
        else if (currentStep === 4) showCareerPaths();
    }
}

function showStep(step) {
    // Hide all steps
    for (let i = 1; i <= 6; i++) {
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
    const steps = document.querySelectorAll('.wizard-step');
    steps.forEach((stepEl, index) => {
        if (index < step) {
            stepEl.classList.add('completed');
            stepEl.classList.remove('active');
        } else if (index === step - 1) {
            stepEl.classList.add('active');
            stepEl.classList.remove('completed');
        } else {
            stepEl.classList.remove('active', 'completed');
        }
    });
}

function updateNavButtons(step) {
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    
    if (prevBtn) {
        prevBtn.style.display = step > 1 ? 'inline-block' : 'none';
    }
    
    if (nextBtn) {
        if (step === 6) {
            nextBtn.style.display = 'none';
        } else {
            nextBtn.style.display = 'inline-block';
            nextBtn.textContent = step === 5 ? 'Generate Roadmap' : 'Next';
            nextBtn.disabled = true; // Will be enabled when selection is made
        }
    }
}