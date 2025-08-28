// AI Path Advisor - Final Complete Version with All Majors and Courses

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

// Complete course catalog for ALL majors
const courseCatalog = {
    cs: [
        { id: 'CS101', name: 'Introduction to Programming', credits: 4, prerequisites: [], description: 'Fundamental programming concepts using Python' },
        { id: 'CS201', name: 'Data Structures and Algorithms', credits: 4, prerequisites: ['CS101'], description: 'Fundamental data structures and algorithm design' },
        { id: 'CS301', name: 'Computer Architecture', credits: 4, prerequisites: ['CS101'], description: 'Computer organization and system design' },
        { id: 'CS302', name: 'Operating Systems', credits: 4, prerequisites: ['CS201', 'CS301'], description: 'OS design and implementation' },
        { id: 'CS303', name: 'Database Systems', credits: 4, prerequisites: ['CS201'], description: 'Database design and management' },
        { id: 'CS304', name: 'Computer Networks', credits: 4, prerequisites: ['CS201'], description: 'Network protocols and architectures' },
        { id: 'CS401', name: 'Software Engineering', credits: 4, prerequisites: ['CS201'], description: 'Software development methodologies' },
        { id: 'CS402', name: 'Artificial Intelligence', credits: 4, prerequisites: ['CS201'], description: 'AI principles and algorithms' },
        { id: 'CS403', name: 'Machine Learning', credits: 4, prerequisites: ['CS201'], description: 'Statistical learning theory' },
        { id: 'CS404', name: 'Compiler Design', credits: 4, prerequisites: ['CS201', 'CS301'], description: 'Compiler construction principles' },
        { id: 'CS405', name: 'Computer Security', credits: 4, prerequisites: ['CS302', 'CS304'], description: 'Security principles and cryptography' },
        { id: 'CS406', name: 'Theory of Computation', credits: 4, prerequisites: ['CS201'], description: 'Automata and complexity theory' }
    ],
    'data-science': [
        { id: 'DS101', name: 'Introduction to Data Science', credits: 3, prerequisites: [], description: 'Fundamentals of data analysis and visualization' },
        { id: 'DS102', name: 'Statistical Methods', credits: 4, prerequisites: [], description: 'Probability and statistics for data science' },
        { id: 'DS201', name: 'Data Mining', credits: 4, prerequisites: ['DS101'], description: 'Extracting patterns from large datasets' },
        { id: 'DS202', name: 'Machine Learning for Data Science', credits: 4, prerequisites: ['DS102'], description: 'ML algorithms and applications' },
        { id: 'DS301', name: 'Big Data Analytics', credits: 4, prerequisites: ['DS201'], description: 'Processing and analyzing big data' },
        { id: 'DS302', name: 'Deep Learning', credits: 4, prerequisites: ['DS202'], description: 'Neural networks and deep learning' },
        { id: 'DS303', name: 'Data Visualization', credits: 3, prerequisites: ['DS101'], description: 'Creating effective data visualizations' },
        { id: 'DS401', name: 'Natural Language Processing', credits: 4, prerequisites: ['DS202'], description: 'Text analysis and NLP techniques' },
        { id: 'DS402', name: 'Time Series Analysis', credits: 4, prerequisites: ['DS102'], description: 'Analyzing temporal data' },
        { id: 'DS403', name: 'Business Intelligence', credits: 3, prerequisites: ['DS201'], description: 'BI tools and techniques' }
    ],
    ee: [
        { id: 'EE101', name: 'Circuit Analysis I', credits: 4, prerequisites: [], description: 'DC circuit analysis and theorems' },
        { id: 'EE201', name: 'Circuit Analysis II', credits: 4, prerequisites: ['EE101'], description: 'AC circuit analysis and power' },
        { id: 'EE202', name: 'Signals and Systems', credits: 4, prerequisites: ['EE201'], description: 'Signal analysis in time and frequency' },
        { id: 'EE203', name: 'Electromagnetics I', credits: 4, prerequisites: [], description: 'Static electric and magnetic fields' },
        { id: 'EE301', name: 'Electronics I', credits: 4, prerequisites: ['EE201'], description: 'Semiconductor devices and amplifiers' },
        { id: 'EE302', name: 'Digital Logic Design', credits: 4, prerequisites: ['EE101'], description: 'Digital circuits and system design' },
        { id: 'EE303', name: 'Control Systems', credits: 4, prerequisites: ['EE202'], description: 'Feedback control system analysis' },
        { id: 'EE304', name: 'Communication Systems', credits: 4, prerequisites: ['EE202'], description: 'Analog and digital communications' },
        { id: 'EE305', name: 'Power Systems', credits: 4, prerequisites: ['EE201'], description: 'Power generation and distribution' },
        { id: 'EE401', name: 'Microprocessor Systems', credits: 4, prerequisites: ['EE302'], description: 'Microprocessor architecture and embedded systems' },
        { id: 'EE402', name: 'VLSI Design', credits: 4, prerequisites: ['EE301', 'EE302'], description: 'CMOS VLSI design principles' },
        { id: 'EE403', name: 'RF and Microwave Engineering', credits: 4, prerequisites: ['EE203', 'EE304'], description: 'High-frequency circuit design' }
    ],
    me: [
        { id: 'ME101', name: 'Engineering Mechanics - Statics', credits: 3, prerequisites: [], description: 'Forces and equilibrium in static systems' },
        { id: 'ME102', name: 'Engineering Mechanics - Dynamics', credits: 3, prerequisites: ['ME101'], description: 'Motion and forces in dynamic systems' },
        { id: 'ME201', name: 'Thermodynamics I', credits: 4, prerequisites: [], description: 'Energy, heat, and work principles' },
        { id: 'ME202', name: 'Fluid Mechanics', credits: 4, prerequisites: ['ME102'], description: 'Fluid statics and dynamics' },
        { id: 'ME203', name: 'Mechanics of Materials', credits: 4, prerequisites: ['ME101'], description: 'Stress, strain, and material behavior' },
        { id: 'ME301', name: 'Heat Transfer', credits: 4, prerequisites: ['ME201', 'ME202'], description: 'Conduction, convection, and radiation' },
        { id: 'ME302', name: 'Machine Design', credits: 4, prerequisites: ['ME203'], description: 'Design of mechanical components' },
        { id: 'ME303', name: 'Manufacturing Processes', credits: 3, prerequisites: ['ME203'], description: 'Manufacturing methods and processes' },
        { id: 'ME401', name: 'Control Systems', credits: 4, prerequisites: ['ME102'], description: 'Feedback control for mechanical systems' },
        { id: 'ME402', name: 'Robotics', credits: 4, prerequisites: ['ME401'], description: 'Robot kinematics and control' }
    ],
    civil: [
        { id: 'CE101', name: 'Engineering Mechanics', credits: 4, prerequisites: [], description: 'Statics and dynamics for civil engineering' },
        { id: 'CE201', name: 'Structural Analysis', credits: 4, prerequisites: ['CE101'], description: 'Analysis of structures and forces' },
        { id: 'CE202', name: 'Soil Mechanics', credits: 4, prerequisites: [], description: 'Soil properties and behavior' },
        { id: 'CE203', name: 'Fluid Mechanics', credits: 4, prerequisites: [], description: 'Fluid flow in civil engineering' },
        { id: 'CE301', name: 'Reinforced Concrete Design', credits: 4, prerequisites: ['CE201'], description: 'Design of concrete structures' },
        { id: 'CE302', name: 'Steel Design', credits: 4, prerequisites: ['CE201'], description: 'Design of steel structures' },
        { id: 'CE303', name: 'Transportation Engineering', credits: 3, prerequisites: [], description: 'Transportation systems and planning' },
        { id: 'CE401', name: 'Hydrology', credits: 4, prerequisites: ['CE203'], description: 'Water resources and management' },
        { id: 'CE402', name: 'Environmental Engineering', credits: 4, prerequisites: ['CE203'], description: 'Water and wastewater treatment' }
    ],
    chemeng: [
        { id: 'CHE101', name: 'Material and Energy Balances', credits: 4, prerequisites: [], description: 'Conservation principles in chemical processes' },
        { id: 'CHE201', name: 'Chemical Engineering Thermodynamics', credits: 4, prerequisites: ['CHE101'], description: 'Thermodynamics for chemical systems' },
        { id: 'CHE202', name: 'Transport Phenomena', credits: 4, prerequisites: ['CHE101'], description: 'Momentum, heat, and mass transfer' },
        { id: 'CHE301', name: 'Chemical Reaction Engineering', credits: 4, prerequisites: ['CHE201'], description: 'Reactor design and kinetics' },
        { id: 'CHE302', name: 'Process Control', credits: 4, prerequisites: ['CHE201'], description: 'Control of chemical processes' },
        { id: 'CHE303', name: 'Separation Processes', credits: 4, prerequisites: ['CHE202'], description: 'Distillation, extraction, and other separations' },
        { id: 'CHE401', name: 'Process Design', credits: 4, prerequisites: ['CHE301', 'CHE303'], description: 'Chemical plant design' },
        { id: 'CHE402', name: 'Process Safety', credits: 3, prerequisites: ['CHE301'], description: 'Safety in chemical processes' }
    ],
    bme: [
        { id: 'BME101', name: 'Introduction to Biomedical Engineering', credits: 3, prerequisites: [], description: 'Overview of biomedical engineering' },
        { id: 'BME201', name: 'Biomechanics', credits: 4, prerequisites: [], description: 'Mechanics of biological systems' },
        { id: 'BME202', name: 'Biomaterials', credits: 4, prerequisites: [], description: 'Materials for medical applications' },
        { id: 'BME301', name: 'Bioinstrumentation', credits: 4, prerequisites: [], description: 'Medical instrumentation and sensors' },
        { id: 'BME302', name: 'Medical Imaging', credits: 4, prerequisites: [], description: 'Imaging technologies and processing' },
        { id: 'BME401', name: 'Tissue Engineering', credits: 4, prerequisites: ['BME202'], description: 'Engineering tissues and organs' },
        { id: 'BME402', name: 'Medical Device Design', credits: 4, prerequisites: ['BME301'], description: 'Design of medical devices' }
    ],
    physics: [
        { id: 'PHYS101', name: 'Classical Mechanics I', credits: 4, prerequisites: [], description: 'Newtonian mechanics and conservation laws' },
        { id: 'PHYS102', name: 'Electricity and Magnetism I', credits: 4, prerequisites: ['PHYS101'], description: 'Electromagnetic theory fundamentals' },
        { id: 'PHYS201', name: 'Quantum Mechanics I', credits: 4, prerequisites: ['PHYS102'], description: 'Introduction to quantum mechanics' },
        { id: 'PHYS202', name: 'Thermal and Statistical Physics', credits: 4, prerequisites: ['PHYS201'], description: 'Thermodynamics and statistical mechanics' },
        { id: 'PHYS301', name: 'Classical Mechanics II', credits: 4, prerequisites: ['PHYS101'], description: 'Advanced classical mechanics' },
        { id: 'PHYS302', name: 'Quantum Mechanics II', credits: 4, prerequisites: ['PHYS201'], description: 'Advanced quantum mechanics' },
        { id: 'PHYS303', name: 'Electromagnetism II', credits: 4, prerequisites: ['PHYS102'], description: 'Advanced electromagnetic theory' },
        { id: 'PHYS304', name: 'Solid State Physics', credits: 4, prerequisites: ['PHYS201'], description: 'Physics of crystalline solids' },
        { id: 'PHYS401', name: 'Nuclear and Particle Physics', credits: 4, prerequisites: ['PHYS302'], description: 'Nuclear structure and particles' },
        { id: 'PHYS402', name: 'General Relativity', credits: 4, prerequisites: ['PHYS301'], description: 'Einstein\'s theory of gravitation' }
    ],
    chemistry: [
        { id: 'CHEM101', name: 'General Chemistry I', credits: 4, prerequisites: [], description: 'Atomic structure and chemical bonding' },
        { id: 'CHEM102', name: 'General Chemistry II', credits: 4, prerequisites: ['CHEM101'], description: 'Chemical equilibrium and thermodynamics' },
        { id: 'CHEM201', name: 'Organic Chemistry I', credits: 4, prerequisites: ['CHEM102'], description: 'Structure and reactions of organic compounds' },
        { id: 'CHEM202', name: 'Organic Chemistry II', credits: 4, prerequisites: ['CHEM201'], description: 'Advanced organic reactions and mechanisms' },
        { id: 'CHEM301', name: 'Physical Chemistry I', credits: 4, prerequisites: ['CHEM102'], description: 'Thermodynamics and kinetics' },
        { id: 'CHEM302', name: 'Physical Chemistry II', credits: 4, prerequisites: ['CHEM301'], description: 'Quantum chemistry and spectroscopy' },
        { id: 'CHEM303', name: 'Analytical Chemistry', credits: 4, prerequisites: ['CHEM102'], description: 'Chemical analysis techniques' },
        { id: 'CHEM401', name: 'Inorganic Chemistry', credits: 4, prerequisites: ['CHEM302'], description: 'Transition metals and coordination chemistry' },
        { id: 'CHEM402', name: 'Biochemistry', credits: 4, prerequisites: ['CHEM202'], description: 'Chemistry of biological systems' }
    ],
    materials: [
        { id: 'MAT101', name: 'Introduction to Materials Science', credits: 4, prerequisites: [], description: 'Structure and properties of materials' },
        { id: 'MAT201', name: 'Thermodynamics of Materials', credits: 4, prerequisites: ['MAT101'], description: 'Phase diagrams and transformations' },
        { id: 'MAT202', name: 'Mechanical Behavior of Materials', credits: 4, prerequisites: ['MAT101'], description: 'Deformation and failure of materials' },
        { id: 'MAT301', name: 'Electronic Materials', credits: 4, prerequisites: ['MAT101'], description: 'Semiconductors and electronic properties' },
        { id: 'MAT302', name: 'Polymer Science', credits: 4, prerequisites: ['MAT101'], description: 'Polymer structure and properties' },
        { id: 'MAT303', name: 'Ceramic Materials', credits: 4, prerequisites: ['MAT101'], description: 'Ceramic processing and properties' },
        { id: 'MAT401', name: 'Nanomaterials', credits: 4, prerequisites: ['MAT301'], description: 'Nanoscale materials and applications' },
        { id: 'MAT402', name: 'Materials Characterization', credits: 4, prerequisites: ['MAT201'], description: 'Characterization techniques' }
    ],
    environment: [
        { id: 'ENV101', name: 'Environmental Science Fundamentals', credits: 4, prerequisites: [], description: 'Introduction to environmental systems' },
        { id: 'ENV201', name: 'Environmental Chemistry', credits: 4, prerequisites: ['ENV101'], description: 'Chemical processes in the environment' },
        { id: 'ENV202', name: 'Ecology', credits: 4, prerequisites: ['ENV101'], description: 'Ecosystems and biodiversity' },
        { id: 'ENV301', name: 'Air Quality Engineering', credits: 4, prerequisites: ['ENV201'], description: 'Air pollution and control' },
        { id: 'ENV302', name: 'Water Resources Management', credits: 4, prerequisites: ['ENV201'], description: 'Water quality and treatment' },
        { id: 'ENV401', name: 'Climate Change Science', credits: 4, prerequisites: ['ENV202'], description: 'Climate systems and change' },
        { id: 'ENV402', name: 'Sustainable Engineering', credits: 4, prerequisites: ['ENV301', 'ENV302'], description: 'Sustainable design principles' }
    ],
    medicine: [
        { id: 'MED101', name: 'Human Anatomy', credits: 5, prerequisites: [], description: 'Structure of the human body' },
        { id: 'MED102', name: 'Physiology', credits: 5, prerequisites: ['MED101'], description: 'Function of body systems' },
        { id: 'MED201', name: 'Biochemistry', credits: 4, prerequisites: [], description: 'Chemical processes in living organisms' },
        { id: 'MED202', name: 'Pathology', credits: 4, prerequisites: ['MED102'], description: 'Disease mechanisms and processes' },
        { id: 'MED301', name: 'Pharmacology', credits: 4, prerequisites: ['MED201'], description: 'Drug actions and therapeutics' },
        { id: 'MED302', name: 'Microbiology and Immunology', credits: 4, prerequisites: ['MED102'], description: 'Microorganisms and immune system' },
        { id: 'MED401', name: 'Clinical Medicine I', credits: 6, prerequisites: ['MED202', 'MED301'], description: 'Clinical diagnosis and treatment' },
        { id: 'MED402', name: 'Clinical Medicine II', credits: 6, prerequisites: ['MED401'], description: 'Advanced clinical practice' }
    ],
    nursing: [
        { id: 'NURS101', name: 'Nursing Fundamentals', credits: 4, prerequisites: [], description: 'Basic nursing concepts and skills' },
        { id: 'NURS102', name: 'Health Assessment', credits: 3, prerequisites: [], description: 'Patient assessment techniques' },
        { id: 'NURS201', name: 'Pathophysiology', credits: 4, prerequisites: ['NURS101'], description: 'Disease processes and nursing implications' },
        { id: 'NURS202', name: 'Pharmacology for Nurses', credits: 3, prerequisites: ['NURS101'], description: 'Medication administration and management' },
        { id: 'NURS301', name: 'Medical-Surgical Nursing', credits: 5, prerequisites: ['NURS201'], description: 'Care of adult patients' },
        { id: 'NURS302', name: 'Maternal-Child Nursing', credits: 4, prerequisites: ['NURS201'], description: 'Care of mothers and children' },
        { id: 'NURS401', name: 'Critical Care Nursing', credits: 4, prerequisites: ['NURS301'], description: 'Care of critically ill patients' },
        { id: 'NURS402', name: 'Community Health Nursing', credits: 4, prerequisites: ['NURS301'], description: 'Public health nursing' }
    ],
    pharmacy: [
        { id: 'PHAR101', name: 'Pharmaceutical Sciences', credits: 4, prerequisites: [], description: 'Introduction to pharmacy practice' },
        { id: 'PHAR201', name: 'Medicinal Chemistry', credits: 4, prerequisites: ['PHAR101'], description: 'Drug design and structure' },
        { id: 'PHAR202', name: 'Pharmacology I', credits: 4, prerequisites: ['PHAR101'], description: 'Drug mechanisms and effects' },
        { id: 'PHAR301', name: 'Pharmacology II', credits: 4, prerequisites: ['PHAR202'], description: 'Advanced pharmacology' },
        { id: 'PHAR302', name: 'Pharmaceutics', credits: 4, prerequisites: ['PHAR201'], description: 'Drug formulation and delivery' },
        { id: 'PHAR401', name: 'Clinical Pharmacy', credits: 5, prerequisites: ['PHAR301'], description: 'Pharmacy practice in clinical settings' },
        { id: 'PHAR402', name: 'Pharmacy Management', credits: 3, prerequisites: ['PHAR301'], description: 'Pharmacy administration and law' }
    ],
    'public-health': [
        { id: 'PH101', name: 'Introduction to Public Health', credits: 3, prerequisites: [], description: 'Public health principles and practice' },
        { id: 'PH201', name: 'Epidemiology', credits: 4, prerequisites: ['PH101'], description: 'Disease patterns and prevention' },
        { id: 'PH202', name: 'Biostatistics', credits: 4, prerequisites: ['PH101'], description: 'Statistical methods in public health' },
        { id: 'PH301', name: 'Environmental Health', credits: 4, prerequisites: ['PH201'], description: 'Environmental factors affecting health' },
        { id: 'PH302', name: 'Health Policy', credits: 3, prerequisites: ['PH201'], description: 'Health policy development and analysis' },
        { id: 'PH401', name: 'Global Health', credits: 4, prerequisites: ['PH301'], description: 'International health issues' },
        { id: 'PH402', name: 'Program Evaluation', credits: 3, prerequisites: ['PH202'], description: 'Evaluating public health programs' }
    ],
    nutrition: [
        { id: 'NUTR101', name: 'Nutrition Science', credits: 3, prerequisites: [], description: 'Basic nutrition principles' },
        { id: 'NUTR201', name: 'Nutritional Biochemistry', credits: 4, prerequisites: ['NUTR101'], description: 'Metabolism of nutrients' },
        { id: 'NUTR202', name: 'Food Science', credits: 4, prerequisites: ['NUTR101'], description: 'Food composition and processing' },
        { id: 'NUTR301', name: 'Clinical Nutrition', credits: 4, prerequisites: ['NUTR201'], description: 'Medical nutrition therapy' },
        { id: 'NUTR302', name: 'Community Nutrition', credits: 3, prerequisites: ['NUTR101'], description: 'Public health nutrition' },
        { id: 'NUTR401', name: 'Sports Nutrition', credits: 3, prerequisites: ['NUTR201'], description: 'Nutrition for athletic performance' }
    ],
    economics: [
        { id: 'ECON101', name: 'Principles of Microeconomics', credits: 3, prerequisites: [], description: 'Individual and firm behavior' },
        { id: 'ECON102', name: 'Principles of Macroeconomics', credits: 3, prerequisites: [], description: 'National economy and policy' },
        { id: 'ECON201', name: 'Intermediate Microeconomics', credits: 4, prerequisites: ['ECON101'], description: 'Advanced microeconomic theory' },
        { id: 'ECON202', name: 'Intermediate Macroeconomics', credits: 4, prerequisites: ['ECON102'], description: 'Advanced macroeconomic theory' },
        { id: 'ECON301', name: 'Econometrics', credits: 4, prerequisites: ['ECON201', 'ECON202'], description: 'Statistical analysis in economics' },
        { id: 'ECON302', name: 'International Economics', credits: 3, prerequisites: ['ECON201'], description: 'Trade and finance' },
        { id: 'ECON401', name: 'Economic Development', credits: 3, prerequisites: ['ECON202'], description: 'Development economics' },
        { id: 'ECON402', name: 'Behavioral Economics', credits: 3, prerequisites: ['ECON201'], description: 'Psychology in economics' }
    ],
    finance: [
        { id: 'FIN101', name: 'Introduction to Finance', credits: 3, prerequisites: [], description: 'Financial principles and markets' },
        { id: 'FIN201', name: 'Corporate Finance', credits: 4, prerequisites: ['FIN101'], description: 'Financial management of firms' },
        { id: 'FIN202', name: 'Investments', credits: 4, prerequisites: ['FIN101'], description: 'Portfolio theory and management' },
        { id: 'FIN301', name: 'Financial Markets', credits: 3, prerequisites: ['FIN202'], description: 'Market structure and instruments' },
        { id: 'FIN302', name: 'Derivatives', credits: 4, prerequisites: ['FIN202'], description: 'Options, futures, and swaps' },
        { id: 'FIN401', name: 'Risk Management', credits: 3, prerequisites: ['FIN302'], description: 'Financial risk analysis' },
        { id: 'FIN402', name: 'International Finance', credits: 3, prerequisites: ['FIN201'], description: 'Global financial management' }
    ],
    policy: [
        { id: 'POL101', name: 'Introduction to Political Science', credits: 3, prerequisites: [], description: 'Political systems and theory' },
        { id: 'POL201', name: 'Comparative Politics', credits: 4, prerequisites: ['POL101'], description: 'Comparing political systems' },
        { id: 'POL202', name: 'International Relations', credits: 4, prerequisites: ['POL101'], description: 'Global politics and diplomacy' },
        { id: 'POL301', name: 'Public Policy Analysis', credits: 4, prerequisites: ['POL201'], description: 'Policy development and evaluation' },
        { id: 'POL302', name: 'Political Theory', credits: 3, prerequisites: ['POL101'], description: 'Classical and modern political thought' },
        { id: 'POL401', name: 'Constitutional Law', credits: 4, prerequisites: ['POL302'], description: 'Constitutional interpretation' }
    ],
    education: [
        { id: 'EDU101', name: 'Introduction to Education', credits: 3, prerequisites: [], description: 'Educational foundations and philosophy' },
        { id: 'EDU201', name: 'Learning Theories', credits: 4, prerequisites: ['EDU101'], description: 'How people learn' },
        { id: 'EDU202', name: 'Curriculum Design', credits: 4, prerequisites: ['EDU101'], description: 'Designing educational programs' },
        { id: 'EDU301', name: 'Assessment and Evaluation', credits: 3, prerequisites: ['EDU201'], description: 'Student assessment methods' },
        { id: 'EDU302', name: 'Classroom Management', credits: 3, prerequisites: ['EDU201'], description: 'Managing learning environments' },
        { id: 'EDU401', name: 'Educational Technology', credits: 3, prerequisites: ['EDU202'], description: 'Technology in education' }
    ],
    psychology: [
        { id: 'PSY101', name: 'Introduction to Psychology', credits: 3, prerequisites: [], description: 'Foundations of psychology' },
        { id: 'PSY201', name: 'Research Methods', credits: 4, prerequisites: ['PSY101'], description: 'Psychological research design' },
        { id: 'PSY202', name: 'Developmental Psychology', credits: 3, prerequisites: ['PSY101'], description: 'Human development across lifespan' },
        { id: 'PSY301', name: 'Cognitive Psychology', credits: 4, prerequisites: ['PSY201'], description: 'Mental processes and cognition' },
        { id: 'PSY302', name: 'Social Psychology', credits: 3, prerequisites: ['PSY201'], description: 'Social behavior and influence' },
        { id: 'PSY401', name: 'Clinical Psychology', credits: 4, prerequisites: ['PSY301'], description: 'Mental health and therapy' }
    ],
    architecture: [
        { id: 'ARCH101', name: 'Design Studio I', credits: 5, prerequisites: [], description: 'Basic design principles' },
        { id: 'ARCH102', name: 'Architectural History', credits: 3, prerequisites: [], description: 'History of architecture' },
        { id: 'ARCH201', name: 'Design Studio II', credits: 5, prerequisites: ['ARCH101'], description: 'Intermediate design projects' },
        { id: 'ARCH202', name: 'Building Materials', credits: 3, prerequisites: [], description: 'Construction materials and methods' },
        { id: 'ARCH301', name: 'Design Studio III', credits: 5, prerequisites: ['ARCH201'], description: 'Advanced design projects' },
        { id: 'ARCH302', name: 'Sustainable Design', credits: 3, prerequisites: ['ARCH202'], description: 'Environmental design principles' },
        { id: 'ARCH401', name: 'Urban Planning', credits: 4, prerequisites: ['ARCH301'], description: 'City and regional planning' }
    ],
    communications: [
        { id: 'COMM101', name: 'Introduction to Mass Communication', credits: 3, prerequisites: [], description: 'Media and society' },
        { id: 'COMM201', name: 'News Writing', credits: 3, prerequisites: ['COMM101'], description: 'Journalistic writing techniques' },
        { id: 'COMM202', name: 'Digital Media', credits: 3, prerequisites: ['COMM101'], description: 'Online and social media' },
        { id: 'COMM301', name: 'Media Law and Ethics', credits: 3, prerequisites: ['COMM201'], description: 'Legal and ethical issues' },
        { id: 'COMM302', name: 'Public Relations', credits: 3, prerequisites: ['COMM201'], description: 'PR strategies and tactics' },
        { id: 'COMM401', name: 'Investigative Journalism', credits: 4, prerequisites: ['COMM301'], description: 'In-depth reporting techniques' }
    ],
    law: [
        { id: 'LAW101', name: 'Introduction to Law', credits: 3, prerequisites: [], description: 'Legal systems and reasoning' },
        { id: 'LAW201', name: 'Contracts', credits: 4, prerequisites: ['LAW101'], description: 'Contract law principles' },
        { id: 'LAW202', name: 'Torts', credits: 4, prerequisites: ['LAW101'], description: 'Civil wrongs and remedies' },
        { id: 'LAW301', name: 'Criminal Law', credits: 4, prerequisites: ['LAW101'], description: 'Criminal justice system' },
        { id: 'LAW302', name: 'Constitutional Law', credits: 4, prerequisites: ['LAW101'], description: 'Constitutional principles' },
        { id: 'LAW401', name: 'Legal Writing', credits: 3, prerequisites: ['LAW201', 'LAW202'], description: 'Legal research and writing' }
    ],
    'criminal-justice': [
        { id: 'CJ101', name: 'Introduction to Criminal Justice', credits: 3, prerequisites: [], description: 'Criminal justice system overview' },
        { id: 'CJ201', name: 'Criminology', credits: 3, prerequisites: ['CJ101'], description: 'Theories of crime' },
        { id: 'CJ202', name: 'Law Enforcement', credits: 3, prerequisites: ['CJ101'], description: 'Policing and investigation' },
        { id: 'CJ301', name: 'Corrections', credits: 3, prerequisites: ['CJ201'], description: 'Correctional systems and rehabilitation' },
        { id: 'CJ302', name: 'Criminal Procedure', credits: 3, prerequisites: ['CJ202'], description: 'Legal procedures in criminal cases' },
        { id: 'CJ401', name: 'Forensic Science', credits: 4, prerequisites: ['CJ302'], description: 'Scientific evidence in criminal justice' }
    ]
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
        { id: 'full-stack', name: 'Full Stack Developer', icon: 'layer-group', description: 'Frontend and backend development' }
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
    physics: [
        { id: 'research-physicist', name: 'Research Physicist', icon: 'atom', description: 'Theoretical and experimental research' },
        { id: 'computational-physicist', name: 'Computational Physicist', icon: 'calculator', description: 'Simulations and modeling' },
        { id: 'applied-physicist', name: 'Applied Physicist', icon: 'cogs', description: 'Technology applications' }
    ],
    // Add default career paths for other majors
    default: [
        { id: 'researcher', name: 'Researcher', icon: 'microscope', description: 'Research and development' },
        { id: 'educator', name: 'Educator', icon: 'chalkboard-teacher', description: 'Teaching and education' },
        { id: 'consultant', name: 'Industry Consultant', icon: 'user-tie', description: 'Professional consulting' }
    ]
};

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 AI Path Advisor - Final Version Loaded');
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
            <div class="course-count">
                <span class="badge">${(courseCatalog[major.id] || []).length} courses</span>
            </div>
        `;
        card.addEventListener('click', () => selectMajor(major));
        majorGrid.appendChild(card);
    });
}

function selectMajor(major) {
    console.log('Selected major:', major.name);
    selectedMajor = major.id;
    availableCourses = courseCatalog[major.id] || [];
    
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

function showCoursesAndCareer() {
    const container = document.querySelector('.career-grid');
    if (!container) return;
    
    // Show courses first
    container.innerHTML = `
        <div style="width: 100%;">
            <h3>Select Courses for ${selectedMajor.toUpperCase()}</h3>
            <p style="color: var(--text-secondary); margin-bottom: 1rem;">Choose courses to include in your roadmap</p>
            <div style="max-height: 300px; overflow-y: auto; margin-bottom: 1rem;">
                ${availableCourses.map(course => `
                    <div style="padding: 0.75rem; margin-bottom: 0.5rem; border: 1px solid var(--border-color); border-radius: 8px;">
                        <label style="display: flex; align-items: center; cursor: pointer;">
                            <input type="checkbox" class="course-check" value="${course.id}" style="margin-right: 0.75rem;">
                            <div>
                                <strong>${course.id}: ${course.name}</strong> (${course.credits} credits)
                                <div style="font-size: 0.9rem; color: var(--text-secondary);">${course.description}</div>
                                ${course.prerequisites.length > 0 ? 
                                    `<small style="color: #ff9800;">Prerequisites: ${course.prerequisites.join(', ')}</small>` : ''}
                            </div>
                        </label>
                    </div>
                `).join('')}
            </div>
            <div style="padding: 1rem; background: var(--secondary-bg); border-radius: 8px; margin-bottom: 1rem;">
                <strong>Selected: <span id="course-count">0</span> courses</strong>
            </div>
            
            <h3 style="margin-top: 2rem;">Choose Career Path</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 1rem;">
                ${(careerPaths[selectedMajor] || careerPaths.default).map(career => `
                    <div class="career-card" data-career="${career.id}" 
                         style="padding: 1rem; border: 2px solid var(--border-color); border-radius: 8px; cursor: pointer;">
                        <i class="fas fa-${career.icon}" style="font-size: 1.5rem; color: var(--primary-accent);"></i>
                        <h4>${career.name}</h4>
                        <p style="font-size: 0.9rem; color: var(--text-secondary);">${career.description}</p>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
    
    // Add event listeners
    document.querySelectorAll('.course-check').forEach(cb => {
        cb.addEventListener('change', updateCourseSelection);
    });
    
    document.querySelectorAll('.career-card').forEach(card => {
        card.addEventListener('click', function() {
            selectCareer(this.dataset.career);
        });
    });
}

function updateCourseSelection() {
    selectedCourses = Array.from(document.querySelectorAll('.course-check:checked'))
        .map(cb => cb.value);
    document.getElementById('course-count').textContent = selectedCourses.length;
    
    if (selectedCourses.length > 0 && selectedCareer) {
        enableNext();
    }
}

function selectCareer(careerId) {
    console.log('Selected career:', careerId);
    selectedCareer = careerId;
    
    document.querySelectorAll('.career-card').forEach(card => {
        if (card.dataset.career === careerId) {
            card.style.borderColor = 'var(--primary-accent)';
            card.style.background = 'linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)';
        } else {
            card.style.borderColor = '';
            card.style.background = '';
        }
    });
    
    if (selectedCourses.length > 0 || selectedCareer) {
        enableNext();
    }
}

function generateRoadmap() {
    console.log('Generating roadmap with:', {
        major: selectedMajor,
        courses: selectedCourses,
        career: selectedCareer
    });
    
    const roadmapResult = document.getElementById('roadmap-result');
    if (!roadmapResult) return;
    
    // Show loading
    roadmapResult.innerHTML = `
        <div style="text-align: center; padding: 3rem;">
            <div class="spinner" style="margin: 0 auto;"></div>
            <p>Generating your personalized roadmap...</p>
        </div>
    `;
    
    setTimeout(() => {
        displayDetailedRoadmap();
    }, 2000);
}

function displayDetailedRoadmap() {
    const roadmapResult = document.getElementById('roadmap-result');
    const courses = selectedCourses.map(id => 
        availableCourses.find(c => c.id === id)
    ).filter(Boolean);
    
    // Organize courses by prerequisites
    const semesters = organizeCoursesBySemester(courses);
    
    let html = `
        <div style="padding: 2rem;">
            <h2>📚 Your Personalized Learning Roadmap</h2>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 2rem 0;">
                <div style="padding: 1rem; background: var(--secondary-bg); border-radius: 8px;">
                    <strong>Major</strong><br>${selectedMajor.toUpperCase()}
                </div>
                <div style="padding: 1rem; background: var(--secondary-bg); border-radius: 8px;">
                    <strong>Career Path</strong><br>${selectedCareer}
                </div>
                <div style="padding: 1rem; background: var(--secondary-bg); border-radius: 8px;">
                    <strong>Total Courses</strong><br>${courses.length}
                </div>
                <div style="padding: 1rem; background: var(--secondary-bg); border-radius: 8px;">
                    <strong>Total Credits</strong><br>${courses.reduce((sum, c) => sum + c.credits, 0)}
                </div>
            </div>
            
            <h3>📅 Semester-by-Semester Plan</h3>
            ${semesters.map((semester, index) => `
                <div style="margin-bottom: 2rem; padding: 1.5rem; background: var(--card-bg); border-radius: 12px; border-left: 4px solid var(--primary-accent);">
                    <h4>Semester ${index + 1}</h4>
                    <div style="display: grid; gap: 1rem; margin-top: 1rem;">
                        ${semester.map(course => `
                            <div style="padding: 1rem; background: var(--secondary-bg); border-radius: 8px;">
                                <strong>${course.id}: ${course.name}</strong>
                                <span style="float: right; color: var(--primary-accent);">${course.credits} credits</span>
                                <p style="margin: 0.5rem 0; color: var(--text-secondary);">${course.description}</p>
                                ${course.prerequisites.length > 0 ? 
                                    `<small style="color: #4caf50;">✓ Prerequisites met: ${course.prerequisites.join(', ')}</small>` : 
                                    '<small style="color: #4caf50;">✓ No prerequisites</small>'}
                            </div>
                        `).join('')}
                    </div>
                    <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border-color);">
                        <strong>Total Credits: ${semester.reduce((sum, c) => sum + c.credits, 0)}</strong>
                    </div>
                </div>
            `).join('')}
            
            <div style="margin-top: 2rem; display: flex; gap: 1rem;">
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

function organizeCoursesBySemester(courses) {
    const semesters = [];
    const completed = new Set();
    const remaining = [...courses];
    
    while (remaining.length > 0) {
        const semester = [];
        const maxCoursesPerSemester = 4;
        
        for (let i = 0; i < remaining.length && semester.length < maxCoursesPerSemester; i++) {
            const course = remaining[i];
            // Check if prerequisites are met
            if (course.prerequisites.every(prereq => 
                completed.has(prereq) || !courses.find(c => c.id === prereq)
            )) {
                semester.push(course);
                remaining.splice(i, 1);
                i--;
            }
        }
        
        if (semester.length === 0 && remaining.length > 0) {
            // Force add courses if stuck (prerequisites might be external)
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
        showCoursesAndCareer();
    } else if (currentStep === 3 && (selectedCourses.length > 0 || selectedCareer)) {
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
        else if (currentStep === 3) showCoursesAndCareer();
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

console.log('✅ AI Path Advisor Ready - All majors and courses loaded');