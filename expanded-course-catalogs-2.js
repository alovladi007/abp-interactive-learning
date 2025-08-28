// Expanded Course Catalogs Part 2 - Healthcare, Business, and Other Fields

// Finance - Complete 28-course catalog
const financeCourseCatalog = [
    // Foundation (100-level)
    { id: 'FIN101', name: 'Introduction to Finance', credits: 3, prerequisites: [], description: 'Financial principles and markets', level: 'foundation' },
    { id: 'FIN102', name: 'Financial Accounting', credits: 3, prerequisites: [], description: 'Accounting principles for finance', level: 'foundation' },
    { id: 'FIN103', name: 'Business Mathematics', credits: 3, prerequisites: [], description: 'Mathematical applications in finance', level: 'foundation' },
    { id: 'FIN104', name: 'Financial Computing', credits: 3, prerequisites: [], description: 'Excel and financial software', level: 'foundation' },
    
    // Core (200-level)
    { id: 'FIN201', name: 'Corporate Finance I', credits: 4, prerequisites: ['FIN101'], description: 'Capital budgeting and valuation', level: 'core' },
    { id: 'FIN202', name: 'Investments', credits: 4, prerequisites: ['FIN101'], description: 'Securities and portfolio theory', level: 'core' },
    { id: 'FIN203', name: 'Financial Markets and Institutions', credits: 3, prerequisites: ['FIN101'], description: 'Structure of financial markets', level: 'core' },
    { id: 'FIN204', name: 'Managerial Accounting', credits: 3, prerequisites: ['FIN102'], description: 'Accounting for decision making', level: 'core' },
    { id: 'FIN205', name: 'Financial Statement Analysis', credits: 3, prerequisites: ['FIN102'], description: 'Analyzing financial statements', level: 'core' },
    { id: 'FIN206', name: 'Money and Banking', credits: 3, prerequisites: ['FIN101'], description: 'Monetary system and banking', level: 'core' },
    
    // Advanced (300-level)
    { id: 'FIN301', name: 'Corporate Finance II', credits: 3, prerequisites: ['FIN201'], description: 'Capital structure and payout policy', level: 'advanced' },
    { id: 'FIN302', name: 'Derivatives', credits: 4, prerequisites: ['FIN202'], description: 'Options, futures, and swaps', level: 'advanced' },
    { id: 'FIN303', name: 'Fixed Income Securities', credits: 3, prerequisites: ['FIN202'], description: 'Bond markets and valuation', level: 'advanced' },
    { id: 'FIN304', name: 'Equity Valuation', credits: 3, prerequisites: ['FIN202', 'FIN205'], description: 'Stock analysis and valuation', level: 'advanced' },
    { id: 'FIN305', name: 'International Finance', credits: 3, prerequisites: ['FIN201'], description: 'Foreign exchange and international markets', level: 'advanced' },
    { id: 'FIN306', name: 'Financial Modeling', credits: 3, prerequisites: ['FIN201', 'FIN104'], description: 'Building financial models', level: 'advanced' },
    { id: 'FIN307', name: 'Portfolio Management', credits: 3, prerequisites: ['FIN202'], description: 'Portfolio construction and management', level: 'advanced' },
    { id: 'FIN308', name: 'Real Estate Finance', credits: 3, prerequisites: ['FIN201'], description: 'Real estate investment and financing', level: 'advanced' },
    
    // Specialized (400-level)
    { id: 'FIN401', name: 'Risk Management', credits: 3, prerequisites: ['FIN302'], description: 'Financial risk measurement and management', level: 'specialized' },
    { id: 'FIN402', name: 'Investment Banking', credits: 3, prerequisites: ['FIN301'], description: 'M&A and capital raising', level: 'specialized' },
    { id: 'FIN403', name: 'Private Equity and Venture Capital', credits: 3, prerequisites: ['FIN301'], description: 'Alternative investments', level: 'specialized' },
    { id: 'FIN404', name: 'Quantitative Finance', credits: 3, prerequisites: ['FIN302'], description: 'Mathematical methods in finance', level: 'specialized' },
    { id: 'FIN405', name: 'Financial Technology', credits: 3, prerequisites: ['FIN203'], description: 'Blockchain and digital finance', level: 'specialized' },
    { id: 'FIN406', name: 'Behavioral Finance', credits: 3, prerequisites: ['FIN202'], description: 'Psychology in financial decisions', level: 'specialized' },
    { id: 'FIN407', name: 'Credit Risk Management', credits: 3, prerequisites: ['FIN401'], description: 'Credit analysis and modeling', level: 'specialized' },
    { id: 'FIN408', name: 'Hedge Fund Strategies', credits: 3, prerequisites: ['FIN307'], description: 'Alternative investment strategies', level: 'specialized' },
    { id: 'FIN409', name: 'Financial Regulation', credits: 3, prerequisites: ['FIN203'], description: 'Regulatory framework and compliance', level: 'specialized' },
    { id: 'FIN410', name: 'Finance Capstone', credits: 4, prerequisites: ['FIN301', 'FIN307'], description: 'Comprehensive finance project', level: 'specialized' }
];

// Medicine (Pre-Med) - Complete 32-course catalog
const medicineCourseCatalog = [
    // Foundation (100-level)
    { id: 'MED101', name: 'Human Anatomy I', credits: 4, prerequisites: [], description: 'Musculoskeletal and nervous systems', level: 'foundation' },
    { id: 'MED102', name: 'Human Anatomy II', credits: 4, prerequisites: ['MED101'], description: 'Cardiovascular, respiratory, digestive systems', level: 'foundation' },
    { id: 'MED103', name: 'Human Physiology I', credits: 4, prerequisites: [], description: 'Cell and organ physiology', level: 'foundation' },
    { id: 'MED104', name: 'Human Physiology II', credits: 4, prerequisites: ['MED103'], description: 'Systems physiology', level: 'foundation' },
    { id: 'MED105', name: 'Medical Terminology', credits: 2, prerequisites: [], description: 'Medical vocabulary and terminology', level: 'foundation' },
    
    // Core (200-level)
    { id: 'MED201', name: 'Biochemistry I', credits: 4, prerequisites: ['CHEM202'], description: 'Biomolecules and metabolism', level: 'core' },
    { id: 'MED202', name: 'Biochemistry II', credits: 4, prerequisites: ['MED201'], description: 'Molecular biology and genetics', level: 'core' },
    { id: 'MED203', name: 'Pathology I', credits: 4, prerequisites: ['MED102', 'MED104'], description: 'General pathology principles', level: 'core' },
    { id: 'MED204', name: 'Pathology II', credits: 4, prerequisites: ['MED203'], description: 'Systemic pathology', level: 'core' },
    { id: 'MED205', name: 'Microbiology', credits: 4, prerequisites: ['BIO101'], description: 'Bacteria, viruses, fungi, parasites', level: 'core' },
    { id: 'MED206', name: 'Immunology', credits: 3, prerequisites: ['MED205'], description: 'Immune system and responses', level: 'core' },
    { id: 'MED207', name: 'Medical Genetics', credits: 3, prerequisites: ['MED202'], description: 'Human genetics and genetic diseases', level: 'core' },
    { id: 'MED208', name: 'Histology', credits: 3, prerequisites: ['MED101'], description: 'Microscopic anatomy of tissues', level: 'core' },
    
    // Advanced (300-level)
    { id: 'MED301', name: 'Pharmacology I', credits: 4, prerequisites: ['MED104', 'MED201'], description: 'Drug mechanisms and pharmacokinetics', level: 'advanced' },
    { id: 'MED302', name: 'Pharmacology II', credits: 4, prerequisites: ['MED301'], description: 'Systems pharmacology', level: 'advanced' },
    { id: 'MED303', name: 'Clinical Medicine I', credits: 5, prerequisites: ['MED204'], description: 'Internal medicine basics', level: 'advanced' },
    { id: 'MED304', name: 'Clinical Medicine II', credits: 5, prerequisites: ['MED303'], description: 'Specialty medicine', level: 'advanced' },
    { id: 'MED305', name: 'Medical Ethics', credits: 2, prerequisites: [], description: 'Ethical issues in medicine', level: 'advanced' },
    { id: 'MED306', name: 'Epidemiology', credits: 3, prerequisites: [], description: 'Disease patterns and prevention', level: 'advanced' },
    { id: 'MED307', name: 'Clinical Skills', credits: 3, prerequisites: ['MED303'], description: 'Patient examination and procedures', level: 'advanced' },
    { id: 'MED308', name: 'Medical Imaging', credits: 3, prerequisites: ['MED102'], description: 'Radiology and imaging interpretation', level: 'advanced' },
    
    // Specialized (400-level)
    { id: 'MED401', name: 'Emergency Medicine', credits: 3, prerequisites: ['MED304'], description: 'Acute care and emergency procedures', level: 'specialized' },
    { id: 'MED402', name: 'Surgery Fundamentals', credits: 4, prerequisites: ['MED102', 'MED304'], description: 'Surgical principles and techniques', level: 'specialized' },
    { id: 'MED403', name: 'Pediatrics', credits: 3, prerequisites: ['MED304'], description: 'Child health and development', level: 'specialized' },
    { id: 'MED404', name: 'Obstetrics and Gynecology', credits: 3, prerequisites: ['MED304'], description: 'Women\'s health and reproduction', level: 'specialized' },
    { id: 'MED405', name: 'Psychiatry', credits: 3, prerequisites: ['MED304'], description: 'Mental health disorders and treatment', level: 'specialized' },
    { id: 'MED406', name: 'Neurology', credits: 3, prerequisites: ['MED304'], description: 'Nervous system disorders', level: 'specialized' },
    { id: 'MED407', name: 'Clinical Research Methods', credits: 3, prerequisites: ['MED306'], description: 'Clinical trials and research design', level: 'specialized' },
    { id: 'MED408', name: 'Global Health', credits: 3, prerequisites: ['MED306'], description: 'International health issues', level: 'specialized' },
    { id: 'MED409', name: 'Medical Informatics', credits: 2, prerequisites: [], description: 'Healthcare information systems', level: 'specialized' },
    { id: 'MED410', name: 'Clinical Rotations', credits: 6, prerequisites: ['MED307'], description: 'Hospital clinical experience', level: 'specialized' }
];

// Nursing - Complete 28-course catalog
const nursingCourseCatalog = [
    // Foundation (100-level)
    { id: 'NURS101', name: 'Nursing Fundamentals', credits: 4, prerequisites: [], description: 'Basic nursing concepts and skills', level: 'foundation' },
    { id: 'NURS102', name: 'Health Assessment', credits: 3, prerequisites: [], description: 'Patient assessment techniques', level: 'foundation' },
    { id: 'NURS103', name: 'Nursing Skills Laboratory', credits: 2, prerequisites: [], description: 'Basic nursing procedures', level: 'foundation' },
    { id: 'NURS104', name: 'Professional Nursing', credits: 2, prerequisites: [], description: 'Nursing profession and ethics', level: 'foundation' },
    
    // Core (200-level)
    { id: 'NURS201', name: 'Pathophysiology', credits: 4, prerequisites: ['MED103'], description: 'Disease processes and nursing implications', level: 'core' },
    { id: 'NURS202', name: 'Pharmacology for Nurses', credits: 3, prerequisites: ['NURS101'], description: 'Medication administration and management', level: 'core' },
    { id: 'NURS203', name: 'Adult Health Nursing I', credits: 5, prerequisites: ['NURS201'], description: 'Care of adults with medical conditions', level: 'core' },
    { id: 'NURS204', name: 'Adult Health Nursing II', credits: 5, prerequisites: ['NURS203'], description: 'Care of adults with surgical conditions', level: 'core' },
    { id: 'NURS205', name: 'Mental Health Nursing', credits: 4, prerequisites: ['NURS101'], description: 'Psychiatric and mental health nursing', level: 'core' },
    { id: 'NURS206', name: 'Nutrition for Nursing', credits: 2, prerequisites: [], description: 'Nutritional needs and therapy', level: 'core' },
    { id: 'NURS207', name: 'Nursing Research', credits: 3, prerequisites: ['STAT101'], description: 'Evidence-based practice', level: 'core' },
    
    // Advanced (300-level)
    { id: 'NURS301', name: 'Medical-Surgical Nursing', credits: 6, prerequisites: ['NURS204'], description: 'Complex medical-surgical care', level: 'advanced' },
    { id: 'NURS302', name: 'Maternal-Child Nursing', credits: 5, prerequisites: ['NURS201'], description: 'Care of mothers and children', level: 'advanced' },
    { id: 'NURS303', name: 'Pediatric Nursing', credits: 4, prerequisites: ['NURS302'], description: 'Care of infants and children', level: 'advanced' },
    { id: 'NURS304', name: 'Gerontological Nursing', credits: 3, prerequisites: ['NURS203'], description: 'Care of older adults', level: 'advanced' },
    { id: 'NURS305', name: 'Community Health Nursing', credits: 4, prerequisites: ['NURS203'], description: 'Public health nursing', level: 'advanced' },
    { id: 'NURS306', name: 'Nursing Leadership', credits: 3, prerequisites: ['NURS301'], description: 'Leadership and management in nursing', level: 'advanced' },
    { id: 'NURS307', name: 'Critical Thinking in Nursing', credits: 2, prerequisites: ['NURS301'], description: 'Clinical reasoning and decision making', level: 'advanced' },
    
    // Specialized (400-level)
    { id: 'NURS401', name: 'Critical Care Nursing', credits: 5, prerequisites: ['NURS301'], description: 'ICU and emergency care', level: 'specialized' },
    { id: 'NURS402', name: 'Emergency Nursing', credits: 4, prerequisites: ['NURS301'], description: 'Emergency department nursing', level: 'specialized' },
    { id: 'NURS403', name: 'Cardiac Nursing', credits: 3, prerequisites: ['NURS401'], description: 'Cardiovascular nursing care', level: 'specialized' },
    { id: 'NURS404', name: 'Oncology Nursing', credits: 3, prerequisites: ['NURS301'], description: 'Cancer care nursing', level: 'specialized' },
    { id: 'NURS405', name: 'Perioperative Nursing', credits: 3, prerequisites: ['NURS204'], description: 'Operating room nursing', level: 'specialized' },
    { id: 'NURS406', name: 'Nursing Informatics', credits: 3, prerequisites: [], description: 'Healthcare technology and data', level: 'specialized' },
    { id: 'NURS407', name: 'Advanced Pharmacology', credits: 3, prerequisites: ['NURS202'], description: 'Complex medication management', level: 'specialized' },
    { id: 'NURS408', name: 'Nursing Education', credits: 3, prerequisites: ['NURS306'], description: 'Teaching in nursing', level: 'specialized' },
    { id: 'NURS409', name: 'Nursing Capstone', credits: 4, prerequisites: ['NURS401'], description: 'Comprehensive clinical practicum', level: 'specialized' },
    { id: 'NURS410', name: 'NCLEX Preparation', credits: 2, prerequisites: ['NURS409'], description: 'Licensure exam preparation', level: 'specialized' }
];

// Pharmacy - Complete 30-course catalog
const pharmacyCourseCatalog = [
    // Foundation (100-level)
    { id: 'PHAR101', name: 'Introduction to Pharmacy', credits: 2, prerequisites: [], description: 'Pharmacy profession overview', level: 'foundation' },
    { id: 'PHAR102', name: 'Pharmaceutical Calculations', credits: 3, prerequisites: [], description: 'Dosage calculations and conversions', level: 'foundation' },
    { id: 'PHAR103', name: 'Pharmacy Practice Lab I', credits: 1, prerequisites: [], description: 'Basic compounding techniques', level: 'foundation' },
    { id: 'PHAR104', name: 'Medical Terminology for Pharmacy', credits: 2, prerequisites: [], description: 'Pharmaceutical terminology', level: 'foundation' },
    
    // Core (200-level)
    { id: 'PHAR201', name: 'Medicinal Chemistry I', credits: 4, prerequisites: ['CHEM202'], description: 'Drug structure and activity', level: 'core' },
    { id: 'PHAR202', name: 'Medicinal Chemistry II', credits: 4, prerequisites: ['PHAR201'], description: 'Drug design and development', level: 'core' },
    { id: 'PHAR203', name: 'Pharmacology I', credits: 4, prerequisites: ['MED103'], description: 'Drug mechanisms and effects', level: 'core' },
    { id: 'PHAR204', name: 'Pharmacology II', credits: 4, prerequisites: ['PHAR203'], description: 'Systems pharmacology', level: 'core' },
    { id: 'PHAR205', name: 'Pharmaceutics I', credits: 3, prerequisites: ['PHAR102'], description: 'Dosage forms and drug delivery', level: 'core' },
    { id: 'PHAR206', name: 'Pharmaceutics II', credits: 3, prerequisites: ['PHAR205'], description: 'Advanced drug formulation', level: 'core' },
    { id: 'PHAR207', name: 'Pharmacokinetics', credits: 3, prerequisites: ['PHAR203'], description: 'Drug absorption and metabolism', level: 'core' },
    { id: 'PHAR208', name: 'Pharmacy Practice Lab II', credits: 2, prerequisites: ['PHAR103'], description: 'Sterile compounding', level: 'core' },
    
    // Advanced (300-level)
    { id: 'PHAR301', name: 'Pharmacotherapy I', credits: 5, prerequisites: ['PHAR204'], description: 'Disease state management', level: 'advanced' },
    { id: 'PHAR302', name: 'Pharmacotherapy II', credits: 5, prerequisites: ['PHAR301'], description: 'Complex disease management', level: 'advanced' },
    { id: 'PHAR303', name: 'Clinical Pharmacy', credits: 4, prerequisites: ['PHAR301'], description: 'Patient-centered care', level: 'advanced' },
    { id: 'PHAR304', name: 'Pharmacy Law and Ethics', credits: 3, prerequisites: [], description: 'Legal and ethical issues', level: 'advanced' },
    { id: 'PHAR305', name: 'Drug Information', credits: 3, prerequisites: ['PHAR301'], description: 'Literature evaluation and resources', level: 'advanced' },
    { id: 'PHAR306', name: 'Pharmacoeconomics', credits: 2, prerequisites: [], description: 'Economic evaluation of drugs', level: 'advanced' },
    { id: 'PHAR307', name: 'Toxicology', credits: 3, prerequisites: ['PHAR204'], description: 'Poisons and antidotes', level: 'advanced' },
    { id: 'PHAR308', name: 'Biopharmaceutics', credits: 3, prerequisites: ['PHAR207'], description: 'Drug bioavailability', level: 'advanced' },
    
    // Specialized (400-level)
    { id: 'PHAR401', name: 'Community Pharmacy Practice', credits: 4, prerequisites: ['PHAR303'], description: 'Retail pharmacy management', level: 'specialized' },
    { id: 'PHAR402', name: 'Hospital Pharmacy Practice', credits: 4, prerequisites: ['PHAR303'], description: 'Institutional pharmacy', level: 'specialized' },
    { id: 'PHAR403', name: 'Ambulatory Care', credits: 3, prerequisites: ['PHAR303'], description: 'Outpatient pharmacy services', level: 'specialized' },
    { id: 'PHAR404', name: 'Pediatric Pharmacy', credits: 3, prerequisites: ['PHAR302'], description: 'Pediatric drug therapy', level: 'specialized' },
    { id: 'PHAR405', name: 'Geriatric Pharmacy', credits: 3, prerequisites: ['PHAR302'], description: 'Elderly patient care', level: 'specialized' },
    { id: 'PHAR406', name: 'Oncology Pharmacy', credits: 3, prerequisites: ['PHAR302'], description: 'Cancer chemotherapy', level: 'specialized' },
    { id: 'PHAR407', name: 'Nuclear Pharmacy', credits: 2, prerequisites: ['PHAR206'], description: 'Radiopharmaceuticals', level: 'specialized' },
    { id: 'PHAR408', name: 'Pharmaceutical Industry', credits: 3, prerequisites: ['PHAR202'], description: 'Drug development and manufacturing', level: 'specialized' },
    { id: 'PHAR409', name: 'Advanced Clinical Rotations', credits: 6, prerequisites: ['PHAR303'], description: 'Clinical practice experience', level: 'specialized' },
    { id: 'PHAR410', name: 'Pharmacy Capstone', credits: 3, prerequisites: ['PHAR409'], description: 'Comprehensive pharmacy project', level: 'specialized' }
];

// Public Health - Complete 28-course catalog
const publicHealthCourseCatalog = [
    // Foundation (100-level)
    { id: 'PH101', name: 'Introduction to Public Health', credits: 3, prerequisites: [], description: 'Public health principles and practice', level: 'foundation' },
    { id: 'PH102', name: 'Global Health', credits: 3, prerequisites: [], description: 'International health issues', level: 'foundation' },
    { id: 'PH103', name: 'Health and Society', credits: 3, prerequisites: [], description: 'Social determinants of health', level: 'foundation' },
    { id: 'PH104', name: 'Public Health Biology', credits: 3, prerequisites: [], description: 'Biological basis of public health', level: 'foundation' },
    
    // Core (200-level)
    { id: 'PH201', name: 'Epidemiology I', credits: 4, prerequisites: ['PH101'], description: 'Disease distribution and determinants', level: 'core' },
    { id: 'PH202', name: 'Biostatistics I', credits: 4, prerequisites: ['STAT101'], description: 'Statistical methods in public health', level: 'core' },
    { id: 'PH203', name: 'Environmental Health', credits: 3, prerequisites: ['PH101'], description: 'Environmental factors affecting health', level: 'core' },
    { id: 'PH204', name: 'Health Policy', credits: 3, prerequisites: ['PH101'], description: 'Health policy development and analysis', level: 'core' },
    { id: 'PH205', name: 'Health Education', credits: 3, prerequisites: ['PH101'], description: 'Health promotion and education', level: 'core' },
    { id: 'PH206', name: 'Community Health', credits: 3, prerequisites: ['PH101'], description: 'Community-based health programs', level: 'core' },
    { id: 'PH207', name: 'Health Communication', credits: 3, prerequisites: ['PH205'], description: 'Health messaging and media', level: 'core' },
    
    // Advanced (300-level)
    { id: 'PH301', name: 'Epidemiology II', credits: 3, prerequisites: ['PH201'], description: 'Advanced epidemiologic methods', level: 'advanced' },
    { id: 'PH302', name: 'Biostatistics II', credits: 3, prerequisites: ['PH202'], description: 'Advanced biostatistical methods', level: 'advanced' },
    { id: 'PH303', name: 'Infectious Disease Epidemiology', credits: 3, prerequisites: ['PH201'], description: 'Infectious disease control', level: 'advanced' },
    { id: 'PH304', name: 'Chronic Disease Epidemiology', credits: 3, prerequisites: ['PH201'], description: 'Non-communicable diseases', level: 'advanced' },
    { id: 'PH305', name: 'Health Economics', credits: 3, prerequisites: ['ECON101'], description: 'Economic analysis of health', level: 'advanced' },
    { id: 'PH306', name: 'Health Services Administration', credits: 3, prerequisites: ['PH204'], description: 'Healthcare management', level: 'advanced' },
    { id: 'PH307', name: 'Program Evaluation', credits: 3, prerequisites: ['PH202'], description: 'Evaluating public health programs', level: 'advanced' },
    { id: 'PH308', name: 'Maternal and Child Health', credits: 3, prerequisites: ['PH201'], description: 'MCH programs and policies', level: 'advanced' },
    { id: 'PH309', name: 'Occupational Health', credits: 3, prerequisites: ['PH203'], description: 'Workplace health and safety', level: 'advanced' },
    
    // Specialized (400-level)
    { id: 'PH401', name: 'Global Health Policy', credits: 3, prerequisites: ['PH204'], description: 'International health policy', level: 'specialized' },
    { id: 'PH402', name: 'Health Disparities', credits: 3, prerequisites: ['PH103'], description: 'Health equity and justice', level: 'specialized' },
    { id: 'PH403', name: 'Disaster and Emergency Management', credits: 3, prerequisites: ['PH206'], description: 'Public health emergencies', level: 'specialized' },
    { id: 'PH404', name: 'Nutritional Epidemiology', credits: 3, prerequisites: ['PH301'], description: 'Diet and disease relationships', level: 'specialized' },
    { id: 'PH405', name: 'Social Epidemiology', credits: 3, prerequisites: ['PH301'], description: 'Social factors in health', level: 'specialized' },
    { id: 'PH406', name: 'Health Informatics', credits: 3, prerequisites: ['PH202'], description: 'Health data systems', level: 'specialized' },
    { id: 'PH407', name: 'Implementation Science', credits: 3, prerequisites: ['PH307'], description: 'Translating research to practice', level: 'specialized' },
    { id: 'PH408', name: 'Public Health Capstone', credits: 4, prerequisites: ['PH301', 'PH302'], description: 'Comprehensive public health project', level: 'specialized' },
    { id: 'PH409', name: 'Field Experience', credits: 3, prerequisites: ['PH301'], description: 'Public health practicum', level: 'specialized' }
];

// Nutrition & Dietetics - Complete 26-course catalog
const nutritionCourseCatalog = [
    // Foundation (100-level)
    { id: 'NUTR101', name: 'Introduction to Nutrition', credits: 3, prerequisites: [], description: 'Basic nutrition principles', level: 'foundation' },
    { id: 'NUTR102', name: 'Food Science Fundamentals', credits: 3, prerequisites: [], description: 'Food composition and properties', level: 'foundation' },
    { id: 'NUTR103', name: 'Culinary Skills for Nutrition', credits: 2, prerequisites: [], description: 'Food preparation techniques', level: 'foundation' },
    { id: 'NUTR104', name: 'Nutrition Through Life Cycle', credits: 3, prerequisites: ['NUTR101'], description: 'Nutritional needs across lifespan', level: 'foundation' },
    
    // Core (200-level)
    { id: 'NUTR201', name: 'Nutritional Biochemistry', credits: 4, prerequisites: ['CHEM102', 'NUTR101'], description: 'Metabolism of nutrients', level: 'core' },
    { id: 'NUTR202', name: 'Advanced Food Science', credits: 4, prerequisites: ['NUTR102'], description: 'Food chemistry and processing', level: 'core' },
    { id: 'NUTR203', name: 'Nutritional Assessment', credits: 3, prerequisites: ['NUTR101'], description: 'Assessment methods and tools', level: 'core' },
    { id: 'NUTR204', name: 'Food Safety and Sanitation', credits: 3, prerequisites: ['NUTR102'], description: 'Food safety principles', level: 'core' },
    { id: 'NUTR205', name: 'Community Nutrition', credits: 3, prerequisites: ['NUTR101'], description: 'Public health nutrition', level: 'core' },
    { id: 'NUTR206', name: 'Food Service Management', credits: 3, prerequisites: ['NUTR103'], description: 'Institutional food service', level: 'core' },
    
    // Advanced (300-level)
    { id: 'NUTR301', name: 'Clinical Nutrition I', credits: 4, prerequisites: ['NUTR201'], description: 'Medical nutrition therapy basics', level: 'advanced' },
    { id: 'NUTR302', name: 'Clinical Nutrition II', credits: 4, prerequisites: ['NUTR301'], description: 'Advanced medical nutrition therapy', level: 'advanced' },
    { id: 'NUTR303', name: 'Sports Nutrition', credits: 3, prerequisites: ['NUTR201'], description: 'Nutrition for athletic performance', level: 'advanced' },
    { id: 'NUTR304', name: 'Pediatric Nutrition', credits: 3, prerequisites: ['NUTR104'], description: 'Child nutrition and feeding', level: 'advanced' },
    { id: 'NUTR305', name: 'Geriatric Nutrition', credits: 3, prerequisites: ['NUTR104'], description: 'Nutrition for older adults', level: 'advanced' },
    { id: 'NUTR306', name: 'Nutrition Counseling', credits: 3, prerequisites: ['NUTR301'], description: 'Counseling techniques and behavior change', level: 'advanced' },
    { id: 'NUTR307', name: 'Nutrition Research Methods', credits: 3, prerequisites: ['NUTR203'], description: 'Research design in nutrition', level: 'advanced' },
    
    // Specialized (400-level)
    { id: 'NUTR401', name: 'Advanced Sports Nutrition', credits: 3, prerequisites: ['NUTR303'], description: 'Performance optimization strategies', level: 'specialized' },
    { id: 'NUTR402', name: 'Eating Disorders', credits: 3, prerequisites: ['NUTR306'], description: 'Treatment of eating disorders', level: 'specialized' },
    { id: 'NUTR403', name: 'Functional Foods', credits: 3, prerequisites: ['NUTR202'], description: 'Bioactive compounds in foods', level: 'specialized' },
    { id: 'NUTR404', name: 'Nutrigenomics', credits: 3, prerequisites: ['NUTR201'], description: 'Genetics and nutrition interactions', level: 'specialized' },
    { id: 'NUTR405', name: 'Global Nutrition', credits: 3, prerequisites: ['NUTR205'], description: 'International nutrition issues', level: 'specialized' },
    { id: 'NUTR406', name: 'Entrepreneurship in Nutrition', credits: 3, prerequisites: ['NUTR306'], description: 'Private practice and business', level: 'specialized' },
    { id: 'NUTR407', name: 'Dietetic Internship Prep', credits: 2, prerequisites: ['NUTR302'], description: 'Preparation for dietetic internship', level: 'specialized' },
    { id: 'NUTR408', name: 'Clinical Practicum', credits: 4, prerequisites: ['NUTR302'], description: 'Supervised clinical practice', level: 'specialized' },
    { id: 'NUTR409', name: 'Nutrition Capstone', credits: 3, prerequisites: ['NUTR307'], description: 'Comprehensive nutrition project', level: 'specialized' }
];

// Political Science - Complete 28-course catalog
const politicalScienceCourseCatalog = [
    // Foundation (100-level)
    { id: 'POL101', name: 'Introduction to Political Science', credits: 3, prerequisites: [], description: 'Political systems and theory', level: 'foundation' },
    { id: 'POL102', name: 'American Government', credits: 3, prerequisites: [], description: 'U.S. political system', level: 'foundation' },
    { id: 'POL103', name: 'Introduction to International Relations', credits: 3, prerequisites: [], description: 'Global politics basics', level: 'foundation' },
    { id: 'POL104', name: 'Political Philosophy', credits: 3, prerequisites: [], description: 'Classical and modern political thought', level: 'foundation' },
    
    // Core (200-level)
    { id: 'POL201', name: 'Comparative Politics', credits: 3, prerequisites: ['POL101'], description: 'Comparing political systems', level: 'core' },
    { id: 'POL202', name: 'International Relations Theory', credits: 3, prerequisites: ['POL103'], description: 'Theories of international politics', level: 'core' },
    { id: 'POL203', name: 'Political Research Methods', credits: 3, prerequisites: ['POL101'], description: 'Research design and analysis', level: 'core' },
    { id: 'POL204', name: 'Public Policy Analysis', credits: 3, prerequisites: ['POL102'], description: 'Policy making process', level: 'core' },
    { id: 'POL205', name: 'Constitutional Law', credits: 3, prerequisites: ['POL102'], description: 'Constitutional interpretation', level: 'core' },
    { id: 'POL206', name: 'Political Economy', credits: 3, prerequisites: ['POL101', 'ECON101'], description: 'Politics and economics intersection', level: 'core' },
    { id: 'POL207', name: 'State and Local Politics', credits: 3, prerequisites: ['POL102'], description: 'Subnational government', level: 'core' },
    
    // Advanced (300-level)
    { id: 'POL301', name: 'Advanced Policy Analysis', credits: 3, prerequisites: ['POL204'], description: 'Policy evaluation techniques', level: 'advanced' },
    { id: 'POL302', name: 'International Security', credits: 3, prerequisites: ['POL202'], description: 'Security studies and strategy', level: 'advanced' },
    { id: 'POL303', name: 'Environmental Politics', credits: 3, prerequisites: ['POL204'], description: 'Environmental policy and politics', level: 'advanced' },
    { id: 'POL304', name: 'Political Parties and Elections', credits: 3, prerequisites: ['POL102'], description: 'Electoral systems and campaigns', level: 'advanced' },
    { id: 'POL305', name: 'Congress and the Presidency', credits: 3, prerequisites: ['POL102'], description: 'Executive-legislative relations', level: 'advanced' },
    { id: 'POL306', name: 'Public Opinion and Media', credits: 3, prerequisites: ['POL203'], description: 'Media influence on politics', level: 'advanced' },
    { id: 'POL307', name: 'International Organizations', credits: 3, prerequisites: ['POL202'], description: 'UN, EU, and global governance', level: 'advanced' },
    { id: 'POL308', name: 'Democratization', credits: 3, prerequisites: ['POL201'], description: 'Democratic transitions', level: 'advanced' },
    
    // Specialized (400-level)
    { id: 'POL401', name: 'Advanced International Relations', credits: 3, prerequisites: ['POL302'], description: 'Complex global issues', level: 'specialized' },
    { id: 'POL402', name: 'Political Communication', credits: 3, prerequisites: ['POL306'], description: 'Strategic political messaging', level: 'specialized' },
    { id: 'POL403', name: 'Intelligence and National Security', credits: 3, prerequisites: ['POL302'], description: 'Intelligence operations and policy', level: 'specialized' },
    { id: 'POL404', name: 'Diplomacy and Negotiation', credits: 3, prerequisites: ['POL202'], description: 'Diplomatic practice and theory', level: 'specialized' },
    { id: 'POL405', name: 'Campaign Management', credits: 3, prerequisites: ['POL304'], description: 'Running political campaigns', level: 'specialized' },
    { id: 'POL406', name: 'Legislative Process', credits: 3, prerequisites: ['POL305'], description: 'How laws are made', level: 'specialized' },
    { id: 'POL407', name: 'Human Rights', credits: 3, prerequisites: ['POL307'], description: 'International human rights', level: 'specialized' },
    { id: 'POL408', name: 'Political Risk Analysis', credits: 3, prerequisites: ['POL201', 'POL206'], description: 'Assessing political risks', level: 'specialized' },
    { id: 'POL409', name: 'Senior Seminar', credits: 3, prerequisites: ['POL301'], description: 'Advanced topics seminar', level: 'specialized' },
    { id: 'POL410', name: 'Thesis/Internship', credits: 4, prerequisites: ['POL203'], description: 'Research or practical experience', level: 'specialized' }
];

// Export all expanded catalogs
const expandedCatalogs2 = {
    finance: financeCourseCatalog,
    medicine: medicineCourseCatalog,
    nursing: nursingCourseCatalog,
    pharmacy: pharmacyCourseCatalog,
    'public-health': publicHealthCourseCatalog,
    nutrition: nutritionCourseCatalog,
    policy: politicalScienceCourseCatalog
};

console.log('Expanded Course Catalogs Part 2 Loaded');
Object.entries(expandedCatalogs2).forEach(([major, catalog]) => {
    console.log(`${major}: ${catalog.length} courses`);
});