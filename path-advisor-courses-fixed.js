// Fixed AI Path Advisor with Course Integration

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

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing AI Path Advisor with Courses...');
    
    // Show first step
    showStep(1);
    
    // Set up event listeners
    setupEventListeners();
    
    // Set up field cards
    setupFieldCards();
});

function setupEventListeners() {
    console.log('Setting up event listeners...');
    
    // Navigation buttons
    const nextBtn = document.getElementById('next-btn');
    const prevBtn = document.getElementById('prev-btn');
    
    if (nextBtn) {
        nextBtn.addEventListener('click', handleNext);
    }
    
    if (prevBtn) {
        prevBtn.addEventListener('click', handlePrevious);
    }
    
    // Preference inputs
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

function setupFieldCards() {
    console.log('Setting up field cards...');
    
    // Add click handlers to existing field cards
    document.querySelectorAll('.field-card').forEach(card => {
        card.addEventListener('click', function() {
            const category = this.dataset.category;
            selectField(category);
        });
    });
}

function selectField(category) {
    console.log('Selected field:', category);
    selectedCategory = category;
    
    // Update UI
    document.querySelectorAll('.field-card').forEach(card => {
        if (card.dataset.category === category) {
            card.classList.add('active');
            card.style.borderColor = 'var(--primary-accent)';
            card.style.transform = 'translateY(-2px)';
        } else {
            card.classList.remove('active');
            card.style.borderColor = '';
            card.style.transform = '';
        }
    });
    
    // Enable next button
    const nextBtn = document.getElementById('next-btn');
    if (nextBtn) {
        nextBtn.disabled = false;
        nextBtn.style.opacity = '1';
    }
}

async function showMajors() {
    console.log('Showing majors for category:', selectedCategory);
    
    const majorGrid = document.getElementById('major-grid');
    if (!majorGrid) return;
    
    // Map categories to available majors in backend
    const categoryMajorMap = {
        'technology': ['cs'],
        'engineering': ['ee'],
        'sciences': ['physics']
    };
    
    const majors = categoryMajorMap[selectedCategory] || [];
    
    majorGrid.innerHTML = '';
    
    for (const majorId of majors) {
        const majorCard = document.createElement('div');
        majorCard.className = 'major-card';
        majorCard.dataset.major = majorId;
        
        const majorNames = {
            'cs': 'Computer Science',
            'ee': 'Electrical Engineering',
            'physics': 'Physics'
        };
        
        const majorIcons = {
            'cs': 'laptop-code',
            'ee': 'bolt',
            'physics': 'atom'
        };
        
        majorCard.innerHTML = `
            <div class="major-icon">
                <i class="fas fa-${majorIcons[majorId] || 'book'}"></i>
            </div>
            <h3>${majorNames[majorId] || majorId}</h3>
            <p>Click to select this major</p>
            <div class="course-count" id="course-count-${majorId}">
                <span class="loading-text">Loading courses...</span>
            </div>
        `;
        
        majorCard.addEventListener('click', () => selectMajor(majorId));
        majorGrid.appendChild(majorCard);
        
        // Fetch course count for this major
        try {
            const response = await fetch(`${API_BASE_URL}/courses/major/${majorId}`);
            if (response.ok) {
                const courses = await response.json();
                const countElement = document.getElementById(`course-count-${majorId}`);
                if (countElement) {
                    countElement.innerHTML = `<span class="badge" style="background: var(--primary-accent); color: white;">${courses.length} courses available</span>`;
                }
            }
        } catch (error) {
            console.error('Error fetching courses for', majorId, error);
            const countElement = document.getElementById(`course-count-${majorId}`);
            if (countElement) {
                countElement.innerHTML = '<span class="text-muted">Backend offline</span>';
            }
        }
    }
}

async function selectMajor(majorId) {
    console.log('Selected major:', majorId);
    selectedMajor = majorId;
    
    // Update UI
    document.querySelectorAll('.major-card').forEach(card => {
        if (card.dataset.major === majorId) {
            card.classList.add('selected');
            card.style.borderColor = 'var(--primary-accent)';
            card.style.background = 'linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)';
        } else {
            card.classList.remove('selected');
            card.style.borderColor = '';
            card.style.background = '';
        }
    });
    
    // Fetch courses for selected major
    try {
        const response = await fetch(`${API_BASE_URL}/courses/major/${majorId}`);
        if (response.ok) {
            availableCourses = await response.json();
            console.log(`Loaded ${availableCourses.length} courses for ${majorId}`);
        }
    } catch (error) {
        console.error('Error fetching courses:', error);
        availableCourses = [];
    }
    
    // Enable next button
    const nextBtn = document.getElementById('next-btn');
    if (nextBtn) {
        nextBtn.disabled = false;
        nextBtn.style.opacity = '1';
    }
}

async function showCourses() {
    console.log('Showing courses for major:', selectedMajor);
    
    const careerGrid = document.querySelector('.career-grid');
    if (!careerGrid) return;
    
    // Transform career grid to show courses instead
    let courseHTML = `
        <div style="width: 100%;">
            <h3 style="margin-bottom: 1rem;">Available Courses for ${selectedMajor.toUpperCase()}</h3>
            <div style="margin-bottom: 1rem;">
                <input type="text" id="course-search" placeholder="Search courses..." 
                       style="width: 100%; padding: 0.5rem; border: 1px solid var(--border-color); border-radius: 8px;">
            </div>
            <div class="course-list" style="max-height: 400px; overflow-y: auto;">
    `;
    
    if (availableCourses.length > 0) {
        for (const course of availableCourses) {
            courseHTML += `
                <div class="course-item" data-course-id="${course.id}" 
                     style="background: var(--card-bg); border: 1px solid var(--border-color); 
                            border-radius: 8px; padding: 1rem; margin-bottom: 0.5rem; cursor: pointer;">
                    <div style="display: flex; align-items: start;">
                        <input type="checkbox" class="course-checkbox" value="${course.id}" 
                               id="course-${course.id}" style="margin-right: 1rem; margin-top: 0.25rem;">
                        <div style="flex: 1;">
                            <label for="course-${course.id}" style="cursor: pointer;">
                                <strong>${course.id}: ${course.name}</strong>
                                <span class="badge" style="margin-left: 0.5rem; background: var(--secondary-bg);">${course.credits} credits</span>
                            </label>
                            <p style="margin: 0.5rem 0; color: var(--text-secondary);">${course.description}</p>
                            ${course.prerequisites.length > 0 ? 
                                `<small style="color: var(--warning-color);">Prerequisites: ${course.prerequisites.join(', ')}</small>` : 
                                '<small style="color: var(--success-color);">No prerequisites</small>'}
                        </div>
                    </div>
                    <button class="btn btn-sm" style="margin-top: 0.5rem; background: var(--primary-accent); color: white;" 
                            onclick="showCourseDetails('${selectedMajor}', '${course.id}')">
                        View Syllabus
                    </button>
                </div>
            `;
        }
    } else {
        courseHTML += '<p>No courses available. Please ensure the backend is running.</p>';
    }
    
    courseHTML += `
            </div>
            <div style="margin-top: 1rem; padding: 1rem; background: var(--secondary-bg); border-radius: 8px;">
                <strong>Selected Courses: <span id="selected-count">0</span></strong>
                <div id="selected-list" style="margin-top: 0.5rem;"></div>
            </div>
        </div>
    `;
    
    careerGrid.innerHTML = courseHTML;
    
    // Add event listeners for course selection
    document.querySelectorAll('.course-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', updateSelectedCourses);
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

function updateSelectedCourses() {
    selectedCourses = [];
    document.querySelectorAll('.course-checkbox:checked').forEach(checkbox => {
        selectedCourses.push(checkbox.value);
    });
    
    document.getElementById('selected-count').textContent = selectedCourses.length;
    
    const selectedList = document.getElementById('selected-list');
    if (selectedCourses.length > 0) {
        selectedList.innerHTML = selectedCourses.map(id => {
            const course = availableCourses.find(c => c.id === id);
            return `<span class="badge" style="background: var(--primary-accent); color: white; margin: 0.25rem;">${course ? course.name : id}</span>`;
        }).join('');
        
        // Enable next button
        const nextBtn = document.getElementById('next-btn');
        if (nextBtn) {
            nextBtn.disabled = false;
            nextBtn.style.opacity = '1';
        }
    } else {
        selectedList.innerHTML = '<span style="color: var(--text-secondary);">No courses selected</span>';
        
        // Disable next button
        const nextBtn = document.getElementById('next-btn');
        if (nextBtn) {
            nextBtn.disabled = true;
            nextBtn.style.opacity = '0.5';
        }
    }
}

async function showCourseDetails(major, courseId) {
    console.log('Fetching details for course:', courseId);
    
    try {
        const response = await fetch(`${API_BASE_URL}/courses/major/${major}/course/${courseId}`);
        if (!response.ok) throw new Error('Failed to fetch course details');
        
        const details = await response.json();
        
        // Create modal
        const modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.8); display: flex; align-items: center;
            justify-content: center; z-index: 9999;
        `;
        
        modal.innerHTML = `
            <div style="background: var(--card-bg); border-radius: 12px; max-width: 800px; 
                        width: 90%; max-height: 90vh; overflow: hidden; display: flex; flex-direction: column;">
                <div style="padding: 1.5rem; border-bottom: 1px solid var(--border-color); 
                            display: flex; justify-content: space-between; align-items: center;">
                    <h3>${details.id}: ${details.name}</h3>
                    <button onclick="this.closest('div').parentElement.remove()" 
                            style="background: none; border: none; font-size: 1.5rem; cursor: pointer;">&times;</button>
                </div>
                <div style="padding: 1.5rem; overflow-y: auto; flex: 1;">
                    <h4>Learning Objectives:</h4>
                    <ul>${details.syllabus.objectives.map(obj => `<li>${obj}</li>`).join('')}</ul>
                    
                    <h4>Weekly Topics:</h4>
                    ${details.syllabus.topics.map(topic => `
                        <div style="margin-bottom: 0.5rem; padding: 0.5rem; background: var(--secondary-bg); border-radius: 8px;">
                            <strong>Week ${topic.week}:</strong> ${topic.topic}
                            <p style="margin: 0.25rem 0 0 0; color: var(--text-secondary);">${topic.content}</p>
                        </div>
                    `).join('')}
                    
                    <h4>Assessment:</h4>
                    <ul>${details.syllabus.assessments.map(a => 
                        `<li>${a.type}: ${a.weight} - ${a.description}</li>`
                    ).join('')}</ul>
                    
                    <h4>Textbooks:</h4>
                    <ul>${details.syllabus.textbooks.map(book => `<li>${book}</li>`).join('')}</ul>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        modal.addEventListener('click', function(e) {
            if (e.target === modal) modal.remove();
        });
        
    } catch (error) {
        console.error('Error fetching course details:', error);
        alert('Could not load course details. Please ensure the backend is running.');
    }
}

function handleNext() {
    console.log('Next clicked, current step:', currentStep);
    
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
        // Show preferences (step 4 already exists in HTML)
    } else if (currentStep === 4) {
        currentStep = 5;
        showStep(5);
        generateRoadmap();
    }
}

function handlePrevious() {
    console.log('Previous clicked, current step:', currentStep);
    
    if (currentStep > 1) {
        currentStep--;
        showStep(currentStep);
        
        if (currentStep === 2) {
            showMajors();
        } else if (currentStep === 3) {
            showCourses();
        }
    }
}

function showStep(step) {
    console.log('Showing step:', step);
    
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
    
    // Update progress indicators
    updateProgress(step);
    
    // Update navigation buttons
    updateNavButtons(step);
}

function updateProgress(step) {
    // Update progress steps (the HTML uses progress-step class)
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
            // Don't disable here - let selection handlers control it
        }
    }
}

async function generateRoadmap() {
    console.log('Generating roadmap...');
    
    // Collect preferences
    userPreferences = {
        field: selectedCategory,
        major: selectedMajor,
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
        <div style="text-align: center; padding: 2rem;">
            <div class="spinner" style="border: 4px solid var(--border-color); border-top: 4px solid var(--primary-accent); 
                                        border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; 
                                        margin: 0 auto;"></div>
            <p style="margin-top: 1rem;">Generating your personalized roadmap with selected courses...</p>
        </div>
    `;
    
    // Add spinner animation if not exists
    if (!document.querySelector('#spinner-style')) {
        const style = document.createElement('style');
        style.id = 'spinner-style';
        style.textContent = '@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }';
        document.head.appendChild(style);
    }
    
    // Try to fetch roadmap from backend
    let roadmap = null;
    try {
        const response = await fetch(`${API_BASE_URL}/courses/major/${selectedMajor}/roadmap`);
        if (response.ok) {
            roadmap = await response.json();
        }
    } catch (error) {
        console.error('Error fetching roadmap:', error);
    }
    
    // Display roadmap after delay
    setTimeout(() => {
        displayRoadmap(roadmap);
    }, 1500);
}

function displayRoadmap(roadmap) {
    const roadmapResult = document.getElementById('roadmap-result');
    
    let html = `
        <div style="padding: 2rem;">
            <h3 style="margin-bottom: 1rem;">Your Personalized Learning Path</h3>
            <div style="margin-bottom: 1.5rem; padding: 1rem; background: var(--secondary-bg); border-radius: 8px;">
                <strong>Major:</strong> ${selectedMajor.toUpperCase()} | 
                <strong>Selected Courses:</strong> ${selectedCourses.length} | 
                <strong>Study Hours:</strong> ${userPreferences.hours} hrs/week
            </div>
    `;
    
    if (roadmap && roadmap.roadmap) {
        // Display semester-based roadmap from backend
        for (const semester of roadmap.roadmap) {
            const semesterCourses = semester.courses.filter(id => 
                selectedCourses.includes(id) || semester.semester === 1
            );
            
            if (semesterCourses.length > 0) {
                html += `
                    <div style="margin-bottom: 1.5rem; padding: 1.5rem; background: var(--card-bg); 
                                border-radius: 12px; border: 1px solid var(--border-color);">
                        <h4 style="margin-bottom: 1rem;">Semester ${semester.semester}</h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                `;
                
                for (const courseId of semesterCourses) {
                    const course = availableCourses.find(c => c.id === courseId);
                    const isSelected = selectedCourses.includes(courseId);
                    
                    html += `
                        <div style="padding: 1rem; background: ${isSelected ? 'linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)' : 'var(--secondary-bg)'}; 
                                    border-radius: 8px; border: 1px solid ${isSelected ? 'var(--primary-accent)' : 'var(--border-color)'};">
                            <h5 style="margin: 0 0 0.5rem 0;">${courseId}</h5>
                            <p style="margin: 0; font-size: 0.9rem; color: var(--text-secondary);">
                                ${course ? course.name : 'Course Details'}
                            </p>
                            ${isSelected ? '<span class="badge" style="background: var(--primary-accent); color: white; margin-top: 0.5rem; display: inline-block;">Selected</span>' : ''}
                        </div>
                    `;
                }
                
                html += `
                        </div>
                    </div>
                `;
            }
        }
    } else {
        // Fallback display if no roadmap from backend
        html += `
            <div style="padding: 1.5rem; background: var(--card-bg); border-radius: 12px; border: 1px solid var(--border-color);">
                <h4>Your Selected Courses</h4>
                <div style="margin-top: 1rem;">
        `;
        
        for (const courseId of selectedCourses) {
            const course = availableCourses.find(c => c.id === courseId);
            html += `
                <div style="margin-bottom: 0.5rem; padding: 0.75rem; background: var(--secondary-bg); border-radius: 8px;">
                    <strong>${courseId}:</strong> ${course ? course.name : 'Course'}
                    ${course && course.prerequisites.length > 0 ? 
                        `<br><small style="color: var(--text-secondary);">Prerequisites: ${course.prerequisites.join(', ')}</small>` : ''}
                </div>
            `;
        }
        
        html += `
                </div>
            </div>
        `;
    }
    
    html += `
            <div style="margin-top: 2rem; display: flex; gap: 1rem;">
                <button class="btn btn-primary" onclick="alert('Roadmap saved! You can access it from your dashboard.')">
                    Save Roadmap
                </button>
                <button class="btn btn-secondary" onclick="location.reload()">
                    Start Over
                </button>
            </div>
        </div>
    `;
    
    roadmapResult.innerHTML = html;
}

// Make functions globally available
window.showCourseDetails = showCourseDetails;