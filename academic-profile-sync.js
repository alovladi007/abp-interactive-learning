// Academic Profile Synchronization System
// This manages the connection between AI Path Advisor and Academic Setup

class AcademicProfileManager {
    constructor() {
        this.profile = this.loadProfile() || this.getDefaultProfile();
        this.initializeEventListeners();
    }

    getDefaultProfile() {
        return {
            educationLevel: 'undergraduate',
            currentLevel: 'Undergraduate',
            activeCourses: 0,
            primaryField: null,
            primaryMajor: null,
            careerPath: null,
            gpa: null,
            fields: [],
            courses: [],
            studyHours: 15,
            budget: '0',
            learningStyle: 'mixed',
            experienceLevel: 'beginner',
            lastUpdated: new Date().toISOString()
        };
    }

    loadProfile() {
        const stored = localStorage.getItem('academicProfile');
        return stored ? JSON.parse(stored) : null;
    }

    saveProfile() {
        localStorage.setItem('academicProfile', JSON.stringify(this.profile));
        this.updateUI();
    }

    updateFromPathAdvisor(data) {
        // Update profile with AI Path Advisor selections
        this.profile.primaryField = data.field;
        this.profile.primaryMajor = data.major;
        this.profile.careerPath = data.career;
        this.profile.studyHours = data.hours;
        this.profile.budget = data.budget;
        this.profile.learningStyle = data.style;
        this.profile.experienceLevel = data.level;
        this.profile.lastUpdated = new Date().toISOString();
        
        // Add the selected field if not already present
        if (data.fieldName && !this.profile.fields.includes(data.fieldName)) {
            this.profile.fields.push(data.fieldName);
        }
        
        // Update active courses count based on study hours
        this.profile.activeCourses = Math.min(5, Math.floor(parseInt(data.hours) / 5));
        
        this.saveProfile();
        this.syncToAcademicSetup();
    }

    syncToAcademicSetup() {
        // Update Academic Setup page if it exists
        if (window.location.pathname.includes('academic-setup.html')) {
            this.updateAcademicSetupUI();
        }
    }

    updateAcademicSetupUI() {
        // Update the header stats
        const statsElements = {
            level: document.querySelector('.stat-value.level'),
            courses: document.querySelector('.stat-value.courses'),
            field: document.querySelector('.stat-value.field'),
            gpa: document.querySelector('.stat-value.gpa')
        };

        if (statsElements.level) {
            statsElements.level.textContent = this.profile.currentLevel;
        }
        if (statsElements.courses) {
            statsElements.courses.textContent = this.profile.activeCourses;
        }
        if (statsElements.field && this.profile.primaryMajor) {
            const majorName = this.getMajorDisplayName(this.profile.primaryMajor);
            statsElements.field.textContent = majorName;
        }
        if (statsElements.gpa && this.profile.gpa) {
            statsElements.gpa.textContent = this.profile.gpa;
        }

        // Check the appropriate field checkboxes
        this.updateFieldCheckboxes();
        
        // Update suggested courses based on career path
        this.updateSuggestedCourses();
    }

    getMajorDisplayName(majorId) {
        const majorNames = {
            'cs': 'Computer Science',
            'data-science': 'Data Science',
            'ee': 'Electrical Engineering',
            'me': 'Mechanical Engineering',
            'civil': 'Civil Engineering',
            'chemeng': 'Chemical Engineering',
            'bme': 'Biomedical Engineering',
            'physics': 'Physics',
            'chemistry': 'Chemistry',
            'materials': 'Materials Science',
            'environment': 'Environmental Science',
            'medicine': 'Medicine',
            'nursing': 'Nursing',
            'pharmacy': 'Pharmacy',
            'public-health': 'Public Health',
            'nutrition': 'Nutrition',
            'economics': 'Economics',
            'finance': 'Finance',
            'policy': 'Political Science',
            'education': 'Education',
            'psychology': 'Psychology',
            'architecture': 'Architecture',
            'communications': 'Communications',
            'law': 'Law',
            'criminal-justice': 'Criminal Justice'
        };
        return majorNames[majorId] || majorId;
    }

    updateFieldCheckboxes() {
        // Map majors to field checkboxes
        const fieldMappings = {
            'cs': 'cs',
            'data-science': 'data-science',
            'ee': 'electrical',
            'me': 'mechanical',
            'bme': 'biomedical',
            'civil': 'civil',
            'chemeng': 'chemical'
        };

        const fieldValue = fieldMappings[this.profile.primaryMajor];
        if (fieldValue) {
            const checkbox = document.querySelector(`input[name="field"][value="${fieldValue}"]`);
            if (checkbox) {
                checkbox.checked = true;
            }
        }
    }

    updateSuggestedCourses() {
        // Generate suggested courses based on career path
        const courseSuggestions = this.getCourseSuggestions();
        
        // Add to current courses section if needed
        const coursesContainer = document.querySelector('.courses-list');
        if (coursesContainer && courseSuggestions.length > 0) {
            // Add suggested courses indicator
            this.addSuggestedCoursesSection(coursesContainer, courseSuggestions);
        }
    }

    getCourseSuggestions() {
        const suggestions = {
            'ml-engineer': [
                { code: 'CS 4780', name: 'Machine Learning', credits: 3 },
                { code: 'CS 5785', name: 'Deep Learning', credits: 3 },
                { code: 'MATH 4710', name: 'Probability Theory', credits: 4 }
            ],
            'full-stack': [
                { code: 'CS 3110', name: 'Web Development', credits: 3 },
                { code: 'CS 4320', name: 'Database Systems', credits: 3 },
                { code: 'CS 5150', name: 'Software Engineering', credits: 4 }
            ],
            'data-engineer': [
                { code: 'CS 4320', name: 'Database Systems', credits: 3 },
                { code: 'CS 5777', name: 'Big Data Technologies', credits: 3 },
                { code: 'CS 4786', name: 'Data Mining', credits: 3 }
            ]
        };
        
        return suggestions[this.profile.careerPath] || [];
    }

    addSuggestedCoursesSection(container, suggestions) {
        // Check if suggestions section already exists
        let suggestionsDiv = document.getElementById('suggested-courses');
        if (!suggestionsDiv) {
            suggestionsDiv = document.createElement('div');
            suggestionsDiv.id = 'suggested-courses';
            suggestionsDiv.className = 'suggested-courses-section';
            suggestionsDiv.innerHTML = `
                <div style="margin-top: 2rem; padding: 1.5rem; background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); border-radius: 12px;">
                    <h4 style="margin: 0 0 1rem 0; color: var(--text-primary);">
                        <i class="fas fa-lightbulb" style="color: var(--primary-accent); margin-right: 0.5rem;"></i>
                        Suggested Courses for ${this.getCareerPathName()}
                    </h4>
                    <div class="suggested-courses-list">
                        ${suggestions.map(course => `
                            <div class="suggested-course-item" style="background: white; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <strong>${course.name}</strong>
                                    <span class="text-secondary" style="margin-left: 1rem;">${course.code} • ${course.credits} Credits</span>
                                </div>
                                <button class="btn btn-sm btn-primary" onclick="academicProfile.addCourse('${course.code}', '${course.name}', ${course.credits})">
                                    <i class="fas fa-plus"></i> Add
                                </button>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
            container.parentElement.appendChild(suggestionsDiv);
        }
    }

    getCareerPathName() {
        const careerNames = {
            'ml-engineer': 'Machine Learning Engineer',
            'full-stack': 'Full Stack Developer',
            'data-engineer': 'Data Engineer',
            'embedded': 'Embedded Systems Engineer',
            'pre-med': 'Pre-Medical Track'
        };
        return careerNames[this.profile.careerPath] || 'Your Career Path';
    }

    addCourse(code, name, credits) {
        const course = {
            id: Date.now(),
            code: code,
            name: name,
            credits: credits,
            semester: 'Spring 2025',
            status: 'planned'
        };
        
        this.profile.courses.push(course);
        this.profile.activeCourses++;
        this.saveProfile();
        
        // Refresh the page to show the new course
        location.reload();
    }

    initializeEventListeners() {
        // Listen for updates from AI Path Advisor
        window.addEventListener('pathAdvisorComplete', (event) => {
            this.updateFromPathAdvisor(event.detail);
        });

        // Listen for profile updates
        window.addEventListener('storage', (event) => {
            if (event.key === 'academicProfile') {
                this.profile = JSON.parse(event.newValue);
                this.updateUI();
            }
        });
    }

    updateUI() {
        // Update any UI elements that depend on the profile
        const profileDisplay = document.getElementById('profile-display');
        if (profileDisplay) {
            profileDisplay.innerHTML = this.renderProfileSummary();
        }
    }

    renderProfileSummary() {
        return `
            <div class="profile-summary">
                <h4>Your Academic Profile</h4>
                <p><strong>Major:</strong> ${this.getMajorDisplayName(this.profile.primaryMajor)}</p>
                <p><strong>Career Path:</strong> ${this.getCareerPathName()}</p>
                <p><strong>Study Hours:</strong> ${this.profile.studyHours} hours/week</p>
                <p><strong>Learning Style:</strong> ${this.profile.learningStyle}</p>
            </div>
        `;
    }
}

// Initialize the profile manager
const academicProfile = new AcademicProfileManager();

// Export for use in other scripts
window.academicProfile = academicProfile;