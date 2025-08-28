// Academic API Client - Connects frontend to backend API
class AcademicAPIClient {
    constructor() {
        this.baseURL = 'http://localhost:8001';  // Update this to your backend URL
        this.userId = this.getUserId();
    }

    getUserId() {
        // Get or create user ID (in production, this would come from authentication)
        let userId = localStorage.getItem('userId');
        if (!userId) {
            userId = 'user_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('userId', userId);
        }
        return userId;
    }

    async fetchAPI(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            }
        };

        try {
            const response = await fetch(url, { ...defaultOptions, ...options });
            if (!response.ok) {
                throw new Error(`API Error: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API Request failed:', error);
            // Fall back to local storage if API is unavailable
            return null;
        }
    }

    // Profile methods
    async getProfile() {
        const profile = await this.fetchAPI(`/profile/${this.userId}`);
        if (profile) {
            // Store locally as backup
            localStorage.setItem('academicProfile', JSON.stringify(profile));
        }
        return profile;
    }

    async updateProfile(updates) {
        const profile = await this.fetchAPI(`/profile/${this.userId}/update`, {
            method: 'POST',
            body: JSON.stringify(updates)
        });
        if (profile) {
            localStorage.setItem('academicProfile', JSON.stringify(profile));
        }
        return profile;
    }

    async syncPathAdvisor(data) {
        const profile = await this.fetchAPI(`/profile/${this.userId}/sync-path-advisor`, {
            method: 'POST',
            body: JSON.stringify(data)
        });
        if (profile) {
            localStorage.setItem('academicProfile', JSON.stringify(profile));
            // Trigger UI updates
            this.updateUIFromProfile(profile);
        }
        return profile;
    }

    // Course methods
    async getCourses() {
        return await this.fetchAPI(`/profile/${this.userId}/courses`);
    }

    async addCourse(course) {
        return await this.fetchAPI(`/profile/${this.userId}/courses/add`, {
            method: 'POST',
            body: JSON.stringify(course)
        });
    }

    async removeCourse(courseCode) {
        return await this.fetchAPI(`/profile/${this.userId}/courses/${courseCode}`, {
            method: 'DELETE'
        });
    }

    async getSuggestedCourses() {
        return await this.fetchAPI(`/profile/${this.userId}/suggested-courses`);
    }

    async calculateGPA() {
        return await this.fetchAPI(`/profile/${this.userId}/calculate-gpa`, {
            method: 'POST'
        });
    }

    // UI Update methods
    updateUIFromProfile(profile) {
        // Update Academic Setup page if we're on it
        if (window.location.pathname.includes('academic-setup.html')) {
            this.updateAcademicSetupUI(profile);
        }
    }

    updateAcademicSetupUI(profile) {
        // Update stats
        const updates = {
            'stat-level': profile.current_level,
            'stat-courses': profile.active_courses,
            'stat-field': this.getMajorDisplayName(profile.primary_major),
            'stat-gpa': profile.gpa || '3.8'
        };

        for (const [id, value] of Object.entries(updates)) {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value;
            }
        }

        // Show career path badge
        if (profile.career_path) {
            const careerBadge = document.getElementById('career-badge');
            const careerText = document.getElementById('career-text');
            if (careerBadge && careerText) {
                careerText.textContent = this.getCareerPathName(profile.career_path);
                careerBadge.style.display = 'block';
            }
        }

        // Display suggested courses
        this.displaySuggestedCourses();
    }

    async displaySuggestedCourses() {
        const suggestions = await this.getSuggestedCourses();
        if (!suggestions || suggestions.length === 0) return;

        const container = document.querySelector('.section-card:nth-of-type(4)');
        if (!container || document.getElementById('api-suggested-courses')) return;

        const suggestionsHTML = `
            <div id="api-suggested-courses" style="margin-top: 2rem; padding: 1.5rem; background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); border-radius: 12px;">
                <h4 style="margin: 0 0 1rem 0; color: var(--text-primary);">
                    <i class="fas fa-lightbulb" style="color: var(--primary-accent); margin-right: 0.5rem;"></i>
                    AI-Recommended Courses for Your Path
                </h4>
                <div class="suggested-courses-list">
                    ${suggestions.map(course => `
                        <div class="suggested-course-item" style="background: white; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <strong>${course.name}</strong>
                                    <span class="text-secondary" style="margin-left: 1rem;">${course.code} • ${course.credits} Credits</span>
                                    <div style="margin-top: 0.25rem;">
                                        <span class="badge" style="background: ${this.getPriorityColor(course.priority)}; color: white; font-size: 0.75rem;">
                                            ${this.getPriorityLabel(course.priority)} Priority
                                        </span>
                                        <span class="text-secondary" style="margin-left: 0.5rem; font-size: 0.85rem;">
                                            ${course.reason}
                                        </span>
                                    </div>
                                </div>
                                <button class="btn btn-sm btn-primary" onclick="apiClient.addCourseFromSuggestion('${course.code}', '${course.name}', ${course.credits})">
                                    <i class="fas fa-plus"></i> Add
                                </button>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;

        container.insertAdjacentHTML('afterend', suggestionsHTML);
    }

    async addCourseFromSuggestion(code, name, credits) {
        const course = {
            id: Date.now().toString(),
            code: code,
            name: name,
            credits: credits,
            semester: 'Spring 2025',
            status: 'planned'
        };

        const result = await this.addCourse(course);
        if (result) {
            // Show success message
            alert(`Successfully added ${name} to your courses!`);
            // Reload to show updated courses
            location.reload();
        }
    }

    getPriorityColor(priority) {
        switch(priority) {
            case 1: return '#dc3545';  // Red for high
            case 2: return '#ffc107';  // Yellow for medium
            case 3: return '#28a745';  // Green for low
            default: return '#6c757d'; // Gray
        }
    }

    getPriorityLabel(priority) {
        switch(priority) {
            case 1: return 'High';
            case 2: return 'Medium';
            case 3: return 'Low';
            default: return 'Normal';
        }
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

    getCareerPathName(careerPath) {
        const careerNames = {
            'ml-engineer': 'Machine Learning Engineer',
            'full-stack': 'Full Stack Developer',
            'data-engineer': 'Data Engineer',
            'embedded': 'Embedded Systems Engineer',
            'pre-med': 'Pre-Medical Track',
            'full-cs': 'Full Computer Science Degree',
            'data-scientist': 'Data Scientist',
            'full-ee': 'Full Electrical Engineering'
        };
        return careerNames[careerPath] || careerPath;
    }
}

// Initialize API client
const apiClient = new AcademicAPIClient();

// Make it globally available
window.apiClient = apiClient;

// Auto-load profile on page load
document.addEventListener('DOMContentLoaded', async () => {
    // Try to connect to backend
    const profile = await apiClient.getProfile();
    if (profile) {
        console.log('Connected to backend API, profile loaded:', profile);
        apiClient.updateUIFromProfile(profile);
    } else {
        console.log('Running in offline mode with local storage');
    }
});