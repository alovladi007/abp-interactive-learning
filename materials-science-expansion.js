// Materials Science Expansion - Complete Course Catalog and Career Paths

// Materials Science Complete Course Catalog
const materialsCourseCatalog = {
    // Foundation Courses (100-level)
    'MAT101': { 
        id: 'MAT101', 
        name: 'Introduction to Materials Science', 
        credits: 4, 
        prerequisites: [], 
        description: 'Crystal structures, bonding, defects, and basic properties of materials', 
        level: 'foundation' 
    },
    'MAT102': { 
        id: 'MAT102', 
        name: 'Materials Chemistry', 
        credits: 3, 
        prerequisites: [], 
        description: 'Chemical principles in materials science, reactions, and synthesis', 
        level: 'foundation' 
    },
    'MAT103': { 
        id: 'MAT103', 
        name: 'Materials Physics', 
        credits: 3, 
        prerequisites: [], 
        description: 'Physical properties of materials, quantum mechanics applications', 
        level: 'foundation' 
    },
    'MAT104': { 
        id: 'MAT104', 
        name: 'Materials Laboratory I', 
        credits: 2, 
        prerequisites: [], 
        description: 'Basic materials characterization techniques and experiments', 
        level: 'foundation' 
    },
    
    // Core Courses (200-level)
    'MAT201': { 
        id: 'MAT201', 
        name: 'Thermodynamics of Materials', 
        credits: 4, 
        prerequisites: ['MAT101'], 
        description: 'Phase diagrams, phase transformations, and thermodynamic principles', 
        level: 'core' 
    },
    'MAT202': { 
        id: 'MAT202', 
        name: 'Mechanical Behavior of Materials', 
        credits: 4, 
        prerequisites: ['MAT101'], 
        description: 'Stress-strain relationships, deformation mechanisms, fracture, and fatigue', 
        level: 'core' 
    },
    'MAT203': { 
        id: 'MAT203', 
        name: 'Electronic Properties of Materials', 
        credits: 4, 
        prerequisites: ['MAT103'], 
        description: 'Band theory, semiconductors, conductors, and insulators', 
        level: 'core' 
    },
    'MAT204': { 
        id: 'MAT204', 
        name: 'Materials Characterization', 
        credits: 4, 
        prerequisites: ['MAT104'], 
        description: 'X-ray diffraction, electron microscopy, spectroscopy techniques', 
        level: 'core' 
    },
    'MAT205': { 
        id: 'MAT205', 
        name: 'Materials Processing', 
        credits: 3, 
        prerequisites: ['MAT101'], 
        description: 'Casting, forming, joining, and powder processing techniques', 
        level: 'core' 
    },
    'MAT206': { 
        id: 'MAT206', 
        name: 'Crystallography and Diffraction', 
        credits: 3, 
        prerequisites: ['MAT101'], 
        description: 'Crystal systems, symmetry, reciprocal lattice, diffraction theory', 
        level: 'core' 
    },
    
    // Advanced Core (300-level)
    'MAT301': { 
        id: 'MAT301', 
        name: 'Polymer Science and Engineering', 
        credits: 4, 
        prerequisites: ['MAT102', 'MAT201'], 
        description: 'Polymer synthesis, structure-property relationships, processing', 
        level: 'advanced' 
    },
    'MAT302': { 
        id: 'MAT302', 
        name: 'Ceramic Materials', 
        credits: 4, 
        prerequisites: ['MAT201'], 
        description: 'Ceramic structures, processing, mechanical and thermal properties', 
        level: 'advanced' 
    },
    'MAT303': { 
        id: 'MAT303', 
        name: 'Metallic Materials', 
        credits: 4, 
        prerequisites: ['MAT202'], 
        description: 'Alloy theory, steel metallurgy, non-ferrous alloys, heat treatment', 
        level: 'advanced' 
    },
    'MAT304': { 
        id: 'MAT304', 
        name: 'Composite Materials', 
        credits: 4, 
        prerequisites: ['MAT202'], 
        description: 'Fiber-reinforced composites, design, manufacturing, and applications', 
        level: 'advanced' 
    },
    'MAT305': { 
        id: 'MAT305', 
        name: 'Nanomaterials and Nanotechnology', 
        credits: 4, 
        prerequisites: ['MAT203', 'MAT204'], 
        description: 'Synthesis, properties, and applications of nanoscale materials', 
        level: 'advanced' 
    },
    'MAT306': { 
        id: 'MAT306', 
        name: 'Biomaterials', 
        credits: 3, 
        prerequisites: ['MAT301'], 
        description: 'Materials for medical implants, tissue engineering, biocompatibility', 
        level: 'advanced' 
    },
    'MAT307': { 
        id: 'MAT307', 
        name: 'Magnetic and Optical Materials', 
        credits: 3, 
        prerequisites: ['MAT203'], 
        description: 'Ferromagnetism, optical properties, photonic materials', 
        level: 'advanced' 
    },
    'MAT308': { 
        id: 'MAT308', 
        name: 'Computational Materials Science', 
        credits: 3, 
        prerequisites: ['MAT201', 'CS101'], 
        description: 'Molecular dynamics, DFT, phase field modeling, Monte Carlo methods', 
        level: 'advanced' 
    },
    'MAT309': { 
        id: 'MAT309', 
        name: 'Corrosion and Degradation', 
        credits: 3, 
        prerequisites: ['MAT102', 'MAT303'], 
        description: 'Corrosion mechanisms, protection methods, environmental degradation', 
        level: 'advanced' 
    },
    'MAT310': { 
        id: 'MAT310', 
        name: 'Materials Laboratory II', 
        credits: 2, 
        prerequisites: ['MAT204'], 
        description: 'Advanced characterization, synthesis, and processing experiments', 
        level: 'advanced' 
    },
    
    // Specialized/Advanced (400-level)
    'MAT401': { 
        id: 'MAT401', 
        name: 'Energy Storage Materials', 
        credits: 4, 
        prerequisites: ['MAT203', 'MAT301'], 
        description: 'Battery materials, fuel cells, supercapacitors, hydrogen storage', 
        level: 'specialized' 
    },
    'MAT402': { 
        id: 'MAT402', 
        name: 'Advanced Semiconductor Materials', 
        credits: 4, 
        prerequisites: ['MAT203', 'MAT305'], 
        description: 'Wide bandgap semiconductors, 2D materials, quantum dots', 
        level: 'specialized' 
    },
    'MAT403': { 
        id: 'MAT403', 
        name: 'Materials for Sustainable Energy', 
        credits: 3, 
        prerequisites: ['MAT401'], 
        description: 'Solar cells, thermoelectrics, energy harvesting materials', 
        level: 'specialized' 
    },
    'MAT404': { 
        id: 'MAT404', 
        name: 'Advanced Manufacturing', 
        credits: 3, 
        prerequisites: ['MAT205', 'MAT304'], 
        description: '3D printing, additive manufacturing, smart manufacturing', 
        level: 'specialized' 
    },
    'MAT405': { 
        id: 'MAT405', 
        name: 'Materials Failure Analysis', 
        credits: 3, 
        prerequisites: ['MAT202', 'MAT309'], 
        description: 'Failure mechanisms, forensic analysis, case studies', 
        level: 'specialized' 
    },
    'MAT406': { 
        id: 'MAT406', 
        name: 'Surface Science and Engineering', 
        credits: 3, 
        prerequisites: ['MAT204', 'MAT309'], 
        description: 'Surface phenomena, coatings, thin films, surface modification', 
        level: 'specialized' 
    },
    'MAT407': { 
        id: 'MAT407', 
        name: 'Materials Design and Selection', 
        credits: 3, 
        prerequisites: ['MAT303', 'MAT304'], 
        description: 'Materials selection methodology, Ashby charts, design optimization', 
        level: 'specialized' 
    },
    'MAT408': { 
        id: 'MAT408', 
        name: 'Quantum Materials', 
        credits: 3, 
        prerequisites: ['MAT203', 'PHYS302'], 
        description: 'Superconductors, topological insulators, quantum phenomena', 
        level: 'specialized' 
    },
    'MAT409': { 
        id: 'MAT409', 
        name: 'Materials Entrepreneurship', 
        credits: 2, 
        prerequisites: ['MAT301', 'MAT302', 'MAT303'], 
        description: 'Technology commercialization, IP, startup strategies', 
        level: 'specialized' 
    },
    'MAT410': { 
        id: 'MAT410', 
        name: 'Senior Design Project', 
        credits: 4, 
        prerequisites: ['MAT310'], 
        description: 'Capstone design project in materials engineering', 
        level: 'specialized' 
    }
};

// Materials Science Career Paths
const materialsCareerPaths = [
    { 
        id: 'nano-engineer', 
        name: 'Nanomaterials Engineer', 
        icon: 'atom', 
        description: 'Design and develop nanoscale materials for advanced applications' 
    },
    { 
        id: 'battery-engineer', 
        name: 'Battery/Energy Storage Engineer', 
        icon: 'battery-full', 
        description: 'Develop materials for batteries and energy storage systems' 
    },
    { 
        id: 'semiconductor-engineer', 
        name: 'Semiconductor Materials Engineer', 
        icon: 'microchip', 
        description: 'Work on electronic materials for chips and devices' 
    },
    { 
        id: 'biomaterials-engineer', 
        name: 'Biomaterials Engineer', 
        icon: 'dna', 
        description: 'Develop materials for medical implants and tissue engineering' 
    },
    { 
        id: 'polymer-engineer', 
        name: 'Polymer Engineer', 
        icon: 'link', 
        description: 'Design and process polymer materials and composites' 
    },
    { 
        id: 'metallurgist', 
        name: 'Metallurgical Engineer', 
        icon: 'hammer', 
        description: 'Develop and process metallic materials and alloys' 
    },
    { 
        id: 'failure-analyst', 
        name: 'Materials Failure Analyst', 
        icon: 'search', 
        description: 'Investigate material failures and improve reliability' 
    },
    { 
        id: 'computational-materials', 
        name: 'Computational Materials Scientist', 
        icon: 'calculator', 
        description: 'Model and simulate materials using computational methods' 
    }
];

// Career-specific course mappings for Materials Science
const materialsCareerCourseMapping = {
    'nano-engineer': {
        required: ['MAT305', 'MAT402', 'MAT408'], // Nanomaterials, Advanced Semi, Quantum
        recommended: ['MAT204', 'MAT406', 'MAT308', 'PHYS302'], // Characterization, Surface, Computational, Quantum Mech
        focus: 'nanoscale materials synthesis, characterization, and applications'
    },
    'battery-engineer': {
        required: ['MAT401', 'MAT403'], // Energy Storage, Sustainable Energy
        recommended: ['MAT203', 'MAT301', 'MAT309', 'CHEM301'], // Electronic Props, Polymers, Corrosion, Physical Chem
        focus: 'energy storage materials and electrochemical systems'
    },
    'semiconductor-engineer': {
        required: ['MAT203', 'MAT402'], // Electronic Properties, Advanced Semiconductors
        recommended: ['MAT305', 'MAT406', 'MAT206', 'EE301'], // Nano, Surface, Crystallography, Electronics
        focus: 'electronic materials for semiconductor devices'
    },
    'biomaterials-engineer': {
        required: ['MAT306'], // Biomaterials
        recommended: ['MAT301', 'MAT302', 'MAT309', 'BME202', 'CHEM402'], // Polymers, Ceramics, Corrosion, Biomaterials, Biochem
        focus: 'biocompatible materials for medical applications'
    },
    'polymer-engineer': {
        required: ['MAT301', 'MAT304'], // Polymers, Composites
        recommended: ['MAT205', 'MAT404', 'MAT309', 'CHEM201'], // Processing, Adv Manufacturing, Corrosion, Organic
        focus: 'polymer synthesis, processing, and composite materials'
    },
    'metallurgist': {
        required: ['MAT303', 'MAT309'], // Metallic Materials, Corrosion
        recommended: ['MAT201', 'MAT202', 'MAT405', 'MAT205'], // Thermo, Mechanical, Failure, Processing
        focus: 'metal alloys, processing, and heat treatment'
    },
    'failure-analyst': {
        required: ['MAT405', 'MAT202'], // Failure Analysis, Mechanical Behavior
        recommended: ['MAT309', 'MAT204', 'MAT303', 'MAT304'], // Corrosion, Characterization, Metals, Composites
        focus: 'failure mechanisms, forensic analysis, and reliability'
    },
    'computational-materials': {
        required: ['MAT308'], // Computational Materials
        recommended: ['MAT201', 'CS201', 'MATH301', 'PHYS302'], // Thermo, Data Structures, Linear Algebra, Quantum
        focus: 'computational modeling and simulation of materials'
    }
};

// Export the expanded Materials Science data
const materialsExpansion = {
    courseCatalog: materialsCourseCatalog,
    careerPaths: materialsCareerPaths,
    careerCourseMapping: materialsCareerCourseMapping,
    
    // Summary statistics
    stats: {
        totalCourses: Object.keys(materialsCourseCatalog).length,
        foundationCourses: Object.values(materialsCourseCatalog).filter(c => c.level === 'foundation').length,
        coreCourses: Object.values(materialsCourseCatalog).filter(c => c.level === 'core').length,
        advancedCourses: Object.values(materialsCourseCatalog).filter(c => c.level === 'advanced').length,
        specializedCourses: Object.values(materialsCourseCatalog).filter(c => c.level === 'specialized').length,
        totalCareerPaths: materialsCareerPaths.length
    }
};

console.log('Materials Science Expansion Loaded:');
console.log(`- ${materialsExpansion.stats.totalCourses} total courses`);
console.log(`- ${materialsExpansion.stats.foundationCourses} foundation courses`);
console.log(`- ${materialsExpansion.stats.coreCourses} core courses`);
console.log(`- ${materialsExpansion.stats.advancedCourses} advanced courses`);
console.log(`- ${materialsExpansion.stats.specializedCourses} specialized courses`);
console.log(`- ${materialsExpansion.stats.totalCareerPaths} career paths`);