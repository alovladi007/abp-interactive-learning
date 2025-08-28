// Expanded Course Catalogs - Full Academic Programs for All Majors

// Chemistry - Complete 30-course catalog
const chemistryCourseCatalog = [
    // Foundation (100-level)
    { id: 'CHEM101', name: 'General Chemistry I', credits: 4, prerequisites: [], description: 'Atomic structure, bonding, stoichiometry', level: 'foundation' },
    { id: 'CHEM102', name: 'General Chemistry II', credits: 4, prerequisites: ['CHEM101'], description: 'Kinetics, equilibrium, thermodynamics', level: 'foundation' },
    { id: 'CHEM103', name: 'General Chemistry Lab I', credits: 1, prerequisites: [], description: 'Basic laboratory techniques', level: 'foundation' },
    { id: 'CHEM104', name: 'General Chemistry Lab II', credits: 1, prerequisites: ['CHEM103'], description: 'Advanced laboratory techniques', level: 'foundation' },
    
    // Core (200-level)
    { id: 'CHEM201', name: 'Organic Chemistry I', credits: 4, prerequisites: ['CHEM102'], description: 'Structure, nomenclature, reactions of organic compounds', level: 'core' },
    { id: 'CHEM202', name: 'Organic Chemistry II', credits: 4, prerequisites: ['CHEM201'], description: 'Aromatic compounds, carbonyl chemistry, biomolecules', level: 'core' },
    { id: 'CHEM203', name: 'Organic Chemistry Lab I', credits: 2, prerequisites: ['CHEM201'], description: 'Organic synthesis and purification', level: 'core' },
    { id: 'CHEM204', name: 'Organic Chemistry Lab II', credits: 2, prerequisites: ['CHEM203'], description: 'Multi-step synthesis and characterization', level: 'core' },
    { id: 'CHEM205', name: 'Quantitative Analysis', credits: 3, prerequisites: ['CHEM102'], description: 'Classical analytical methods', level: 'core' },
    { id: 'CHEM206', name: 'Quantitative Analysis Lab', credits: 1, prerequisites: ['CHEM205'], description: 'Analytical laboratory techniques', level: 'core' },
    
    // Advanced Core (300-level)
    { id: 'CHEM301', name: 'Physical Chemistry I', credits: 4, prerequisites: ['CHEM102', 'MATH201'], description: 'Thermodynamics and kinetics', level: 'advanced' },
    { id: 'CHEM302', name: 'Physical Chemistry II', credits: 4, prerequisites: ['CHEM301'], description: 'Quantum mechanics and spectroscopy', level: 'advanced' },
    { id: 'CHEM303', name: 'Analytical Chemistry', credits: 4, prerequisites: ['CHEM205'], description: 'Modern analytical techniques and instrumentation', level: 'advanced' },
    { id: 'CHEM304', name: 'Instrumental Analysis', credits: 3, prerequisites: ['CHEM303'], description: 'Spectroscopy, chromatography, mass spectrometry', level: 'advanced' },
    { id: 'CHEM305', name: 'Separation Science', credits: 3, prerequisites: ['CHEM303'], description: 'Chromatographic and electrophoretic methods', level: 'advanced' },
    { id: 'CHEM306', name: 'Advanced Organic Chemistry', credits: 3, prerequisites: ['CHEM202'], description: 'Reaction mechanisms and synthesis strategies', level: 'advanced' },
    { id: 'CHEM307', name: 'Organometallic Chemistry', credits: 3, prerequisites: ['CHEM306', 'CHEM401'], description: 'Metal-carbon bonds and catalysis', level: 'advanced' },
    { id: 'CHEM308', name: 'Forensic Chemistry', credits: 3, prerequisites: ['CHEM303'], description: 'Chemical evidence analysis', level: 'advanced' },
    { id: 'CHEM309', name: 'Toxicology', credits: 3, prerequisites: ['CHEM202', 'BIO201'], description: 'Toxic substances and their effects', level: 'advanced' },
    { id: 'CHEM310', name: 'Polymer Chemistry', credits: 3, prerequisites: ['CHEM202', 'CHEM301'], description: 'Polymer synthesis and properties', level: 'advanced' },
    
    // Specialized (400-level)
    { id: 'CHEM401', name: 'Inorganic Chemistry', credits: 4, prerequisites: ['CHEM302'], description: 'Transition metals, coordination compounds', level: 'specialized' },
    { id: 'CHEM402', name: 'Biochemistry I', credits: 4, prerequisites: ['CHEM202'], description: 'Proteins, enzymes, metabolism', level: 'specialized' },
    { id: 'CHEM403', name: 'Biochemistry II', credits: 4, prerequisites: ['CHEM402'], description: 'Nucleic acids, gene expression, biotechnology', level: 'specialized' },
    { id: 'CHEM404', name: 'Medicinal Chemistry', credits: 3, prerequisites: ['CHEM402'], description: 'Drug design and development', level: 'specialized' },
    { id: 'CHEM405', name: 'Environmental Chemistry', credits: 3, prerequisites: ['CHEM301'], description: 'Chemical processes in the environment', level: 'specialized' },
    { id: 'CHEM406', name: 'Computational Chemistry', credits: 3, prerequisites: ['CHEM302'], description: 'Molecular modeling and simulations', level: 'specialized' },
    { id: 'CHEM407', name: 'Surface Chemistry', credits: 3, prerequisites: ['CHEM301'], description: 'Interfaces, colloids, and nanomaterials', level: 'specialized' },
    { id: 'CHEM408', name: 'Chemical Biology', credits: 3, prerequisites: ['CHEM402'], description: 'Chemical approaches to biological problems', level: 'specialized' },
    { id: 'CHEM409', name: 'Advanced Spectroscopy', credits: 3, prerequisites: ['CHEM302', 'CHEM304'], description: 'NMR, MS, and advanced techniques', level: 'specialized' },
    { id: 'CHEM410', name: 'Chemistry Research Project', credits: 4, prerequisites: ['CHEM301', 'CHEM302'], description: 'Independent research project', level: 'specialized' }
];

// Environmental Science - Complete 28-course catalog
const environmentCourseCatalog = [
    // Foundation (100-level)
    { id: 'ENV101', name: 'Introduction to Environmental Science', credits: 3, prerequisites: [], description: 'Environmental systems and sustainability', level: 'foundation' },
    { id: 'ENV102', name: 'Earth Systems Science', credits: 3, prerequisites: [], description: 'Atmosphere, hydrosphere, lithosphere, biosphere', level: 'foundation' },
    { id: 'ENV103', name: 'Environmental Field Methods', credits: 2, prerequisites: [], description: 'Field sampling and measurement techniques', level: 'foundation' },
    { id: 'ENV104', name: 'Environmental Data Analysis', credits: 3, prerequisites: [], description: 'Statistical methods for environmental data', level: 'foundation' },
    
    // Core (200-level)
    { id: 'ENV201', name: 'Environmental Chemistry', credits: 4, prerequisites: ['CHEM101'], description: 'Chemical processes in the environment', level: 'core' },
    { id: 'ENV202', name: 'Ecology', credits: 4, prerequisites: ['BIO101'], description: 'Ecosystems, populations, communities', level: 'core' },
    { id: 'ENV203', name: 'Environmental Geology', credits: 3, prerequisites: ['ENV102'], description: 'Geological processes and hazards', level: 'core' },
    { id: 'ENV204', name: 'Environmental Microbiology', credits: 3, prerequisites: ['BIO101'], description: 'Microorganisms in the environment', level: 'core' },
    { id: 'ENV205', name: 'GIS for Environmental Science', credits: 3, prerequisites: ['ENV101'], description: 'Geographic information systems applications', level: 'core' },
    { id: 'ENV206', name: 'Environmental Economics', credits: 3, prerequisites: ['ECON101'], description: 'Economic analysis of environmental issues', level: 'core' },
    
    // Advanced (300-level)
    { id: 'ENV301', name: 'Air Quality Engineering', credits: 4, prerequisites: ['ENV201'], description: 'Air pollution sources, transport, control', level: 'advanced' },
    { id: 'ENV302', name: 'Water Resources Management', credits: 4, prerequisites: ['ENV201'], description: 'Surface and groundwater hydrology', level: 'advanced' },
    { id: 'ENV303', name: 'Soil Science', credits: 3, prerequisites: ['ENV201', 'ENV203'], description: 'Soil formation, properties, contamination', level: 'advanced' },
    { id: 'ENV304', name: 'Environmental Toxicology', credits: 3, prerequisites: ['ENV201', 'BIO201'], description: 'Effects of pollutants on organisms', level: 'advanced' },
    { id: 'ENV305', name: 'Environmental Impact Assessment', credits: 3, prerequisites: ['ENV101'], description: 'EIA methods and regulations', level: 'advanced' },
    { id: 'ENV306', name: 'Conservation Biology', credits: 3, prerequisites: ['ENV202'], description: 'Biodiversity preservation strategies', level: 'advanced' },
    { id: 'ENV307', name: 'Environmental Policy', credits: 3, prerequisites: ['ENV101'], description: 'Environmental law and regulation', level: 'advanced' },
    { id: 'ENV308', name: 'Waste Management', credits: 3, prerequisites: ['ENV201'], description: 'Solid and hazardous waste treatment', level: 'advanced' },
    { id: 'ENV309', name: 'Environmental Monitoring', credits: 3, prerequisites: ['ENV301', 'ENV302'], description: 'Monitoring techniques and programs', level: 'advanced' },
    { id: 'ENV310', name: 'Remote Sensing', credits: 3, prerequisites: ['ENV205'], description: 'Satellite and aerial imagery analysis', level: 'advanced' },
    
    // Specialized (400-level)
    { id: 'ENV401', name: 'Climate Change Science', credits: 4, prerequisites: ['ENV301'], description: 'Climate systems and global change', level: 'specialized' },
    { id: 'ENV402', name: 'Sustainable Engineering', credits: 3, prerequisites: ['ENV301', 'ENV302'], description: 'Green design and technology', level: 'specialized' },
    { id: 'ENV403', name: 'Atmospheric Science', credits: 3, prerequisites: ['ENV301'], description: 'Atmospheric chemistry and physics', level: 'specialized' },
    { id: 'ENV404', name: 'Climate Modeling', credits: 3, prerequisites: ['ENV401'], description: 'Computational climate models', level: 'specialized' },
    { id: 'ENV405', name: 'Restoration Ecology', credits: 3, prerequisites: ['ENV306'], description: 'Ecosystem restoration techniques', level: 'specialized' },
    { id: 'ENV406', name: 'Environmental Law', credits: 3, prerequisites: ['ENV307'], description: 'Environmental legislation and compliance', level: 'specialized' },
    { id: 'ENV407', name: 'Marine Environmental Science', credits: 3, prerequisites: ['ENV202'], description: 'Ocean ecosystems and pollution', level: 'specialized' },
    { id: 'ENV408', name: 'Environmental Capstone Project', credits: 4, prerequisites: ['ENV305'], description: 'Comprehensive environmental project', level: 'specialized' }
];

// Civil Engineering - Complete 32-course catalog
const civilCourseCatalog = [
    // Foundation (100-level)
    { id: 'CE101', name: 'Engineering Mechanics - Statics', credits: 3, prerequisites: [], description: 'Force systems and equilibrium', level: 'foundation' },
    { id: 'CE102', name: 'Engineering Mechanics - Dynamics', credits: 3, prerequisites: ['CE101'], description: 'Kinematics and kinetics', level: 'foundation' },
    { id: 'CE103', name: 'Engineering Graphics', credits: 2, prerequisites: [], description: 'CAD and technical drawing', level: 'foundation' },
    { id: 'CE104', name: 'Surveying', credits: 3, prerequisites: [], description: 'Land surveying and mapping', level: 'foundation' },
    
    // Core (200-level)
    { id: 'CE201', name: 'Structural Analysis I', credits: 3, prerequisites: ['CE101'], description: 'Analysis of determinate structures', level: 'core' },
    { id: 'CE202', name: 'Soil Mechanics', credits: 4, prerequisites: ['CE101'], description: 'Soil properties and behavior', level: 'core' },
    { id: 'CE203', name: 'Fluid Mechanics', credits: 4, prerequisites: ['CE102'], description: 'Fluid statics and dynamics', level: 'core' },
    { id: 'CE204', name: 'Materials of Construction', credits: 3, prerequisites: [], description: 'Properties of civil engineering materials', level: 'core' },
    { id: 'CE205', name: 'Engineering Economics', credits: 3, prerequisites: [], description: 'Economic analysis for engineering', level: 'core' },
    { id: 'CE206', name: 'Numerical Methods', credits: 3, prerequisites: ['MATH201'], description: 'Computational methods in civil engineering', level: 'core' },
    
    // Advanced Core (300-level)
    { id: 'CE301', name: 'Reinforced Concrete Design', credits: 4, prerequisites: ['CE201'], description: 'Design of concrete structures', level: 'advanced' },
    { id: 'CE302', name: 'Steel Design', credits: 4, prerequisites: ['CE201'], description: 'Design of steel structures', level: 'advanced' },
    { id: 'CE303', name: 'Transportation Engineering', credits: 3, prerequisites: ['CE104'], description: 'Highway and traffic engineering', level: 'advanced' },
    { id: 'CE304', name: 'Structural Analysis II', credits: 3, prerequisites: ['CE201'], description: 'Indeterminate structures and matrix methods', level: 'advanced' },
    { id: 'CE305', name: 'Foundation Engineering', credits: 3, prerequisites: ['CE202'], description: 'Design of foundations', level: 'advanced' },
    { id: 'CE306', name: 'Hydraulic Engineering', credits: 3, prerequisites: ['CE203'], description: 'Open channel flow and hydraulic structures', level: 'advanced' },
    { id: 'CE307', name: 'Construction Management', credits: 3, prerequisites: ['CE205'], description: 'Project planning and management', level: 'advanced' },
    { id: 'CE308', name: 'Environmental Engineering', credits: 3, prerequisites: ['CE203'], description: 'Water and wastewater treatment', level: 'advanced' },
    { id: 'CE309', name: 'Geotechnical Engineering', credits: 3, prerequisites: ['CE202'], description: 'Slope stability and earth structures', level: 'advanced' },
    { id: 'CE310', name: 'Structural Dynamics', credits: 3, prerequisites: ['CE304'], description: 'Dynamic analysis of structures', level: 'advanced' },
    
    // Specialized (400-level)
    { id: 'CE401', name: 'Hydrology', credits: 3, prerequisites: ['CE306'], description: 'Surface and groundwater hydrology', level: 'specialized' },
    { id: 'CE402', name: 'Water Resources Engineering', credits: 3, prerequisites: ['CE401'], description: 'Water supply and distribution', level: 'specialized' },
    { id: 'CE403', name: 'Advanced Structural Design', credits: 3, prerequisites: ['CE301', 'CE302'], description: 'Complex structural systems', level: 'specialized' },
    { id: 'CE404', name: 'Earthquake Engineering', credits: 3, prerequisites: ['CE310'], description: 'Seismic analysis and design', level: 'specialized' },
    { id: 'CE405', name: 'Bridge Engineering', credits: 3, prerequisites: ['CE301', 'CE302'], description: 'Bridge design and analysis', level: 'specialized' },
    { id: 'CE406', name: 'Traffic Engineering', credits: 3, prerequisites: ['CE303'], description: 'Traffic flow and control', level: 'specialized' },
    { id: 'CE407', name: 'Highway Design', credits: 3, prerequisites: ['CE303'], description: 'Geometric design of highways', level: 'specialized' },
    { id: 'CE408', name: 'Airport and Railway Engineering', credits: 3, prerequisites: ['CE303'], description: 'Design of airports and railways', level: 'specialized' },
    { id: 'CE409', name: 'Coastal Engineering', credits: 3, prerequisites: ['CE306'], description: 'Coastal processes and structures', level: 'specialized' },
    { id: 'CE410', name: 'Rock Mechanics', credits: 3, prerequisites: ['CE309'], description: 'Rock properties and tunneling', level: 'specialized' },
    { id: 'CE411', name: 'Pavement Design', credits: 3, prerequisites: ['CE303', 'CE204'], description: 'Flexible and rigid pavement design', level: 'specialized' },
    { id: 'CE412', name: 'Senior Design Project', credits: 4, prerequisites: ['CE301', 'CE302'], description: 'Comprehensive civil engineering project', level: 'specialized' }
];

// Chemical Engineering - Complete 28-course catalog
const chemEngCourseCatalog = [
    // Foundation (100-level)
    { id: 'CHE101', name: 'Introduction to Chemical Engineering', credits: 3, prerequisites: [], description: 'Chemical engineering principles', level: 'foundation' },
    { id: 'CHE102', name: 'Material and Energy Balances', credits: 4, prerequisites: ['CHEM101'], description: 'Conservation principles', level: 'foundation' },
    { id: 'CHE103', name: 'Chemical Engineering Calculations', credits: 3, prerequisites: [], description: 'Engineering calculations and analysis', level: 'foundation' },
    
    // Core (200-level)
    { id: 'CHE201', name: 'Chemical Engineering Thermodynamics I', credits: 3, prerequisites: ['CHE102'], description: 'Laws of thermodynamics', level: 'core' },
    { id: 'CHE202', name: 'Chemical Engineering Thermodynamics II', credits: 3, prerequisites: ['CHE201'], description: 'Phase equilibria and chemical equilibrium', level: 'core' },
    { id: 'CHE203', name: 'Fluid Mechanics', credits: 3, prerequisites: ['CHE102'], description: 'Fluid flow and transport', level: 'core' },
    { id: 'CHE204', name: 'Heat Transfer', credits: 3, prerequisites: ['CHE203'], description: 'Heat transfer mechanisms', level: 'core' },
    { id: 'CHE205', name: 'Mass Transfer', credits: 3, prerequisites: ['CHE203'], description: 'Mass transfer operations', level: 'core' },
    { id: 'CHE206', name: 'Chemical Engineering Laboratory I', credits: 2, prerequisites: ['CHE203'], description: 'Transport phenomena experiments', level: 'core' },
    
    // Advanced (300-level)
    { id: 'CHE301', name: 'Chemical Reaction Engineering', credits: 4, prerequisites: ['CHE201'], description: 'Reactor design and kinetics', level: 'advanced' },
    { id: 'CHE302', name: 'Process Control', credits: 3, prerequisites: ['CHE301'], description: 'Process dynamics and control', level: 'advanced' },
    { id: 'CHE303', name: 'Separation Processes', credits: 3, prerequisites: ['CHE205'], description: 'Distillation, extraction, absorption', level: 'advanced' },
    { id: 'CHE304', name: 'Process Design I', credits: 3, prerequisites: ['CHE301', 'CHE303'], description: 'Equipment design and sizing', level: 'advanced' },
    { id: 'CHE305', name: 'Process Design II', credits: 3, prerequisites: ['CHE304'], description: 'Process flowsheet development', level: 'advanced' },
    { id: 'CHE306', name: 'Chemical Engineering Laboratory II', credits: 2, prerequisites: ['CHE301'], description: 'Reaction and separation experiments', level: 'advanced' },
    { id: 'CHE307', name: 'Process Safety', credits: 3, prerequisites: ['CHE301'], description: 'Safety in chemical processes', level: 'advanced' },
    { id: 'CHE308', name: 'Process Economics', credits: 3, prerequisites: ['CHE304'], description: 'Economic evaluation of processes', level: 'advanced' },
    
    // Specialized (400-level)
    { id: 'CHE401', name: 'Plant Design Project', credits: 4, prerequisites: ['CHE305'], description: 'Complete plant design project', level: 'specialized' },
    { id: 'CHE402', name: 'Process Optimization', credits: 3, prerequisites: ['CHE305'], description: 'Optimization techniques', level: 'specialized' },
    { id: 'CHE403', name: 'Biochemical Engineering', credits: 3, prerequisites: ['CHE301'], description: 'Bioprocessing and fermentation', level: 'specialized' },
    { id: 'CHE404', name: 'Polymer Engineering', credits: 3, prerequisites: ['CHE301'], description: 'Polymer processing and properties', level: 'specialized' },
    { id: 'CHE405', name: 'Petroleum Refining', credits: 3, prerequisites: ['CHE303'], description: 'Oil refining processes', level: 'specialized' },
    { id: 'CHE406', name: 'Natural Gas Processing', credits: 3, prerequisites: ['CHE303'], description: 'Gas processing and LNG', level: 'specialized' },
    { id: 'CHE407', name: 'Catalysis and Catalytic Processes', credits: 3, prerequisites: ['CHE301'], description: 'Heterogeneous catalysis', level: 'specialized' },
    { id: 'CHE408', name: 'Pharmaceutical Engineering', credits: 3, prerequisites: ['CHE403'], description: 'Drug manufacturing processes', level: 'specialized' },
    { id: 'CHE409', name: 'Environmental Chemical Engineering', credits: 3, prerequisites: ['CHE301'], description: 'Pollution control technologies', level: 'specialized' },
    { id: 'CHE410', name: 'Energy Systems Engineering', credits: 3, prerequisites: ['CHE201'], description: 'Energy conversion and storage', level: 'specialized' },
    { id: 'CHE411', name: 'Nanotechnology in Chemical Engineering', credits: 3, prerequisites: ['CHE301'], description: 'Nanoscale phenomena and applications', level: 'specialized' }
];

// Biomedical Engineering - Complete 28-course catalog
const bmeCourseCatalog = [
    // Foundation (100-level)
    { id: 'BME101', name: 'Introduction to Biomedical Engineering', credits: 3, prerequisites: [], description: 'Overview of biomedical engineering', level: 'foundation' },
    { id: 'BME102', name: 'Human Anatomy for Engineers', credits: 3, prerequisites: [], description: 'Anatomical systems and structures', level: 'foundation' },
    { id: 'BME103', name: 'Human Physiology for Engineers', credits: 3, prerequisites: ['BME102'], description: 'Physiological systems and functions', level: 'foundation' },
    { id: 'BME104', name: 'Biomedical Computing', credits: 3, prerequisites: [], description: 'Programming for biomedical applications', level: 'foundation' },
    
    // Core (200-level)
    { id: 'BME201', name: 'Biomechanics', credits: 4, prerequisites: ['BME103'], description: 'Mechanics of biological systems', level: 'core' },
    { id: 'BME202', name: 'Biomaterials', credits: 4, prerequisites: ['BME101'], description: 'Materials for medical applications', level: 'core' },
    { id: 'BME203', name: 'Biomedical Transport Phenomena', credits: 3, prerequisites: ['BME103'], description: 'Mass and heat transfer in biological systems', level: 'core' },
    { id: 'BME204', name: 'Biomedical Signals and Systems', credits: 3, prerequisites: ['BME104'], description: 'Signal processing for biomedical signals', level: 'core' },
    { id: 'BME205', name: 'Cell and Molecular Biology for Engineers', credits: 3, prerequisites: ['BME101'], description: 'Cellular and molecular processes', level: 'core' },
    { id: 'BME206', name: 'Biomedical Laboratory I', credits: 2, prerequisites: ['BME201'], description: 'Basic biomedical experiments', level: 'core' },
    
    // Advanced (300-level)
    { id: 'BME301', name: 'Bioinstrumentation', credits: 4, prerequisites: ['BME204'], description: 'Medical instrumentation and sensors', level: 'advanced' },
    { id: 'BME302', name: 'Medical Imaging', credits: 4, prerequisites: ['BME204'], description: 'X-ray, CT, MRI, ultrasound', level: 'advanced' },
    { id: 'BME303', name: 'Biomedical Optics', credits: 3, prerequisites: ['BME301'], description: 'Optical techniques in medicine', level: 'advanced' },
    { id: 'BME304', name: 'Tissue Engineering', credits: 3, prerequisites: ['BME202', 'BME205'], description: 'Engineering tissues and organs', level: 'advanced' },
    { id: 'BME305', name: 'Biofluid Mechanics', credits: 3, prerequisites: ['BME203'], description: 'Blood flow and cardiovascular mechanics', level: 'advanced' },
    { id: 'BME306', name: 'Biomedical Laboratory II', credits: 2, prerequisites: ['BME301'], description: 'Advanced biomedical experiments', level: 'advanced' },
    { id: 'BME307', name: 'Biocompatibility', credits: 3, prerequisites: ['BME202'], description: 'Host response to biomaterials', level: 'advanced' },
    { id: 'BME308', name: 'Biomedical Ethics and Regulations', credits: 2, prerequisites: ['BME301'], description: 'FDA regulations and ethical considerations', level: 'advanced' },
    
    // Specialized (400-level)
    { id: 'BME401', name: 'Medical Device Design', credits: 4, prerequisites: ['BME301'], description: 'Design and development of medical devices', level: 'specialized' },
    { id: 'BME402', name: 'Clinical Engineering', credits: 3, prerequisites: ['BME301'], description: 'Hospital equipment management', level: 'specialized' },
    { id: 'BME403', name: 'Neural Engineering', credits: 3, prerequisites: ['BME301'], description: 'Neural interfaces and neuroprosthetics', level: 'specialized' },
    { id: 'BME404', name: 'Cardiovascular Engineering', credits: 3, prerequisites: ['BME305'], description: 'Cardiovascular devices and therapies', level: 'specialized' },
    { id: 'BME405', name: 'Orthopedic Biomechanics', credits: 3, prerequisites: ['BME201'], description: 'Musculoskeletal mechanics and implants', level: 'specialized' },
    { id: 'BME406', name: 'Rehabilitation Engineering', credits: 3, prerequisites: ['BME201'], description: 'Assistive technologies and prosthetics', level: 'specialized' },
    { id: 'BME407', name: 'Drug Delivery Systems', credits: 3, prerequisites: ['BME203'], description: 'Controlled drug release technologies', level: 'specialized' },
    { id: 'BME408', name: 'Biomedical Nanotechnology', credits: 3, prerequisites: ['BME202'], description: 'Nanoscale biomedical applications', level: 'specialized' },
    { id: 'BME409', name: 'Systems Biology', credits: 3, prerequisites: ['BME205'], description: 'Computational modeling of biological systems', level: 'specialized' },
    { id: 'BME410', name: 'Senior Design Project', credits: 4, prerequisites: ['BME401'], description: 'Capstone biomedical engineering project', level: 'specialized' }
];

// Economics - Complete 30-course catalog
const economicsCourseCatalog = [
    // Foundation (100-level)
    { id: 'ECON101', name: 'Principles of Microeconomics', credits: 3, prerequisites: [], description: 'Consumer and firm behavior', level: 'foundation' },
    { id: 'ECON102', name: 'Principles of Macroeconomics', credits: 3, prerequisites: [], description: 'National economy and policy', level: 'foundation' },
    { id: 'ECON103', name: 'Mathematics for Economics', credits: 3, prerequisites: [], description: 'Mathematical tools for economics', level: 'foundation' },
    { id: 'ECON104', name: 'Economic Statistics', credits: 3, prerequisites: [], description: 'Statistical methods in economics', level: 'foundation' },
    
    // Core (200-level)
    { id: 'ECON201', name: 'Intermediate Microeconomics', credits: 4, prerequisites: ['ECON101', 'ECON103'], description: 'Advanced microeconomic theory', level: 'core' },
    { id: 'ECON202', name: 'Intermediate Macroeconomics', credits: 4, prerequisites: ['ECON102', 'ECON103'], description: 'Advanced macroeconomic theory', level: 'core' },
    { id: 'ECON203', name: 'Money and Banking', credits: 3, prerequisites: ['ECON102'], description: 'Financial institutions and monetary policy', level: 'core' },
    { id: 'ECON204', name: 'Economic History', credits: 3, prerequisites: ['ECON101', 'ECON102'], description: 'Historical development of economies', level: 'core' },
    { id: 'ECON205', name: 'Mathematical Economics', credits: 3, prerequisites: ['ECON201'], description: 'Mathematical modeling in economics', level: 'core' },
    { id: 'ECON206', name: 'Game Theory', credits: 3, prerequisites: ['ECON201'], description: 'Strategic decision making', level: 'core' },
    
    // Advanced (300-level)
    { id: 'ECON301', name: 'Econometrics I', credits: 4, prerequisites: ['ECON104', 'ECON201'], description: 'Regression analysis and hypothesis testing', level: 'advanced' },
    { id: 'ECON302', name: 'International Economics', credits: 3, prerequisites: ['ECON201', 'ECON202'], description: 'Trade and finance', level: 'advanced' },
    { id: 'ECON303', name: 'Financial Economics', credits: 3, prerequisites: ['ECON201'], description: 'Asset pricing and financial markets', level: 'advanced' },
    { id: 'ECON304', name: 'Labor Economics', credits: 3, prerequisites: ['ECON201'], description: 'Labor markets and employment', level: 'advanced' },
    { id: 'ECON305', name: 'Public Economics', credits: 3, prerequisites: ['ECON201'], description: 'Government spending and taxation', level: 'advanced' },
    { id: 'ECON306', name: 'Industrial Organization', credits: 3, prerequisites: ['ECON201'], description: 'Market structure and competition', level: 'advanced' },
    { id: 'ECON307', name: 'Urban Economics', credits: 3, prerequisites: ['ECON201'], description: 'Economics of cities and regions', level: 'advanced' },
    { id: 'ECON308', name: 'Environmental Economics', credits: 3, prerequisites: ['ECON201'], description: 'Economics of environmental issues', level: 'advanced' },
    { id: 'ECON309', name: 'Health Economics', credits: 3, prerequisites: ['ECON201'], description: 'Healthcare markets and policy', level: 'advanced' },
    { id: 'ECON310', name: 'Econometrics II', credits: 3, prerequisites: ['ECON301'], description: 'Advanced econometric methods', level: 'advanced' },
    
    // Specialized (400-level)
    { id: 'ECON401', name: 'Economic Development', credits: 3, prerequisites: ['ECON202'], description: 'Growth and development economics', level: 'specialized' },
    { id: 'ECON402', name: 'Behavioral Economics', credits: 3, prerequisites: ['ECON201'], description: 'Psychology in economic decisions', level: 'specialized' },
    { id: 'ECON403', name: 'Experimental Economics', credits: 3, prerequisites: ['ECON402'], description: 'Laboratory experiments in economics', level: 'specialized' },
    { id: 'ECON404', name: 'Time Series Analysis', credits: 3, prerequisites: ['ECON310'], description: 'Time series econometrics', level: 'specialized' },
    { id: 'ECON405', name: 'Economic Forecasting', credits: 3, prerequisites: ['ECON404'], description: 'Forecasting methods and applications', level: 'specialized' },
    { id: 'ECON406', name: 'Law and Economics', credits: 3, prerequisites: ['ECON201'], description: 'Economic analysis of law', level: 'specialized' },
    { id: 'ECON407', name: 'Political Economy', credits: 3, prerequisites: ['ECON305'], description: 'Politics and economic policy', level: 'specialized' },
    { id: 'ECON408', name: 'Advanced Microeconomic Theory', credits: 3, prerequisites: ['ECON205'], description: 'Graduate-level microeconomics', level: 'specialized' },
    { id: 'ECON409', name: 'Advanced Macroeconomic Theory', credits: 3, prerequisites: ['ECON202'], description: 'Graduate-level macroeconomics', level: 'specialized' },
    { id: 'ECON410', name: 'Senior Thesis', credits: 4, prerequisites: ['ECON301'], description: 'Independent research project', level: 'specialized' }
];

// Psychology - Complete 32-course catalog
const psychologyCourseCatalog = [
    // Foundation (100-level)
    { id: 'PSY101', name: 'Introduction to Psychology', credits: 3, prerequisites: [], description: 'Foundations of psychology', level: 'foundation' },
    { id: 'PSY102', name: 'Biological Psychology', credits: 3, prerequisites: ['PSY101'], description: 'Brain and behavior', level: 'foundation' },
    { id: 'PSY103', name: 'Psychology as a Science', credits: 2, prerequisites: ['PSY101'], description: 'Scientific method in psychology', level: 'foundation' },
    { id: 'PSY104', name: 'Statistics for Psychology', credits: 3, prerequisites: [], description: 'Statistical methods in psychology', level: 'foundation' },
    
    // Core (200-level)
    { id: 'PSY201', name: 'Research Methods', credits: 4, prerequisites: ['PSY103', 'PSY104'], description: 'Experimental design and methodology', level: 'core' },
    { id: 'PSY202', name: 'Developmental Psychology', credits: 3, prerequisites: ['PSY101'], description: 'Human development across lifespan', level: 'core' },
    { id: 'PSY203', name: 'Cognitive Psychology', credits: 3, prerequisites: ['PSY101'], description: 'Mental processes and cognition', level: 'core' },
    { id: 'PSY204', name: 'Social Psychology', credits: 3, prerequisites: ['PSY101'], description: 'Social behavior and influence', level: 'core' },
    { id: 'PSY205', name: 'Personality Psychology', credits: 3, prerequisites: ['PSY101'], description: 'Theories of personality', level: 'core' },
    { id: 'PSY206', name: 'Abnormal Psychology', credits: 3, prerequisites: ['PSY101'], description: 'Psychological disorders', level: 'core' },
    { id: 'PSY207', name: 'Learning and Memory', credits: 3, prerequisites: ['PSY203'], description: 'Principles of learning and memory', level: 'core' },
    { id: 'PSY208', name: 'Sensation and Perception', credits: 3, prerequisites: ['PSY102'], description: 'Sensory systems and perception', level: 'core' },
    
    // Advanced (300-level)
    { id: 'PSY301', name: 'Advanced Statistics', credits: 3, prerequisites: ['PSY201'], description: 'Multivariate statistics and modeling', level: 'advanced' },
    { id: 'PSY302', name: 'Psychological Testing', credits: 3, prerequisites: ['PSY201'], description: 'Test construction and assessment', level: 'advanced' },
    { id: 'PSY303', name: 'Clinical Psychology', credits: 3, prerequisites: ['PSY206'], description: 'Clinical assessment and intervention', level: 'advanced' },
    { id: 'PSY304', name: 'Counseling Psychology', credits: 3, prerequisites: ['PSY206'], description: 'Counseling theories and techniques', level: 'advanced' },
    { id: 'PSY305', name: 'Health Psychology', credits: 3, prerequisites: ['PSY102'], description: 'Psychology of health and illness', level: 'advanced' },
    { id: 'PSY306', name: 'Neuropsychology', credits: 3, prerequisites: ['PSY102', 'PSY203'], description: 'Brain-behavior relationships', level: 'advanced' },
    { id: 'PSY307', name: 'Child Psychology', credits: 3, prerequisites: ['PSY202'], description: 'Child development and behavior', level: 'advanced' },
    { id: 'PSY308', name: 'Adolescent Psychology', credits: 3, prerequisites: ['PSY202'], description: 'Adolescent development', level: 'advanced' },
    { id: 'PSY309', name: 'Psychology of Aging', credits: 3, prerequisites: ['PSY202'], description: 'Aging and older adults', level: 'advanced' },
    { id: 'PSY310', name: 'Group Dynamics', credits: 3, prerequisites: ['PSY204'], description: 'Group behavior and processes', level: 'advanced' },
    
    // Specialized (400-level)
    { id: 'PSY401', name: 'Psychopathology', credits: 3, prerequisites: ['PSY303'], description: 'Advanced study of mental disorders', level: 'specialized' },
    { id: 'PSY402', name: 'Psychotherapy', credits: 3, prerequisites: ['PSY304'], description: 'Therapy techniques and approaches', level: 'specialized' },
    { id: 'PSY403', name: 'Forensic Psychology', credits: 3, prerequisites: ['PSY303'], description: 'Psychology in legal settings', level: 'specialized' },
    { id: 'PSY404', name: 'Industrial/Organizational Psychology', credits: 3, prerequisites: ['PSY204'], description: 'Psychology in the workplace', level: 'specialized' },
    { id: 'PSY405', name: 'Sports Psychology', credits: 3, prerequisites: ['PSY203'], description: 'Psychology of athletic performance', level: 'specialized' },
    { id: 'PSY406', name: 'Cognitive Neuroscience', credits: 3, prerequisites: ['PSY306'], description: 'Neural basis of cognition', level: 'specialized' },
    { id: 'PSY407', name: 'Psychopharmacology', credits: 3, prerequisites: ['PSY102', 'PSY206'], description: 'Drugs and behavior', level: 'specialized' },
    { id: 'PSY408', name: 'Cross-Cultural Psychology', credits: 3, prerequisites: ['PSY204'], description: 'Culture and psychological processes', level: 'specialized' },
    { id: 'PSY409', name: 'Psychology Research Lab', credits: 3, prerequisites: ['PSY301'], description: 'Hands-on research experience', level: 'specialized' },
    { id: 'PSY410', name: 'Senior Thesis', credits: 4, prerequisites: ['PSY409'], description: 'Independent research project', level: 'specialized' }
];

// Add other expanded catalogs...
const expandedCatalogs = {
    chemistry: chemistryCourseCatalog,
    environment: environmentCourseCatalog,
    civil: civilCourseCatalog,
    chemeng: chemEngCourseCatalog,
    bme: bmeCourseCatalog,
    economics: economicsCourseCatalog,
    psychology: psychologyCourseCatalog
};

console.log('Expanded Course Catalogs Loaded');
Object.entries(expandedCatalogs).forEach(([major, catalog]) => {
    console.log(`${major}: ${catalog.length} courses`);
});