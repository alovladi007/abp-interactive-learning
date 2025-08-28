// AI Path Advisor - Career-Based Course Selection

// State management
let currentStep = 1;
let selectedCategory = null;
let selectedMajor = null;
let selectedCareer = null;
let selectedCourses = [];
let availableCourses = [];
let careerSpecificCourses = [];
let userPreferences = {};

// Backend API base URL
const API_BASE_URL = 'http://localhost:8000';

// Career-specific course recommendations
const careerCourseMapping = {
    // Electrical Engineering careers
    'embedded-engineer': {
        required: ['EE302', 'EE401'], // Digital Logic, Microprocessor Systems
        recommended: ['EE301', 'CS101', 'CS201'], // Electronics, Programming, Data Structures
        focus: 'firmware and embedded systems'
    },
    'rf-engineer': {
        required: ['EE403', 'EE304'], // RF & Microwave, Communication Systems
        recommended: ['EE203', 'EE202', 'PHYS102'], // Electromagnetics, Signals, E&M
        focus: 'wireless communication and antenna design'
    },
    'power-engineer': {
        required: ['EE305'], // Power Systems
        recommended: ['EE201', 'EE303', 'ME201'], // Circuits II, Control Systems, Thermodynamics
        focus: 'power generation and distribution'
    },
    
    // Computer Science careers
    'software-engineer': {
        required: ['CS401', 'CS303'], // Software Engineering, Database Systems
        recommended: ['CS304', 'CS201', 'CS302'], // Networks, Data Structures, OS
        focus: 'full-stack application development'
    },
    'ml-engineer': {
        required: ['CS402', 'CS403'], // AI, Machine Learning
        recommended: ['DS202', 'MATH301', 'CS201'], // Deep Learning, Linear Algebra, Data Structures
        focus: 'artificial intelligence and machine learning'
    },
    'data-engineer': {
        required: ['CS303', 'DS301'], // Database Systems, Big Data
        recommended: ['CS304', 'DS201', 'CS201'], // Networks, Data Mining, Data Structures
        focus: 'data pipelines and infrastructure'
    },
    
    // Mechanical Engineering careers
    'robotics-engineer': {
        required: ['ME402', 'ME401'], // Robotics, Control Systems
        recommended: ['EE301', 'CS101', 'ME302'], // Electronics, Programming, Machine Design
        focus: 'robotic systems and automation'
    },
    'thermal-engineer': {
        required: ['ME301', 'ME201'], // Heat Transfer, Thermodynamics
        recommended: ['ME202', 'CHEM101', 'MAT201'], // Fluid Mechanics, Chemistry, Materials
        focus: 'thermal systems and energy'
    },
    'design-engineer': {
        required: ['ME302', 'ME303'], // Machine Design, Manufacturing
        recommended: ['ME203', 'MAT202', 'ME101'], // Mechanics of Materials, Material Behavior, Statics
        focus: 'mechanical design and manufacturing'
    },
    
    // Physics careers
    'research-physicist': {
        required: ['PHYS302', 'PHYS401'], // Quantum II, Nuclear Physics
        recommended: ['PHYS402', 'MATH401', 'PHYS303'], // General Relativity, Advanced Math, E&M II
        focus: 'theoretical and experimental research'
    },
    'computational-physicist': {
        required: ['PHYS302', 'CS201'], // Quantum II, Data Structures
        recommended: ['PHYS202', 'MATH301', 'CS403'], // Statistical Physics, Linear Algebra, ML
        focus: 'computational modeling and simulation'
    },
    'applied-physicist': {
        required: ['PHYS304', 'MAT301'], // Solid State, Electronic Materials
        recommended: ['PHYS303', 'EE301', 'MAT401'], // E&M II, Electronics, Nanomaterials
        focus: 'technology applications and materials'
    },
    
    // Data Science careers
    'data-scientist': {
        required: ['DS202', 'DS402'], // Machine Learning, Time Series
        recommended: ['DS401', 'DS303', 'MATH301'], // NLP, Visualization, Linear Algebra
        focus: 'statistical analysis and predictive modeling'
    },
    'bi-analyst': {
        required: ['DS403', 'DS303'], // Business Intelligence, Visualization
        recommended: ['DS101', 'ECON301', 'FIN202'], // Intro to DS, Econometrics, Investments
        focus: 'business analytics and reporting'
    },
    
    // Materials Science careers
    'nano-engineer': {
        required: ['MAT305', 'MAT402', 'MAT408'], // Nanomaterials, Advanced Semi, Quantum
        recommended: ['MAT204', 'MAT406', 'MAT308'], // Characterization, Surface, Computational
        focus: 'nanoscale materials synthesis, characterization, and applications'
    },
    'battery-engineer': {
        required: ['MAT401', 'MAT403'], // Energy Storage, Sustainable Energy
        recommended: ['MAT203', 'MAT301', 'MAT309'], // Electronic Props, Polymers, Corrosion
        focus: 'energy storage materials and electrochemical systems'
    },
    'semiconductor-engineer': {
        required: ['MAT203', 'MAT402'], // Electronic Properties, Advanced Semiconductors
        recommended: ['MAT305', 'MAT406', 'MAT206'], // Nano, Surface, Crystallography
        focus: 'electronic materials for semiconductor devices'
    },
    'biomaterials-engineer': {
        required: ['MAT306'], // Biomaterials
        recommended: ['MAT301', 'MAT302', 'MAT309'], // Polymers, Ceramics, Corrosion
        focus: 'biocompatible materials for medical applications'
    },
    'polymer-engineer': {
        required: ['MAT301', 'MAT304'], // Polymers, Composites
        recommended: ['MAT205', 'MAT404', 'MAT309'], // Processing, Adv Manufacturing, Corrosion
        focus: 'polymer synthesis, processing, and composite materials'
    },
    'metallurgist': {
        required: ['MAT303', 'MAT309'], // Metallic Materials, Corrosion
        recommended: ['MAT201', 'MAT202', 'MAT405'], // Thermo, Mechanical, Failure
        focus: 'metal alloys, processing, and heat treatment'
    },
    'failure-analyst': {
        required: ['MAT405', 'MAT202'], // Failure Analysis, Mechanical Behavior
        recommended: ['MAT309', 'MAT204', 'MAT303'], // Corrosion, Characterization, Metals
        focus: 'failure mechanisms, forensic analysis, and reliability'
    },
    'computational-materials': {
        required: ['MAT308'], // Computational Materials
        recommended: ['MAT201', 'CS201', 'MATH301'], // Thermo, Data Structures, Linear Algebra
        focus: 'computational modeling and simulation of materials'
    },
    
    // Chemistry careers - expanded course requirements
    'pharmaceutical-chemist': {
        required: ['CHEM201', 'CHEM202', 'CHEM402', 'CHEM404'], 
        recommended: ['CHEM303', 'CHEM408', 'PHAR201', 'BIO201', 'CHEM301', 'CHEM403'],
        focus: 'drug design, synthesis, and pharmaceutical development'
    },
    'analytical-chemist': {
        required: ['CHEM303', 'CHEM304', 'CHEM205', 'CHEM302'],
        recommended: ['CHEM305', 'CHEM409', 'STAT201', 'CHEM301', 'CHEM206', 'CS101'],
        focus: 'chemical analysis, instrumentation, and quality control'
    },
    'forensic-chemist': {
        required: ['CHEM303', 'CHEM308', 'CHEM309', 'CHEM304'],
        recommended: ['CJ301', 'BIO302', 'CHEM205', 'LAW101', 'CHEM402', 'PSY403'],
        focus: 'evidence analysis, toxicology, and criminal investigation'
    },
    'organic-synthesis': {
        required: ['CHEM201', 'CHEM202', 'CHEM306', 'CHEM203', 'CHEM204'],
        recommended: ['CHEM307', 'CHEM401', 'CHEM406', 'CHEM409', 'CHEM310', 'CHEM302'],
        focus: 'synthetic methodology and complex molecule synthesis'
    },
    'materials-chemist': {
        required: ['CHEM310', 'CHEM301', 'CHEM407', 'MAT101'],
        recommended: ['CHEM401', 'MAT301', 'CHEM302', 'CHEM406', 'PHYS301', 'CHEM405'],
        focus: 'polymer synthesis, materials characterization, and nanotechnology'
    },
    'environmental-chemist': {
        required: ['CHEM405', 'ENV201', 'CHEM301', 'CHEM303'],
        recommended: ['ENV301', 'CHEM309', 'BIO202', 'ENV302', 'CHEM205', 'GEO201'],
        focus: 'environmental monitoring, pollution control, and green chemistry'
    },
    
    // Environmental Science careers
    'climate-scientist': {
        required: ['ENV401', 'ENV403'],
        recommended: ['ENV404', 'MATH301', 'CS308'],
        focus: 'climate systems, modeling, and global change research'
    },
    'conservation-scientist': {
        required: ['ENV202', 'ENV407'],
        recommended: ['BIO303', 'ENV408', 'GIS301'],
        focus: 'biodiversity conservation, habitat management, and restoration'
    },
    'water-resource-specialist': {
        required: ['ENV302', 'ENV409'],
        recommended: ['ENV301', 'CE401', 'CHEM312'],
        focus: 'water quality assessment, watershed management, and treatment'
    },
    
    // Civil Engineering careers
    'structural-engineer': {
        required: ['CE201', 'CE301', 'CE302'],
        recommended: ['CE403', 'CE404', 'CE405'],
        focus: 'structural design, analysis, and seismic engineering'
    },
    'transportation-engineer': {
        required: ['CE303', 'CE406'],
        recommended: ['CE407', 'CE408', 'PLAN301'],
        focus: 'transportation planning, traffic flow, and infrastructure design'
    },
    'geotechnical-engineer': {
        required: ['CE202', 'CE410'],
        recommended: ['CE411', 'CE412', 'GEOL201'],
        focus: 'soil mechanics, foundation design, and ground improvement'
    },
    
    // Default for other careers
    'default': {
        required: [],
        recommended: [],
        focus: 'comprehensive foundation in the field'
    }
};

// Complete course catalog for ALL majors
const courseCatalog = {
    cs: [
        { id: 'CS101', name: 'Introduction to Programming', credits: 4, prerequisites: [], description: 'Fundamental programming concepts using Python', level: 'foundation' },
        { id: 'CS201', name: 'Data Structures and Algorithms', credits: 4, prerequisites: ['CS101'], description: 'Fundamental data structures and algorithm design', level: 'core' },
        { id: 'CS301', name: 'Computer Architecture', credits: 4, prerequisites: ['CS101'], description: 'Computer organization and system design', level: 'core' },
        { id: 'CS302', name: 'Operating Systems', credits: 4, prerequisites: ['CS201', 'CS301'], description: 'OS design and implementation', level: 'advanced' },
        { id: 'CS303', name: 'Database Systems', credits: 4, prerequisites: ['CS201'], description: 'Database design and management', level: 'core' },
        { id: 'CS304', name: 'Computer Networks', credits: 4, prerequisites: ['CS201'], description: 'Network protocols and architectures', level: 'core' },
        { id: 'CS401', name: 'Software Engineering', credits: 4, prerequisites: ['CS201'], description: 'Software development methodologies', level: 'advanced' },
        { id: 'CS402', name: 'Artificial Intelligence', credits: 4, prerequisites: ['CS201'], description: 'AI principles and algorithms', level: 'advanced' },
        { id: 'CS403', name: 'Machine Learning', credits: 4, prerequisites: ['CS201'], description: 'Statistical learning theory', level: 'advanced' },
        { id: 'CS404', name: 'Compiler Design', credits: 4, prerequisites: ['CS201', 'CS301'], description: 'Compiler construction principles', level: 'advanced' },
        { id: 'CS405', name: 'Computer Security', credits: 4, prerequisites: ['CS302', 'CS304'], description: 'Security principles and cryptography', level: 'advanced' },
        { id: 'CS406', name: 'Theory of Computation', credits: 4, prerequisites: ['CS201'], description: 'Automata and complexity theory', level: 'advanced' }
    ],
    'data-science': [
        { id: 'DS101', name: 'Introduction to Data Science', credits: 3, prerequisites: [], description: 'Fundamentals of data analysis and visualization', level: 'foundation' },
        { id: 'DS102', name: 'Statistical Methods', credits: 4, prerequisites: [], description: 'Probability and statistics for data science', level: 'foundation' },
        { id: 'DS201', name: 'Data Mining', credits: 4, prerequisites: ['DS101'], description: 'Extracting patterns from large datasets', level: 'core' },
        { id: 'DS202', name: 'Machine Learning for Data Science', credits: 4, prerequisites: ['DS102'], description: 'ML algorithms and applications', level: 'core' },
        { id: 'DS301', name: 'Big Data Analytics', credits: 4, prerequisites: ['DS201'], description: 'Processing and analyzing big data', level: 'advanced' },
        { id: 'DS302', name: 'Deep Learning', credits: 4, prerequisites: ['DS202'], description: 'Neural networks and deep learning', level: 'advanced' },
        { id: 'DS303', name: 'Data Visualization', credits: 3, prerequisites: ['DS101'], description: 'Creating effective data visualizations', level: 'core' },
        { id: 'DS401', name: 'Natural Language Processing', credits: 4, prerequisites: ['DS202'], description: 'Text analysis and NLP techniques', level: 'advanced' },
        { id: 'DS402', name: 'Time Series Analysis', credits: 4, prerequisites: ['DS102'], description: 'Analyzing temporal data', level: 'advanced' },
        { id: 'DS403', name: 'Business Intelligence', credits: 3, prerequisites: ['DS201'], description: 'BI tools and techniques', level: 'advanced' }
    ],
    ee: [
        { id: 'EE101', name: 'Circuit Analysis I', credits: 4, prerequisites: [], description: 'DC circuit analysis and theorems', level: 'foundation' },
        { id: 'EE201', name: 'Circuit Analysis II', credits: 4, prerequisites: ['EE101'], description: 'AC circuit analysis and power', level: 'core' },
        { id: 'EE202', name: 'Signals and Systems', credits: 4, prerequisites: ['EE201'], description: 'Signal analysis in time and frequency', level: 'core' },
        { id: 'EE203', name: 'Electromagnetics I', credits: 4, prerequisites: [], description: 'Static electric and magnetic fields', level: 'core' },
        { id: 'EE301', name: 'Electronics I', credits: 4, prerequisites: ['EE201'], description: 'Semiconductor devices and amplifiers', level: 'core' },
        { id: 'EE302', name: 'Digital Logic Design', credits: 4, prerequisites: ['EE101'], description: 'Digital circuits and system design', level: 'core' },
        { id: 'EE303', name: 'Control Systems', credits: 4, prerequisites: ['EE202'], description: 'Feedback control system analysis', level: 'advanced' },
        { id: 'EE304', name: 'Communication Systems', credits: 4, prerequisites: ['EE202'], description: 'Analog and digital communications', level: 'advanced' },
        { id: 'EE305', name: 'Power Systems', credits: 4, prerequisites: ['EE201'], description: 'Power generation and distribution', level: 'advanced' },
        { id: 'EE401', name: 'Microprocessor Systems', credits: 4, prerequisites: ['EE302'], description: 'Microprocessor architecture and embedded systems', level: 'advanced' },
        { id: 'EE402', name: 'VLSI Design', credits: 4, prerequisites: ['EE301', 'EE302'], description: 'CMOS VLSI design principles', level: 'advanced' },
        { id: 'EE403', name: 'RF and Microwave Engineering', credits: 4, prerequisites: ['EE203', 'EE304'], description: 'High-frequency circuit design', level: 'advanced' }
    ],
    me: [
        { id: 'ME101', name: 'Engineering Mechanics - Statics', credits: 3, prerequisites: [], description: 'Forces and equilibrium in static systems', level: 'foundation' },
        { id: 'ME102', name: 'Engineering Mechanics - Dynamics', credits: 3, prerequisites: ['ME101'], description: 'Motion and forces in dynamic systems', level: 'foundation' },
        { id: 'ME201', name: 'Thermodynamics I', credits: 4, prerequisites: [], description: 'Energy, heat, and work principles', level: 'core' },
        { id: 'ME202', name: 'Fluid Mechanics', credits: 4, prerequisites: ['ME102'], description: 'Fluid statics and dynamics', level: 'core' },
        { id: 'ME203', name: 'Mechanics of Materials', credits: 4, prerequisites: ['ME101'], description: 'Stress, strain, and material behavior', level: 'core' },
        { id: 'ME301', name: 'Heat Transfer', credits: 4, prerequisites: ['ME201', 'ME202'], description: 'Conduction, convection, and radiation', level: 'advanced' },
        { id: 'ME302', name: 'Machine Design', credits: 4, prerequisites: ['ME203'], description: 'Design of mechanical components', level: 'advanced' },
        { id: 'ME303', name: 'Manufacturing Processes', credits: 3, prerequisites: ['ME203'], description: 'Manufacturing methods and processes', level: 'advanced' },
        { id: 'ME401', name: 'Control Systems', credits: 4, prerequisites: ['ME102'], description: 'Feedback control for mechanical systems', level: 'advanced' },
        { id: 'ME402', name: 'Robotics', credits: 4, prerequisites: ['ME401'], description: 'Robot kinematics and control', level: 'advanced' }
    ],
    physics: [
        { id: 'PHYS101', name: 'Classical Mechanics I', credits: 4, prerequisites: [], description: 'Newtonian mechanics and conservation laws', level: 'foundation' },
        { id: 'PHYS102', name: 'Electricity and Magnetism I', credits: 4, prerequisites: ['PHYS101'], description: 'Electromagnetic theory fundamentals', level: 'foundation' },
        { id: 'PHYS201', name: 'Quantum Mechanics I', credits: 4, prerequisites: ['PHYS102'], description: 'Introduction to quantum mechanics', level: 'core' },
        { id: 'PHYS202', name: 'Thermal and Statistical Physics', credits: 4, prerequisites: ['PHYS201'], description: 'Thermodynamics and statistical mechanics', level: 'core' },
        { id: 'PHYS301', name: 'Classical Mechanics II', credits: 4, prerequisites: ['PHYS101'], description: 'Advanced classical mechanics', level: 'advanced' },
        { id: 'PHYS302', name: 'Quantum Mechanics II', credits: 4, prerequisites: ['PHYS201'], description: 'Advanced quantum mechanics', level: 'advanced' },
        { id: 'PHYS303', name: 'Electromagnetism II', credits: 4, prerequisites: ['PHYS102'], description: 'Advanced electromagnetic theory', level: 'advanced' },
        { id: 'PHYS304', name: 'Solid State Physics', credits: 4, prerequisites: ['PHYS201'], description: 'Physics of crystalline solids', level: 'advanced' },
        { id: 'PHYS401', name: 'Nuclear and Particle Physics', credits: 4, prerequisites: ['PHYS302'], description: 'Nuclear structure and particles', level: 'advanced' },
        { id: 'PHYS402', name: 'General Relativity', credits: 4, prerequisites: ['PHYS301'], description: 'Einstein\'s theory of gravitation', level: 'advanced' }
    ],
    materials: [
        { id: 'MAT101', name: 'Introduction to Materials Science', credits: 4, prerequisites: [], description: 'Crystal structures, bonding, defects, and basic properties', level: 'foundation' },
        { id: 'MAT102', name: 'Materials Chemistry', credits: 3, prerequisites: [], description: 'Chemical principles in materials science', level: 'foundation' },
        { id: 'MAT103', name: 'Materials Physics', credits: 3, prerequisites: [], description: 'Physical properties and quantum mechanics applications', level: 'foundation' },
        { id: 'MAT104', name: 'Materials Laboratory I', credits: 2, prerequisites: [], description: 'Basic characterization techniques and experiments', level: 'foundation' },
        { id: 'MAT201', name: 'Thermodynamics of Materials', credits: 4, prerequisites: ['MAT101'], description: 'Phase diagrams, phase transformations, thermodynamics', level: 'core' },
        { id: 'MAT202', name: 'Mechanical Behavior of Materials', credits: 4, prerequisites: ['MAT101'], description: 'Stress-strain, deformation, fracture, fatigue', level: 'core' },
        { id: 'MAT203', name: 'Electronic Properties of Materials', credits: 4, prerequisites: ['MAT103'], description: 'Band theory, semiconductors, conductors, insulators', level: 'core' },
        { id: 'MAT204', name: 'Materials Characterization', credits: 4, prerequisites: ['MAT104'], description: 'XRD, electron microscopy, spectroscopy techniques', level: 'core' },
        { id: 'MAT205', name: 'Materials Processing', credits: 3, prerequisites: ['MAT101'], description: 'Casting, forming, joining, powder processing', level: 'core' },
        { id: 'MAT206', name: 'Crystallography and Diffraction', credits: 3, prerequisites: ['MAT101'], description: 'Crystal systems, symmetry, diffraction theory', level: 'core' },
        { id: 'MAT301', name: 'Polymer Science and Engineering', credits: 4, prerequisites: ['MAT102', 'MAT201'], description: 'Polymer synthesis, structure-property relationships', level: 'advanced' },
        { id: 'MAT302', name: 'Ceramic Materials', credits: 4, prerequisites: ['MAT201'], description: 'Ceramic structures, processing, properties', level: 'advanced' },
        { id: 'MAT303', name: 'Metallic Materials', credits: 4, prerequisites: ['MAT202'], description: 'Alloy theory, steel metallurgy, heat treatment', level: 'advanced' },
        { id: 'MAT304', name: 'Composite Materials', credits: 4, prerequisites: ['MAT202'], description: 'Fiber-reinforced composites, design, manufacturing', level: 'advanced' },
        { id: 'MAT305', name: 'Nanomaterials and Nanotechnology', credits: 4, prerequisites: ['MAT203', 'MAT204'], description: 'Synthesis and applications of nanoscale materials', level: 'advanced' },
        { id: 'MAT306', name: 'Biomaterials', credits: 3, prerequisites: ['MAT301'], description: 'Medical implants, tissue engineering, biocompatibility', level: 'advanced' },
        { id: 'MAT307', name: 'Magnetic and Optical Materials', credits: 3, prerequisites: ['MAT203'], description: 'Ferromagnetism, optical properties, photonics', level: 'advanced' },
        { id: 'MAT308', name: 'Computational Materials Science', credits: 3, prerequisites: ['MAT201'], description: 'Molecular dynamics, DFT, phase field modeling', level: 'advanced' },
        { id: 'MAT309', name: 'Corrosion and Degradation', credits: 3, prerequisites: ['MAT102', 'MAT303'], description: 'Corrosion mechanisms, protection methods', level: 'advanced' },
        { id: 'MAT310', name: 'Materials Laboratory II', credits: 2, prerequisites: ['MAT204'], description: 'Advanced characterization and synthesis experiments', level: 'advanced' },
        { id: 'MAT401', name: 'Energy Storage Materials', credits: 4, prerequisites: ['MAT203', 'MAT301'], description: 'Battery materials, fuel cells, supercapacitors', level: 'specialized' },
        { id: 'MAT402', name: 'Advanced Semiconductor Materials', credits: 4, prerequisites: ['MAT203', 'MAT305'], description: 'Wide bandgap semiconductors, 2D materials, quantum dots', level: 'specialized' },
        { id: 'MAT403', name: 'Materials for Sustainable Energy', credits: 3, prerequisites: ['MAT401'], description: 'Solar cells, thermoelectrics, energy harvesting', level: 'specialized' },
        { id: 'MAT404', name: 'Advanced Manufacturing', credits: 3, prerequisites: ['MAT205', 'MAT304'], description: '3D printing, additive manufacturing, smart manufacturing', level: 'specialized' },
        { id: 'MAT405', name: 'Materials Failure Analysis', credits: 3, prerequisites: ['MAT202', 'MAT309'], description: 'Failure mechanisms, forensic analysis, case studies', level: 'specialized' },
        { id: 'MAT406', name: 'Surface Science and Engineering', credits: 3, prerequisites: ['MAT204', 'MAT309'], description: 'Surface phenomena, coatings, thin films', level: 'specialized' },
        { id: 'MAT407', name: 'Materials Design and Selection', credits: 3, prerequisites: ['MAT303', 'MAT304'], description: 'Selection methodology, Ashby charts, optimization', level: 'specialized' },
        { id: 'MAT408', name: 'Quantum Materials', credits: 3, prerequisites: ['MAT203'], description: 'Superconductors, topological insulators, quantum phenomena', level: 'specialized' },
        { id: 'MAT409', name: 'Materials Entrepreneurship', credits: 2, prerequisites: ['MAT301', 'MAT302', 'MAT303'], description: 'Technology commercialization, IP, startups', level: 'specialized' },
        { id: 'MAT410', name: 'Senior Design Project', credits: 4, prerequisites: ['MAT310'], description: 'Capstone design project in materials engineering', level: 'specialized' }
    ]
};

// Add more course catalogs for other majors (using simplified versions for now)
const additionalCatalogs = {
    civil: ['CE101', 'CE201', 'CE202', 'CE203', 'CE301', 'CE302', 'CE303', 'CE401', 'CE402'],
    chemeng: ['CHE101', 'CHE201', 'CHE202', 'CHE301', 'CHE302', 'CHE303', 'CHE401', 'CHE402'],
    bme: ['BME101', 'BME201', 'BME202', 'BME301', 'BME302', 'BME401', 'BME402'],
    chemistry: ['CHEM101', 'CHEM102', 'CHEM201', 'CHEM202', 'CHEM301', 'CHEM302', 'CHEM303', 'CHEM401', 'CHEM402'],
    environment: ['ENV101', 'ENV201', 'ENV202', 'ENV301', 'ENV302', 'ENV401', 'ENV402']
};

// Major categories with complete mapping
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

// Career paths for each major
const careerPaths = {
    cs: [
        { id: 'software-engineer', name: 'Software Engineer', icon: 'code', description: 'Build scalable applications' },
        { id: 'ml-engineer', name: 'Machine Learning Engineer', icon: 'robot', description: 'Develop AI/ML systems' },
        { id: 'data-engineer', name: 'Data Engineer', icon: 'database', description: 'Build data pipelines' }
    ],
    'data-science': [
        { id: 'data-scientist', name: 'Data Scientist', icon: 'chart-line', description: 'Analyze complex datasets' },
        { id: 'ml-engineer', name: 'ML Engineer', icon: 'brain', description: 'Build ML models' },
        { id: 'bi-analyst', name: 'Business Intelligence Analyst', icon: 'chart-pie', description: 'Business insights from data' }
    ],
    ee: [
        { id: 'embedded-engineer', name: 'Embedded Systems Engineer', icon: 'microchip', description: 'Firmware and embedded systems' },
        { id: 'rf-engineer', name: 'RF Engineer', icon: 'wifi', description: 'Wireless communication systems' },
        { id: 'power-engineer', name: 'Power Systems Engineer', icon: 'plug', description: 'Power generation and distribution' }
    ],
    me: [
        { id: 'robotics-engineer', name: 'Robotics Engineer', icon: 'robot', description: 'Design and build robots' },
        { id: 'thermal-engineer', name: 'Thermal Systems Engineer', icon: 'fire', description: 'Heat and energy systems' },
        { id: 'design-engineer', name: 'Mechanical Design Engineer', icon: 'drafting-compass', description: 'Product design and development' }
    ],
    physics: [
        { id: 'research-physicist', name: 'Research Physicist', icon: 'atom', description: 'Theoretical and experimental research' },
        { id: 'computational-physicist', name: 'Computational Physicist', icon: 'calculator', description: 'Simulations and modeling' },
        { id: 'applied-physicist', name: 'Applied Physicist', icon: 'cogs', description: 'Technology applications' }
    ],
    materials: [
        { id: 'nano-engineer', name: 'Nanomaterials Engineer', icon: 'atom', description: 'Design nanoscale materials for advanced applications' },
        { id: 'battery-engineer', name: 'Battery/Energy Storage Engineer', icon: 'battery-full', description: 'Develop materials for energy storage systems' },
        { id: 'semiconductor-engineer', name: 'Semiconductor Materials Engineer', icon: 'microchip', description: 'Work on electronic materials for chips and devices' },
        { id: 'biomaterials-engineer', name: 'Biomaterials Engineer', icon: 'dna', description: 'Develop materials for medical implants and tissue engineering' },
        { id: 'polymer-engineer', name: 'Polymer Engineer', icon: 'link', description: 'Design and process polymer materials and composites' },
        { id: 'metallurgist', name: 'Metallurgical Engineer', icon: 'hammer', description: 'Develop and process metallic materials and alloys' },
        { id: 'failure-analyst', name: 'Materials Failure Analyst', icon: 'search', description: 'Investigate material failures and improve reliability' },
        { id: 'computational-materials', name: 'Computational Materials Scientist', icon: 'calculator', description: 'Model and simulate materials using computational methods' }
    ],
    chemistry: [
        { id: 'pharmaceutical-chemist', name: 'Pharmaceutical Chemist', icon: 'pills', description: 'Drug discovery and development' },
        { id: 'analytical-chemist', name: 'Analytical Chemist', icon: 'flask', description: 'Chemical analysis and quality control' },
        { id: 'organic-synthesis', name: 'Organic Synthesis Chemist', icon: 'atom', description: 'Design and synthesize organic compounds' },
        { id: 'forensic-chemist', name: 'Forensic Chemist', icon: 'fingerprint', description: 'Criminal investigation and evidence analysis' },
        { id: 'materials-chemist', name: 'Materials Chemist', icon: 'cubes', description: 'Develop new materials and polymers' },
        { id: 'environmental-chemist', name: 'Environmental Chemist', icon: 'leaf', description: 'Study chemical processes in environment' }
    ],
    environment: [
        { id: 'climate-scientist', name: 'Climate Scientist', icon: 'cloud-sun', description: 'Study climate change and modeling' },
        { id: 'environmental-consultant', name: 'Environmental Consultant', icon: 'briefcase', description: 'Environmental impact assessment' },
        { id: 'conservation-scientist', name: 'Conservation Scientist', icon: 'tree', description: 'Ecosystem and wildlife conservation' },
        { id: 'water-resource-specialist', name: 'Water Resource Specialist', icon: 'water', description: 'Water quality and management' },
        { id: 'sustainability-manager', name: 'Sustainability Manager', icon: 'recycle', description: 'Corporate sustainability programs' },
        { id: 'air-quality-specialist', name: 'Air Quality Specialist', icon: 'wind', description: 'Air pollution monitoring and control' }
    ],
    civil: [
        { id: 'structural-engineer', name: 'Structural Engineer', icon: 'building', description: 'Design buildings and bridges' },
        { id: 'transportation-engineer', name: 'Transportation Engineer', icon: 'road', description: 'Design transportation systems' },
        { id: 'water-resources-engineer', name: 'Water Resources Engineer', icon: 'tint', description: 'Water supply and treatment systems' },
        { id: 'geotechnical-engineer', name: 'Geotechnical Engineer', icon: 'mountain', description: 'Soil and foundation engineering' },
        { id: 'construction-manager', name: 'Construction Manager', icon: 'hard-hat', description: 'Manage construction projects' },
        { id: 'environmental-engineer', name: 'Environmental Engineer', icon: 'leaf', description: 'Environmental protection systems' }
    ],
    chemeng: [
        { id: 'process-engineer', name: 'Process Engineer', icon: 'industry', description: 'Design and optimize chemical processes' },
        { id: 'petrochemical-engineer', name: 'Petrochemical Engineer', icon: 'oil-can', description: 'Oil and gas processing' },
        { id: 'pharmaceutical-engineer', name: 'Pharmaceutical Engineer', icon: 'prescription', description: 'Drug manufacturing processes' },
        { id: 'biotechnology-engineer', name: 'Biotechnology Engineer', icon: 'dna', description: 'Bioprocessing and fermentation' }
    ],
    bme: [
        { id: 'medical-device-engineer', name: 'Medical Device Engineer', icon: 'heartbeat', description: 'Design medical devices and implants' },
        { id: 'clinical-engineer', name: 'Clinical Engineer', icon: 'hospital', description: 'Hospital equipment management' },
        { id: 'tissue-engineer', name: 'Tissue Engineer', icon: 'dna', description: 'Regenerative medicine and tissue engineering' },
        { id: 'imaging-engineer', name: 'Medical Imaging Engineer', icon: 'x-ray', description: 'Develop imaging technologies' }
    ],
    economics: [
        { id: 'financial-economist', name: 'Financial Economist', icon: 'chart-line', description: 'Financial markets analysis' },
        { id: 'policy-economist', name: 'Policy Economist', icon: 'landmark', description: 'Economic policy analysis' },
        { id: 'data-economist', name: 'Economic Data Analyst', icon: 'database', description: 'Economic data and forecasting' },
        { id: 'behavioral-economist', name: 'Behavioral Economist', icon: 'brain', description: 'Psychology in economic decisions' }
    ],
    finance: [
        { id: 'investment-banker', name: 'Investment Banker', icon: 'building', description: 'Mergers, acquisitions, and capital raising' },
        { id: 'portfolio-manager', name: 'Portfolio Manager', icon: 'chart-pie', description: 'Manage investment portfolios' },
        { id: 'risk-analyst', name: 'Risk Analyst', icon: 'shield-alt', description: 'Financial risk assessment' },
        { id: 'quant-analyst', name: 'Quantitative Analyst', icon: 'calculator', description: 'Mathematical finance and trading' }
    ],
    psychology: [
        { id: 'clinical-psychologist', name: 'Clinical Psychologist', icon: 'user-md', description: 'Mental health treatment' },
        { id: 'neuropsychologist', name: 'Neuropsychologist', icon: 'brain', description: 'Brain-behavior relationships' },
        { id: 'organizational-psychologist', name: 'I/O Psychologist', icon: 'users', description: 'Workplace psychology' },
        { id: 'forensic-psychologist', name: 'Forensic Psychologist', icon: 'gavel', description: 'Psychology in legal system' }
    ],
    policy: [
        { id: 'policy-analyst', name: 'Policy Analyst', icon: 'clipboard', description: 'Analyze and develop public policy' },
        { id: 'campaign-manager', name: 'Campaign Manager', icon: 'vote-yea', description: 'Political campaign management' },
        { id: 'diplomat', name: 'Foreign Service Officer', icon: 'globe', description: 'International relations and diplomacy' },
        { id: 'intelligence-analyst', name: 'Intelligence Analyst', icon: 'user-secret', description: 'Security and intelligence analysis' }
    ],
    education: [
        { id: 'elementary-teacher', name: 'Elementary Teacher', icon: 'child', description: 'Teach elementary school students' },
        { id: 'secondary-teacher', name: 'Secondary Teacher', icon: 'chalkboard-teacher', description: 'Teach middle/high school' },
        { id: 'special-ed-teacher', name: 'Special Education Teacher', icon: 'hands-helping', description: 'Teach students with disabilities' },
        { id: 'curriculum-designer', name: 'Curriculum Designer', icon: 'book-open', description: 'Design educational programs' }
    ],
    medicine: [
        { id: 'physician', name: 'Physician (MD)', icon: 'user-md', description: 'Medical doctor - various specialties' },
        { id: 'surgeon', name: 'Surgeon', icon: 'procedures', description: 'Surgical specialist' },
        { id: 'medical-researcher', name: 'Medical Researcher', icon: 'microscope', description: 'Biomedical research' },
        { id: 'psychiatrist', name: 'Psychiatrist', icon: 'brain', description: 'Mental health physician' }
    ],
    nursing: [
        { id: 'clinical-nurse', name: 'Clinical Nurse (RN)', icon: 'user-nurse', description: 'Direct patient care' },
        { id: 'nurse-practitioner', name: 'Nurse Practitioner', icon: 'stethoscope', description: 'Advanced practice nursing' },
        { id: 'critical-care-nurse', name: 'Critical Care Nurse', icon: 'heartbeat', description: 'ICU and emergency care' },
        { id: 'pediatric-nurse', name: 'Pediatric Nurse', icon: 'baby', description: 'Child healthcare' }
    ],
    pharmacy: [
        { id: 'clinical-pharmacist', name: 'Clinical Pharmacist', icon: 'pills', description: 'Hospital and clinical pharmacy' },
        { id: 'retail-pharmacist', name: 'Retail Pharmacist', icon: 'store', description: 'Community pharmacy practice' },
        { id: 'pharmaceutical-scientist', name: 'Pharmaceutical Scientist', icon: 'flask', description: 'Drug development and research' },
        { id: 'regulatory-pharmacist', name: 'Regulatory Affairs Specialist', icon: 'clipboard-check', description: 'Drug regulation and compliance' }
    ],
    'public-health': [
        { id: 'epidemiologist', name: 'Epidemiologist', icon: 'virus', description: 'Disease patterns and prevention' },
        { id: 'health-policy-analyst', name: 'Health Policy Analyst', icon: 'clipboard', description: 'Healthcare policy development' },
        { id: 'biostatistician', name: 'Biostatistician', icon: 'chart-bar', description: 'Health data analysis' },
        { id: 'global-health', name: 'Global Health Specialist', icon: 'globe', description: 'International health programs' }
    ],
    nutrition: [
        { id: 'clinical-dietitian', name: 'Clinical Dietitian', icon: 'heartbeat', description: 'Medical nutrition therapy' },
        { id: 'sports-nutritionist', name: 'Sports Nutritionist', icon: 'running', description: 'Athletic performance nutrition' },
        { id: 'food-scientist', name: 'Food Scientist', icon: 'flask', description: 'Food development and safety' },
        { id: 'community-nutritionist', name: 'Community Nutritionist', icon: 'users', description: 'Public health nutrition' }
    ],
    'criminal-justice': [
        { id: 'detective', name: 'Criminal Investigator', icon: 'search', description: 'Criminal investigation and evidence' },
        { id: 'forensic-analyst', name: 'Forensic Analyst', icon: 'fingerprint', description: 'Crime scene and evidence analysis' },
        { id: 'corrections-officer', name: 'Corrections Specialist', icon: 'lock', description: 'Rehabilitation and corrections' },
        { id: 'probation-officer', name: 'Probation Officer', icon: 'balance-scale', description: 'Offender supervision and rehabilitation' }
    ],
    law: [
        { id: 'corporate-lawyer', name: 'Corporate Lawyer', icon: 'briefcase', description: 'Business and corporate law' },
        { id: 'criminal-lawyer', name: 'Criminal Defense Lawyer', icon: 'gavel', description: 'Criminal defense and prosecution' },
        { id: 'environmental-lawyer', name: 'Environmental Lawyer', icon: 'leaf', description: 'Environmental law and regulation' },
        { id: 'patent-lawyer', name: 'Patent Attorney', icon: 'lightbulb', description: 'Intellectual property law' }
    ],
    architecture: [
        { id: 'residential-architect', name: 'Residential Architect', icon: 'home', description: 'Design homes and residential buildings' },
        { id: 'commercial-architect', name: 'Commercial Architect', icon: 'building', description: 'Design commercial and office buildings' },
        { id: 'landscape-architect', name: 'Landscape Architect', icon: 'tree', description: 'Design outdoor spaces and landscapes' },
        { id: 'urban-planner', name: 'Urban Planner', icon: 'city', description: 'City and regional planning' }
    ],
    communications: [
        { id: 'journalist', name: 'Journalist', icon: 'newspaper', description: 'News reporting and writing' },
        { id: 'pr-specialist', name: 'Public Relations Specialist', icon: 'bullhorn', description: 'Public relations and communications' },
        { id: 'digital-marketer', name: 'Digital Marketing Specialist', icon: 'mobile-alt', description: 'Digital media and marketing' },
        { id: 'broadcast-producer', name: 'Broadcast Producer', icon: 'tv', description: 'Television and radio production' }
    ],
    default: [
        { id: 'researcher', name: 'Researcher', icon: 'microscope', description: 'Research and development' },
        { id: 'educator', name: 'Educator', icon: 'chalkboard-teacher', description: 'Teaching and education' },
        { id: 'consultant', name: 'Industry Consultant', icon: 'user-tie', description: 'Professional consulting' }
    ]
};

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 AI Path Advisor - Career-Based Course Selection');
    initializeApp();
});

function initializeApp() {
    showStep(1);
    setupEventListeners();
    console.log('✅ Application initialized');
}

function setupEventListeners() {
    // Navigation buttons
    const nextBtn = document.getElementById('next-btn');
    const prevBtn = document.getElementById('prev-btn');
    
    if (nextBtn) {
        nextBtn.replaceWith(nextBtn.cloneNode(true));
        document.getElementById('next-btn').addEventListener('click', handleNext);
    }
    
    if (prevBtn) {
        prevBtn.replaceWith(prevBtn.cloneNode(true));
        document.getElementById('prev-btn').addEventListener('click', handlePrevious);
    }
    
    // Field cards
    document.querySelectorAll('.field-card').forEach(card => {
        card.style.cursor = 'pointer';
        card.addEventListener('click', function() {
            selectField(this.dataset.category);
        });
    });
    
    // Preference sliders
    const hoursSlider = document.getElementById('hours-slider');
    if (hoursSlider) {
        hoursSlider.addEventListener('input', function() {
            const display = document.getElementById('hours-value');
            if (display) display.textContent = this.value + ' hours/week';
        });
    }
}

function selectField(category) {
    console.log('Selected field:', category);
    selectedCategory = category;
    
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
    
    enableNext();
}

function showMajors() {
    const majorGrid = document.getElementById('major-grid');
    if (!majorGrid) return;
    
    const majors = majorsByCategory[selectedCategory] || [];
    majorGrid.innerHTML = '';
    
    majors.forEach(major => {
        const card = document.createElement('div');
        card.className = 'major-card';
        card.dataset.major = major.id;
        card.style.cursor = 'pointer';
        card.innerHTML = `
            <div style="font-size: 2rem; color: var(--primary-accent); margin-bottom: 1rem;">
                <i class="fas fa-${major.icon}"></i>
            </div>
            <h3>${major.name}</h3>
            <p style="color: var(--text-secondary);">${major.description}</p>
        `;
        card.addEventListener('click', () => selectMajor(major));
        majorGrid.appendChild(card);
    });
}

function selectMajor(major) {
    console.log('Selected major:', major.name);
    selectedMajor = major.id;
    availableCourses = courseCatalog[major.id] || generateDefaultCourses(major.id);
    
    document.querySelectorAll('.major-card').forEach(card => {
        if (card.dataset.major === major.id) {
            card.style.borderColor = 'var(--primary-accent)';
            card.style.background = 'linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)';
        } else {
            card.style.borderColor = '';
            card.style.background = '';
        }
    });
    
    enableNext();
}

function showCareerSelection() {
    const container = document.querySelector('.career-grid');
    if (!container) return;
    
    const careers = careerPaths[selectedMajor] || careerPaths.default;
    
    container.innerHTML = `
        <div style="width: 100%;">
            <h3 style="margin-bottom: 1rem;">Choose Your Career Path</h3>
            <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">
                Your career choice will determine which courses are recommended for your learning path
            </p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem;">
                ${careers.map(career => `
                    <div class="career-option" data-career="${career.id}" 
                         style="padding: 1.5rem; border: 2px solid var(--border-color); 
                                border-radius: 12px; cursor: pointer; transition: all 0.3s ease;
                                background: var(--card-bg);">
                        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                            <i class="fas fa-${career.icon}" style="font-size: 2rem; color: var(--primary-accent); margin-right: 1rem;"></i>
                            <h4 style="margin: 0;">${career.name}</h4>
                        </div>
                        <p style="color: var(--text-secondary); margin: 0;">${career.description}</p>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
    
    // Add event listeners
    document.querySelectorAll('.career-option').forEach(card => {
        card.addEventListener('click', function() {
            selectCareerAndShowCourses(this.dataset.career);
        });
    });
}

function selectCareerAndShowCourses(careerId) {
    console.log('Selected career:', careerId);
    selectedCareer = careerId;
    
    // Highlight selected career
    document.querySelectorAll('.career-option').forEach(card => {
        if (card.dataset.career === careerId) {
            card.style.borderColor = 'var(--primary-accent)';
            card.style.background = 'linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)';
        } else {
            card.style.borderColor = '';
            card.style.background = '';
        }
    });
    
    // Show career-specific courses
    showCareerBasedCourses(careerId);
}

function showCareerBasedCourses(careerId) {
    const container = document.querySelector('.career-grid');
    if (!container) return;
    
    // Get career-specific course recommendations
    const careerMapping = careerCourseMapping[careerId] || careerCourseMapping.default;
    const requiredCourses = careerMapping.required || [];
    const recommendedCourses = careerMapping.recommended || [];
    
    // Categorize courses
    const categorizedCourses = {
        required: [],
        recommended: [],
        foundation: [],
        elective: []
    };
    
    availableCourses.forEach(course => {
        if (requiredCourses.includes(course.id)) {
            categorizedCourses.required.push(course);
        } else if (recommendedCourses.includes(course.id)) {
            categorizedCourses.recommended.push(course);
        } else if (course.level === 'foundation') {
            categorizedCourses.foundation.push(course);
        } else {
            categorizedCourses.elective.push(course);
        }
    });
    
    // Build the course selection UI
    let html = `
        <div style="width: 100%; margin-top: 2rem;">
            <h3>Select Courses for Your ${getCareerName(careerId)} Path</h3>
            <p style="color: var(--text-secondary); margin-bottom: 1rem;">
                Courses are organized based on your career focus: <strong>${careerMapping.focus}</strong>
            </p>
            
            <!-- Required Courses -->
            ${categorizedCourses.required.length > 0 ? `
                <div style="margin-bottom: 2rem;">
                    <h4 style="color: var(--primary-accent); margin-bottom: 1rem;">
                        <i class="fas fa-star"></i> Required for ${getCareerName(careerId)}
                    </h4>
                    <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                                padding: 1rem; border-radius: 8px; border: 2px solid var(--primary-accent);">
                        ${categorizedCourses.required.map(course => createCourseCard(course, 'required')).join('')}
                    </div>
                </div>
            ` : ''}
            
            <!-- Recommended Courses -->
            ${categorizedCourses.recommended.length > 0 ? `
                <div style="margin-bottom: 2rem;">
                    <h4 style="color: #ff9800; margin-bottom: 1rem;">
                        <i class="fas fa-thumbs-up"></i> Highly Recommended
                    </h4>
                    <div style="background: rgba(255, 152, 0, 0.1); padding: 1rem; border-radius: 8px; 
                                border: 2px solid #ff9800;">
                        ${categorizedCourses.recommended.map(course => createCourseCard(course, 'recommended')).join('')}
                    </div>
                </div>
            ` : ''}
            
            <!-- Foundation Courses -->
            ${categorizedCourses.foundation.length > 0 ? `
                <div style="margin-bottom: 2rem;">
                    <h4 style="color: #4caf50; margin-bottom: 1rem;">
                        <i class="fas fa-graduation-cap"></i> Foundation Courses
                    </h4>
                    <div style="background: rgba(76, 175, 80, 0.1); padding: 1rem; border-radius: 8px;">
                        ${categorizedCourses.foundation.map(course => createCourseCard(course, 'foundation')).join('')}
                    </div>
                </div>
            ` : ''}
            
            <!-- Elective Courses -->
            ${categorizedCourses.elective.length > 0 ? `
                <div style="margin-bottom: 2rem;">
                    <h4 style="color: var(--text-secondary); margin-bottom: 1rem;">
                        <i class="fas fa-book"></i> Additional Electives
                    </h4>
                    <div style="background: var(--secondary-bg); padding: 1rem; border-radius: 8px;">
                        ${categorizedCourses.elective.map(course => createCourseCard(course, 'elective')).join('')}
                    </div>
                </div>
            ` : ''}
            
            <div style="padding: 1rem; background: var(--secondary-bg); border-radius: 8px; margin-bottom: 1rem;">
                <strong>Selected: <span id="course-count">0</span> courses | 
                Total Credits: <span id="credit-count">0</span></strong>
                <div id="selected-summary" style="margin-top: 0.5rem; color: var(--text-secondary);"></div>
            </div>
        </div>
    `;
    
    container.innerHTML = html;
    
    // Pre-select required courses
    setTimeout(() => {
        categorizedCourses.required.forEach(course => {
            const checkbox = document.querySelector(`#course-${course.id}`);
            if (checkbox) {
                checkbox.checked = true;
            }
        });
        updateCourseSelection();
    }, 100);
    
    // Add event listeners
    document.querySelectorAll('.course-check').forEach(cb => {
        cb.addEventListener('change', updateCourseSelection);
    });
    
    enableNext();
}

function createCourseCard(course, type) {
    const typeStyles = {
        required: 'border-left: 4px solid var(--primary-accent);',
        recommended: 'border-left: 4px solid #ff9800;',
        foundation: 'border-left: 4px solid #4caf50;',
        elective: 'border-left: 4px solid var(--border-color);'
    };
    
    const typeLabels = {
        required: '<span class="badge" style="background: var(--primary-accent); color: white;">Required</span>',
        recommended: '<span class="badge" style="background: #ff9800; color: white;">Recommended</span>',
        foundation: '<span class="badge" style="background: #4caf50; color: white;">Foundation</span>',
        elective: ''
    };
    
    // Generate syllabus link for the course
    const syllabusUrl = `/syllabi/${selectedMajor}/${course.id}-syllabus.pdf`;
    
    return `
        <div style="padding: 1rem; margin-bottom: 0.75rem; background: var(--card-bg); 
                    border-radius: 8px; ${typeStyles[type]}">
            <label style="display: flex; align-items: start; cursor: pointer;">
                <input type="checkbox" class="course-check" id="course-${course.id}" 
                       value="${course.id}" style="margin-right: 1rem; margin-top: 0.25rem;"
                       ${type === 'required' ? 'checked' : ''}>
                <div style="flex: 1;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong>${course.id}: ${course.name}</strong>
                        <div>
                            ${typeLabels[type]}
                            <span class="badge" style="background: var(--secondary-bg); margin-left: 0.5rem;">
                                ${course.credits} credits
                            </span>
                            <a href="${syllabusUrl}" 
                               target="_blank"
                               onclick="event.stopPropagation();"
                               style="margin-left: 0.5rem; padding: 0.25rem 0.5rem; 
                                      background: #667eea; color: white; text-decoration: none; 
                                      border-radius: 4px; font-size: 0.85rem; display: inline-block;">
                                <i class="fas fa-file-alt"></i> Syllabus
                            </a>
                        </div>
                    </div>
                    <p style="margin: 0.5rem 0 0 0; color: var(--text-secondary);">
                        ${course.description}
                    </p>
                    ${course.prerequisites && course.prerequisites.length > 0 ? 
                        `<small style="color: #ff9800;">Prerequisites: ${course.prerequisites.join(', ')}</small>` : ''}
                    <small style="color: #999; display: block; margin-top: 0.25rem;">
                        <i class="fas fa-info-circle"></i> Click "Syllabus" for detailed course information, weekly schedule, and grading criteria
                    </small>
                </div>
            </label>
        </div>
    `;
}

function getCareerName(careerId) {
    const careers = careerPaths[selectedMajor] || careerPaths.default;
    const career = careers.find(c => c.id === careerId);
    return career ? career.name : careerId;
}

function updateCourseSelection() {
    selectedCourses = Array.from(document.querySelectorAll('.course-check:checked'))
        .map(cb => cb.value);
    
    const totalCredits = selectedCourses.reduce((sum, courseId) => {
        const course = availableCourses.find(c => c.id === courseId);
        return sum + (course ? course.credits : 0);
    }, 0);
    
    document.getElementById('course-count').textContent = selectedCourses.length;
    document.getElementById('credit-count').textContent = totalCredits;
    
    // Show summary
    const summary = document.getElementById('selected-summary');
    if (selectedCourses.length > 0) {
        const careerMapping = careerCourseMapping[selectedCareer] || careerCourseMapping.default;
        const requiredSelected = selectedCourses.filter(id => careerMapping.required.includes(id)).length;
        const recommendedSelected = selectedCourses.filter(id => careerMapping.recommended.includes(id)).length;
        
        summary.innerHTML = `
            ✅ ${requiredSelected} required courses | 
            👍 ${recommendedSelected} recommended courses | 
            📚 ${selectedCourses.length - requiredSelected - recommendedSelected} additional courses
        `;
    } else {
        summary.innerHTML = 'Select courses to build your learning path';
    }
    
    if (selectedCourses.length > 0) {
        enableNext();
    }
}

function generateDefaultCourses(majorId) {
    // Generate basic course structure for majors without detailed catalog
    const prefix = majorId.toUpperCase().slice(0, 3);
    return [
        { id: `${prefix}101`, name: `Introduction to ${majorId}`, credits: 3, prerequisites: [], level: 'foundation' },
        { id: `${prefix}201`, name: `Intermediate ${majorId}`, credits: 4, prerequisites: [`${prefix}101`], level: 'core' },
        { id: `${prefix}301`, name: `Advanced ${majorId}`, credits: 4, prerequisites: [`${prefix}201`], level: 'advanced' }
    ];
}

function generateRoadmap() {
    console.log('Generating career-focused roadmap:', {
        major: selectedMajor,
        career: selectedCareer,
        courses: selectedCourses
    });
    
    const roadmapResult = document.getElementById('roadmap-result');
    if (!roadmapResult) return;
    
    roadmapResult.innerHTML = `
        <div style="text-align: center; padding: 3rem;">
            <div class="spinner" style="margin: 0 auto;"></div>
            <p>Generating your ${getCareerName(selectedCareer)} roadmap...</p>
        </div>
    `;
    
    setTimeout(() => {
        displayCareerRoadmap();
    }, 2000);
}

function displayCareerRoadmap() {
    const roadmapResult = document.getElementById('roadmap-result');
    const courses = selectedCourses.map(id => 
        availableCourses.find(c => c.id === id)
    ).filter(Boolean);
    
    const careerMapping = careerCourseMapping[selectedCareer] || careerCourseMapping.default;
    const semesters = organizeCoursesBySemester(courses);
    
    let html = `
        <div style="padding: 2rem;">
            <h2>📚 Your ${getCareerName(selectedCareer)} Learning Roadmap</h2>
            
            <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                        padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem;">
                <h3 style="margin-top: 0;">Career Focus: ${careerMapping.focus}</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                    <div>
                        <strong>Major</strong><br>${selectedMajor.toUpperCase()}
                    </div>
                    <div>
                        <strong>Career Path</strong><br>${getCareerName(selectedCareer)}
                    </div>
                    <div>
                        <strong>Total Courses</strong><br>${courses.length}
                    </div>
                    <div>
                        <strong>Total Credits</strong><br>${courses.reduce((sum, c) => sum + c.credits, 0)}
                    </div>
                </div>
            </div>
            
            <h3>📅 Semester-by-Semester Plan</h3>
            ${semesters.map((semester, index) => `
                <div style="margin-bottom: 2rem; padding: 1.5rem; background: var(--card-bg); 
                            border-radius: 12px; border-left: 4px solid var(--primary-accent);">
                    <h4>Semester ${index + 1}</h4>
                    <div style="display: grid; gap: 1rem; margin-top: 1rem;">
                        ${semester.map(course => {
                            const isRequired = careerMapping.required.includes(course.id);
                            const isRecommended = careerMapping.recommended.includes(course.id);
                            return `
                                <div style="padding: 1rem; background: var(--secondary-bg); border-radius: 8px;
                                            ${isRequired ? 'border: 2px solid var(--primary-accent);' : 
                                              isRecommended ? 'border: 2px solid #ff9800;' : ''}">
                                    <div style="display: flex; justify-content: space-between; align-items: center;">
                                        <strong>${course.id}: ${course.name}</strong>
                                        <div>
                                            ${isRequired ? '<span class="badge" style="background: var(--primary-accent); color: white;">Career Required</span>' : 
                                              isRecommended ? '<span class="badge" style="background: #ff9800; color: white;">Recommended</span>' : ''}
                                            <span style="margin-left: 0.5rem; color: var(--primary-accent);">${course.credits} credits</span>
                                            <a href="/syllabi/${selectedMajor}/${course.id}-syllabus.pdf" 
                                               target="_blank"
                                               style="margin-left: 0.5rem; padding: 0.2rem 0.4rem; 
                                                      background: #667eea; color: white; text-decoration: none; 
                                                      border-radius: 3px; font-size: 0.8rem;">
                                                <i class="fas fa-file-pdf"></i> Syllabus
                                            </a>
                                        </div>
                                    </div>
                                    <p style="margin: 0.5rem 0; color: var(--text-secondary);">${course.description}</p>
                                    ${course.prerequisites.length > 0 ? 
                                        `<small style="color: #4caf50;">✓ Prerequisites met: ${course.prerequisites.join(', ')}</small>` : 
                                        '<small style="color: #4caf50;">✓ No prerequisites</small>'}
                                </div>
                            `;
                        }).join('')}
                    </div>
                    <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border-color);">
                        <strong>Semester Credits: ${semester.reduce((sum, c) => sum + c.credits, 0)}</strong>
                    </div>
                </div>
            `).join('')}
            
            <div style="margin-top: 2rem; padding: 1.5rem; background: var(--secondary-bg); border-radius: 12px;">
                <h4>🎯 Career Preparation Tips for ${getCareerName(selectedCareer)}</h4>
                <ul style="margin: 1rem 0;">
                    ${getCareerTips(selectedCareer).map(tip => `<li>${tip}</li>`).join('')}
                </ul>
            </div>
            
            <div style="margin-top: 2rem; display: flex; gap: 1rem; flex-wrap: wrap;">
                <button onclick="alert('Roadmap saved!')" style="padding: 0.75rem 1.5rem; background: var(--primary-accent); color: white; border: none; border-radius: 8px; cursor: pointer;">
                    💾 Save Roadmap
                </button>
                <button onclick="window.print()" style="padding: 0.75rem 1.5rem; background: var(--secondary-bg); border: 1px solid var(--border-color); border-radius: 8px; cursor: pointer;">
                    🖨️ Print
                </button>
                <button onclick="location.reload()" style="padding: 0.75rem 1.5rem; background: transparent; border: 1px solid var(--border-color); border-radius: 8px; cursor: pointer;">
                    🔄 Start Over
                </button>
            </div>
        </div>
    `;
    
    roadmapResult.innerHTML = html;
}

function getCareerTips(careerId) {
    const tips = {
        'embedded-engineer': [
            'Focus on C/C++ programming and assembly language',
            'Build projects with microcontrollers (Arduino, STM32)',
            'Learn RTOS and real-time programming concepts',
            'Contribute to open-source embedded projects'
        ],
        'rf-engineer': [
            'Master electromagnetic theory and antenna design',
            'Gain hands-on experience with RF test equipment',
            'Learn simulation tools like CST or HFSS',
            'Get familiar with wireless standards (WiFi, 5G, Bluetooth)'
        ],
        'power-engineer': [
            'Study renewable energy technologies',
            'Learn power system simulation software (ETAP, PSS/E)',
            'Understand smart grid technologies',
            'Get certified in electrical safety standards'
        ],
        'ml-engineer': [
            'Build a portfolio of ML projects on GitHub',
            'Master TensorFlow/PyTorch frameworks',
            'Participate in Kaggle competitions',
            'Stay updated with latest research papers'
        ],
        'software-engineer': [
            'Contribute to open-source projects',
            'Build full-stack applications',
            'Practice data structures and algorithms daily',
            'Learn cloud platforms (AWS, Azure, GCP)'
        ],
        'nano-engineer': [
            'Gain hands-on experience with electron microscopy and AFM',
            'Learn nanofabrication techniques in cleanroom facilities',
            'Study quantum mechanics and solid-state physics',
            'Pursue research in graphene, quantum dots, or carbon nanotubes'
        ],
        'battery-engineer': [
            'Master electrochemistry and electrochemical characterization',
            'Learn battery testing protocols and safety standards',
            'Study lithium-ion, solid-state, and next-gen battery technologies',
            'Gain experience with battery management systems (BMS)'
        ],
        'semiconductor-engineer': [
            'Learn semiconductor fabrication processes and cleanroom protocols',
            'Master characterization techniques (SEM, TEM, XRD, ellipsometry)',
            'Study CMOS technology and device physics',
            'Gain experience with process simulation software (TCAD)'
        ],
        'biomaterials-engineer': [
            'Understand FDA regulations and biocompatibility testing',
            'Learn cell culture and tissue engineering techniques',
            'Study biomechanics and physiological systems',
            'Gain clinical exposure through hospital internships'
        ],
        'polymer-engineer': [
            'Master polymer synthesis and characterization techniques',
            'Learn rheology and polymer processing methods',
            'Study structure-property relationships in polymers',
            'Gain experience with CAD and FEA for composite design'
        ],
        'metallurgist': [
            'Learn heat treatment processes and phase transformations',
            'Master metallography and mechanical testing',
            'Study corrosion prevention and surface treatments',
            'Gain experience with welding and joining technologies'
        ],
        'failure-analyst': [
            'Develop expertise in fractography and failure mechanisms',
            'Learn non-destructive testing (NDT) techniques',
            'Study forensic engineering and root cause analysis',
            'Gain experience with failure analysis case studies'
        ],
        'computational-materials': [
            'Master DFT, molecular dynamics, and Monte Carlo methods',
            'Learn Python, MATLAB, and materials modeling software',
            'Study statistical mechanics and quantum mechanics',
            'Contribute to open-source computational materials projects'
        ],
        default: [
            'Build a strong portfolio of projects',
            'Network with professionals in your field',
            'Seek internships and co-op opportunities',
            'Stay current with industry trends'
        ]
    };
    
    return tips[careerId] || tips.default;
}

function organizeCoursesBySemester(courses) {
    const semesters = [];
    const completed = new Set();
    const remaining = [...courses];
    
    // Sort courses by prerequisites and importance
    remaining.sort((a, b) => {
        const careerMapping = careerCourseMapping[selectedCareer] || careerCourseMapping.default;
        const aRequired = careerMapping.required.includes(a.id);
        const bRequired = careerMapping.required.includes(b.id);
        const aRecommended = careerMapping.recommended.includes(a.id);
        const bRecommended = careerMapping.recommended.includes(b.id);
        
        // Prioritize required courses
        if (aRequired && !bRequired) return -1;
        if (!aRequired && bRequired) return 1;
        
        // Then recommended courses
        if (aRecommended && !bRecommended) return -1;
        if (!aRecommended && bRecommended) return 1;
        
        // Then by prerequisites
        return a.prerequisites.length - b.prerequisites.length;
    });
    
    while (remaining.length > 0) {
        const semester = [];
        const maxCoursesPerSemester = 4;
        
        for (let i = 0; i < remaining.length && semester.length < maxCoursesPerSemester; i++) {
            const course = remaining[i];
            if (course.prerequisites.every(prereq => 
                completed.has(prereq) || !courses.find(c => c.id === prereq)
            )) {
                semester.push(course);
                remaining.splice(i, 1);
                i--;
            }
        }
        
        if (semester.length === 0 && remaining.length > 0) {
            semester.push(remaining.shift());
        }
        
        semester.forEach(c => completed.add(c.id));
        if (semester.length > 0) {
            semesters.push(semester);
        }
    }
    
    return semesters;
}

function handleNext() {
    console.log('Next clicked, step:', currentStep);
    
    if (currentStep === 1 && selectedCategory) {
        currentStep = 2;
        showStep(2);
        showMajors();
    } else if (currentStep === 2 && selectedMajor) {
        currentStep = 3;
        showStep(3);
        showCareerSelection();
    } else if (currentStep === 3 && selectedCourses.length > 0) {
        currentStep = 4;
        showStep(4);
    } else if (currentStep === 4) {
        currentStep = 5;
        showStep(5);
        generateRoadmap();
    }
}

function handlePrevious() {
    if (currentStep > 1) {
        currentStep--;
        showStep(currentStep);
        
        if (currentStep === 2) showMajors();
        else if (currentStep === 3) showCareerSelection();
    }
}

function showStep(step) {
    // Hide all steps
    for (let i = 1; i <= 5; i++) {
        const el = document.getElementById(`step-${i}`);
        if (el) el.style.display = 'none';
    }
    
    // Show current step
    const current = document.getElementById(`step-${step}`);
    if (current) current.style.display = 'block';
    
    // Update progress
    for (let i = 1; i <= 5; i++) {
        const prog = document.getElementById(`step-${i}-progress`);
        if (prog) {
            prog.classList.remove('active', 'completed');
            if (i < step) prog.classList.add('completed');
            else if (i === step) prog.classList.add('active');
        }
    }
    
    // Update buttons
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    
    if (prevBtn) prevBtn.style.display = step > 1 ? 'inline-block' : 'none';
    if (nextBtn) {
        nextBtn.style.display = step === 5 ? 'none' : 'inline-block';
        nextBtn.textContent = step === 4 ? 'Generate Roadmap' : 'Next';
    }
}

function enableNext() {
    const btn = document.getElementById('next-btn');
    if (btn) {
        btn.disabled = false;
        btn.style.opacity = '1';
    }
}

console.log('✅ Career-Based Course Selection Ready');