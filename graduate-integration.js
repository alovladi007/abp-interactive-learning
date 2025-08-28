// Graduate and Professional Programs Integration for AI Path Advisor
// This file extends the existing path advisor with graduate/professional options

// Add to the existing path advisor after loading
function integrateGraduatePrograms() {
    // Add program level selection before field selection
    addProgramLevelStep();
    
    // Extend categories with graduate options
    extendCategoriesWithGraduate();
    
    // Add graduate-specific course mappings
    addGraduateCourseMappings();
}

// Add program level as new first step
function addProgramLevelStep() {
    // Insert before existing step 1
    const wizardSteps = document.querySelector('.progress-steps');
    if (!wizardSteps) return;
    
    // Add new step indicator
    const levelStep = document.createElement('div');
    levelStep.className = 'progress-step active';
    levelStep.innerHTML = `
        <div class="step-circle">1</div>
        <div class="step-label">Program Level</div>
    `;
    wizardSteps.insertBefore(levelStep, wizardSteps.firstChild);
    
    // Renumber other steps
    const allSteps = wizardSteps.querySelectorAll('.progress-step');
    allSteps.forEach((step, index) => {
        if (index > 0) {
            step.querySelector('.step-circle').textContent = index + 1;
        }
    });
}

// Program levels configuration
const programLevels = {
    undergraduate: {
        name: 'Undergraduate (Bachelor\'s)',
        icon: '🎓',
        duration: '4 years',
        description: 'Foundation degree programs'
    },
    masters: {
        name: 'Graduate (Master\'s)',
        icon: '📚', 
        duration: '1-2 years',
        description: 'Advanced specialization'
    },
    doctoral: {
        name: 'Doctoral (PhD)',
        icon: '🔬',
        duration: '4-6 years', 
        description: 'Research-focused programs'
    },
    professional: {
        name: 'Professional',
        icon: '💼',
        duration: '2-4 years',
        description: 'MD, JD, MBA, PharmD, etc.'
    }
};

// Graduate program categories
const graduateCategories = {
    'graduate-stem': {
        name: 'STEM Graduate Programs',
        icon: '🔬',
        programs: [
            'ms-computer-science',
            'ms-data-science',
            'ms-engineering',
            'ms-mathematics',
            'ms-physics',
            'ms-chemistry',
            'ms-biology'
        ]
    },
    'graduate-business': {
        name: 'Business Graduate Programs', 
        icon: '💼',
        programs: [
            'mba',
            'ms-finance',
            'ms-accounting',
            'ms-marketing',
            'executive-mba'
        ]
    },
    'professional-medicine': {
        name: 'Medical & Health Professional',
        icon: '⚕️',
        programs: [
            'md',
            'do',
            'dds',
            'pharmd',
            'dvm',
            'dnp'
        ]
    },
    'professional-law': {
        name: 'Law Professional',
        icon: '⚖️',
        programs: [
            'jd',
            'llm'
        ]
    },
    'doctoral-programs': {
        name: 'PhD Programs',
        icon: '🎓',
        programs: [
            'phd-computer-science',
            'phd-engineering',
            'phd-physics',
            'phd-chemistry',
            'phd-biology',
            'phd-mathematics',
            'phd-psychology',
            'phd-economics'
        ]
    }
};

// Graduate program details
const graduateProgramData = {
    'ms-computer-science': {
        name: 'MS in Computer Science',
        duration: '2 years',
        credits: 30,
        admission: {
            gpa: '3.0+',
            test: 'GRE (optional at many schools)',
            prerequisites: ['Data Structures', 'Algorithms', 'Operating Systems']
        },
        courses: [
            { id: 'CS501', name: 'Advanced Algorithms', credits: 3 },
            { id: 'CS502', name: 'Machine Learning', credits: 3 },
            { id: 'CS503', name: 'Distributed Systems', credits: 3 },
            { id: 'CS504', name: 'Advanced Databases', credits: 3 },
            { id: 'CS511', name: 'Deep Learning', credits: 3 },
            { id: 'CS512', name: 'Computer Vision', credits: 3 },
            { id: 'CS513', name: 'Natural Language Processing', credits: 3 },
            { id: 'CS599', name: 'Thesis/Project', credits: 6 }
        ],
        careers: ['ML Engineer', 'Research Scientist', 'Software Architect', 'Data Scientist']
    },
    
    'mba': {
        name: 'Master of Business Administration',
        duration: '2 years',
        credits: 60,
        admission: {
            gpa: '3.0+',
            test: 'GMAT 650+ or GRE',
            experience: '2-5 years work experience'
        },
        courses: [
            { id: 'MBA501', name: 'Financial Accounting', credits: 3 },
            { id: 'MBA502', name: 'Corporate Finance', credits: 3 },
            { id: 'MBA503', name: 'Strategic Management', credits: 3 },
            { id: 'MBA504', name: 'Marketing Management', credits: 3 },
            { id: 'MBA505', name: 'Operations Management', credits: 3 },
            { id: 'MBA506', name: 'Leadership', credits: 3 },
            { id: 'MBA511', name: 'Entrepreneurship', credits: 3 },
            { id: 'MBA512', name: 'Business Analytics', credits: 3 }
        ],
        careers: ['Management Consultant', 'Product Manager', 'Investment Banker', 'CEO/Executive']
    },
    
    'md': {
        name: 'Doctor of Medicine',
        duration: '4 years',
        credits: 200,
        admission: {
            gpa: '3.7+',
            test: 'MCAT 510+',
            prerequisites: [
                'Biology (2 semesters with lab)',
                'General Chemistry (2 semesters with lab)', 
                'Organic Chemistry (2 semesters with lab)',
                'Physics (2 semesters with lab)',
                'Biochemistry',
                'Psychology',
                'Sociology',
                'English (2 semesters)'
            ],
            experience: 'Clinical shadowing, research, volunteering'
        },
        curriculum: {
            year1: 'Basic Sciences: Anatomy, Biochemistry, Physiology, Histology',
            year2: 'Clinical Sciences: Pathology, Pharmacology, Microbiology',
            year3: 'Core Clinical Rotations: Internal Medicine, Surgery, Pediatrics, OB/GYN, Psychiatry',
            year4: 'Elective Rotations and Residency Applications'
        },
        careers: ['Physician', 'Surgeon', 'Medical Researcher', 'Hospital Administrator']
    },
    
    'jd': {
        name: 'Juris Doctor',
        duration: '3 years',
        credits: 90,
        admission: {
            gpa: '3.5+',
            test: 'LSAT 160+',
            prerequisites: ['Bachelor\'s degree in any field']
        },
        curriculum: {
            year1: 'Core: Contracts, Torts, Criminal Law, Constitutional Law, Civil Procedure, Legal Writing',
            year2: 'Evidence, Professional Responsibility, Electives, Journal/Moot Court',
            year3: 'Specialization, Clinical Programs, Bar Preparation'
        },
        careers: ['Attorney', 'Corporate Counsel', 'Judge', 'Legal Consultant']
    },
    
    'phd-computer-science': {
        name: 'PhD in Computer Science',
        duration: '4-6 years',
        credits: 72,
        admission: {
            gpa: '3.5+',
            test: 'GRE (Quant 165+)',
            prerequisites: ['MS in CS or exceptional BS with research'],
            experience: 'Research publications preferred'
        },
        milestones: [
            'Coursework (Years 1-2)',
            'Qualifying Exams',
            'Thesis Proposal Defense',
            'Dissertation Research',
            'Final Defense'
        ],
        careers: ['Professor', 'Research Scientist', 'R&D Director', 'Chief Scientist']
    },
    
    'ms-data-science': {
        name: 'MS in Data Science',
        duration: '1.5-2 years',
        credits: 36,
        admission: {
            gpa: '3.0+',
            prerequisites: ['Statistics', 'Linear Algebra', 'Programming']
        },
        courses: [
            { id: 'DS501', name: 'Statistical Learning', credits: 3 },
            { id: 'DS502', name: 'Big Data Analytics', credits: 3 },
            { id: 'DS503', name: 'Machine Learning', credits: 3 },
            { id: 'DS504', name: 'Data Visualization', credits: 3 },
            { id: 'DS505', name: 'Deep Learning', credits: 3 },
            { id: 'DS599', name: 'Capstone Project', credits: 3 }
        ],
        careers: ['Data Scientist', 'ML Engineer', 'Analytics Manager', 'Quantitative Analyst']
    },
    
    'pharmd': {
        name: 'Doctor of Pharmacy',
        duration: '4 years',
        credits: 150,
        admission: {
            gpa: '3.0+',
            test: 'PCAT (optional at many schools)',
            prerequisites: [
                'General Chemistry (2 semesters)',
                'Organic Chemistry (2 semesters)',
                'Biology (2 semesters)',
                'Physics (2 semesters)',
                'Calculus',
                'Statistics'
            ]
        },
        curriculum: {
            years1to3: 'Didactic: Pharmaceutical Sciences, Pharmacology, Therapeutics',
            year4: 'Clinical Rotations (APPEs)'
        },
        careers: ['Clinical Pharmacist', 'Hospital Pharmacist', 'Pharmaceutical Industry', 'Pharmacy Owner']
    }
};

// Function to display program level selection
function displayProgramLevelSelection() {
    const container = document.querySelector('#step-1-content');
    if (!container) return;
    
    container.innerHTML = `
        <div class="step-header">
            <h2 style="color: var(--primary-accent); margin-bottom: 1rem;">
                <i class="fas fa-graduation-cap"></i> Choose Your Education Level
            </h2>
            <p style="color: var(--text-secondary); margin-bottom: 2rem;">
                Select the type of program you're interested in pursuing
            </p>
        </div>
        
        <div class="level-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">
            ${Object.entries(programLevels).map(([key, level]) => `
                <div class="level-card" data-level="${key}" onclick="selectProgramLevel('${key}')" style="
                    background: var(--card-bg);
                    border: 2px solid var(--border-color);
                    border-radius: 12px;
                    padding: 2rem;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    text-align: center;
                ">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">${level.icon}</div>
                    <h3 style="color: var(--text-primary); margin-bottom: 0.5rem;">${level.name}</h3>
                    <p style="color: var(--primary-accent); margin-bottom: 0.5rem;">${level.duration}</p>
                    <p style="color: var(--text-secondary); font-size: 0.9rem;">${level.description}</p>
                </div>
            `).join('')}
        </div>
        
        <div id="level-info" style="margin-top: 2rem; padding: 1.5rem; background: var(--secondary-bg); 
             border-radius: 8px; display: none;">
            <h4 style="color: var(--primary-accent); margin-bottom: 1rem;">
                <i class="fas fa-info-circle"></i> Program Information
            </h4>
            <div id="level-details"></div>
        </div>
    `;
}

// Function to handle program level selection
function selectProgramLevel(level) {
    // Update UI
    document.querySelectorAll('.level-card').forEach(card => {
        card.style.borderColor = card.dataset.level === level ? 'var(--primary-accent)' : 'var(--border-color)';
    });
    
    // Store selection
    window.selectedProgramLevel = level;
    
    // Show appropriate info
    const infoDiv = document.getElementById('level-info');
    const detailsDiv = document.getElementById('level-details');
    
    let details = '';
    switch(level) {
        case 'undergraduate':
            details = 'Traditional 4-year bachelor\'s degree programs across all major fields of study.';
            break;
        case 'masters':
            details = 'Advanced degree programs requiring a bachelor\'s degree. Includes MS, MA, MBA, MEng, and more.';
            break;
        case 'doctoral':
            details = 'Research-focused PhD programs preparing students for careers in academia and research.';
            break;
        case 'professional':
            details = 'Professional practice degrees like MD (Medicine), JD (Law), PharmD (Pharmacy), DDS (Dentistry).';
            break;
    }
    
    detailsDiv.innerHTML = `<p style="color: var(--text-secondary);">${details}</p>`;
    infoDiv.style.display = 'block';
    
    // Enable next button
    enableNextButton();
}

// Export functions for integration
window.graduatePrograms = {
    programLevels,
    graduateCategories,
    graduateProgramData,
    displayProgramLevelSelection,
    selectProgramLevel
};