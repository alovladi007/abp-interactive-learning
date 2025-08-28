// Complete Career Paths Expansion for All Majors

// Chemistry Career Paths and Course Mappings
const chemistryCareerPaths = [
    { id: 'pharmaceutical-chemist', name: 'Pharmaceutical Chemist', icon: 'pills', description: 'Drug discovery and development' },
    { id: 'analytical-chemist', name: 'Analytical Chemist', icon: 'flask', description: 'Chemical analysis and quality control' },
    { id: 'organic-synthesis', name: 'Organic Synthesis Chemist', icon: 'atom', description: 'Design and synthesize organic compounds' },
    { id: 'forensic-chemist', name: 'Forensic Chemist', icon: 'fingerprint', description: 'Criminal investigation and evidence analysis' },
    { id: 'materials-chemist', name: 'Materials Chemist', icon: 'cubes', description: 'Develop new materials and polymers' },
    { id: 'environmental-chemist', name: 'Environmental Chemist', icon: 'leaf', description: 'Study chemical processes in environment' }
];

const chemistryCareerMapping = {
    'pharmaceutical-chemist': {
        required: ['CHEM201', 'CHEM202', 'CHEM402'], // Organic I & II, Biochemistry
        recommended: ['CHEM303', 'BIO201', 'PHAR201'], // Analytical, Cell Biology, Medicinal Chem
        focus: 'drug design, synthesis, and pharmaceutical development'
    },
    'analytical-chemist': {
        required: ['CHEM303', 'CHEM302'], // Analytical Chemistry, Physical Chem II
        recommended: ['CHEM304', 'CHEM305', 'STAT201'], // Instrumental Analysis, Separation Science, Statistics
        focus: 'chemical analysis, instrumentation, and quality control'
    },
    'organic-synthesis': {
        required: ['CHEM201', 'CHEM202', 'CHEM306'], // Organic I & II, Advanced Organic
        recommended: ['CHEM307', 'CHEM401'], // Organometallic, Inorganic
        focus: 'synthetic methodology and complex molecule synthesis'
    },
    'forensic-chemist': {
        required: ['CHEM303', 'CHEM308'], // Analytical, Forensic Chemistry
        recommended: ['CHEM309', 'CJ301', 'BIO302'], // Toxicology, Criminal Justice, Genetics
        focus: 'evidence analysis, toxicology, and criminal investigation'
    },
    'materials-chemist': {
        required: ['CHEM301', 'CHEM310'], // Physical Chem I, Polymer Chemistry
        recommended: ['MAT301', 'CHEM401', 'CHEM311'], // Polymers, Inorganic, Nanochemistry
        focus: 'polymer synthesis, materials characterization, and nanotechnology'
    },
    'environmental-chemist': {
        required: ['CHEM312', 'ENV201'], // Environmental Chemistry, Environmental Science
        recommended: ['CHEM303', 'BIO202', 'CHEM313'], // Analytical, Ecology, Atmospheric Chemistry
        focus: 'environmental monitoring, pollution control, and green chemistry'
    }
};

// Environmental Science Career Paths
const environmentCareerPaths = [
    { id: 'climate-scientist', name: 'Climate Scientist', icon: 'cloud-sun', description: 'Study climate change and modeling' },
    { id: 'environmental-consultant', name: 'Environmental Consultant', icon: 'briefcase', description: 'Environmental impact assessment' },
    { id: 'conservation-scientist', name: 'Conservation Scientist', icon: 'tree', description: 'Ecosystem and wildlife conservation' },
    { id: 'water-resource-specialist', name: 'Water Resource Specialist', icon: 'water', description: 'Water quality and management' },
    { id: 'sustainability-manager', name: 'Sustainability Manager', icon: 'recycle', description: 'Corporate sustainability programs' },
    { id: 'air-quality-specialist', name: 'Air Quality Specialist', icon: 'wind', description: 'Air pollution monitoring and control' }
];

const environmentCareerMapping = {
    'climate-scientist': {
        required: ['ENV401', 'ENV403'], // Climate Change Science, Atmospheric Science
        recommended: ['ENV404', 'MATH301', 'CS308'], // Climate Modeling, Linear Algebra, Computational Methods
        focus: 'climate systems, modeling, and global change research'
    },
    'environmental-consultant': {
        required: ['ENV305', 'ENV406'], // Environmental Impact Assessment, Environmental Law
        recommended: ['ENV302', 'ECON302', 'POL301'], // Water Resources, Environmental Economics, Policy
        focus: 'environmental compliance, impact assessment, and remediation'
    },
    'conservation-scientist': {
        required: ['ENV202', 'ENV407'], // Ecology, Conservation Biology
        recommended: ['BIO303', 'ENV408', 'GIS301'], // Wildlife Biology, Restoration Ecology, GIS
        focus: 'biodiversity conservation, habitat management, and restoration'
    },
    'water-resource-specialist': {
        required: ['ENV302', 'ENV409'], // Water Resources, Hydrology
        recommended: ['ENV301', 'CE401', 'CHEM312'], // Air Quality, Water Engineering, Environmental Chemistry
        focus: 'water quality assessment, watershed management, and treatment'
    },
    'sustainability-manager': {
        required: ['ENV402', 'ENV410'], // Sustainable Engineering, Renewable Energy
        recommended: ['BUS301', 'ENV411', 'ECON302'], // Business Management, Life Cycle Assessment, Environmental Economics
        focus: 'sustainable practices, renewable energy, and corporate responsibility'
    },
    'air-quality-specialist': {
        required: ['ENV301', 'ENV403'], // Air Quality Engineering, Atmospheric Science
        recommended: ['CHEM313', 'ENV412', 'PH301'], // Atmospheric Chemistry, Air Pollution Control, Environmental Health
        focus: 'air quality monitoring, pollution control, and regulatory compliance'
    }
};

// Civil Engineering Career Paths
const civilCareerPaths = [
    { id: 'structural-engineer', name: 'Structural Engineer', icon: 'building', description: 'Design buildings and bridges' },
    { id: 'transportation-engineer', name: 'Transportation Engineer', icon: 'road', description: 'Design transportation systems' },
    { id: 'water-resources-engineer', name: 'Water Resources Engineer', icon: 'tint', description: 'Water supply and treatment systems' },
    { id: 'geotechnical-engineer', name: 'Geotechnical Engineer', icon: 'mountain', description: 'Soil and foundation engineering' },
    { id: 'construction-manager', name: 'Construction Manager', icon: 'hard-hat', description: 'Manage construction projects' },
    { id: 'environmental-engineer', name: 'Environmental Engineer', icon: 'leaf', description: 'Environmental protection systems' }
];

const civilCareerMapping = {
    'structural-engineer': {
        required: ['CE201', 'CE301', 'CE302'], // Structural Analysis, Reinforced Concrete, Steel Design
        recommended: ['CE403', 'CE404', 'CE405'], // Advanced Structures, Earthquake Engineering, Bridge Design
        focus: 'structural design, analysis, and seismic engineering'
    },
    'transportation-engineer': {
        required: ['CE303', 'CE406'], // Transportation Engineering, Traffic Engineering
        recommended: ['CE407', 'CE408', 'PLAN301'], // Highway Design, Transit Systems, Urban Planning
        focus: 'transportation planning, traffic flow, and infrastructure design'
    },
    'water-resources-engineer': {
        required: ['CE203', 'CE401'], // Fluid Mechanics, Hydrology
        recommended: ['CE402', 'CE409', 'ENV302'], // Environmental Engineering, Water Treatment, Water Resources
        focus: 'water supply, treatment, and distribution systems'
    },
    'geotechnical-engineer': {
        required: ['CE202', 'CE410'], // Soil Mechanics, Foundation Engineering
        recommended: ['CE411', 'CE412', 'GEOL201'], // Slope Stability, Ground Improvement, Engineering Geology
        focus: 'soil mechanics, foundation design, and ground improvement'
    },
    'construction-manager': {
        required: ['CE413', 'CE414'], // Construction Management, Project Management
        recommended: ['CE415', 'BUS301', 'CE416'], // Construction Law, Business Management, Cost Estimation
        focus: 'project management, scheduling, and construction operations'
    },
    'environmental-engineer': {
        required: ['CE402', 'CE417'], // Environmental Engineering, Waste Management
        recommended: ['ENV201', 'CE418', 'CHEM312'], // Environmental Chemistry, Air Pollution Control, Environmental Chemistry
        focus: 'environmental protection, remediation, and sustainable design'
    }
};

// Chemical Engineering Career Paths
const chemEngCareerPaths = [
    { id: 'process-engineer', name: 'Process Engineer', icon: 'industry', description: 'Design and optimize chemical processes' },
    { id: 'petrochemical-engineer', name: 'Petrochemical Engineer', icon: 'oil-can', description: 'Oil and gas processing' },
    { id: 'pharmaceutical-engineer', name: 'Pharmaceutical Engineer', icon: 'prescription', description: 'Drug manufacturing processes' },
    { id: 'food-process-engineer', name: 'Food Process Engineer', icon: 'utensils', description: 'Food and beverage production' },
    { id: 'energy-engineer', name: 'Energy Systems Engineer', icon: 'solar-panel', description: 'Renewable energy and fuel cells' },
    { id: 'biotechnology-engineer', name: 'Biotechnology Engineer', icon: 'dna', description: 'Bioprocessing and fermentation' }
];

const chemEngCareerMapping = {
    'process-engineer': {
        required: ['CHE301', 'CHE401'], // Reaction Engineering, Process Design
        recommended: ['CHE302', 'CHE303', 'CHE404'], // Process Control, Separations, Optimization
        focus: 'process design, optimization, and plant operations'
    },
    'petrochemical-engineer': {
        required: ['CHE405', 'CHE406'], // Petroleum Refining, Natural Gas Processing
        recommended: ['CHE303', 'CHE407', 'CHE402'], // Separations, Catalysis, Process Safety
        focus: 'oil refining, petrochemicals, and gas processing'
    },
    'pharmaceutical-engineer': {
        required: ['CHE408', 'CHE409'], // Pharmaceutical Engineering, Bioprocessing
        recommended: ['CHE410', 'PHAR301', 'CHE411'], // GMP, Pharmacology, Validation
        focus: 'drug manufacturing, GMP compliance, and process validation'
    },
    'food-process-engineer': {
        required: ['CHE412', 'CHE413'], // Food Process Engineering, Food Safety
        recommended: ['CHE414', 'NUTR201', 'CHE415'], // Packaging, Food Science, Quality Control
        focus: 'food processing, preservation, and safety systems'
    },
    'energy-engineer': {
        required: ['CHE416', 'CHE417'], // Energy Systems, Fuel Cells
        recommended: ['CHE418', 'MAT401', 'CHE419'], // Solar Energy, Energy Storage, Hydrogen Systems
        focus: 'renewable energy, fuel cells, and energy storage'
    },
    'biotechnology-engineer': {
        required: ['CHE409', 'CHE420'], // Bioprocessing, Fermentation
        recommended: ['CHE421', 'BIO301', 'CHE422'], // Bioreactor Design, Molecular Biology, Downstream Processing
        focus: 'bioprocessing, fermentation, and biopharmaceutical production'
    }
};

// Biomedical Engineering Career Paths
const bmeCareerPaths = [
    { id: 'medical-device-engineer', name: 'Medical Device Engineer', icon: 'heartbeat', description: 'Design medical devices and implants' },
    { id: 'clinical-engineer', name: 'Clinical Engineer', icon: 'hospital', description: 'Hospital equipment management' },
    { id: 'tissue-engineer', name: 'Tissue Engineer', icon: 'dna', description: 'Regenerative medicine and tissue engineering' },
    { id: 'biomechanics-engineer', name: 'Biomechanics Engineer', icon: 'running', description: 'Study body mechanics and prosthetics' },
    { id: 'imaging-engineer', name: 'Medical Imaging Engineer', icon: 'x-ray', description: 'Develop imaging technologies' },
    { id: 'neural-engineer', name: 'Neural Engineer', icon: 'brain', description: 'Brain-computer interfaces' }
];

const bmeCareerMapping = {
    'medical-device-engineer': {
        required: ['BME402', 'BME403'], // Medical Device Design, FDA Regulations
        recommended: ['BME301', 'MAT306', 'BME404'], // Bioinstrumentation, Biomaterials, Device Testing
        focus: 'medical device design, regulatory compliance, and testing'
    },
    'clinical-engineer': {
        required: ['BME301', 'BME405'], // Bioinstrumentation, Clinical Engineering
        recommended: ['BME406', 'EE301', 'BME407'], // Medical Equipment, Electronics, Hospital Systems
        focus: 'medical equipment management, safety, and maintenance'
    },
    'tissue-engineer': {
        required: ['BME401', 'BME408'], // Tissue Engineering, Cell & Tissue Culture
        recommended: ['BME202', 'BIO304', 'BME409'], // Biomaterials, Cell Biology, Scaffold Design
        focus: 'tissue regeneration, stem cells, and scaffold design'
    },
    'biomechanics-engineer': {
        required: ['BME201', 'BME410'], // Biomechanics, Prosthetics & Orthotics
        recommended: ['BME411', 'ME302', 'BME412'], // Gait Analysis, Machine Design, Rehabilitation Engineering
        focus: 'human movement, prosthetics, and rehabilitation devices'
    },
    'imaging-engineer': {
        required: ['BME302', 'BME413'], // Medical Imaging, Image Processing
        recommended: ['BME414', 'CS403', 'BME415'], // MRI/CT Technology, Machine Learning, Image Reconstruction
        focus: 'medical imaging systems, image processing, and diagnostics'
    },
    'neural-engineer': {
        required: ['BME416', 'BME417'], // Neural Engineering, Brain-Computer Interfaces
        recommended: ['BME418', 'NEURO301', 'BME419'], // Neural Signal Processing, Neuroscience, Neural Implants
        focus: 'neural interfaces, neuroprosthetics, and brain stimulation'
    }
};

// Economics Career Paths
const economicsCareerPaths = [
    { id: 'financial-economist', name: 'Financial Economist', icon: 'chart-line', description: 'Financial markets analysis' },
    { id: 'policy-economist', name: 'Policy Economist', icon: 'landmark', description: 'Economic policy analysis' },
    { id: 'data-economist', name: 'Economic Data Analyst', icon: 'database', description: 'Economic data and forecasting' },
    { id: 'development-economist', name: 'Development Economist', icon: 'globe', description: 'International development' },
    { id: 'behavioral-economist', name: 'Behavioral Economist', icon: 'brain', description: 'Psychology in economic decisions' },
    { id: 'environmental-economist', name: 'Environmental Economist', icon: 'leaf', description: 'Environmental policy and resources' }
];

const economicsCareerMapping = {
    'financial-economist': {
        required: ['ECON303', 'ECON304'], // Financial Economics, Asset Pricing
        recommended: ['FIN202', 'ECON301', 'MATH401'], // Investments, Econometrics, Stochastic Calculus
        focus: 'financial markets, asset pricing, and risk analysis'
    },
    'policy-economist': {
        required: ['ECON305', 'ECON306'], // Public Economics, Policy Analysis
        recommended: ['POL301', 'ECON307', 'STAT301'], // Public Policy, Welfare Economics, Advanced Statistics
        focus: 'economic policy analysis, government programs, and regulation'
    },
    'data-economist': {
        required: ['ECON301', 'ECON308'], // Econometrics, Economic Forecasting
        recommended: ['DS201', 'ECON309', 'CS201'], // Data Mining, Time Series, Programming
        focus: 'economic data analysis, forecasting, and modeling'
    },
    'development-economist': {
        required: ['ECON401', 'ECON310'], // Development Economics, International Development
        recommended: ['ECON302', 'POL202', 'ECON311'], // International Economics, International Relations, Poverty Analysis
        focus: 'economic development, poverty reduction, and international aid'
    },
    'behavioral-economist': {
        required: ['ECON402', 'PSY301'], // Behavioral Economics, Cognitive Psychology
        recommended: ['ECON312', 'PSY302', 'ECON313'], // Experimental Economics, Social Psychology, Decision Theory
        focus: 'psychological factors in economic decisions and market behavior'
    },
    'environmental-economist': {
        required: ['ECON314', 'ENV201'], // Environmental Economics, Environmental Science
        recommended: ['ECON315', 'POL303', 'ECON316'], // Resource Economics, Environmental Policy, Climate Economics
        focus: 'environmental valuation, resource management, and climate policy'
    }
};

// Finance Career Paths
const financeCareerPaths = [
    { id: 'investment-banker', name: 'Investment Banker', icon: 'building', description: 'Mergers, acquisitions, and capital raising' },
    { id: 'portfolio-manager', name: 'Portfolio Manager', icon: 'chart-pie', description: 'Manage investment portfolios' },
    { id: 'risk-analyst', name: 'Risk Analyst', icon: 'shield-alt', description: 'Financial risk assessment' },
    { id: 'corporate-finance', name: 'Corporate Finance Manager', icon: 'briefcase', description: 'Corporate financial planning' },
    { id: 'quant-analyst', name: 'Quantitative Analyst', icon: 'calculator', description: 'Mathematical finance and trading' },
    { id: 'fintech-specialist', name: 'FinTech Specialist', icon: 'mobile-alt', description: 'Financial technology and innovation' }
];

const financeCareerMapping = {
    'investment-banker': {
        required: ['FIN301', 'FIN303'], // Investment Banking, M&A
        recommended: ['FIN304', 'ACCT301', 'FIN305'], // Valuation, Financial Accounting, Capital Markets
        focus: 'mergers & acquisitions, IPOs, and corporate restructuring'
    },
    'portfolio-manager': {
        required: ['FIN202', 'FIN306'], // Investments, Portfolio Management
        recommended: ['FIN307', 'FIN302', 'ECON303'], // Asset Allocation, Derivatives, Financial Economics
        focus: 'portfolio construction, asset allocation, and performance analysis'
    },
    'risk-analyst': {
        required: ['FIN401', 'FIN308'], // Risk Management, Credit Risk
        recommended: ['FIN309', 'STAT302', 'FIN310'], // Market Risk, Probability Theory, Stress Testing
        focus: 'risk measurement, modeling, and mitigation strategies'
    },
    'corporate-finance': {
        required: ['FIN201', 'FIN311'], // Corporate Finance, Financial Planning
        recommended: ['FIN312', 'ACCT302', 'FIN313'], // Working Capital, Managerial Accounting, Treasury Management
        focus: 'capital budgeting, financial planning, and corporate strategy'
    },
    'quant-analyst': {
        required: ['FIN314', 'MATH402'], // Quantitative Finance, Stochastic Calculus
        recommended: ['FIN302', 'CS403', 'FIN315'], // Derivatives, Machine Learning, Algorithmic Trading
        focus: 'mathematical modeling, derivatives pricing, and trading strategies'
    },
    'fintech-specialist': {
        required: ['FIN316', 'CS303'], // FinTech, Database Systems
        recommended: ['FIN317', 'CS405', 'FIN318'], // Blockchain, Cybersecurity, Digital Banking
        focus: 'financial technology, blockchain, and digital transformation'
    }
};

// Psychology Career Paths
const psychologyCareerPaths = [
    { id: 'clinical-psychologist', name: 'Clinical Psychologist', icon: 'user-md', description: 'Mental health treatment' },
    { id: 'neuropsychologist', name: 'Neuropsychologist', icon: 'brain', description: 'Brain-behavior relationships' },
    { id: 'organizational-psychologist', name: 'I/O Psychologist', icon: 'users', description: 'Workplace psychology' },
    { id: 'school-psychologist', name: 'School Psychologist', icon: 'graduation-cap', description: 'Educational psychology' },
    { id: 'forensic-psychologist', name: 'Forensic Psychologist', icon: 'gavel', description: 'Psychology in legal system' },
    { id: 'research-psychologist', name: 'Research Psychologist', icon: 'microscope', description: 'Psychological research' }
];

const psychologyCareerMapping = {
    'clinical-psychologist': {
        required: ['PSY401', 'PSY402'], // Clinical Psychology, Psychopathology
        recommended: ['PSY403', 'PSY404', 'PSY405'], // Therapy Techniques, Assessment, Ethics
        focus: 'mental health assessment, diagnosis, and treatment'
    },
    'neuropsychologist': {
        required: ['PSY406', 'PSY407'], // Neuropsychology, Brain & Behavior
        recommended: ['BIO305', 'PSY408', 'PSY409'], // Neuroscience, Cognitive Neuroscience, Neuroimaging
        focus: 'brain function, cognitive assessment, and rehabilitation'
    },
    'organizational-psychologist': {
        required: ['PSY410', 'PSY411'], // I/O Psychology, Organizational Behavior
        recommended: ['BUS302', 'PSY412', 'STAT303'], // HR Management, Leadership Psychology, Advanced Statistics
        focus: 'workplace behavior, employee selection, and organizational development'
    },
    'school-psychologist': {
        required: ['PSY413', 'PSY414'], // School Psychology, Educational Psychology
        recommended: ['PSY202', 'EDU301', 'PSY415'], // Developmental, Assessment Methods, Learning Disabilities
        focus: 'student assessment, learning problems, and school interventions'
    },
    'forensic-psychologist': {
        required: ['PSY416', 'PSY417'], // Forensic Psychology, Criminal Behavior
        recommended: ['LAW301', 'PSY418', 'CJ201'], // Criminal Law, Risk Assessment, Criminology
        focus: 'criminal behavior, legal competency, and expert testimony'
    },
    'research-psychologist': {
        required: ['PSY201', 'PSY419'], // Research Methods, Advanced Research Design
        recommended: ['STAT304', 'PSY420', 'PSY421'], // Multivariate Statistics, Grant Writing, Publication
        focus: 'experimental design, data analysis, and scientific publication'
    }
};

// Political Science Career Paths
const politicalCareerPaths = [
    { id: 'policy-analyst', name: 'Policy Analyst', icon: 'clipboard', description: 'Analyze and develop public policy' },
    { id: 'campaign-manager', name: 'Campaign Manager', icon: 'vote-yea', description: 'Political campaign management' },
    { id: 'diplomat', name: 'Foreign Service Officer', icon: 'globe', description: 'International relations and diplomacy' },
    { id: 'legislative-aide', name: 'Legislative Aide', icon: 'landmark', description: 'Support legislative processes' },
    { id: 'political-consultant', name: 'Political Consultant', icon: 'handshake', description: 'Strategic political advice' },
    { id: 'intelligence-analyst', name: 'Intelligence Analyst', icon: 'user-secret', description: 'Security and intelligence analysis' }
];

const politicalCareerMapping = {
    'policy-analyst': {
        required: ['POL301', 'POL304'], // Policy Analysis, Policy Implementation
        recommended: ['ECON305', 'STAT201', 'POL305'], // Public Economics, Statistics, Program Evaluation
        focus: 'policy research, analysis, and recommendations'
    },
    'campaign-manager': {
        required: ['POL306', 'POL307'], // Campaign Management, Political Communication
        recommended: ['COMM302', 'POL308', 'MKT301'], // Public Relations, Polling, Marketing
        focus: 'campaign strategy, voter outreach, and political messaging'
    },
    'diplomat': {
        required: ['POL202', 'POL309'], // International Relations, Diplomacy
        recommended: ['POL310', 'LANG301', 'POL311'], // International Law, Foreign Language, Regional Studies
        focus: 'international negotiation, foreign policy, and cultural relations'
    },
    'legislative-aide': {
        required: ['POL312', 'POL313'], // Legislative Process, Congressional Politics
        recommended: ['LAW101', 'POL314', 'COMM201'], // Introduction to Law, Lobbying, Writing
        focus: 'legislative research, bill drafting, and constituent services'
    },
    'political-consultant': {
        required: ['POL307', 'POL315'], // Political Communication, Strategic Consulting
        recommended: ['POL308', 'DATA301', 'POL316'], // Polling, Data Analytics, Crisis Management
        focus: 'political strategy, messaging, and campaign consulting'
    },
    'intelligence-analyst': {
        required: ['POL317', 'POL318'], // Intelligence Analysis, National Security
        recommended: ['POL202', 'CS405', 'POL319'], // International Relations, Cybersecurity, Terrorism Studies
        focus: 'security threats, intelligence gathering, and strategic analysis'
    }
};

// Education Career Paths
const educationCareerPaths = [
    { id: 'elementary-teacher', name: 'Elementary Teacher', icon: 'child', description: 'Teach elementary school students' },
    { id: 'secondary-teacher', name: 'Secondary Teacher', icon: 'chalkboard-teacher', description: 'Teach middle/high school' },
    { id: 'special-ed-teacher', name: 'Special Education Teacher', icon: 'hands-helping', description: 'Teach students with disabilities' },
    { id: 'curriculum-designer', name: 'Curriculum Designer', icon: 'book-open', description: 'Design educational programs' },
    { id: 'educational-technologist', name: 'Educational Technologist', icon: 'laptop', description: 'Integrate technology in education' },
    { id: 'school-administrator', name: 'School Administrator', icon: 'school', description: 'School leadership and management' }
];

const educationCareerMapping = {
    'elementary-teacher': {
        required: ['EDU301', 'EDU302'], // Elementary Methods, Child Development
        recommended: ['EDU303', 'PSY202', 'EDU304'], // Classroom Management, Developmental Psychology, Literacy
        focus: 'elementary curriculum, child development, and classroom management'
    },
    'secondary-teacher': {
        required: ['EDU305', 'EDU306'], // Secondary Methods, Subject Pedagogy
        recommended: ['EDU307', 'EDU308', 'PSY413'], // Adolescent Development, Assessment, Educational Psychology
        focus: 'subject-specific teaching, adolescent learning, and curriculum design'
    },
    'special-ed-teacher': {
        required: ['EDU309', 'EDU310'], // Special Education, Inclusive Practices
        recommended: ['EDU311', 'PSY415', 'EDU312'], // IEP Development, Learning Disabilities, Assistive Technology
        focus: 'individualized education, disability support, and adaptive teaching'
    },
    'curriculum-designer': {
        required: ['EDU202', 'EDU313'], // Curriculum Design, Instructional Design
        recommended: ['EDU301', 'EDU314', 'EDU315'], // Assessment, Standards Alignment, Program Evaluation
        focus: 'curriculum development, learning objectives, and educational standards'
    },
    'educational-technologist': {
        required: ['EDU401', 'EDU316'], // Educational Technology, Digital Learning
        recommended: ['CS101', 'EDU317', 'EDU318'], // Programming, Learning Management Systems, Multimedia Design
        focus: 'technology integration, online learning, and educational software'
    },
    'school-administrator': {
        required: ['EDU319', 'EDU320'], // Educational Leadership, School Management
        recommended: ['EDU321', 'BUS301', 'EDU322'], // School Law, Management, Budget & Finance
        focus: 'school leadership, policy implementation, and organizational management'
    }
};

// Medicine (Pre-Med) Career Paths
const medicineCareerPaths = [
    { id: 'physician', name: 'Physician (MD)', icon: 'user-md', description: 'Medical doctor - various specialties' },
    { id: 'surgeon', name: 'Surgeon', icon: 'procedures', description: 'Surgical specialist' },
    { id: 'medical-researcher', name: 'Medical Researcher', icon: 'microscope', description: 'Biomedical research' },
    { id: 'pathologist', name: 'Pathologist', icon: 'diagnoses', description: 'Disease diagnosis and research' },
    { id: 'radiologist', name: 'Radiologist', icon: 'x-ray', description: 'Medical imaging specialist' },
    { id: 'psychiatrist', name: 'Psychiatrist', icon: 'brain', description: 'Mental health physician' }
];

const medicineCareerMapping = {
    'physician': {
        required: ['MED401', 'MED402'], // Clinical Medicine I & II
        recommended: ['MED301', 'MED302', 'MED403'], // Pharmacology, Microbiology, Patient Care
        focus: 'clinical diagnosis, treatment, and patient care'
    },
    'surgeon': {
        required: ['MED404', 'MED405'], // Surgery, Surgical Anatomy
        recommended: ['MED101', 'MED406', 'MED407'], // Anatomy, Critical Care, Surgical Techniques
        focus: 'surgical procedures, operative techniques, and patient management'
    },
    'medical-researcher': {
        required: ['MED408', 'MED409'], // Medical Research Methods, Translational Medicine
        recommended: ['BIO401', 'STAT305', 'MED410'], // Molecular Biology, Biostatistics, Clinical Trials
        focus: 'biomedical research, clinical trials, and drug development'
    },
    'pathologist': {
        required: ['MED202', 'MED411'], // Pathology, Laboratory Medicine
        recommended: ['MED412', 'BIO302', 'MED413'], // Histopathology, Genetics, Molecular Diagnostics
        focus: 'disease diagnosis, laboratory testing, and tissue analysis'
    },
    'radiologist': {
        required: ['MED414', 'MED415'], // Radiology, Medical Imaging
        recommended: ['PHYS301', 'MED416', 'CS413'], // Radiation Physics, Interventional Radiology, Image Processing
        focus: 'medical imaging interpretation, diagnostic procedures, and interventional techniques'
    },
    'psychiatrist': {
        required: ['MED417', 'MED418'], // Psychiatry, Psychopharmacology
        recommended: ['PSY401', 'MED419', 'NEURO301'], // Clinical Psychology, Neuropsychiatry, Neuroscience
        focus: 'mental health diagnosis, medication management, and psychotherapy'
    }
};

// Nursing Career Paths
const nursingCareerPaths = [
    { id: 'clinical-nurse', name: 'Clinical Nurse (RN)', icon: 'user-nurse', description: 'Direct patient care' },
    { id: 'nurse-practitioner', name: 'Nurse Practitioner', icon: 'stethoscope', description: 'Advanced practice nursing' },
    { id: 'critical-care-nurse', name: 'Critical Care Nurse', icon: 'heartbeat', description: 'ICU and emergency care' },
    { id: 'pediatric-nurse', name: 'Pediatric Nurse', icon: 'baby', description: 'Child healthcare' },
    { id: 'nurse-educator', name: 'Nurse Educator', icon: 'chalkboard-teacher', description: 'Nursing education' },
    { id: 'public-health-nurse', name: 'Public Health Nurse', icon: 'globe', description: 'Community health nursing' }
];

const nursingCareerMapping = {
    'clinical-nurse': {
        required: ['NURS301', 'NURS201'], // Medical-Surgical Nursing, Pathophysiology
        recommended: ['NURS202', 'NURS303', 'NURS304'], // Pharmacology, Patient Assessment, Clinical Skills
        focus: 'patient care, medication administration, and clinical procedures'
    },
    'nurse-practitioner': {
        required: ['NURS501', 'NURS502'], // Advanced Practice Nursing, Advanced Pharmacology
        recommended: ['NURS503', 'NURS504', 'NURS505'], // Diagnosis & Treatment, Primary Care, Clinical Decision Making
        focus: 'advanced assessment, diagnosis, and treatment planning'
    },
    'critical-care-nurse': {
        required: ['NURS401', 'NURS402'], // Critical Care Nursing, Emergency Nursing
        recommended: ['NURS403', 'NURS404', 'NURS405'], // Cardiac Care, Trauma Nursing, Life Support
        focus: 'intensive care, emergency response, and life support systems'
    },
    'pediatric-nurse': {
        required: ['NURS302', 'NURS406'], // Maternal-Child Nursing, Pediatric Nursing
        recommended: ['NURS407', 'PSY202', 'NURS408'], // Neonatal Care, Child Development, Family Nursing
        focus: 'child health, developmental care, and family-centered nursing'
    },
    'nurse-educator': {
        required: ['NURS409', 'EDU201'], // Nursing Education, Learning Theories
        recommended: ['NURS410', 'EDU202', 'NURS411'], // Clinical Teaching, Curriculum Design, Simulation
        focus: 'nursing education, curriculum development, and clinical teaching'
    },
    'public-health-nurse': {
        required: ['NURS402', 'PH201'], // Community Health Nursing, Epidemiology
        recommended: ['PH301', 'NURS412', 'PH302'], // Environmental Health, Health Promotion, Health Policy
        focus: 'population health, disease prevention, and community outreach'
    }
};

// Pharmacy Career Paths
const pharmacyCareerPaths = [
    { id: 'clinical-pharmacist', name: 'Clinical Pharmacist', icon: 'pills', description: 'Hospital and clinical pharmacy' },
    { id: 'retail-pharmacist', name: 'Retail Pharmacist', icon: 'store', description: 'Community pharmacy practice' },
    { id: 'pharmaceutical-scientist', name: 'Pharmaceutical Scientist', icon: 'flask', description: 'Drug development and research' },
    { id: 'regulatory-pharmacist', name: 'Regulatory Affairs Specialist', icon: 'clipboard-check', description: 'Drug regulation and compliance' },
    { id: 'industrial-pharmacist', name: 'Industrial Pharmacist', icon: 'industry', description: 'Pharmaceutical manufacturing' },
    { id: 'pharmacology-researcher', name: 'Pharmacology Researcher', icon: 'microscope', description: 'Drug discovery and testing' }
];

const pharmacyCareerMapping = {
    'clinical-pharmacist': {
        required: ['PHAR401', 'PHAR402'], // Clinical Pharmacy, Therapeutics
        recommended: ['PHAR403', 'MED301', 'PHAR404'], // Clinical Rotations, Pharmacology, Patient Counseling
        focus: 'medication therapy management, clinical services, and patient care'
    },
    'retail-pharmacist': {
        required: ['PHAR405', 'PHAR402'], // Community Pharmacy, Pharmacy Management
        recommended: ['PHAR406', 'BUS301', 'PHAR407'], // OTC Medications, Business Management, Immunizations
        focus: 'prescription dispensing, patient counseling, and pharmacy operations'
    },
    'pharmaceutical-scientist': {
        required: ['PHAR201', 'PHAR408'], // Medicinal Chemistry, Drug Development
        recommended: ['PHAR302', 'CHEM306', 'PHAR409'], // Pharmaceutics, Advanced Organic, Formulation
        focus: 'drug design, development, and pharmaceutical research'
    },
    'regulatory-pharmacist': {
        required: ['PHAR410', 'PHAR411'], // Regulatory Affairs, Drug Law
        recommended: ['PHAR412', 'LAW301', 'PHAR413'], // FDA Regulations, Healthcare Law, Quality Assurance
        focus: 'regulatory compliance, drug approval, and quality control'
    },
    'industrial-pharmacist': {
        required: ['PHAR414', 'PHAR415'], // Pharmaceutical Manufacturing, Quality Control
        recommended: ['CHE401', 'PHAR416', 'PHAR417'], // Process Design, GMP, Validation
        focus: 'drug manufacturing, quality assurance, and process optimization'
    },
    'pharmacology-researcher': {
        required: ['PHAR202', 'PHAR418'], // Pharmacology I & II, Research Methods
        recommended: ['BIO401', 'PHAR419', 'STAT306'], // Molecular Biology, Toxicology, Biostatistics
        focus: 'drug discovery, mechanism studies, and clinical trials'
    }
};

// Public Health Career Paths
const publicHealthCareerPaths = [
    { id: 'epidemiologist', name: 'Epidemiologist', icon: 'virus', description: 'Disease patterns and prevention' },
    { id: 'health-policy-analyst', name: 'Health Policy Analyst', icon: 'clipboard', description: 'Healthcare policy development' },
    { id: 'biostatistician', name: 'Biostatistician', icon: 'chart-bar', description: 'Health data analysis' },
    { id: 'environmental-health', name: 'Environmental Health Specialist', icon: 'leaf', description: 'Environmental health hazards' },
    { id: 'global-health', name: 'Global Health Specialist', icon: 'globe', description: 'International health programs' },
    { id: 'health-educator', name: 'Health Educator', icon: 'chalkboard-teacher', description: 'Community health education' }
];

const publicHealthCareerMapping = {
    'epidemiologist': {
        required: ['PH201', 'PH303'], // Epidemiology, Infectious Disease Epidemiology
        recommended: ['PH202', 'PH304', 'STAT307'], // Biostatistics, Outbreak Investigation, Survival Analysis
        focus: 'disease surveillance, outbreak investigation, and prevention strategies'
    },
    'health-policy-analyst': {
        required: ['PH302', 'PH305'], // Health Policy, Health Economics
        recommended: ['POL301', 'PH306', 'ECON305'], // Policy Analysis, Health Law, Public Economics
        focus: 'healthcare policy analysis, reform, and implementation'
    },
    'biostatistician': {
        required: ['PH202', 'PH307'], // Biostatistics, Advanced Biostatistics
        recommended: ['STAT308', 'PH308', 'CS201'], // Statistical Modeling, Clinical Trials, Programming
        focus: 'statistical analysis, study design, and health data interpretation'
    },
    'environmental-health': {
        required: ['PH301', 'PH309'], // Environmental Health, Toxicology
        recommended: ['ENV301', 'PH310', 'CHEM312'], // Air Quality, Water Quality, Environmental Chemistry
        focus: 'environmental hazards, risk assessment, and pollution control'
    },
    'global-health': {
        required: ['PH401', 'PH311'], // Global Health, International Health Systems
        recommended: ['PH312', 'ANTH301', 'PH313'], // Humanitarian Aid, Medical Anthropology, Tropical Medicine
        focus: 'international health programs, disease control, and health equity'
    },
    'health-educator': {
        required: ['PH314', 'PH315'], // Health Education, Health Communication
        recommended: ['EDU201', 'PH316', 'COMM301'], // Learning Theories, Community Engagement, Media Communication
        focus: 'health promotion, behavior change, and community outreach'
    }
};

// Nutrition & Dietetics Career Paths
const nutritionCareerPaths = [
    { id: 'clinical-dietitian', name: 'Clinical Dietitian', icon: 'heartbeat', description: 'Medical nutrition therapy' },
    { id: 'sports-nutritionist', name: 'Sports Nutritionist', icon: 'running', description: 'Athletic performance nutrition' },
    { id: 'food-scientist', name: 'Food Scientist', icon: 'flask', description: 'Food development and safety' },
    { id: 'community-nutritionist', name: 'Community Nutritionist', icon: 'users', description: 'Public health nutrition' },
    { id: 'research-nutritionist', name: 'Nutrition Researcher', icon: 'microscope', description: 'Nutrition science research' },
    { id: 'wellness-coach', name: 'Wellness Coach', icon: 'heart', description: 'Lifestyle and wellness counseling' }
];

const nutritionCareerMapping = {
    'clinical-dietitian': {
        required: ['NUTR301', 'NUTR302'], // Clinical Nutrition, Medical Nutrition Therapy
        recommended: ['NUTR303', 'MED102', 'NUTR304'], // Nutritional Assessment, Physiology, Disease Management
        focus: 'medical nutrition therapy, patient assessment, and clinical care'
    },
    'sports-nutritionist': {
        required: ['NUTR401', 'NUTR402'], // Sports Nutrition, Exercise Physiology
        recommended: ['NUTR403', 'KINE301', 'NUTR404'], // Performance Nutrition, Kinesiology, Supplement Science
        focus: 'athletic performance, training nutrition, and competition strategies'
    },
    'food-scientist': {
        required: ['NUTR202', 'NUTR405'], // Food Science, Food Safety
        recommended: ['NUTR406', 'CHEM303', 'NUTR407'], // Food Processing, Analytical Chemistry, Product Development
        focus: 'food development, quality control, and safety systems'
    },
    'community-nutritionist': {
        required: ['NUTR302', 'PH314'], // Community Nutrition, Health Education
        recommended: ['NUTR408', 'PH201', 'NUTR409'], // Program Planning, Epidemiology, Policy
        focus: 'community health programs, nutrition education, and policy'
    },
    'research-nutritionist': {
        required: ['NUTR201', 'NUTR410'], // Nutritional Biochemistry, Research Methods
        recommended: ['STAT309', 'NUTR411', 'BIO401'], // Biostatistics, Nutrigenomics, Molecular Biology
        focus: 'nutrition research, clinical trials, and scientific publication'
    },
    'wellness-coach': {
        required: ['NUTR412', 'NUTR413'], // Wellness Coaching, Behavior Change
        recommended: ['PSY301', 'NUTR414', 'KINE302'], // Health Psychology, Lifestyle Medicine, Fitness
        focus: 'lifestyle counseling, behavior modification, and wellness programs'
    }
};

// Export all career data
const completeCareerExpansion = {
    chemistry: { paths: chemistryCareerPaths, mapping: chemistryCareerMapping },
    environment: { paths: environmentCareerPaths, mapping: environmentCareerMapping },
    civil: { paths: civilCareerPaths, mapping: civilCareerMapping },
    chemeng: { paths: chemEngCareerPaths, mapping: chemEngCareerMapping },
    bme: { paths: bmeCareerPaths, mapping: bmeCareerMapping },
    economics: { paths: economicsCareerPaths, mapping: economicsCareerMapping },
    finance: { paths: financeCareerPaths, mapping: financeCareerMapping },
    psychology: { paths: psychologyCareerPaths, mapping: psychologyCareerMapping },
    policy: { paths: politicalCareerPaths, mapping: politicalCareerMapping },
    education: { paths: educationCareerPaths, mapping: educationCareerMapping },
    medicine: { paths: medicineCareerPaths, mapping: medicineCareerMapping },
    nursing: { paths: nursingCareerPaths, mapping: nursingCareerMapping },
    pharmacy: { paths: pharmacyCareerPaths, mapping: pharmacyCareerMapping },
    'public-health': { paths: publicHealthCareerPaths, mapping: publicHealthCareerMapping },
    nutrition: { paths: nutritionCareerPaths, mapping: nutritionCareerMapping }
};

console.log('Complete Career Paths Expansion Loaded');
console.log('Total majors with expanded careers:', Object.keys(completeCareerExpansion).length);
Object.entries(completeCareerExpansion).forEach(([major, data]) => {
    console.log(`${major}: ${data.paths.length} career paths`);
});