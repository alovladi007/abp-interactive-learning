// Course Syllabus System - Academic Standard Syllabi for All Courses

// Base URL for syllabus storage (can be changed to actual university system)
const SYLLABUS_BASE_URL = '/syllabi';

// Syllabus template generator
function generateSyllabusLink(courseId, majorId) {
    return `${SYLLABUS_BASE_URL}/${majorId}/${courseId}-syllabus.pdf`;
}

// Complete syllabus structure for each course
const courseSyllabusTemplate = {
    courseId: '',
    courseName: '',
    credits: 0,
    instructor: '',
    semester: '',
    meetingTime: '',
    location: '',
    officeHours: '',
    
    courseDescription: '',
    learningObjectives: [],
    prerequisites: [],
    corequisites: [],
    
    requiredTextbooks: [],
    supplementaryMaterials: [],
    
    gradingScale: {
        'A': '93-100%',
        'A-': '90-92%',
        'B+': '87-89%',
        'B': '83-86%',
        'B-': '80-82%',
        'C+': '77-79%',
        'C': '73-76%',
        'C-': '70-72%',
        'D': '60-69%',
        'F': 'Below 60%'
    },
    
    gradingBreakdown: {
        'Exams': 40,
        'Assignments': 25,
        'Laboratory': 20,
        'Participation': 5,
        'Final Project': 10
    },
    
    weeklySchedule: [], // 15-16 weeks of content
    
    assignments: [],
    exams: [],
    
    policies: {
        attendance: '',
        lateWork: '',
        academicIntegrity: '',
        accommodations: ''
    },
    
    resources: {
        tutoring: '',
        library: '',
        writingCenter: '',
        academicSupport: ''
    }
};

// Generate detailed syllabus for Chemistry courses
const chemistrySyllabi = {
    'CHEM101': {
        courseId: 'CHEM101',
        courseName: 'General Chemistry I',
        credits: 4,
        syllabusUrl: generateSyllabusLink('CHEM101', 'chemistry'),
        
        courseDescription: 'Introduction to chemical principles including atomic structure, chemical bonding, stoichiometry, gases, thermochemistry, and periodic properties.',
        
        learningObjectives: [
            'Understand atomic structure and electron configuration',
            'Master chemical nomenclature and formula writing',
            'Perform stoichiometric calculations',
            'Apply gas laws to solve problems',
            'Analyze thermochemical processes',
            'Predict periodic trends and properties'
        ],
        
        prerequisites: ['High school chemistry', 'MATH101 (may be taken concurrently)'],
        
        requiredTextbooks: [
            {
                title: 'Chemistry: The Central Science',
                authors: 'Brown, LeMay, Bursten, Murphy, Woodward',
                edition: '14th',
                isbn: '978-0134414232',
                required: true
            }
        ],
        
        weeklySchedule: [
            { week: 1, topic: 'Introduction to Chemistry & Measurement', readings: 'Ch. 1', assignments: ['Problem Set 1'] },
            { week: 2, topic: 'Atoms, Molecules, and Ions', readings: 'Ch. 2', assignments: ['Problem Set 2', 'Lab 1'] },
            { week: 3, topic: 'Stoichiometry', readings: 'Ch. 3', assignments: ['Problem Set 3', 'Lab 2'] },
            { week: 4, topic: 'Reactions in Aqueous Solutions', readings: 'Ch. 4', assignments: ['Problem Set 4', 'Lab 3'] },
            { week: 5, topic: 'Thermochemistry', readings: 'Ch. 5', assignments: ['Problem Set 5'] },
            { week: 6, topic: 'Exam 1 Review', readings: 'Ch. 1-5', assignments: ['Exam 1'] },
            { week: 7, topic: 'Electronic Structure of Atoms', readings: 'Ch. 6', assignments: ['Problem Set 6', 'Lab 4'] },
            { week: 8, topic: 'Periodic Properties', readings: 'Ch. 7', assignments: ['Problem Set 7', 'Lab 5'] },
            { week: 9, topic: 'Chemical Bonding I', readings: 'Ch. 8', assignments: ['Problem Set 8'] },
            { week: 10, topic: 'Chemical Bonding II', readings: 'Ch. 9', assignments: ['Problem Set 9', 'Lab 6'] },
            { week: 11, topic: 'Gases', readings: 'Ch. 10', assignments: ['Problem Set 10', 'Lab 7'] },
            { week: 12, topic: 'Exam 2 Review', readings: 'Ch. 6-10', assignments: ['Exam 2'] },
            { week: 13, topic: 'Intermolecular Forces', readings: 'Ch. 11', assignments: ['Problem Set 11', 'Lab 8'] },
            { week: 14, topic: 'Solutions', readings: 'Ch. 13', assignments: ['Problem Set 12'] },
            { week: 15, topic: 'Review and Integration', readings: 'All chapters', assignments: ['Final Project'] },
            { week: 16, topic: 'Final Exam', readings: 'Comprehensive', assignments: ['Final Exam'] }
        ],
        
        gradingBreakdown: {
            'Midterm Exams (2)': 30,
            'Final Exam': 20,
            'Laboratory': 25,
            'Problem Sets': 15,
            'Quizzes': 5,
            'Participation': 5
        },
        
        labComponent: {
            required: true,
            hours: 3,
            description: 'Weekly 3-hour laboratory sessions covering basic techniques, safety, and experimental chemistry'
        }
    },
    
    'CHEM201': {
        courseId: 'CHEM201',
        courseName: 'Organic Chemistry I',
        credits: 4,
        syllabusUrl: generateSyllabusLink('CHEM201', 'chemistry'),
        
        courseDescription: 'Structure, nomenclature, reactions, and synthesis of organic compounds including alkanes, alkenes, alkynes, and alkyl halides.',
        
        learningObjectives: [
            'Draw and interpret organic structures using various representations',
            'Apply IUPAC nomenclature rules',
            'Predict products of organic reactions',
            'Propose reaction mechanisms',
            'Design synthetic routes to target molecules',
            'Understand stereochemistry and chirality'
        ],
        
        prerequisites: ['CHEM102'],
        
        requiredTextbooks: [
            {
                title: 'Organic Chemistry',
                authors: 'Wade & Simek',
                edition: '9th',
                isbn: '978-0321971371',
                required: true
            },
            {
                title: 'Organic Chemistry Study Guide and Solutions Manual',
                authors: 'Wade & Simek',
                edition: '9th',
                isbn: '978-0134160375',
                required: false
            }
        ],
        
        weeklySchedule: [
            { week: 1, topic: 'Structure and Bonding', readings: 'Ch. 1', assignments: ['Problem Set 1'] },
            { week: 2, topic: 'Acids and Bases', readings: 'Ch. 2', assignments: ['Problem Set 2'] },
            { week: 3, topic: 'Alkanes and Cycloalkanes', readings: 'Ch. 3', assignments: ['Problem Set 3', 'Lab 1'] },
            { week: 4, topic: 'Stereochemistry', readings: 'Ch. 5', assignments: ['Problem Set 4', 'Lab 2'] },
            { week: 5, topic: 'Alkyl Halides: Nucleophilic Substitution', readings: 'Ch. 6', assignments: ['Problem Set 5', 'Lab 3'] },
            { week: 6, topic: 'Alkyl Halides: Elimination', readings: 'Ch. 7', assignments: ['Exam 1'] },
            { week: 7, topic: 'Alkenes: Structure and Synthesis', readings: 'Ch. 8', assignments: ['Problem Set 6', 'Lab 4'] },
            { week: 8, topic: 'Reactions of Alkenes', readings: 'Ch. 9', assignments: ['Problem Set 7', 'Lab 5'] },
            { week: 9, topic: 'Alkynes', readings: 'Ch. 10', assignments: ['Problem Set 8'] },
            { week: 10, topic: 'Alcohols', readings: 'Ch. 11', assignments: ['Problem Set 9', 'Lab 6'] },
            { week: 11, topic: 'Ethers and Epoxides', readings: 'Ch. 12', assignments: ['Problem Set 10', 'Lab 7'] },
            { week: 12, topic: 'Exam 2 Review', readings: 'Ch. 8-12', assignments: ['Exam 2'] },
            { week: 13, topic: 'Spectroscopy: IR and MS', readings: 'Ch. 13', assignments: ['Problem Set 11', 'Lab 8'] },
            { week: 14, topic: 'NMR Spectroscopy', readings: 'Ch. 14', assignments: ['Problem Set 12', 'Lab 9'] },
            { week: 15, topic: 'Synthesis Workshop', readings: 'Review', assignments: ['Synthesis Project'] },
            { week: 16, topic: 'Final Exam', readings: 'Comprehensive', assignments: ['Final Exam'] }
        ]
    }
};

// Generate syllabus data for all Computer Science courses
const computerScienceSyllabi = {
    'CS101': {
        courseId: 'CS101',
        courseName: 'Introduction to Programming',
        credits: 4,
        syllabusUrl: generateSyllabusLink('CS101', 'cs'),
        
        courseDescription: 'Introduction to programming concepts using Python. Topics include variables, control structures, functions, data structures, and object-oriented programming.',
        
        learningObjectives: [
            'Write, test, and debug Python programs',
            'Use fundamental programming constructs',
            'Implement basic algorithms and data structures',
            'Apply object-oriented programming principles',
            'Develop problem-solving skills',
            'Follow software development best practices'
        ],
        
        prerequisites: ['None'],
        
        requiredTextbooks: [
            {
                title: 'Introduction to Computing Using Python',
                authors: 'Perkovic',
                edition: '3rd',
                isbn: '978-1119498537',
                required: true
            }
        ],
        
        weeklySchedule: [
            { week: 1, topic: 'Introduction to Computing', readings: 'Ch. 1', assignments: ['Lab 1', 'HW 1'] },
            { week: 2, topic: 'Variables and Expressions', readings: 'Ch. 2', assignments: ['Lab 2', 'HW 2'] },
            { week: 3, topic: 'Control Flow: Conditionals', readings: 'Ch. 3.1-3.3', assignments: ['Lab 3', 'HW 3'] },
            { week: 4, topic: 'Control Flow: Loops', readings: 'Ch. 3.4-3.6', assignments: ['Lab 4', 'Project 1'] },
            { week: 5, topic: 'Functions', readings: 'Ch. 4', assignments: ['Lab 5', 'HW 4'] },
            { week: 6, topic: 'Lists and Tuples', readings: 'Ch. 5', assignments: ['Midterm Exam'] },
            { week: 7, topic: 'Strings', readings: 'Ch. 6', assignments: ['Lab 6', 'HW 5'] },
            { week: 8, topic: 'Dictionaries and Sets', readings: 'Ch. 7', assignments: ['Lab 7', 'Project 2'] },
            { week: 9, topic: 'File I/O', readings: 'Ch. 8', assignments: ['Lab 8', 'HW 6'] },
            { week: 10, topic: 'Exception Handling', readings: 'Ch. 9', assignments: ['Lab 9', 'HW 7'] },
            { week: 11, topic: 'Object-Oriented Programming I', readings: 'Ch. 10', assignments: ['Lab 10', 'HW 8'] },
            { week: 12, topic: 'Object-Oriented Programming II', readings: 'Ch. 11', assignments: ['Lab 11', 'Project 3'] },
            { week: 13, topic: 'Recursion', readings: 'Ch. 12', assignments: ['Lab 12', 'HW 9'] },
            { week: 14, topic: 'Algorithm Analysis', readings: 'Ch. 13', assignments: ['Lab 13', 'HW 10'] },
            { week: 15, topic: 'Review and Advanced Topics', readings: 'Review', assignments: ['Final Project'] },
            { week: 16, topic: 'Final Exam', readings: 'Comprehensive', assignments: ['Final Exam'] }
        ],
        
        gradingBreakdown: {
            'Programming Projects (3)': 30,
            'Homework Assignments': 20,
            'Lab Exercises': 15,
            'Midterm Exam': 15,
            'Final Exam': 15,
            'Participation': 5
        }
    },
    
    'CS201': {
        courseId: 'CS201',
        courseName: 'Data Structures and Algorithms',
        credits: 4,
        syllabusUrl: generateSyllabusLink('CS201', 'cs'),
        
        courseDescription: 'Fundamental data structures (arrays, linked lists, stacks, queues, trees, graphs, hash tables) and algorithms (sorting, searching, graph algorithms).',
        
        learningObjectives: [
            'Implement and analyze fundamental data structures',
            'Design and analyze algorithms',
            'Apply Big-O notation for complexity analysis',
            'Select appropriate data structures for problems',
            'Implement recursive algorithms',
            'Understand space-time tradeoffs'
        ],
        
        prerequisites: ['CS101'],
        
        requiredTextbooks: [
            {
                title: 'Introduction to Algorithms',
                authors: 'Cormen, Leiserson, Rivest, Stein',
                edition: '3rd',
                isbn: '978-0262033848',
                required: true
            }
        ],
        
        weeklySchedule: [
            { week: 1, topic: 'Algorithm Analysis and Big-O', readings: 'Ch. 1-3', assignments: ['PS 1'] },
            { week: 2, topic: 'Arrays and Dynamic Arrays', readings: 'Ch. 4', assignments: ['PS 2', 'Lab 1'] },
            { week: 3, topic: 'Linked Lists', readings: 'Ch. 10', assignments: ['PS 3', 'Lab 2'] },
            { week: 4, topic: 'Stacks and Queues', readings: 'Ch. 10', assignments: ['Project 1'] },
            { week: 5, topic: 'Recursion and Divide-and-Conquer', readings: 'Ch. 4', assignments: ['PS 4', 'Lab 3'] },
            { week: 6, topic: 'Sorting Algorithms I', readings: 'Ch. 6-7', assignments: ['Midterm 1'] },
            { week: 7, topic: 'Sorting Algorithms II', readings: 'Ch. 8-9', assignments: ['PS 5', 'Lab 4'] },
            { week: 8, topic: 'Binary Search Trees', readings: 'Ch. 12', assignments: ['PS 6', 'Lab 5'] },
            { week: 9, topic: 'Balanced Trees (AVL, Red-Black)', readings: 'Ch. 13', assignments: ['Project 2'] },
            { week: 10, topic: 'Hash Tables', readings: 'Ch. 11', assignments: ['PS 7', 'Lab 6'] },
            { week: 11, topic: 'Heaps and Priority Queues', readings: 'Ch. 6', assignments: ['PS 8', 'Lab 7'] },
            { week: 12, topic: 'Graph Representations', readings: 'Ch. 22', assignments: ['Midterm 2'] },
            { week: 13, topic: 'Graph Algorithms: BFS/DFS', readings: 'Ch. 22', assignments: ['PS 9', 'Lab 8'] },
            { week: 14, topic: 'Shortest Path Algorithms', readings: 'Ch. 24', assignments: ['PS 10', 'Lab 9'] },
            { week: 15, topic: 'Dynamic Programming', readings: 'Ch. 15', assignments: ['Final Project'] },
            { week: 16, topic: 'Final Exam', readings: 'Comprehensive', assignments: ['Final Exam'] }
        ]
    }
};

// Function to add syllabus links to existing course catalogs
function enrichCourseWithSyllabus(course, majorId) {
    return {
        ...course,
        syllabusUrl: generateSyllabusLink(course.id, majorId),
        syllabusAvailable: true,
        syllabusFormat: 'PDF',
        lastUpdated: '2024-01',
        syllabusComponents: {
            hasLearningObjectives: true,
            hasWeeklySchedule: true,
            hasGradingRubric: true,
            hasTextbooks: true,
            hasPolicies: true,
            hasOfficeHours: true
        }
    };
}

// Enhanced course display with syllabus link
function displayCourseWithSyllabus(course) {
    return `
        <div class="course-card" style="border: 1px solid #ddd; padding: 1rem; margin-bottom: 1rem; border-radius: 8px;">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div style="flex: 1;">
                    <h4>${course.id}: ${course.name}</h4>
                    <p style="color: #666;">${course.description}</p>
                    <div style="margin-top: 0.5rem;">
                        <span class="badge" style="background: #f0f0f0; padding: 0.25rem 0.5rem; margin-right: 0.5rem;">
                            ${course.credits} credits
                        </span>
                        <span class="badge" style="background: #e8f4f8; padding: 0.25rem 0.5rem;">
                            ${course.level}
                        </span>
                    </div>
                    ${course.prerequisites.length > 0 ? 
                        `<p style="margin-top: 0.5rem; font-size: 0.9rem; color: #ff9800;">
                            Prerequisites: ${course.prerequisites.join(', ')}
                        </p>` : ''}
                </div>
                <div style="text-align: right;">
                    <a href="${course.syllabusUrl}" 
                       target="_blank" 
                       class="syllabus-link" 
                       style="display: inline-block; padding: 0.5rem 1rem; background: #667eea; color: white; 
                              text-decoration: none; border-radius: 4px; font-size: 0.9rem;">
                        <i class="fas fa-file-pdf"></i> View Syllabus
                    </a>
                    <div style="margin-top: 0.5rem; font-size: 0.8rem; color: #999;">
                        Updated: ${course.lastUpdated}
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Generate syllabus preview modal
function showSyllabusPreview(courseId, majorId) {
    const syllabus = getSyllabusData(courseId, majorId);
    
    return `
        <div class="syllabus-modal" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; 
                                          background: rgba(0,0,0,0.5); display: flex; 
                                          align-items: center; justify-content: center; z-index: 1000;">
            <div style="background: white; padding: 2rem; border-radius: 12px; max-width: 800px; 
                        max-height: 80vh; overflow-y: auto; width: 90%;">
                <h2>${syllabus.courseId}: ${syllabus.courseName}</h2>
                <p style="color: #666; margin-bottom: 1rem;">${syllabus.credits} Credit Hours</p>
                
                <h3>Course Description</h3>
                <p>${syllabus.courseDescription}</p>
                
                <h3>Learning Objectives</h3>
                <ul>
                    ${syllabus.learningObjectives.map(obj => `<li>${obj}</li>`).join('')}
                </ul>
                
                <h3>Prerequisites</h3>
                <p>${syllabus.prerequisites.join(', ') || 'None'}</p>
                
                <h3>Required Textbooks</h3>
                ${syllabus.requiredTextbooks.map(book => `
                    <div style="margin-bottom: 1rem;">
                        <strong>${book.title}</strong><br>
                        Authors: ${book.authors}<br>
                        Edition: ${book.edition} | ISBN: ${book.isbn}
                    </div>
                `).join('')}
                
                <h3>Grading Breakdown</h3>
                <table style="width: 100%; border-collapse: collapse;">
                    ${Object.entries(syllabus.gradingBreakdown).map(([component, weight]) => `
                        <tr>
                            <td style="padding: 0.5rem; border-bottom: 1px solid #eee;">${component}</td>
                            <td style="padding: 0.5rem; border-bottom: 1px solid #eee; text-align: right;">${weight}%</td>
                        </tr>
                    `).join('')}
                </table>
                
                <h3>Weekly Schedule</h3>
                <div style="max-height: 300px; overflow-y: auto;">
                    ${syllabus.weeklySchedule.map(week => `
                        <div style="margin-bottom: 1rem; padding: 0.5rem; background: #f9f9f9; border-radius: 4px;">
                            <strong>Week ${week.week}: ${week.topic}</strong><br>
                            Readings: ${week.readings}<br>
                            Assignments: ${week.assignments.join(', ')}
                        </div>
                    `).join('')}
                </div>
                
                <div style="margin-top: 2rem; text-align: center;">
                    <a href="${syllabus.syllabusUrl}" 
                       class="btn btn-primary" 
                       style="padding: 0.75rem 1.5rem; background: #667eea; color: white; 
                              text-decoration: none; border-radius: 6px; display: inline-block;">
                        <i class="fas fa-download"></i> Download Full Syllabus (PDF)
                    </a>
                    <button onclick="closeSyllabusModal()" 
                            style="margin-left: 1rem; padding: 0.75rem 1.5rem; background: #f0f0f0; 
                                   border: none; border-radius: 6px; cursor: pointer;">
                        Close
                    </button>
                </div>
            </div>
        </div>
    `;
}

// Export syllabus system
const syllabusSystem = {
    generateSyllabusLink,
    enrichCourseWithSyllabus,
    displayCourseWithSyllabus,
    showSyllabusPreview,
    chemistrySyllabi,
    computerScienceSyllabi,
    
    // Add syllabus links to all courses in a catalog
    enrichCatalog: function(catalog, majorId) {
        return catalog.map(course => enrichCourseWithSyllabus(course, majorId));
    },
    
    // Get syllabus data for a specific course
    getSyllabus: function(courseId, majorId) {
        // Check if detailed syllabus exists
        const syllabusData = {
            chemistry: chemistrySyllabi,
            cs: computerScienceSyllabi
        };
        
        if (syllabusData[majorId] && syllabusData[majorId][courseId]) {
            return syllabusData[majorId][courseId];
        }
        
        // Return basic syllabus link
        return {
            courseId,
            syllabusUrl: generateSyllabusLink(courseId, majorId),
            available: true
        };
    }
};

console.log('Course Syllabus System Loaded');
console.log('Syllabus links available for all courses');
console.log('Detailed syllabi available for:', Object.keys(chemistrySyllabi).length + Object.keys(computerScienceSyllabi).length, 'courses');