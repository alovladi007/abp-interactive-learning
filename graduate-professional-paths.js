// Graduate and Professional Programs Extension for AI Path Advisor
// Includes Masters, PhD, Medical School, Law School, MBA, and other professional programs

const graduateProfessionalPrograms = {
    // Program levels
    programLevels: {
        undergraduate: {
            name: 'Undergraduate',
            duration: '4 years',
            description: 'Bachelor\'s degree programs',
            icon: '🎓'
        },
        masters: {
            name: 'Master\'s',
            duration: '1-2 years',
            description: 'Graduate degree programs',
            icon: '📚'
        },
        doctoral: {
            name: 'Doctoral (PhD)',
            duration: '4-6 years',
            description: 'Research-focused doctoral programs',
            icon: '🔬'
        },
        professional: {
            name: 'Professional',
            duration: '2-4 years',
            description: 'Professional degree programs',
            icon: '💼'
        }
    },

    // Graduate Programs by Field
    graduatePrograms: {
        // Master's Programs
        'ms-computer-science': {
            name: 'MS in Computer Science',
            level: 'masters',
            duration: '2 years',
            credits: 30,
            focus: 'Advanced computing, AI, systems, theory',
            admissionRequirements: {
                gpa: 3.0,
                gre: 'Required (Quant: 160+)',
                prerequisites: ['Data Structures', 'Algorithms', 'Operating Systems'],
                experience: 'Research or industry experience preferred'
            },
            careers: [
                'ml-engineer',
                'research-scientist',
                'software-architect',
                'ai-specialist'
            ],
            coreCourses: [
                { id: 'CS501', name: 'Advanced Algorithms', credits: 3 },
                { id: 'CS502', name: 'Machine Learning Theory', credits: 3 },
                { id: 'CS503', name: 'Distributed Systems', credits: 3 },
                { id: 'CS504', name: 'Research Methods in CS', credits: 3 }
            ],
            specializations: {
                'artificial-intelligence': {
                    name: 'Artificial Intelligence',
                    courses: [
                        { id: 'CS511', name: 'Deep Learning', credits: 3 },
                        { id: 'CS512', name: 'Natural Language Processing', credits: 3 },
                        { id: 'CS513', name: 'Computer Vision', credits: 3 },
                        { id: 'CS514', name: 'Reinforcement Learning', credits: 3 }
                    ]
                },
                'systems': {
                    name: 'Computer Systems',
                    courses: [
                        { id: 'CS521', name: 'Advanced Operating Systems', credits: 3 },
                        { id: 'CS522', name: 'Cloud Computing', credits: 3 },
                        { id: 'CS523', name: 'Network Security', credits: 3 },
                        { id: 'CS524', name: 'Database Systems', credits: 3 }
                    ]
                }
            }
        },

        'ms-data-science': {
            name: 'MS in Data Science',
            level: 'masters',
            duration: '1.5 years',
            credits: 36,
            focus: 'Statistical analysis, machine learning, big data',
            admissionRequirements: {
                gpa: 3.2,
                gre: 'Optional',
                prerequisites: ['Statistics', 'Linear Algebra', 'Programming'],
                experience: 'Analytical experience preferred'
            },
            careers: [
                'data-scientist',
                'ml-engineer',
                'business-analyst',
                'quantitative-analyst'
            ],
            coreCourses: [
                { id: 'DS501', name: 'Statistical Learning', credits: 3 },
                { id: 'DS502', name: 'Big Data Analytics', credits: 3 },
                { id: 'DS503', name: 'Data Mining', credits: 3 },
                { id: 'DS504', name: 'Data Visualization', credits: 3 }
            ]
        },

        'mba': {
            name: 'Master of Business Administration',
            level: 'masters',
            duration: '2 years',
            credits: 60,
            focus: 'Business leadership, strategy, management',
            admissionRequirements: {
                gpa: 3.0,
                gmat: 'Required (650+) or GRE',
                prerequisites: [],
                experience: '2-5 years work experience required'
            },
            careers: [
                'management-consultant',
                'investment-banker',
                'product-manager',
                'entrepreneur'
            ],
            coreCourses: [
                { id: 'MBA501', name: 'Financial Accounting', credits: 3 },
                { id: 'MBA502', name: 'Corporate Finance', credits: 3 },
                { id: 'MBA503', name: 'Strategic Management', credits: 3 },
                { id: 'MBA504', name: 'Marketing Management', credits: 3 },
                { id: 'MBA505', name: 'Operations Management', credits: 3 },
                { id: 'MBA506', name: 'Leadership & Organizations', credits: 3 }
            ]
        },

        'ms-engineering': {
            name: 'MS in Engineering',
            level: 'masters',
            duration: '2 years',
            credits: 30,
            focus: 'Advanced engineering principles and research',
            specializations: {
                'electrical': {
                    name: 'Electrical Engineering',
                    courses: [
                        { id: 'EE501', name: 'Advanced Signal Processing', credits: 3 },
                        { id: 'EE502', name: 'RF Circuit Design', credits: 3 },
                        { id: 'EE503', name: 'Power Electronics', credits: 3 },
                        { id: 'EE504', name: 'Control Systems Theory', credits: 3 }
                    ]
                },
                'mechanical': {
                    name: 'Mechanical Engineering',
                    courses: [
                        { id: 'ME501', name: 'Advanced Thermodynamics', credits: 3 },
                        { id: 'ME502', name: 'Computational Fluid Dynamics', credits: 3 },
                        { id: 'ME503', name: 'Robotics & Automation', credits: 3 },
                        { id: 'ME504', name: 'Advanced Materials', credits: 3 }
                    ]
                }
            }
        },

        // PhD Programs
        'phd-computer-science': {
            name: 'PhD in Computer Science',
            level: 'doctoral',
            duration: '5 years',
            credits: 72,
            focus: 'Original research in computing',
            admissionRequirements: {
                gpa: 3.5,
                gre: 'Required (Quant: 165+)',
                prerequisites: ['MS in CS or equivalent'],
                experience: 'Research publications preferred'
            },
            milestones: [
                'Coursework (Years 1-2)',
                'Qualifying Exams',
                'Thesis Proposal',
                'Dissertation Research',
                'Dissertation Defense'
            ],
            coreCourses: [
                { id: 'CS701', name: 'Advanced Theory of Computation', credits: 3 },
                { id: 'CS702', name: 'Research Seminar', credits: 1 },
                { id: 'CS703', name: 'Dissertation Research', credits: 12 }
            ]
        },

        'phd-physics': {
            name: 'PhD in Physics',
            level: 'doctoral',
            duration: '5-6 years',
            credits: 72,
            focus: 'Theoretical or experimental physics research',
            admissionRequirements: {
                gpa: 3.5,
                gre: 'Required (Physics GRE recommended)',
                prerequisites: ['BS in Physics or related'],
                experience: 'Research experience required'
            },
            coreCourses: [
                { id: 'PHYS701', name: 'Quantum Mechanics III', credits: 3 },
                { id: 'PHYS702', name: 'Statistical Mechanics', credits: 3 },
                { id: 'PHYS703', name: 'Electrodynamics II', credits: 3 },
                { id: 'PHYS704', name: 'Research Methods', credits: 3 }
            ]
        }
    },

    // Professional Programs
    professionalPrograms: {
        // Medical School
        'md': {
            name: 'Doctor of Medicine (MD)',
            level: 'professional',
            duration: '4 years',
            credits: 200,
            focus: 'Clinical medicine and patient care',
            admissionRequirements: {
                gpa: 3.7,
                mcat: 'Required (510+)',
                prerequisites: [
                    'Biology (2 semesters)',
                    'Chemistry (2 semesters)',
                    'Organic Chemistry (2 semesters)',
                    'Physics (2 semesters)',
                    'Biochemistry',
                    'Psychology',
                    'Sociology'
                ],
                experience: 'Clinical shadowing, volunteering, research'
            },
            curriculum: {
                'year1': {
                    name: 'Pre-Clinical Year 1',
                    courses: [
                        { id: 'MED501', name: 'Gross Anatomy', credits: 8 },
                        { id: 'MED502', name: 'Biochemistry & Genetics', credits: 6 },
                        { id: 'MED503', name: 'Physiology', credits: 6 },
                        { id: 'MED504', name: 'Histology', credits: 4 },
                        { id: 'MED505', name: 'Medical Ethics', credits: 2 }
                    ]
                },
                'year2': {
                    name: 'Pre-Clinical Year 2',
                    courses: [
                        { id: 'MED601', name: 'Pathology', credits: 8 },
                        { id: 'MED602', name: 'Pharmacology', credits: 6 },
                        { id: 'MED603', name: 'Microbiology & Immunology', credits: 6 },
                        { id: 'MED604', name: 'Clinical Skills', credits: 4 }
                    ]
                },
                'year3': {
                    name: 'Clinical Rotations',
                    rotations: [
                        'Internal Medicine (12 weeks)',
                        'Surgery (8 weeks)',
                        'Pediatrics (8 weeks)',
                        'OB/GYN (6 weeks)',
                        'Psychiatry (6 weeks)',
                        'Family Medicine (6 weeks)'
                    ]
                },
                'year4': {
                    name: 'Advanced Clinical',
                    components: [
                        'Sub-internship',
                        'Emergency Medicine',
                        'Elective Rotations',
                        'Residency Applications'
                    ]
                }
            },
            nextSteps: 'Residency (3-7 years) → Fellowship (optional)'
        },

        // Law School
        'jd': {
            name: 'Juris Doctor (JD)',
            level: 'professional',
            duration: '3 years',
            credits: 90,
            focus: 'Legal theory, practice, and professional skills',
            admissionRequirements: {
                gpa: 3.5,
                lsat: 'Required (160+)',
                prerequisites: ['Bachelor\'s degree in any field'],
                experience: 'Leadership, public service, internships'
            },
            curriculum: {
                'year1': {
                    name: '1L Year (Required)',
                    courses: [
                        { id: 'LAW501', name: 'Contracts', credits: 6 },
                        { id: 'LAW502', name: 'Torts', credits: 6 },
                        { id: 'LAW503', name: 'Criminal Law', credits: 4 },
                        { id: 'LAW504', name: 'Constitutional Law', credits: 6 },
                        { id: 'LAW505', name: 'Civil Procedure', credits: 6 },
                        { id: 'LAW506', name: 'Legal Research & Writing', credits: 4 }
                    ]
                },
                'year2': {
                    name: '2L Year',
                    requirements: [
                        'Evidence',
                        'Professional Responsibility',
                        'Electives',
                        'Moot Court or Journal'
                    ]
                },
                'year3': {
                    name: '3L Year',
                    components: [
                        'Specialization courses',
                        'Clinical programs',
                        'Externships',
                        'Bar preparation'
                    ]
                }
            },
            specializations: [
                'Corporate Law',
                'Criminal Law',
                'Environmental Law',
                'Intellectual Property',
                'International Law',
                'Public Interest Law'
            ],
            nextSteps: 'Bar Exam → Practice or Judicial Clerkship'
        },

        // Dental School
        'dds': {
            name: 'Doctor of Dental Surgery (DDS)',
            level: 'professional',
            duration: '4 years',
            credits: 180,
            focus: 'Oral health and dental medicine',
            admissionRequirements: {
                gpa: 3.5,
                dat: 'Required (20+)',
                prerequisites: [
                    'Biology', 'Chemistry', 'Organic Chemistry',
                    'Physics', 'Biochemistry'
                ],
                experience: 'Dental shadowing required'
            },
            curriculum: {
                'years1-2': 'Biomedical sciences and pre-clinical training',
                'years3-4': 'Clinical rotations and patient care'
            }
        },

        // Pharmacy School
        'pharmd': {
            name: 'Doctor of Pharmacy (PharmD)',
            level: 'professional',
            duration: '4 years',
            credits: 150,
            focus: 'Pharmaceutical sciences and patient care',
            admissionRequirements: {
                gpa: 3.0,
                pcat: 'Optional at many schools',
                prerequisites: [
                    'Chemistry (2 semesters)',
                    'Organic Chemistry (2 semesters)',
                    'Biology (2 semesters)',
                    'Physics',
                    'Calculus',
                    'Statistics'
                ],
                experience: 'Pharmacy experience preferred'
            },
            curriculum: {
                'year1': {
                    courses: [
                        { id: 'PHAR501', name: 'Pharmaceutical Chemistry', credits: 4 },
                        { id: 'PHAR502', name: 'Pharmacology I', credits: 4 },
                        { id: 'PHAR503', name: 'Pharmacy Practice', credits: 3 }
                    ]
                },
                'year4': 'Advanced Pharmacy Practice Experiences (APPEs)'
            }
        },

        // Veterinary School
        'dvm': {
            name: 'Doctor of Veterinary Medicine (DVM)',
            level: 'professional',
            duration: '4 years',
            credits: 180,
            focus: 'Animal health and veterinary medicine',
            admissionRequirements: {
                gpa: 3.5,
                gre: 'Required at most schools',
                prerequisites: [
                    'Biology', 'Chemistry', 'Organic Chemistry',
                    'Physics', 'Biochemistry', 'Microbiology'
                ],
                experience: 'Animal/veterinary experience required'
            }
        },

        // Nursing Programs
        'msn': {
            name: 'Master of Science in Nursing',
            level: 'masters',
            duration: '2 years',
            credits: 45,
            focus: 'Advanced nursing practice',
            specializations: [
                'Nurse Practitioner',
                'Clinical Nurse Specialist',
                'Nurse Educator',
                'Nurse Administrator'
            ]
        },

        'dnp': {
            name: 'Doctor of Nursing Practice',
            level: 'professional',
            duration: '3-4 years',
            credits: 75,
            focus: 'Clinical nursing leadership'
        }
    },

    // Career paths for graduate/professional degrees
    advancedCareerPaths: {
        // Medical careers
        'physician': {
            name: 'Physician',
            program: 'md',
            requiredDegree: 'MD',
            additionalTraining: 'Residency (3-7 years)',
            specializations: [
                'Internal Medicine',
                'Surgery',
                'Pediatrics',
                'Emergency Medicine',
                'Radiology',
                'Anesthesiology'
            ]
        },
        'surgeon': {
            name: 'Surgeon',
            program: 'md',
            requiredDegree: 'MD',
            additionalTraining: 'Surgery Residency (5-7 years) + Fellowship'
        },
        
        // Legal careers
        'attorney': {
            name: 'Attorney',
            program: 'jd',
            requiredDegree: 'JD',
            additionalRequirement: 'Pass Bar Exam',
            specializations: [
                'Corporate Lawyer',
                'Criminal Defense Attorney',
                'Prosecutor',
                'Patent Attorney',
                'Environmental Lawyer'
            ]
        },
        'judge': {
            name: 'Judge',
            program: 'jd',
            requiredDegree: 'JD',
            additionalRequirement: 'Legal experience + appointment/election'
        },
        
        // Academic careers
        'professor': {
            name: 'University Professor',
            programs: ['phd-computer-science', 'phd-physics'],
            requiredDegree: 'PhD',
            path: 'Postdoc → Assistant Prof → Associate Prof → Full Prof'
        },
        'research-scientist': {
            name: 'Research Scientist',
            programs: ['phd-computer-science', 'phd-physics', 'ms-computer-science'],
            requiredDegree: 'MS or PhD',
            sectors: ['Academia', 'Industry', 'Government Labs']
        },
        
        // Business careers
        'ceo': {
            name: 'Chief Executive Officer',
            program: 'mba',
            requiredDegree: 'MBA (often)',
            path: 'Analyst → Manager → Director → VP → C-Suite'
        },
        'management-consultant': {
            name: 'Management Consultant',
            program: 'mba',
            requiredDegree: 'MBA',
            firms: ['McKinsey', 'BCG', 'Bain', 'Deloitte']
        },
        'investment-banker': {
            name: 'Investment Banker',
            program: 'mba',
            requiredDegree: 'MBA or relevant MS',
            path: 'Analyst → Associate → VP → Director → MD'
        }
    },

    // Prerequisites tracking
    prerequisiteChains: {
        'premed': {
            name: 'Pre-Medical Track',
            targetProgram: 'md',
            requirements: [
                { course: 'BIOL101', name: 'Biology I', credits: 4 },
                { course: 'BIOL102', name: 'Biology II', credits: 4 },
                { course: 'CHEM101', name: 'Chemistry I', credits: 4 },
                { course: 'CHEM102', name: 'Chemistry II', credits: 4 },
                { course: 'CHEM201', name: 'Organic Chemistry I', credits: 4 },
                { course: 'CHEM202', name: 'Organic Chemistry II', credits: 4 },
                { course: 'PHYS101', name: 'Physics I', credits: 4 },
                { course: 'PHYS102', name: 'Physics II', credits: 4 },
                { course: 'MATH101', name: 'Calculus I', credits: 4 },
                { course: 'MATH201', name: 'Statistics', credits: 3 },
                { course: 'BIOL301', name: 'Biochemistry', credits: 4 },
                { course: 'PSY101', name: 'Psychology', credits: 3 },
                { course: 'SOC101', name: 'Sociology', credits: 3 }
            ],
            timeline: {
                'year1': ['BIOL101', 'BIOL102', 'CHEM101', 'CHEM102', 'MATH101'],
                'year2': ['CHEM201', 'CHEM202', 'PHYS101', 'PHYS102', 'MATH201'],
                'year3': ['BIOL301', 'PSY101', 'SOC101', 'MCAT Prep'],
                'year4': ['Medical School Applications', 'Clinical Experience']
            }
        },
        
        'prelaw': {
            name: 'Pre-Law Track',
            targetProgram: 'jd',
            recommendedMajors: [
                'Political Science',
                'Philosophy',
                'English',
                'History',
                'Economics'
            ],
            skills: [
                'Critical thinking',
                'Analytical reasoning',
                'Writing',
                'Public speaking',
                'Research'
            ],
            activities: [
                'Mock Trial',
                'Debate Team',
                'Internships',
                'Student Government'
            ]
        }
    },

    // Admission test preparation
    admissionTests: {
        'gre': {
            name: 'Graduate Record Examination',
            sections: ['Verbal', 'Quantitative', 'Analytical Writing'],
            programs: ['MS', 'PhD programs'],
            prepTime: '2-3 months'
        },
        'gmat': {
            name: 'Graduate Management Admission Test',
            sections: ['Verbal', 'Quantitative', 'Integrated Reasoning', 'AWA'],
            programs: ['MBA programs'],
            prepTime: '3-4 months'
        },
        'mcat': {
            name: 'Medical College Admission Test',
            sections: ['Bio/Biochem', 'Chem/Phys', 'CARS', 'Psych/Soc'],
            programs: ['Medical school'],
            prepTime: '3-6 months'
        },
        'lsat': {
            name: 'Law School Admission Test',
            sections: ['Logical Reasoning', 'Reading Comp', 'Logic Games'],
            programs: ['Law school'],
            prepTime: '3-4 months'
        },
        'dat': {
            name: 'Dental Admission Test',
            programs: ['Dental school'],
            prepTime: '2-3 months'
        }
    }
};

// Export for use in main path advisor
if (typeof module !== 'undefined' && module.exports) {
    module.exports = graduateProfessionalPrograms;
}