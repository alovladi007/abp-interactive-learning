// AI Path Advisor JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // State management
    const pathAdvisorState = {
        currentStep: 1,
        selectedGoal: null,
        userProfile: {
            goal: '',
            currentLevel: {},
            constraints: {},
            skills: [],
            weeklyHours: 15,
            budget: 100,
            timeHorizon: 12
        },
        generatedRoadmap: null
    };

    // Skill Graph Data Structure
    const skillGraph = {
        // Computer Science Skills
        'cs.programming.basics': {
            name: 'Programming Fundamentals',
            prereqs: [],
            difficulty: 1,
            hours: 40
        },
        'cs.programming.python': {
            name: 'Python Programming',
            prereqs: ['cs.programming.basics'],
            difficulty: 2,
            hours: 60
        },
        'cs.ds.algorithms': {
            name: 'Data Structures & Algorithms',
            prereqs: ['cs.programming.python'],
            difficulty: 4,
            hours: 120
        },
        'math.linear_algebra': {
            name: 'Linear Algebra',
            prereqs: ['math.calculus_1'],
            difficulty: 3,
            hours: 80
        },
        'math.calculus_1': {
            name: 'Calculus I',
            prereqs: [],
            difficulty: 3,
            hours: 60
        },
        'math.statistics': {
            name: 'Statistics & Probability',
            prereqs: ['math.calculus_1'],
            difficulty: 3,
            hours: 60
        },
        'ml.fundamentals': {
            name: 'Machine Learning Fundamentals',
            prereqs: ['cs.programming.python', 'math.linear_algebra', 'math.statistics'],
            difficulty: 4,
            hours: 100
        },
        'ml.deep_learning': {
            name: 'Deep Learning',
            prereqs: ['ml.fundamentals'],
            difficulty: 5,
            hours: 120
        },
        'ml.mlops': {
            name: 'MLOps & Production',
            prereqs: ['ml.fundamentals', 'cs.systems.docker'],
            difficulty: 4,
            hours: 80
        },
        'cs.systems.docker': {
            name: 'Docker & Containerization',
            prereqs: ['cs.programming.basics'],
            difficulty: 3,
            hours: 40
        }
    };

    // Resource Catalog
    const resourceCatalog = {
        'book.strang.la': {
            type: 'book',
            title: 'Linear Algebra - Gilbert Strang',
            skills: ['math.linear_algebra'],
            hours: 80,
            cost: 0,
            quality: 9.5,
            format: ['text', 'problems']
        },
        'course.3blue1brown.la': {
            type: 'video',
            title: '3Blue1Brown - Essence of Linear Algebra',
            skills: ['math.linear_algebra'],
            hours: 10,
            cost: 0,
            quality: 9.8,
            format: ['video', 'visual']
        },
        'book.clrs': {
            type: 'book',
            title: 'Introduction to Algorithms (CLRS)',
            skills: ['cs.ds.algorithms'],
            hours: 120,
            cost: 60,
            quality: 9.6,
            format: ['text', 'problems']
        },
        'course.cs50': {
            type: 'course',
            title: 'Harvard CS50',
            skills: ['cs.programming.basics'],
            hours: 100,
            cost: 0,
            quality: 9.7,
            format: ['video', 'projects']
        },
        'book.islr': {
            type: 'book',
            title: 'Introduction to Statistical Learning',
            skills: ['ml.fundamentals'],
            hours: 80,
            cost: 0,
            quality: 9.4,
            format: ['text', 'R-code']
        },
        'course.fast.ai': {
            type: 'course',
            title: 'Fast.ai Practical Deep Learning',
            skills: ['ml.deep_learning'],
            hours: 60,
            cost: 0,
            quality: 9.3,
            format: ['video', 'notebooks']
        }
    };

    // Career Path Templates
    const careerPaths = {
        'ml-engineer': {
            name: 'Machine Learning Engineer',
            targetSkills: ['ml.fundamentals', 'ml.deep_learning', 'ml.mlops'],
            duration: 12,
            description: 'Master ML algorithms, deep learning, and production deployment'
        },
        'embedded-engineer': {
            name: 'Embedded Systems Engineer',
            targetSkills: ['cs.programming.c', 'ee.digital', 'ee.embedded'],
            duration: 10,
            description: 'Firmware development, RTOS, and hardware interfacing'
        },
        'data-engineer': {
            name: 'Data Engineer',
            targetSkills: ['cs.databases', 'cs.distributed', 'cs.streaming'],
            duration: 8,
            description: 'ETL pipelines, data warehousing, and streaming systems'
        },
        'full-stack': {
            name: 'Full Stack Developer',
            targetSkills: ['cs.web.frontend', 'cs.web.backend', 'cs.databases'],
            duration: 6,
            description: 'Frontend, backend, databases, and DevOps'
        }
    };

    // Initialize event handlers
    window.nextStep = function() {
        if (pathAdvisorState.currentStep < 5) {
            // Validate current step
            if (pathAdvisorState.currentStep === 1 && !pathAdvisorState.selectedGoal) {
                showNotification('Please select a learning goal', 'warning');
                return;
            }

            pathAdvisorState.currentStep++;
            updateWizardDisplay();
        }
    };

    window.previousStep = function() {
        if (pathAdvisorState.currentStep > 1) {
            pathAdvisorState.currentStep--;
            updateWizardDisplay();
        }
    };

    window.generateRoadmap = function() {
        showNotification('Generating your personalized roadmap...', 'info');
        
        // Simulate AI processing
        setTimeout(() => {
            const roadmap = planLearningPath(
                pathAdvisorState.selectedGoal,
                pathAdvisorState.userProfile
            );
            
            pathAdvisorState.generatedRoadmap = roadmap;
            pathAdvisorState.currentStep = 4;
            updateWizardDisplay();
            showNotification('Roadmap generated successfully!', 'success');
        }, 2000);
    };

    window.startLearning = function() {
        pathAdvisorState.currentStep = 5;
        updateWizardDisplay();
        showNotification('Welcome to your learning journey!', 'success');
        
        // Save roadmap to user profile
        saveUserRoadmap(pathAdvisorState.generatedRoadmap);
    };

    window.showCustomGoal = function() {
        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.innerHTML = `
            <div class="modal-content" style="max-width: 500px;">
                <h2>Define Custom Goal</h2>
                <textarea placeholder="Describe your learning goal..." 
                          style="width: 100%; height: 100px; margin: 1rem 0;"></textarea>
                <div style="display: flex; gap: 1rem; justify-content: flex-end;">
                    <button class="btn btn-outline" onclick="this.closest('.modal-overlay').remove()">Cancel</button>
                    <button class="btn btn-primary">Create Goal</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    };

    // Path Planning Algorithm
    function planLearningPath(goalId, profile) {
        const goal = careerPaths[goalId];
        if (!goal) return null;

        const path = [];
        const visited = new Set();
        const targetSkills = goal.targetSkills;

        // Topological sort with prerequisites
        function addSkillToPath(skillId) {
            if (visited.has(skillId)) return;
            
            const skill = skillGraph[skillId];
            if (!skill) return;

            // Add prerequisites first
            skill.prereqs.forEach(prereq => {
                addSkillToPath(prereq);
            });

            // Add current skill if not already mastered
            if (!profile.skills.includes(skillId)) {
                path.push({
                    skillId: skillId,
                    skill: skill,
                    resources: selectBestResources(skillId, profile)
                });
            }
            
            visited.add(skillId);
        }

        // Build path for all target skills
        targetSkills.forEach(skill => {
            addSkillToPath(skill);
        });

        // Convert to weekly schedule
        return schedulePathToWeeks(path, profile.weeklyHours);
    }

    // Resource Selection Algorithm
    function selectBestResources(skillId, profile) {
        const candidates = Object.entries(resourceCatalog)
            .filter(([id, resource]) => resource.skills.includes(skillId));

        // Score resources based on quality, cost, and learning style
        const scored = candidates.map(([id, resource]) => {
            let score = resource.quality * 10;
            
            // Adjust for budget
            if (resource.cost > profile.budget) {
                score -= 50;
            } else if (resource.cost === 0) {
                score += 10;
            }

            // Adjust for learning style
            if (profile.learningStyle === 'visual' && resource.format.includes('video')) {
                score += 15;
            } else if (profile.learningStyle === 'hands-on' && resource.format.includes('projects')) {
                score += 15;
            }

            return { id, resource, score };
        });

        // Sort by score and return top 2
        scored.sort((a, b) => b.score - a.score);
        return scored.slice(0, 2).map(item => item.id);
    }

    // Schedule modules into weeks
    function schedulePathToWeeks(path, weeklyHours) {
        const schedule = {
            modules: [],
            totalWeeks: 0,
            milestones: []
        };

        let currentWeek = 1;

        path.forEach((item, index) => {
            const weeksNeeded = Math.ceil(item.skill.hours / weeklyHours);
            
            schedule.modules.push({
                skillId: item.skillId,
                name: item.skill.name,
                startWeek: currentWeek,
                endWeek: currentWeek + weeksNeeded - 1,
                resources: item.resources,
                assessments: generateAssessments(item.skillId)
            });

            // Add milestone every 4 modules
            if ((index + 1) % 4 === 0) {
                schedule.milestones.push({
                    week: currentWeek + weeksNeeded - 1,
                    name: `Checkpoint ${Math.floor(index / 4) + 1}`
                });
            }

            currentWeek += weeksNeeded;
        });

        schedule.totalWeeks = currentWeek - 1;
        return schedule;
    }

    // Generate assessments for a skill
    function generateAssessments(skillId) {
        return [
            { type: 'quiz', name: 'Concept Check', questions: 20 },
            { type: 'project', name: 'Hands-on Project' },
            { type: 'problems', name: 'Problem Set', count: 10 }
        ];
    }

    // Update wizard display
    function updateWizardDisplay() {
        // Update step indicators
        document.querySelectorAll('.wizard-step').forEach((step, index) => {
            step.classList.remove('active', 'completed');
            if (index + 1 < pathAdvisorState.currentStep) {
                step.classList.add('completed');
            } else if (index + 1 === pathAdvisorState.currentStep) {
                step.classList.add('active');
            }
        });

        // Show/hide content sections
        document.querySelectorAll('.wizard-content').forEach((content, index) => {
            content.style.display = (index + 1 === pathAdvisorState.currentStep) ? 'block' : 'none';
        });

        // Update progress if on step 5
        if (pathAdvisorState.currentStep === 5) {
            startProgressTracking();
        }
    }

    // Goal card selection
    document.querySelectorAll('.goal-card').forEach(card => {
        card.addEventListener('click', function() {
            document.querySelectorAll('.goal-card').forEach(c => c.classList.remove('selected'));
            this.classList.add('selected');
            pathAdvisorState.selectedGoal = this.dataset.goal;
            pathAdvisorState.userProfile.goal = careerPaths[this.dataset.goal].name;
        });
    });

    // Weekly hours slider
    const hoursSlider = document.getElementById('weekly-hours');
    if (hoursSlider) {
        hoursSlider.addEventListener('input', function() {
            document.getElementById('hours-display').textContent = `${this.value} hours/week`;
            pathAdvisorState.userProfile.weeklyHours = parseInt(this.value);
        });
    }

    // Progress tracking
    function startProgressTracking() {
        // Update progress every 5 seconds (in real app, this would be based on actual learning activity)
        setInterval(() => {
            updateLearningProgress();
        }, 5000);
    }

    function updateLearningProgress() {
        // Simulate progress updates
        const progressBar = document.querySelector('.progress-bar > div');
        if (progressBar) {
            const currentWidth = parseFloat(progressBar.style.width) || 15;
            if (currentWidth < 100) {
                progressBar.style.width = (currentWidth + 0.5) + '%';
            }
        }
    }

    // Save roadmap to user profile
    function saveUserRoadmap(roadmap) {
        // In a real app, this would save to backend
        localStorage.setItem('userRoadmap', JSON.stringify(roadmap));
        console.log('Roadmap saved:', roadmap);
    }

    // Notification helper
    function showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            background: ${type === 'success' ? 'var(--success-color)' : type === 'warning' ? 'var(--warning-color)' : 'var(--primary-accent)'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: var(--shadow-lg);
            z-index: 10000;
            animation: slideIn 0.3s ease;
        `;
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    // Add animation styles
    if (!document.getElementById('path-advisor-animations')) {
        const style = document.createElement('style');
        style.id = 'path-advisor-animations';
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slideOut {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
            .modal-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.7);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10000;
                animation: fadeIn 0.3s ease;
            }
            .modal-content {
                background: var(--card-bg);
                border-radius: 12px;
                padding: 2rem;
                box-shadow: var(--shadow-xl);
                animation: slideUp 0.3s ease;
            }
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            @keyframes slideUp {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
    }

    console.log('AI Path Advisor initialized successfully!');
});