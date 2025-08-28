// Enhanced Tutoring Videos System with Subcategories
// Each of the 20 categories now has detailed subcategories

const enhancedVideoCategories = {
    'mathematics': {
        name: 'Mathematics',
        icon: '📐',
        description: 'From basic arithmetic to advanced calculus and statistics',
        subcategories: {
            'algebra': {
                name: 'Algebra',
                topics: ['Linear Equations', 'Quadratic Equations', 'Polynomials', 'Systems of Equations', 'Matrices'],
                videoCount: 10
            },
            'calculus': {
                name: 'Calculus',
                topics: ['Limits', 'Derivatives', 'Integrals', 'Differential Equations', 'Multivariable Calculus'],
                videoCount: 10
            },
            'geometry': {
                name: 'Geometry',
                topics: ['Euclidean Geometry', 'Trigonometry', 'Analytical Geometry', 'Solid Geometry', 'Topology'],
                videoCount: 10
            },
            'statistics': {
                name: 'Statistics & Probability',
                topics: ['Descriptive Statistics', 'Probability Theory', 'Hypothesis Testing', 'Regression Analysis', 'Bayesian Statistics'],
                videoCount: 10
            },
            'discrete-math': {
                name: 'Discrete Mathematics',
                topics: ['Logic', 'Set Theory', 'Graph Theory', 'Combinatorics', 'Number Theory'],
                videoCount: 10
            }
        }
    },
    
    'computer-science': {
        name: 'Computer Science',
        icon: '💻',
        description: 'Programming, algorithms, AI, and software development',
        subcategories: {
            'programming-basics': {
                name: 'Programming Fundamentals',
                topics: ['Python', 'Java', 'C++', 'JavaScript', 'Variables & Data Types'],
                videoCount: 10
            },
            'data-structures': {
                name: 'Data Structures & Algorithms',
                topics: ['Arrays', 'Linked Lists', 'Trees', 'Graphs', 'Sorting Algorithms'],
                videoCount: 10
            },
            'web-development': {
                name: 'Web Development',
                topics: ['HTML/CSS', 'React', 'Node.js', 'Databases', 'REST APIs'],
                videoCount: 10
            },
            'artificial-intelligence': {
                name: 'AI & Machine Learning',
                topics: ['Neural Networks', 'Deep Learning', 'NLP', 'Computer Vision', 'Reinforcement Learning'],
                videoCount: 10
            },
            'systems': {
                name: 'Systems & Networks',
                topics: ['Operating Systems', 'Computer Networks', 'Distributed Systems', 'Cloud Computing', 'Cybersecurity'],
                videoCount: 10
            }
        }
    },
    
    'physics': {
        name: 'Physics',
        icon: '⚛️',
        description: 'Classical mechanics, quantum physics, and relativity',
        subcategories: {
            'classical-mechanics': {
                name: 'Classical Mechanics',
                topics: ['Kinematics', 'Dynamics', 'Energy & Momentum', 'Rotational Motion', 'Oscillations'],
                videoCount: 10
            },
            'electromagnetism': {
                name: 'Electricity & Magnetism',
                topics: ['Electric Fields', 'Magnetic Fields', 'Circuits', 'Electromagnetic Waves', 'Maxwell Equations'],
                videoCount: 10
            },
            'quantum-physics': {
                name: 'Quantum Physics',
                topics: ['Wave-Particle Duality', 'Schrödinger Equation', 'Quantum States', 'Uncertainty Principle', 'Quantum Computing'],
                videoCount: 10
            },
            'thermodynamics': {
                name: 'Thermodynamics',
                topics: ['Laws of Thermodynamics', 'Heat Transfer', 'Entropy', 'Statistical Mechanics', 'Phase Transitions'],
                videoCount: 10
            },
            'modern-physics': {
                name: 'Modern Physics',
                topics: ['Special Relativity', 'General Relativity', 'Nuclear Physics', 'Particle Physics', 'Cosmology'],
                videoCount: 10
            }
        }
    },
    
    'chemistry': {
        name: 'Chemistry',
        icon: '🧪',
        description: 'Organic, inorganic, physical chemistry and lab techniques',
        subcategories: {
            'general-chemistry': {
                name: 'General Chemistry',
                topics: ['Atomic Structure', 'Chemical Bonding', 'Stoichiometry', 'States of Matter', 'Solutions'],
                videoCount: 10
            },
            'organic-chemistry': {
                name: 'Organic Chemistry',
                topics: ['Hydrocarbons', 'Functional Groups', 'Reactions', 'Synthesis', 'Spectroscopy'],
                videoCount: 10
            },
            'inorganic-chemistry': {
                name: 'Inorganic Chemistry',
                topics: ['Periodic Table', 'Coordination Compounds', 'Crystal Structure', 'Transition Metals', 'Organometallics'],
                videoCount: 10
            },
            'physical-chemistry': {
                name: 'Physical Chemistry',
                topics: ['Thermodynamics', 'Kinetics', 'Quantum Chemistry', 'Electrochemistry', 'Surface Chemistry'],
                videoCount: 10
            },
            'analytical-chemistry': {
                name: 'Analytical Chemistry',
                topics: ['Chromatography', 'Spectroscopy', 'Mass Spectrometry', 'Titration', 'Instrumental Analysis'],
                videoCount: 10
            }
        }
    },
    
    'biology': {
        name: 'Biology',
        icon: '🧬',
        description: 'Cell biology, genetics, ecology, and human anatomy',
        subcategories: {
            'cell-biology': {
                name: 'Cell & Molecular Biology',
                topics: ['Cell Structure', 'Cell Division', 'DNA/RNA', 'Protein Synthesis', 'Cell Signaling'],
                videoCount: 10
            },
            'genetics': {
                name: 'Genetics',
                topics: ['Mendelian Genetics', 'Molecular Genetics', 'Population Genetics', 'Genetic Engineering', 'Genomics'],
                videoCount: 10
            },
            'anatomy-physiology': {
                name: 'Anatomy & Physiology',
                topics: ['Body Systems', 'Organs', 'Tissues', 'Homeostasis', 'Human Development'],
                videoCount: 10
            },
            'ecology': {
                name: 'Ecology & Evolution',
                topics: ['Ecosystems', 'Population Dynamics', 'Natural Selection', 'Biodiversity', 'Conservation'],
                videoCount: 10
            },
            'microbiology': {
                name: 'Microbiology',
                topics: ['Bacteria', 'Viruses', 'Fungi', 'Immunology', 'Pathogenic Microbes'],
                videoCount: 10
            }
        }
    },
    
    'engineering': {
        name: 'Engineering',
        icon: '⚙️',
        description: 'Electrical, mechanical, civil, photonics, and advanced engineering disciplines',
        subcategories: {
            'electrical': {
                name: 'Electrical Engineering',
                topics: ['Circuit Analysis', 'Digital Logic', 'Signal Processing', 'Power Systems', 'Control Systems'],
                videoCount: 10
            },
            'mechanical': {
                name: 'Mechanical Engineering',
                topics: ['Statics', 'Dynamics', 'Fluid Mechanics', 'Heat Transfer', 'Machine Design'],
                videoCount: 10
            },
            'civil': {
                name: 'Civil Engineering',
                topics: ['Structural Analysis', 'Geotechnical', 'Transportation', 'Hydraulics', 'Construction Management'],
                videoCount: 10
            },
            'chemical': {
                name: 'Chemical Engineering',
                topics: ['Process Design', 'Reactor Design', 'Separation Processes', 'Process Control', 'Materials'],
                videoCount: 10
            },
            'aerospace': {
                name: 'Aerospace Engineering',
                topics: ['Aerodynamics', 'Propulsion', 'Flight Mechanics', 'Spacecraft Design', 'Orbital Mechanics'],
                videoCount: 10
            },
            'photonics-optical': {
                name: 'Photonics & Optical Engineering',
                topics: [
                    'Fundamentals of Semiconductors',
                    'Physics of Photonic Devices',
                    'Photonics - Optical Electronics',
                    'Nanophotonics',
                    'Principles of Optics',
                    'Non-Linear Optics',
                    'Optical Metrology',
                    'Fundamental Principles of Lithography',
                    'EUV Lithography',
                    'Advanced Optical Systems'
                ],
                videoCount: 20,
                description: 'Advanced topics in photonics, optical engineering, and semiconductor lithography'
            }
        }
    },
    
    'business': {
        name: 'Business & Economics',
        icon: '📊',
        description: 'Finance, marketing, management, and economic theory',
        subcategories: {
            'finance': {
                name: 'Finance',
                topics: ['Corporate Finance', 'Investment Analysis', 'Financial Markets', 'Risk Management', 'Portfolio Theory'],
                videoCount: 10
            },
            'marketing': {
                name: 'Marketing',
                topics: ['Digital Marketing', 'Brand Management', 'Consumer Behavior', 'Market Research', 'Social Media Marketing'],
                videoCount: 10
            },
            'management': {
                name: 'Management',
                topics: ['Strategic Management', 'Operations Management', 'Project Management', 'Leadership', 'Organizational Behavior'],
                videoCount: 10
            },
            'economics': {
                name: 'Economics',
                topics: ['Microeconomics', 'Macroeconomics', 'Econometrics', 'International Trade', 'Development Economics'],
                videoCount: 10
            },
            'entrepreneurship': {
                name: 'Entrepreneurship',
                topics: ['Startup Strategy', 'Business Planning', 'Venture Capital', 'Innovation', 'Scaling Businesses'],
                videoCount: 10
            }
        }
    },
    
    'medicine': {
        name: 'Medicine & Health',
        icon: '⚕️',
        description: 'Medical sciences, nursing, public health, and anatomy',
        subcategories: {
            'basic-sciences': {
                name: 'Basic Medical Sciences',
                topics: ['Anatomy', 'Physiology', 'Biochemistry', 'Pathology', 'Pharmacology'],
                videoCount: 10
            },
            'clinical-medicine': {
                name: 'Clinical Medicine',
                topics: ['Internal Medicine', 'Surgery', 'Pediatrics', 'Obstetrics', 'Emergency Medicine'],
                videoCount: 10
            },
            'nursing': {
                name: 'Nursing',
                topics: ['Patient Care', 'Clinical Skills', 'Pharmacology for Nurses', 'Critical Care', 'Community Health'],
                videoCount: 10
            },
            'public-health': {
                name: 'Public Health',
                topics: ['Epidemiology', 'Biostatistics', 'Health Policy', 'Global Health', 'Environmental Health'],
                videoCount: 10
            },
            'specialties': {
                name: 'Medical Specialties',
                topics: ['Cardiology', 'Neurology', 'Oncology', 'Radiology', 'Psychiatry'],
                videoCount: 10
            }
        }
    },
    
    'psychology': {
        name: 'Psychology',
        icon: '🧠',
        description: 'Cognitive, clinical, social, and developmental psychology',
        subcategories: {
            'cognitive': {
                name: 'Cognitive Psychology',
                topics: ['Memory', 'Attention', 'Perception', 'Language', 'Problem Solving'],
                videoCount: 10
            },
            'clinical': {
                name: 'Clinical Psychology',
                topics: ['Psychopathology', 'Therapy Techniques', 'Assessment', 'DSM-5', 'Treatment Planning'],
                videoCount: 10
            },
            'developmental': {
                name: 'Developmental Psychology',
                topics: ['Child Development', 'Adolescence', 'Adult Development', 'Aging', 'Attachment Theory'],
                videoCount: 10
            },
            'social': {
                name: 'Social Psychology',
                topics: ['Social Influence', 'Group Dynamics', 'Attitudes', 'Prejudice', 'Interpersonal Relations'],
                videoCount: 10
            },
            'neuroscience': {
                name: 'Behavioral Neuroscience',
                topics: ['Brain Structure', 'Neurotransmitters', 'Neuroplasticity', 'Brain Disorders', 'Cognitive Neuroscience'],
                videoCount: 10
            }
        }
    },
    
    'language': {
        name: 'Language & Literature',
        icon: '📚',
        description: 'English, foreign languages, writing, and literary analysis',
        subcategories: {
            'english-composition': {
                name: 'English Composition',
                topics: ['Essay Writing', 'Grammar', 'Research Papers', 'Creative Writing', 'Technical Writing'],
                videoCount: 10
            },
            'literature': {
                name: 'Literature',
                topics: ['American Literature', 'British Literature', 'World Literature', 'Poetry Analysis', 'Literary Theory'],
                videoCount: 10
            },
            'foreign-languages': {
                name: 'Foreign Languages',
                topics: ['Spanish', 'French', 'Mandarin', 'German', 'Arabic'],
                videoCount: 10
            },
            'linguistics': {
                name: 'Linguistics',
                topics: ['Phonetics', 'Syntax', 'Semantics', 'Sociolinguistics', 'Language Acquisition'],
                videoCount: 10
            },
            'communication': {
                name: 'Communication Studies',
                topics: ['Public Speaking', 'Rhetoric', 'Media Studies', 'Interpersonal Communication', 'Digital Communication'],
                videoCount: 10
            }
        }
    },
    
    'history': {
        name: 'History',
        icon: '📜',
        description: 'World history, American history, and historical analysis',
        subcategories: {
            'ancient-history': {
                name: 'Ancient History',
                topics: ['Ancient Egypt', 'Greece', 'Rome', 'Mesopotamia', 'Ancient China'],
                videoCount: 10
            },
            'medieval-history': {
                name: 'Medieval History',
                topics: ['Byzantine Empire', 'Islamic Golden Age', 'Medieval Europe', 'Crusades', 'Renaissance'],
                videoCount: 10
            },
            'modern-history': {
                name: 'Modern History',
                topics: ['Industrial Revolution', 'World Wars', 'Cold War', 'Decolonization', 'Contemporary History'],
                videoCount: 10
            },
            'american-history': {
                name: 'American History',
                topics: ['Colonial Period', 'Revolutionary War', 'Civil War', 'Civil Rights', 'Modern America'],
                videoCount: 10
            },
            'world-regions': {
                name: 'Regional History',
                topics: ['European History', 'Asian History', 'African History', 'Latin American History', 'Middle Eastern History'],
                videoCount: 10
            }
        }
    },
    
    'art': {
        name: 'Art & Design',
        icon: '🎨',
        description: 'Drawing, painting, graphic design, and art history',
        subcategories: {
            'drawing-painting': {
                name: 'Drawing & Painting',
                topics: ['Sketching', 'Oil Painting', 'Watercolor', 'Portrait Drawing', 'Landscape Art'],
                videoCount: 10
            },
            'digital-art': {
                name: 'Digital Art',
                topics: ['Photoshop', 'Illustrator', 'Digital Painting', '3D Modeling', 'Animation'],
                videoCount: 10
            },
            'graphic-design': {
                name: 'Graphic Design',
                topics: ['Typography', 'Logo Design', 'Layout Design', 'Branding', 'UI/UX Design'],
                videoCount: 10
            },
            'art-history': {
                name: 'Art History',
                topics: ['Renaissance Art', 'Modern Art', 'Contemporary Art', 'Art Movements', 'Art Criticism'],
                videoCount: 10
            },
            'photography': {
                name: 'Photography',
                topics: ['Camera Basics', 'Composition', 'Lighting', 'Photo Editing', 'Portrait Photography'],
                videoCount: 10
            }
        }
    },
    
    'music': {
        name: 'Music',
        icon: '🎵',
        description: 'Music theory, instruments, composition, and performance',
        subcategories: {
            'music-theory': {
                name: 'Music Theory',
                topics: ['Notes & Scales', 'Harmony', 'Rhythm', 'Chord Progressions', 'Music Analysis'],
                videoCount: 10
            },
            'instruments': {
                name: 'Instruments',
                topics: ['Piano', 'Guitar', 'Violin', 'Drums', 'Voice Training'],
                videoCount: 10
            },
            'composition': {
                name: 'Composition & Songwriting',
                topics: ['Melody Writing', 'Arranging', 'Orchestration', 'Lyrics', 'Song Structure'],
                videoCount: 10
            },
            'music-production': {
                name: 'Music Production',
                topics: ['DAW Software', 'Recording', 'Mixing', 'Mastering', 'Sound Design'],
                videoCount: 10
            },
            'music-history': {
                name: 'Music History',
                topics: ['Classical Period', 'Romantic Era', 'Jazz History', 'Rock Evolution', 'World Music'],
                videoCount: 10
            }
        }
    },
    
    'philosophy': {
        name: 'Philosophy',
        icon: '💭',
        description: 'Ethics, logic, metaphysics, and philosophical thinking',
        subcategories: {
            'ethics': {
                name: 'Ethics & Moral Philosophy',
                topics: ['Normative Ethics', 'Applied Ethics', 'Metaethics', 'Bioethics', 'Environmental Ethics'],
                videoCount: 10
            },
            'logic': {
                name: 'Logic & Critical Thinking',
                topics: ['Formal Logic', 'Informal Logic', 'Fallacies', 'Argument Analysis', 'Symbolic Logic'],
                videoCount: 10
            },
            'metaphysics': {
                name: 'Metaphysics',
                topics: ['Existence', 'Reality', 'Free Will', 'Mind-Body Problem', 'Personal Identity'],
                videoCount: 10
            },
            'epistemology': {
                name: 'Epistemology',
                topics: ['Knowledge', 'Truth', 'Skepticism', 'Justification', 'Scientific Method'],
                videoCount: 10
            },
            'history-philosophy': {
                name: 'History of Philosophy',
                topics: ['Ancient Philosophy', 'Medieval Philosophy', 'Modern Philosophy', 'Contemporary Philosophy', 'Eastern Philosophy'],
                videoCount: 10
            }
        }
    },
    
    'law': {
        name: 'Law',
        icon: '⚖️',
        description: 'Constitutional law, criminal law, and legal studies',
        subcategories: {
            'constitutional': {
                name: 'Constitutional Law',
                topics: ['Bill of Rights', 'Separation of Powers', 'Due Process', 'Equal Protection', 'First Amendment'],
                videoCount: 10
            },
            'criminal': {
                name: 'Criminal Law',
                topics: ['Criminal Procedure', 'Evidence', 'Crimes', 'Defenses', 'Sentencing'],
                videoCount: 10
            },
            'civil': {
                name: 'Civil Law',
                topics: ['Contracts', 'Torts', 'Property Law', 'Family Law', 'Employment Law'],
                videoCount: 10
            },
            'international': {
                name: 'International Law',
                topics: ['Treaties', 'Human Rights', 'International Courts', 'Trade Law', 'War Crimes'],
                videoCount: 10
            },
            'legal-skills': {
                name: 'Legal Skills',
                topics: ['Legal Research', 'Legal Writing', 'Case Analysis', 'Oral Advocacy', 'Negotiation'],
                videoCount: 10
            }
        }
    },
    
    'environmental': {
        name: 'Environmental Science',
        icon: '🌍',
        description: 'Climate science, ecology, and sustainability',
        subcategories: {
            'climate-science': {
                name: 'Climate Science',
                topics: ['Climate Change', 'Greenhouse Effect', 'Weather Systems', 'Ocean Currents', 'Climate Models'],
                videoCount: 10
            },
            'ecology': {
                name: 'Ecology',
                topics: ['Ecosystems', 'Food Webs', 'Biodiversity', 'Population Ecology', 'Community Ecology'],
                videoCount: 10
            },
            'conservation': {
                name: 'Conservation',
                topics: ['Wildlife Conservation', 'Habitat Protection', 'Endangered Species', 'Marine Conservation', 'Forest Management'],
                videoCount: 10
            },
            'sustainability': {
                name: 'Sustainability',
                topics: ['Renewable Energy', 'Sustainable Agriculture', 'Green Building', 'Circular Economy', 'Carbon Footprint'],
                videoCount: 10
            },
            'environmental-policy': {
                name: 'Environmental Policy',
                topics: ['Environmental Law', 'Climate Policy', 'Environmental Justice', 'International Agreements', 'Impact Assessment'],
                videoCount: 10
            }
        }
    },
    
    'data-science': {
        name: 'Data Science',
        icon: '📈',
        description: 'Machine learning, statistics, and data analysis',
        subcategories: {
            'statistics': {
                name: 'Statistics for Data Science',
                topics: ['Descriptive Statistics', 'Inferential Statistics', 'Bayesian Statistics', 'Time Series', 'A/B Testing'],
                videoCount: 10
            },
            'machine-learning': {
                name: 'Machine Learning',
                topics: ['Supervised Learning', 'Unsupervised Learning', 'Neural Networks', 'Deep Learning', 'Reinforcement Learning'],
                videoCount: 10
            },
            'data-analysis': {
                name: 'Data Analysis',
                topics: ['Exploratory Data Analysis', 'Data Cleaning', 'Feature Engineering', 'Data Visualization', 'SQL'],
                videoCount: 10
            },
            'big-data': {
                name: 'Big Data',
                topics: ['Hadoop', 'Spark', 'NoSQL Databases', 'Data Pipelines', 'Cloud Computing'],
                videoCount: 10
            },
            'ai-applications': {
                name: 'AI Applications',
                topics: ['Computer Vision', 'Natural Language Processing', 'Recommendation Systems', 'Chatbots', 'Predictive Analytics'],
                videoCount: 10
            }
        }
    },
    
    'test-prep': {
        name: 'Test Preparation',
        icon: '📝',
        description: 'SAT, ACT, GRE, GMAT, MCAT, and other standardized tests',
        subcategories: {
            'college-admission': {
                name: 'College Admission Tests',
                topics: ['SAT Math', 'SAT Reading', 'ACT Science', 'ACT English', 'Test Strategies'],
                videoCount: 10
            },
            'graduate-tests': {
                name: 'Graduate School Tests',
                topics: ['GRE Verbal', 'GRE Quantitative', 'GRE Writing', 'GMAT', 'LSAT'],
                videoCount: 10
            },
            'professional-tests': {
                name: 'Professional Tests',
                topics: ['MCAT Biology', 'MCAT Chemistry', 'MCAT Physics', 'DAT', 'PCAT'],
                videoCount: 10
            },
            'language-tests': {
                name: 'Language Proficiency',
                topics: ['TOEFL', 'IELTS', 'Duolingo English Test', 'Cambridge English', 'PTE Academic'],
                videoCount: 10
            },
            'certification-exams': {
                name: 'Certification Exams',
                topics: ['PMP', 'AWS Certification', 'CompTIA', 'CPA', 'Bar Exam Prep'],
                videoCount: 10
            }
        }
    },
    
    'study-skills': {
        name: 'Study Skills',
        icon: '✏️',
        description: 'Note-taking, time management, and learning strategies',
        subcategories: {
            'learning-techniques': {
                name: 'Learning Techniques',
                topics: ['Active Learning', 'Spaced Repetition', 'Mind Mapping', 'Memory Palaces', 'Speed Reading'],
                videoCount: 10
            },
            'note-taking': {
                name: 'Note-Taking Methods',
                topics: ['Cornell Method', 'Outline Method', 'Mapping Method', 'Digital Notes', 'Sketchnoting'],
                videoCount: 10
            },
            'time-management': {
                name: 'Time Management',
                topics: ['Pomodoro Technique', 'Time Blocking', 'Priority Matrix', 'Goal Setting', 'Productivity Tools'],
                videoCount: 10
            },
            'test-taking': {
                name: 'Test-Taking Strategies',
                topics: ['Multiple Choice', 'Essay Writing', 'Problem Solving', 'Test Anxiety', 'Review Techniques'],
                videoCount: 10
            },
            'research-skills': {
                name: 'Research Skills',
                topics: ['Literature Review', 'Citation Styles', 'Academic Writing', 'Critical Analysis', 'Presentation Skills'],
                videoCount: 10
            }
        }
    },
    
    'career': {
        name: 'Career Development',
        icon: '🚀',
        description: 'Resume writing, interview skills, and professional growth',
        subcategories: {
            'job-search': {
                name: 'Job Search Strategies',
                topics: ['Resume Writing', 'Cover Letters', 'LinkedIn Optimization', 'Job Boards', 'Networking'],
                videoCount: 10
            },
            'interview-skills': {
                name: 'Interview Preparation',
                topics: ['Behavioral Interviews', 'Technical Interviews', 'Case Interviews', 'Phone Screens', 'Salary Negotiation'],
                videoCount: 10
            },
            'professional-skills': {
                name: 'Professional Skills',
                topics: ['Communication', 'Leadership', 'Teamwork', 'Problem Solving', 'Emotional Intelligence'],
                videoCount: 10
            },
            'career-planning': {
                name: 'Career Planning',
                topics: ['Career Assessment', 'Goal Setting', 'Career Transitions', 'Personal Branding', 'Work-Life Balance'],
                videoCount: 10
            },
            'entrepreneurship': {
                name: 'Entrepreneurship',
                topics: ['Business Ideas', 'Business Planning', 'Funding', 'Marketing', 'Scaling'],
                videoCount: 10
            }
        }
    }
};

// Generate videos for subcategories
function generateSubcategoryVideos(categoryId, subcategoryId, subcategory) {
    const videos = [];
    const levels = ['Beginner', 'Intermediate', 'Advanced'];
    const instructors = [
        'Dr. Sarah Johnson', 'Prof. Michael Chen', 'Dr. Emily Rodriguez',
        'Prof. David Kim', 'Dr. Lisa Anderson', 'Prof. James Wilson'
    ];
    
    subcategory.topics.forEach((topic, topicIndex) => {
        // Generate 2 videos per topic (10 topics × 2 = 20 videos per subcategory)
        for (let i = 0; i < 2; i++) {
            const level = levels[Math.floor(Math.random() * levels.length)];
            const instructor = instructors[Math.floor(Math.random() * instructors.length)];
            const partNum = i + 1;
            
            videos.push({
                id: `${categoryId}-${subcategoryId}-${topicIndex}-${partNum}`,
                title: `${topic} - ${level} (Part ${partNum})`,
                instructor: instructor,
                duration: `${Math.floor(Math.random() * 45) + 15}:${Math.floor(Math.random() * 60).toString().padStart(2, '0')}`,
                views: Math.floor(Math.random() * 50000) + 1000,
                rating: (Math.random() * 2 + 3).toFixed(1),
                level: level,
                topic: topic,
                subcategory: subcategory.name,
                category: enhancedVideoCategories[categoryId].name,
                description: `Comprehensive tutorial on ${topic} for ${level.toLowerCase()} learners.`,
                isPremium: Math.random() > 0.7
            });
        }
    });
    
    return videos;
}

// Initialize all subcategory videos
function initializeAllVideos() {
    const allVideos = {};
    
    Object.entries(enhancedVideoCategories).forEach(([categoryId, category]) => {
        allVideos[categoryId] = {};
        
        Object.entries(category.subcategories).forEach(([subcategoryId, subcategory]) => {
            allVideos[categoryId][subcategoryId] = generateSubcategoryVideos(
                categoryId, 
                subcategoryId, 
                subcategory
            );
        });
    });
    
    return allVideos;
}

// Store all videos
const videoDatabase = initializeAllVideos();

// UI Functions for subcategory navigation
function displayCategoryWithSubcategories(categoryId) {
    const category = enhancedVideoCategories[categoryId];
    if (!category) return;
    
    const container = document.getElementById('subcategories-container');
    if (!container) return;
    
    let html = `
        <div class="category-header">
            <button class="back-btn" onclick="showCategories()">
                <i class="fas fa-arrow-left"></i> Back to Categories
            </button>
            <h2 style="color: var(--primary-accent); margin: 1.5rem 0;">
                ${category.icon} ${category.name}
            </h2>
            <p style="color: var(--text-secondary); margin-bottom: 2rem;">
                ${category.description}
            </p>
        </div>
        
        <div class="subcategories-grid">
    `;
    
    Object.entries(category.subcategories).forEach(([subcategoryId, subcategory]) => {
        const videoCount = videoDatabase[categoryId][subcategoryId].length;
        const totalDuration = videoDatabase[categoryId][subcategoryId].reduce((sum, video) => {
            const [minutes] = video.duration.split(':').map(Number);
            return sum + minutes;
        }, 0);
        
        html += `
            <div class="subcategory-card" onclick="showSubcategoryVideos('${categoryId}', '${subcategoryId}')">
                <h3 class="subcategory-title">${subcategory.name}</h3>
                <div class="subcategory-topics">
                    ${subcategory.topics.slice(0, 3).map(topic => 
                        `<span class="topic-tag">${topic}</span>`
                    ).join('')}
                    ${subcategory.topics.length > 3 ? 
                        `<span class="topic-tag">+${subcategory.topics.length - 3} more</span>` : ''}
                </div>
                <div class="subcategory-stats">
                    <span><i class="fas fa-video"></i> ${videoCount} videos</span>
                    <span><i class="fas fa-clock"></i> ${Math.round(totalDuration / 60)} hours</span>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
    
    // Show subcategories section
    document.getElementById('categories-section').style.display = 'none';
    document.getElementById('subcategories-section').style.display = 'block';
}

// Display videos for a specific subcategory
function showSubcategoryVideos(categoryId, subcategoryId) {
    const category = enhancedVideoCategories[categoryId];
    const subcategory = category.subcategories[subcategoryId];
    const videos = videoDatabase[categoryId][subcategoryId];
    
    const container = document.getElementById('videos-container');
    if (!container) return;
    
    let html = `
        <div class="videos-header">
            <button class="back-btn" onclick="displayCategoryWithSubcategories('${categoryId}')">
                <i class="fas fa-arrow-left"></i> Back to ${category.name}
            </button>
            <h2 style="color: var(--primary-accent); margin: 1.5rem 0;">
                ${subcategory.name}
            </h2>
            <div class="breadcrumb">
                <span>${category.name}</span>
                <i class="fas fa-chevron-right"></i>
                <span>${subcategory.name}</span>
            </div>
        </div>
        
        <div class="videos-grid">
    `;
    
    videos.forEach(video => {
        html += `
            <div class="video-card" onclick="playVideo('${video.id}')">
                <div class="video-thumbnail">
                    <i class="fas fa-play-circle"></i>
                    <span class="video-duration">${video.duration}</span>
                    ${video.isPremium ? '<span class="premium-badge">Premium</span>' : ''}
                    <span class="level-badge level-${video.level.toLowerCase()}">${video.level}</span>
                </div>
                <div class="video-info">
                    <h4 class="video-title">${video.title}</h4>
                    <p class="video-instructor">${video.instructor}</p>
                    <div class="video-meta">
                        <span class="video-views">
                            <i class="fas fa-eye"></i> ${formatNumber(video.views)}
                        </span>
                        <span class="video-rating">
                            <i class="fas fa-star"></i> ${video.rating}
                        </span>
                    </div>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
    
    // Show videos section
    document.getElementById('subcategories-section').style.display = 'none';
    document.getElementById('videos-display-section').style.display = 'block';
}

// Helper function to format numbers
function formatNumber(num) {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        enhancedVideoCategories,
        videoDatabase,
        displayCategoryWithSubcategories,
        showSubcategoryVideos
    };
}