// Specialized Photonics & Optical Engineering Courses
// Advanced Electrical Engineering Topics

const photonicsCourses = {
    category: 'Electrical Engineering - Photonics & Optical Engineering',
    icon: '💡',
    description: 'Advanced courses in photonics, optical engineering, and semiconductor lithography technology',
    
    courses: [
        {
            id: 'EE-PHOT-001',
            title: 'Fundamentals of Semiconductors',
            level: 'Intermediate',
            duration: '45 hours',
            modules: 12,
            description: 'Comprehensive study of semiconductor physics, band theory, and device fundamentals',
            topics: [
                'Crystal Structure and Band Theory',
                'Carrier Transport and Recombination',
                'PN Junctions and Diodes',
                'Bipolar Junction Transistors',
                'Field Effect Transistors',
                'Semiconductor Processing'
            ],
            prerequisites: ['Physics II', 'Quantum Mechanics Basics'],
            instructor: 'Dr. Michael Chen',
            rating: 4.8,
            enrolled: 2500
        },
        
        {
            id: 'EE-PHOT-002',
            title: 'Physics of Photonic Devices',
            level: 'Advanced',
            duration: '50 hours',
            modules: 14,
            description: 'In-depth exploration of photonic device physics including lasers, LEDs, and photodetectors',
            topics: [
                'Optical Processes in Semiconductors',
                'Light Emitting Diodes (LEDs)',
                'Semiconductor Lasers',
                'Photodetectors and Solar Cells',
                'Quantum Well Devices',
                'Photonic Integration'
            ],
            prerequisites: ['Fundamentals of Semiconductors', 'Electromagnetic Theory'],
            instructor: 'Prof. Sarah Johnson',
            rating: 4.9,
            enrolled: 1800
        },
        
        {
            id: 'EE-PHOT-003',
            title: 'Photonics - Optical Electronics',
            level: 'Advanced',
            duration: '48 hours',
            modules: 13,
            description: 'Integration of photonics and electronics for modern optical communication systems',
            topics: [
                'Optical Waveguides and Fibers',
                'Integrated Optics',
                'Optical Modulators',
                'Optical Amplifiers',
                'Wavelength Division Multiplexing',
                'Optical Networks'
            ],
            prerequisites: ['Physics of Photonic Devices', 'Signal Processing'],
            instructor: 'Dr. Emily Rodriguez',
            rating: 4.7,
            enrolled: 1500
        },
        
        {
            id: 'EE-PHOT-004',
            title: 'Nanophotonics',
            level: 'Advanced',
            duration: '55 hours',
            modules: 15,
            description: 'Cutting-edge topics in nanoscale photonics and plasmonics',
            topics: [
                'Photonic Crystals',
                'Plasmonics and Surface Plasmons',
                'Metamaterials',
                'Quantum Dots and Nanowires',
                'Near-field Optics',
                'Nanofabrication Techniques'
            ],
            prerequisites: ['Photonics - Optical Electronics', 'Nanotechnology Basics'],
            instructor: 'Prof. David Kim',
            rating: 4.9,
            enrolled: 1200
        },
        
        {
            id: 'EE-PHOT-005',
            title: 'Principles of Optics',
            level: 'Intermediate',
            duration: '40 hours',
            modules: 11,
            description: 'Fundamental principles of classical and modern optics',
            topics: [
                'Geometrical Optics',
                'Wave Optics',
                'Interference and Diffraction',
                'Polarization',
                'Fourier Optics',
                'Coherence Theory'
            ],
            prerequisites: ['Physics II', 'Mathematics III'],
            instructor: 'Dr. Lisa Anderson',
            rating: 4.6,
            enrolled: 3000
        },
        
        {
            id: 'EE-PHOT-006',
            title: 'Non-Linear Optics',
            level: 'Advanced',
            duration: '52 hours',
            modules: 14,
            description: 'Advanced study of non-linear optical phenomena and applications',
            topics: [
                'Non-linear Susceptibility',
                'Second Harmonic Generation',
                'Parametric Processes',
                'Third-Order Non-linearities',
                'Solitons and Self-focusing',
                'Non-linear Optical Materials'
            ],
            prerequisites: ['Principles of Optics', 'Electromagnetic Theory'],
            instructor: 'Prof. James Wilson',
            rating: 4.8,
            enrolled: 900
        },
        
        {
            id: 'EE-PHOT-007',
            title: 'Optical Metrology',
            level: 'Advanced',
            duration: '46 hours',
            modules: 12,
            description: 'Precision measurement techniques using optical methods',
            topics: [
                'Interferometry',
                'Holography',
                'Speckle Metrology',
                'Optical Coherence Tomography',
                'Laser Doppler Velocimetry',
                'Digital Image Correlation'
            ],
            prerequisites: ['Principles of Optics', 'Signal Processing'],
            instructor: 'Dr. Maria Garcia',
            rating: 4.7,
            enrolled: 1100
        },
        
        {
            id: 'EE-PHOT-008',
            title: 'Fundamental Principles of Lithography',
            level: 'Advanced',
            duration: '50 hours',
            modules: 13,
            description: 'Comprehensive coverage of lithography principles for semiconductor manufacturing',
            topics: [
                'Optical Lithography Basics',
                'Photoresist Chemistry',
                'Resolution and Depth of Focus',
                'Optical Proximity Correction',
                'Phase Shift Masks',
                'Immersion Lithography'
            ],
            prerequisites: ['Fundamentals of Semiconductors', 'Principles of Optics'],
            instructor: 'Prof. Robert Brown',
            rating: 4.8,
            enrolled: 1400
        },
        
        {
            id: 'EE-PHOT-009',
            title: 'EUV Lithography',
            level: 'Expert',
            duration: '60 hours',
            modules: 16,
            description: 'State-of-the-art extreme ultraviolet lithography for advanced semiconductor nodes',
            topics: [
                'EUV Source Technology',
                'EUV Optics and Mirrors',
                'EUV Photoresists',
                'EUV Masks and Pellicles',
                'Stochastic Effects in EUV',
                'High-NA EUV Systems',
                'EUV Process Integration',
                'Future of EUV Technology'
            ],
            prerequisites: ['Fundamental Principles of Lithography', 'Advanced Semiconductor Processing'],
            instructor: 'Dr. Jennifer Lee',
            rating: 4.9,
            enrolled: 800
        },
        
        {
            id: 'EE-PHOT-010',
            title: 'Advanced Optical Systems Design',
            level: 'Advanced',
            duration: '54 hours',
            modules: 14,
            description: 'Design and optimization of complex optical systems',
            topics: [
                'Lens Design Theory',
                'Aberration Theory',
                'Optical System Modeling',
                'Zemax/Code V Software',
                'Tolerance Analysis',
                'Thermal Effects',
                'Optical Testing and Alignment'
            ],
            prerequisites: ['Principles of Optics', 'Engineering Mathematics'],
            instructor: 'Prof. Christopher Martinez',
            rating: 4.7,
            enrolled: 950
        }
    ],
    
    learningPath: {
        beginner: [
            'Principles of Optics',
            'Fundamentals of Semiconductors'
        ],
        intermediate: [
            'Physics of Photonic Devices',
            'Photonics - Optical Electronics',
            'Optical Metrology'
        ],
        advanced: [
            'Nanophotonics',
            'Non-Linear Optics',
            'Fundamental Principles of Lithography',
            'Advanced Optical Systems Design'
        ],
        expert: [
            'EUV Lithography'
        ]
    },
    
    careerPaths: [
        {
            title: 'Photonics Engineer',
            requiredCourses: ['Physics of Photonic Devices', 'Photonics - Optical Electronics', 'Principles of Optics'],
            averageSalary: '$95,000 - $140,000',
            companies: ['Intel', 'ASML', 'Thorlabs', 'Coherent', 'IPG Photonics']
        },
        {
            title: 'Optical Systems Engineer',
            requiredCourses: ['Principles of Optics', 'Advanced Optical Systems Design', 'Optical Metrology'],
            averageSalary: '$90,000 - $135,000',
            companies: ['Zeiss', 'Nikon', 'Canon', 'Apple', 'Google']
        },
        {
            title: 'Semiconductor Lithography Engineer',
            requiredCourses: ['Fundamentals of Semiconductors', 'Fundamental Principles of Lithography', 'EUV Lithography'],
            averageSalary: '$110,000 - $160,000',
            companies: ['ASML', 'Applied Materials', 'KLA', 'Lam Research', 'Tokyo Electron']
        },
        {
            title: 'Nanophotonics Researcher',
            requiredCourses: ['Nanophotonics', 'Non-Linear Optics', 'Physics of Photonic Devices'],
            averageSalary: '$85,000 - $125,000',
            companies: ['IBM Research', 'Bell Labs', 'MIT Lincoln Laboratory', 'NIST']
        }
    ],
    
    resources: {
        textbooks: [
            'Photonic Devices by Jia-Ming Liu',
            'Fundamentals of Photonics by Saleh & Teich',
            'Semiconductor Physics and Devices by Donald Neamen',
            'Principles of Lithography by Harry Levinson',
            'Nonlinear Optics by Robert Boyd'
        ],
        software: [
            'Zemax OpticStudio',
            'COMSOL Multiphysics',
            'Lumerical FDTD',
            'RSoft Photonic Suite',
            'MATLAB Photonics Toolbox'
        ],
        labs: [
            'Optical Bench Experiments',
            'Laser Laboratory',
            'Cleanroom Fabrication',
            'Optical Characterization Lab',
            'Semiconductor Device Testing'
        ]
    }
};

// Function to display photonics courses in the UI
function displayPhotonicsCourses() {
    const container = document.getElementById('photonics-courses-container');
    if (!container) return;
    
    let html = `
        <div class="photonics-header">
            <h2 style="color: var(--primary-accent); margin-bottom: 1rem;">
                ${photonicsCourses.icon} ${photonicsCourses.category}
            </h2>
            <p style="color: var(--text-secondary); margin-bottom: 2rem;">
                ${photonicsCourses.description}
            </p>
        </div>
        
        <div class="courses-grid">
    `;
    
    photonicsCourses.courses.forEach(course => {
        html += `
            <div class="course-card" onclick="viewCourseDetails('${course.id}')">
                <div class="course-header">
                    <h3>${course.title}</h3>
                    <span class="level-badge level-${course.level.toLowerCase()}">${course.level}</span>
                </div>
                
                <p class="course-description">${course.description}</p>
                
                <div class="course-meta">
                    <span><i class="fas fa-clock"></i> ${course.duration}</span>
                    <span><i class="fas fa-book"></i> ${course.modules} modules</span>
                    <span><i class="fas fa-star"></i> ${course.rating}</span>
                </div>
                
                <div class="course-topics">
                    <strong>Key Topics:</strong>
                    <ul>
                        ${course.topics.slice(0, 3).map(topic => 
                            `<li>${topic}</li>`
                        ).join('')}
                        ${course.topics.length > 3 ? `<li>+${course.topics.length - 3} more topics</li>` : ''}
                    </ul>
                </div>
                
                <div class="course-footer">
                    <span class="instructor">
                        <i class="fas fa-user-tie"></i> ${course.instructor}
                    </span>
                    <span class="enrolled">
                        <i class="fas fa-users"></i> ${course.enrolled.toLocaleString()} enrolled
                    </span>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = photonicsCourses;
}