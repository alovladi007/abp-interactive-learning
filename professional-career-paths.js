// Professional Career Paths for EUREKA Platform
// Comprehensive professional education and career guidance system

class ProfessionalCareerPaths {
    constructor() {
        this.professionalPaths = this.initializeProfessionalPaths();
    }

    initializeProfessionalPaths() {
        return {
            // Legal Professions
            legal: {
                name: "Legal Professions",
                icon: "fas fa-balance-scale",
                color: "#8B4513",
                description: "Law school preparation and legal career paths",
                subcategories: {
                    lawyer: {
                        name: "Lawyer/Attorney",
                        programs: ["JD", "LLM"],
                        prerequisites: ["Bachelor's Degree", "LSAT Score"],
                        duration: "3-4 years",
                        specializations: [
                            "Corporate Law",
                            "Criminal Defense",
                            "Personal Injury",
                            "Family Law",
                            "Immigration Law",
                            "Environmental Law",
                            "Intellectual Property",
                            "Tax Law",
                            "Real Estate Law",
                            "Constitutional Law"
                        ],
                        careerPath: "Law School → Bar Exam → Associate → Partner",
                        salaryRange: "$70k - $300k+",
                        keySkills: ["Research", "Writing", "Oral Advocacy", "Critical Thinking"],
                        courses: [
                            "Constitutional Law",
                            "Contracts",
                            "Torts",
                            "Criminal Law",
                            "Property Law",
                            "Civil Procedure",
                            "Evidence",
                            "Professional Responsibility"
                        ]
                    },
                    paralegal: {
                        name: "Paralegal",
                        programs: ["Associate's", "Certificate", "Bachelor's"],
                        prerequisites: ["High School Diploma"],
                        duration: "1-4 years",
                        specializations: [
                            "Corporate Paralegal",
                            "Litigation Paralegal",
                            "Real Estate Paralegal",
                            "Criminal Law Paralegal",
                            "Family Law Paralegal"
                        ],
                        careerPath: "Certificate/Associate's → Entry Level → Senior Paralegal",
                        salaryRange: "$35k - $80k",
                        keySkills: ["Legal Research", "Document Preparation", "Case Management"],
                        courses: [
                            "Legal Research & Writing",
                            "Civil Procedure",
                            "Legal Ethics",
                            "Document Preparation",
                            "Case Management Software"
                        ]
                    },
                    judge: {
                        name: "Judge",
                        programs: ["JD + Experience"],
                        prerequisites: ["Law Degree", "Legal Experience", "Appointment/Election"],
                        duration: "5-15+ years",
                        careerPath: "Lawyer → Judicial Experience → Appointment/Election",
                        salaryRange: "$100k - $250k+",
                        keySkills: ["Legal Knowledge", "Fairness", "Decision Making", "Court Management"]
                    }
                }
            },

            // Medical Professions
            medical: {
                name: "Medical Professions",
                icon: "fas fa-user-md",
                color: "#DC143C",
                description: "Medical school preparation and healthcare careers",
                subcategories: {
                    physician: {
                        name: "Physician/Doctor",
                        programs: ["MD", "DO"],
                        prerequisites: ["Bachelor's Degree", "MCAT Score", "Pre-med courses"],
                        duration: "4 years medical school + 3-7 years residency",
                        specializations: [
                            "Internal Medicine",
                            "Surgery",
                            "Pediatrics",
                            "Cardiology",
                            "Neurology",
                            "Psychiatry",
                            "Dermatology",
                            "Radiology",
                            "Emergency Medicine",
                            "Family Medicine"
                        ],
                        careerPath: "Pre-med → Medical School → Residency → Fellowship → Practice",
                        salaryRange: "$200k - $500k+",
                        keySkills: ["Diagnosis", "Treatment Planning", "Patient Communication", "Medical Knowledge"],
                        courses: [
                            "Anatomy & Physiology",
                            "Biochemistry",
                            "Pathology",
                            "Pharmacology",
                            "Clinical Medicine",
                            "Medical Ethics"
                        ]
                    },
                    nurse: {
                        name: "Registered Nurse",
                        programs: ["BSN", "ADN", "Diploma"],
                        prerequisites: ["High School Diploma", "Prerequisites"],
                        duration: "2-4 years",
                        specializations: [
                            "ICU Nursing",
                            "Emergency Nursing",
                            "Pediatric Nursing",
                            "Surgical Nursing",
                            "Psychiatric Nursing",
                            "Oncology Nursing",
                            "Nurse Anesthetist",
                            "Nurse Practitioner"
                        ],
                        careerPath: "Nursing School → NCLEX → Clinical Practice → Specialization",
                        salaryRange: "$50k - $120k+",
                        keySkills: ["Patient Care", "Medical Knowledge", "Communication", "Critical Thinking"],
                        courses: [
                            "Fundamentals of Nursing",
                            "Medical-Surgical Nursing",
                            "Pharmacology",
                            "Mental Health Nursing",
                            "Community Health",
                            "Nursing Leadership"
                        ]
                    },
                    pharmacist: {
                        name: "Pharmacist",
                        programs: ["PharmD"],
                        prerequisites: ["Bachelor's Degree", "PCAT Score", "Prerequisites"],
                        duration: "4 years",
                        specializations: [
                            "Clinical Pharmacy",
                            "Hospital Pharmacy",
                            "Community Pharmacy",
                            "Industrial Pharmacy",
                            "Nuclear Pharmacy"
                        ],
                        careerPath: "Pre-pharmacy → Pharmacy School → Residency → Practice",
                        salaryRange: "$100k - $150k",
                        keySkills: ["Medication Knowledge", "Patient Counseling", "Drug Interactions"],
                        courses: [
                            "Pharmaceutical Chemistry",
                            "Pharmacology",
                            "Pharmacy Practice",
                            "Drug Information",
                            "Clinical Pharmacy"
                        ]
                    }
                }
            },

            // Dental Professions
            dental: {
                name: "Dental Professions",
                icon: "fas fa-tooth",
                color: "#4169E1",
                description: "Dental school and oral healthcare careers",
                subcategories: {
                    dentist: {
                        name: "Dentist",
                        programs: ["DDS", "DMD"],
                        prerequisites: ["Bachelor's Degree", "DAT Score", "Prerequisites"],
                        duration: "4 years dental school",
                        specializations: [
                            "General Dentistry",
                            "Oral Surgery",
                            "Orthodontics",
                            "Endodontics",
                            "Periodontics",
                            "Pediatric Dentistry",
                            "Prosthodontics",
                            "Oral Pathology"
                        ],
                        careerPath: "Pre-dental → Dental School → Residency (optional) → Practice",
                        salaryRange: "$120k - $250k+",
                        keySkills: ["Manual Dexterity", "Patient Care", "Diagnosis", "Treatment Planning"],
                        courses: [
                            "Oral Anatomy",
                            "Dental Materials",
                            "Oral Pathology",
                            "Periodontics",
                            "Endodontics",
                            "Oral Surgery",
                            "Prosthodontics",
                            "Orthodontics"
                        ]
                    },
                    dentalHygienist: {
                        name: "Dental Hygienist",
                        programs: ["Associate's", "Bachelor's"],
                        prerequisites: ["High School Diploma"],
                        duration: "2-4 years",
                        careerPath: "Dental Hygiene Program → Licensure → Practice",
                        salaryRange: "$50k - $90k",
                        keySkills: ["Teeth Cleaning", "Patient Education", "Oral Health Assessment"],
                        courses: [
                            "Dental Hygiene Theory",
                            "Periodontics",
                            "Oral Pathology",
                            "Dental Materials",
                            "Community Health"
                        ]
                    },
                    dentalAssistant: {
                        name: "Dental Assistant",
                        programs: ["Certificate", "Diploma"],
                        prerequisites: ["High School Diploma"],
                        duration: "9-12 months",
                        careerPath: "Training Program → Certification → Practice",
                        salaryRange: "$30k - $60k",
                        keySkills: ["Chairside Assistance", "Sterilization", "Patient Care"],
                        courses: [
                            "Dental Procedures",
                            "Infection Control",
                            "Dental Materials",
                            "Patient Management",
                            "Office Administration"
                        ]
                    }
                }
            },

            // Business & Finance
            business: {
                name: "Business & Finance",
                icon: "fas fa-briefcase",
                color: "#228B22",
                description: "Business school and corporate career paths",
                subcategories: {
                    mba: {
                        name: "MBA Professional",
                        programs: ["MBA", "EMBA", "Specialized Master's"],
                        prerequisites: ["Bachelor's Degree", "GMAT/GRE Score", "Work Experience"],
                        duration: "1-2 years",
                        specializations: [
                            "Finance",
                            "Marketing",
                            "Operations",
                            "Strategy",
                            "Entrepreneurship",
                            "International Business",
                            "Healthcare Management",
                            "Technology Management"
                        ],
                        careerPath: "Work Experience → MBA → Management → Executive",
                        salaryRange: "$80k - $200k+",
                        keySkills: ["Leadership", "Strategic Thinking", "Financial Analysis", "Team Management"],
                        courses: [
                            "Financial Accounting",
                            "Managerial Economics",
                            "Marketing Strategy",
                            "Operations Management",
                            "Organizational Behavior",
                            "Business Strategy"
                        ]
                    },
                    cfa: {
                        name: "Chartered Financial Analyst",
                        programs: ["CFA Charter"],
                        prerequisites: ["Bachelor's Degree", "4 Years Experience"],
                        duration: "2-3 years (exam preparation)",
                        specializations: [
                            "Portfolio Management",
                            "Investment Analysis",
                            "Risk Management",
                            "Corporate Finance"
                        ],
                        careerPath: "Finance Background → CFA Exams → Charter → Senior Roles",
                        salaryRange: "$70k - $250k+",
                        keySkills: ["Financial Analysis", "Investment Knowledge", "Risk Assessment"],
                        courses: [
                            "Ethical and Professional Standards",
                            "Quantitative Methods",
                            "Economics",
                            "Financial Reporting",
                            "Corporate Finance",
                            "Portfolio Management"
                        ]
                    },
                    cpa: {
                        name: "Certified Public Accountant",
                        programs: ["CPA License"],
                        prerequisites: ["Bachelor's Degree", "150 Credit Hours", "Experience"],
                        duration: "1-2 years (exam preparation)",
                        specializations: [
                            "Tax Accounting",
                            "Auditing",
                            "Management Accounting",
                            "Forensic Accounting"
                        ],
                        careerPath: "Accounting Degree → CPA Exam → Public/Private Practice",
                        salaryRange: "$50k - $150k+",
                        keySkills: ["Financial Reporting", "Tax Knowledge", "Auditing", "Analysis"],
                        courses: [
                            "Financial Accounting",
                            "Auditing & Attestation",
                            "Regulation",
                            "Business Environment"
                        ]
                    }
                }
            },

            // Technology & Engineering
            technology: {
                name: "Technology & Engineering",
                icon: "fas fa-laptop-code",
                color: "#FF6347",
                description: "Tech certifications and engineering careers",
                subcategories: {
                    softwareEngineer: {
                        name: "Software Engineer",
                        programs: ["Bootcamp", "Bachelor's", "Self-taught"],
                        prerequisites: ["High School Diploma"],
                        duration: "3 months - 4 years",
                        specializations: [
                            "Frontend Development",
                            "Backend Development",
                            "Full Stack Development",
                            "Mobile Development",
                            "DevOps",
                            "Machine Learning Engineering",
                            "Game Development",
                            "Cybersecurity"
                        ],
                        careerPath: "Training → Junior Developer → Senior Developer → Lead/Architect",
                        salaryRange: "$60k - $200k+",
                        keySkills: ["Programming", "Problem Solving", "System Design", "Collaboration"],
                        courses: [
                            "Programming Fundamentals",
                            "Data Structures & Algorithms",
                            "Software Engineering",
                            "Database Systems",
                            "Web Development",
                            "System Design"
                        ]
                    },
                    dataScientist: {
                        name: "Data Scientist",
                        programs: ["Master's", "PhD", "Bootcamp"],
                        prerequisites: ["Bachelor's Degree", "Math/Stats Background"],
                        duration: "6 months - 3 years",
                        specializations: [
                            "Machine Learning",
                            "Deep Learning",
                            "Natural Language Processing",
                            "Computer Vision",
                            "Business Analytics",
                            "Research"
                        ],
                        careerPath: "Education → Junior Data Scientist → Senior → Principal",
                        salaryRange: "$80k - $180k+",
                        keySkills: ["Statistics", "Programming", "Machine Learning", "Business Acumen"],
                        courses: [
                            "Statistics & Probability",
                            "Machine Learning",
                            "Data Visualization",
                            "Database Systems",
                            "Python/R Programming",
                            "Big Data Technologies"
                        ]
                    },
                    cybersecurity: {
                        name: "Cybersecurity Professional",
                        programs: ["Certifications", "Bachelor's", "Master's"],
                        prerequisites: ["IT Background"],
                        duration: "6 months - 4 years",
                        specializations: [
                            "Penetration Testing",
                            "Security Architecture",
                            "Incident Response",
                            "Compliance",
                            "Risk Management"
                        ],
                        careerPath: "IT Background → Security Training → Junior → Senior → Lead",
                        salaryRange: "$70k - $150k+",
                        keySkills: ["Security Knowledge", "Risk Assessment", "Incident Response"],
                        courses: [
                            "Network Security",
                            "Ethical Hacking",
                            "Risk Management",
                            "Compliance",
                            "Incident Response",
                            "Security Architecture"
                        ]
                    }
                }
            },

            // Education & Academia
            education: {
                name: "Education & Academia",
                icon: "fas fa-chalkboard-teacher",
                color: "#9932CC",
                description: "Teaching and academic career paths",
                subcategories: {
                    professor: {
                        name: "University Professor",
                        programs: ["PhD", "Postdoc"],
                        prerequisites: ["Master's Degree", "Research Experience"],
                        duration: "5-8 years",
                        specializations: [
                            "Research Focus",
                            "Teaching Focus",
                            "Administrative Roles"
                        ],
                        careerPath: "PhD → Postdoc → Assistant Prof → Associate → Full Prof",
                        salaryRange: "$60k - $150k+",
                        keySkills: ["Research", "Teaching", "Writing", "Mentoring"],
                        courses: [
                            "Research Methods",
                            "Academic Writing",
                            "Teaching Methods",
                            "Grant Writing",
                            "Academic Ethics"
                        ]
                    },
                    teacher: {
                        name: "K-12 Teacher",
                        programs: ["Bachelor's in Education", "Teaching License"],
                        prerequisites: ["Bachelor's Degree", "Student Teaching"],
                        duration: "4-5 years",
                        specializations: [
                            "Elementary Education",
                            "Secondary Education",
                            "Special Education",
                            "Subject Specialization"
                        ],
                        careerPath: "Education Degree → Student Teaching → License → Classroom Teacher",
                        salaryRange: "$35k - $80k",
                        keySkills: ["Classroom Management", "Curriculum Design", "Student Assessment"],
                        courses: [
                            "Educational Psychology",
                            "Teaching Methods",
                            "Classroom Management",
                            "Curriculum Development",
                            "Assessment & Evaluation"
                        ]
                    }
                }
            },

            // Healthcare Support
            healthcareSupport: {
                name: "Healthcare Support",
                icon: "fas fa-heartbeat",
                color: "#FF69B4",
                description: "Allied health and healthcare support careers",
                subcategories: {
                    physicalTherapist: {
                        name: "Physical Therapist",
                        programs: ["DPT"],
                        prerequisites: ["Bachelor's Degree", "Prerequisites"],
                        duration: "3 years",
                        specializations: [
                            "Orthopedic PT",
                            "Neurological PT",
                            "Pediatric PT",
                            "Sports PT",
                            "Geriatric PT"
                        ],
                        careerPath: "Pre-PT → PT School → Licensure → Specialization",
                        salaryRange: "$70k - $100k+",
                        keySkills: ["Patient Assessment", "Treatment Planning", "Manual Therapy"],
                        courses: [
                            "Anatomy & Physiology",
                            "Kinesiology",
                            "Pathophysiology",
                            "Therapeutic Exercise",
                            "Manual Therapy"
                        ]
                    },
                    occupationalTherapist: {
                        name: "Occupational Therapist",
                        programs: ["MOT", "OTD"],
                        prerequisites: ["Bachelor's Degree", "Prerequisites"],
                        duration: "2-3 years",
                        careerPath: "Pre-OT → OT School → Licensure → Practice",
                        salaryRange: "$60k - $90k+",
                        keySkills: ["Activity Analysis", "Adaptive Equipment", "Patient Care"],
                        courses: [
                            "Occupational Therapy Theory",
                            "Activity Analysis",
                            "Adaptive Equipment",
                            "Pediatric OT",
                            "Mental Health OT"
                        ]
                    },
                    physicianAssistant: {
                        name: "Physician Assistant",
                        programs: ["MPAS", "MS"],
                        prerequisites: ["Bachelor's Degree", "Healthcare Experience", "Prerequisites"],
                        duration: "2-3 years",
                        careerPath: "Pre-PA → PA School → Licensure → Practice",
                        salaryRange: "$90k - $130k+",
                        keySkills: ["Diagnosis", "Treatment", "Patient Care", "Medical Knowledge"],
                        courses: [
                            "Medical Anatomy",
                            "Pathophysiology",
                            "Clinical Medicine",
                            "Pharmacology",
                            "Clinical Skills"
                        ]
                    }
                }
            }
        };
    }

    // Get all professional categories
    getCategories() {
        return Object.keys(this.professionalPaths).map(key => ({
            id: key,
            name: this.professionalPaths[key].name,
            icon: this.professionalPaths[key].icon,
            color: this.professionalPaths[key].color,
            description: this.professionalPaths[key].description
        }));
    }

    // Get subcategories for a specific category
    getSubcategories(categoryId) {
        const category = this.professionalPaths[categoryId];
        if (!category) return [];
        
        return Object.keys(category.subcategories).map(key => ({
            id: key,
            ...category.subcategories[key]
        }));
    }

    // Get detailed information about a specific career path
    getCareerPathDetails(categoryId, subcategoryId) {
        const category = this.professionalPaths[categoryId];
        if (!category || !category.subcategories[subcategoryId]) {
            return null;
        }
        
        return {
            category: category.name,
            ...category.subcategories[subcategoryId]
        };
    }

    // Get recommended courses for a career path
    getRecommendedCourses(categoryId, subcategoryId) {
        const careerPath = this.getCareerPathDetails(categoryId, subcategoryId);
        return careerPath ? careerPath.courses || [] : [];
    }

    // Get prerequisites for a career path
    getPrerequisites(categoryId, subcategoryId) {
        const careerPath = this.getCareerPathDetails(categoryId, subcategoryId);
        return careerPath ? careerPath.prerequisites || [] : [];
    }

    // Get salary range for a career path
    getSalaryRange(categoryId, subcategoryId) {
        const careerPath = this.getCareerPathDetails(categoryId, subcategoryId);
        return careerPath ? careerPath.salaryRange || 'Not specified' : 'Not specified';
    }

    // Generate a learning plan for a professional career path
    generateLearningPlan(categoryId, subcategoryId, currentLevel = 'beginner') {
        const careerPath = this.getCareerPathDetails(categoryId, subcategoryId);
        if (!careerPath) return null;

        const plans = {
            beginner: {
                duration: '6-12 months',
                focus: 'Foundation building and prerequisites',
                steps: [
                    'Research career requirements and prerequisites',
                    'Take foundational courses in relevant subjects',
                    'Gain relevant experience or shadowing',
                    'Prepare for entrance exams (if applicable)',
                    'Apply to programs or certifications'
                ]
            },
            intermediate: {
                duration: '1-3 years',
                focus: 'Core education and skill development',
                steps: [
                    'Complete core curriculum',
                    'Gain hands-on experience through internships',
                    'Develop specialized skills in chosen area',
                    'Network with professionals in the field',
                    'Prepare for licensure or certification exams'
                ]
            },
            advanced: {
                duration: '2-5 years',
                focus: 'Specialization and career advancement',
                steps: [
                    'Complete advanced coursework or specialization',
                    'Gain significant professional experience',
                    'Pursue additional certifications or credentials',
                    'Develop leadership and management skills',
                    'Consider advanced degrees or fellowships'
                ]
            }
        };

        return {
            careerPath: careerPath.name,
            level: currentLevel,
            ...plans[currentLevel],
            recommendedCourses: this.getRecommendedCourses(categoryId, subcategoryId),
            prerequisites: this.getPrerequisites(categoryId, subcategoryId)
        };
    }

    // Search for career paths by keyword
    searchCareerPaths(keyword) {
        const results = [];
        const searchTerm = keyword.toLowerCase();

        Object.keys(this.professionalPaths).forEach(categoryId => {
            const category = this.professionalPaths[categoryId];
            
            // Check category name
            if (category.name.toLowerCase().includes(searchTerm)) {
                results.push({
                    type: 'category',
                    categoryId,
                    name: category.name,
                    description: category.description
                });
            }

            // Check subcategories
            Object.keys(category.subcategories).forEach(subcategoryId => {
                const subcategory = category.subcategories[subcategoryId];
                
                if (subcategory.name.toLowerCase().includes(searchTerm) ||
                    (subcategory.specializations && subcategory.specializations.some(spec => 
                        spec.toLowerCase().includes(searchTerm)))) {
                    
                    results.push({
                        type: 'career',
                        categoryId,
                        subcategoryId,
                        name: subcategory.name,
                        category: category.name,
                        description: `Specialized career in ${category.name}`
                    });
                }
            });
        });

        return results;
    }
}

// Initialize the professional career paths system
const professionalCareerPaths = new ProfessionalCareerPaths();

// Export for use in other scripts
window.professionalCareerPaths = professionalCareerPaths;
