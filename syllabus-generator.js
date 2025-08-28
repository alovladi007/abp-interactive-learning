// Syllabus Generator - Creates actual syllabus content for all courses

// Complete syllabus database for all courses
const syllabusDatabase = {
    // Chemistry courses
    'CHEM101': {
        courseId: 'CHEM101',
        courseName: 'General Chemistry I',
        credits: 4,
        instructor: 'Dr. Sarah Johnson',
        email: 'sjohnson@university.edu',
        officeHours: 'MWF 2:00-3:00 PM, Science Building 302',
        meetingTime: 'MWF 10:00-10:50 AM, Lab: T 2:00-5:00 PM',
        location: 'Chemistry Building 101',
        
        description: 'Introduction to chemical principles including atomic structure, chemical bonding, stoichiometry, gases, thermochemistry, and periodic properties. This course provides the foundation for all advanced chemistry courses.',
        
        objectives: [
            'Understand and apply atomic structure concepts and electron configurations',
            'Master chemical nomenclature and write correct chemical formulas',
            'Perform stoichiometric calculations for chemical reactions',
            'Apply gas laws to solve real-world problems',
            'Analyze thermochemical processes and calculate energy changes',
            'Predict and explain periodic trends and properties',
            'Demonstrate safe laboratory practices and techniques',
            'Interpret experimental data and write comprehensive lab reports'
        ],
        
        prerequisites: 'High school chemistry and MATH 101 (may be taken concurrently)',
        
        textbooks: [
            {
                title: 'Chemistry: The Central Science',
                authors: 'Brown, LeMay, Bursten, Murphy, Woodward',
                edition: '14th Edition',
                isbn: '978-0134414232',
                required: true,
                price: '$325'
            },
            {
                title: 'General Chemistry Laboratory Manual',
                authors: 'University Chemistry Department',
                edition: '2024 Edition',
                required: true,
                price: '$45'
            }
        ],
        
        gradingBreakdown: {
            'Midterm Exams (2)': 30,
            'Final Exam': 20,
            'Laboratory': 25,
            'Problem Sets': 15,
            'Quizzes': 5,
            'Participation': 5
        },
        
        weeklySchedule: [
            { week: 1, topic: 'Introduction to Chemistry & Measurement', reading: 'Chapter 1', assignments: 'Problem Set 1, Safety Quiz' },
            { week: 2, topic: 'Atoms, Molecules, and Ions', reading: 'Chapter 2', assignments: 'Problem Set 2, Lab 1: Basic Techniques' },
            { week: 3, topic: 'Stoichiometry: Calculations with Chemical Formulas', reading: 'Chapter 3', assignments: 'Problem Set 3, Lab 2: Stoichiometry' },
            { week: 4, topic: 'Reactions in Aqueous Solutions', reading: 'Chapter 4', assignments: 'Problem Set 4, Lab 3: Titration' },
            { week: 5, topic: 'Thermochemistry', reading: 'Chapter 5', assignments: 'Problem Set 5, Quiz 1' },
            { week: 6, topic: 'Review and Midterm Exam 1', reading: 'Chapters 1-5', assignments: 'Midterm Exam 1' },
            { week: 7, topic: 'Electronic Structure of Atoms', reading: 'Chapter 6', assignments: 'Problem Set 6, Lab 4: Spectroscopy' },
            { week: 8, topic: 'Periodic Properties of Elements', reading: 'Chapter 7', assignments: 'Problem Set 7, Lab 5: Periodic Trends' },
            { week: 9, topic: 'Basic Concepts of Chemical Bonding', reading: 'Chapter 8', assignments: 'Problem Set 8, Quiz 2' },
            { week: 10, topic: 'Molecular Geometry and Bonding Theories', reading: 'Chapter 9', assignments: 'Problem Set 9, Lab 6: Molecular Models' },
            { week: 11, topic: 'Gases', reading: 'Chapter 10', assignments: 'Problem Set 10, Lab 7: Gas Laws' },
            { week: 12, topic: 'Review and Midterm Exam 2', reading: 'Chapters 6-10', assignments: 'Midterm Exam 2' },
            { week: 13, topic: 'Intermolecular Forces, Liquids, and Solids', reading: 'Chapter 11', assignments: 'Problem Set 11, Lab 8: Crystal Structures' },
            { week: 14, topic: 'Properties of Solutions', reading: 'Chapter 13', assignments: 'Problem Set 12, Quiz 3' },
            { week: 15, topic: 'Chemical Kinetics (Introduction)', reading: 'Chapter 14.1-14.3', assignments: 'Final Project Presentations' },
            { week: 16, topic: 'Final Exam Week', reading: 'Comprehensive Review', assignments: 'Final Exam' }
        ]
    },
    
    'CS101': {
        courseId: 'CS101',
        courseName: 'Introduction to Programming',
        credits: 4,
        instructor: 'Prof. Michael Chen',
        email: 'mchen@university.edu',
        officeHours: 'TTh 3:00-5:00 PM, Computer Science Building 215',
        meetingTime: 'TTh 10:30 AM-12:00 PM',
        location: 'Computer Science Building 110',
        
        description: 'Introduction to programming concepts using Python. Topics include variables, control structures, functions, data structures, object-oriented programming, and algorithm development. No prior programming experience required.',
        
        objectives: [
            'Write, test, and debug Python programs independently',
            'Use fundamental programming constructs including loops, conditionals, and functions',
            'Implement and use basic data structures (lists, dictionaries, sets)',
            'Apply object-oriented programming principles to solve problems',
            'Develop algorithms to solve computational problems',
            'Follow software development best practices including documentation and testing',
            'Collaborate on programming projects using version control (Git)',
            'Analyze the efficiency of simple algorithms'
        ],
        
        prerequisites: 'None',
        
        textbooks: [
            {
                title: 'Introduction to Computing Using Python',
                authors: 'Ljubomir Perkovic',
                edition: '3rd Edition',
                isbn: '978-1119498537',
                required: true,
                price: '$145'
            },
            {
                title: 'Python Documentation',
                authors: 'Python Software Foundation',
                edition: 'Online',
                required: false,
                price: 'Free',
                url: 'https://docs.python.org'
            }
        ],
        
        gradingBreakdown: {
            'Programming Projects (3)': 30,
            'Homework Assignments': 20,
            'Lab Exercises': 15,
            'Midterm Exam': 15,
            'Final Exam': 15,
            'Class Participation': 5
        },
        
        weeklySchedule: [
            { week: 1, topic: 'Introduction to Computing and Python', reading: 'Chapter 1', assignments: 'Lab 1: Setup, HW 1: First Program' },
            { week: 2, topic: 'Variables, Expressions, and Statements', reading: 'Chapter 2', assignments: 'Lab 2: Variables, HW 2: Calculations' },
            { week: 3, topic: 'Conditional Execution (if/else)', reading: 'Chapter 3.1-3.3', assignments: 'Lab 3: Conditionals, HW 3: Decision Making' },
            { week: 4, topic: 'Iteration (Loops)', reading: 'Chapter 3.4-3.6', assignments: 'Lab 4: Loops, Project 1 Assigned' },
            { week: 5, topic: 'Functions', reading: 'Chapter 4', assignments: 'Lab 5: Functions, HW 4: Function Design' },
            { week: 6, topic: 'Lists and Tuples', reading: 'Chapter 5', assignments: 'Project 1 Due, Midterm Exam' },
            { week: 7, topic: 'String Processing', reading: 'Chapter 6', assignments: 'Lab 6: Strings, HW 5: Text Processing' },
            { week: 8, topic: 'Dictionaries and Sets', reading: 'Chapter 7', assignments: 'Lab 7: Dictionaries, Project 2 Assigned' },
            { week: 9, topic: 'File Input/Output', reading: 'Chapter 8', assignments: 'Lab 8: Files, HW 6: File Processing' },
            { week: 10, topic: 'Exception Handling and Debugging', reading: 'Chapter 9', assignments: 'Lab 9: Exceptions, HW 7: Error Handling' },
            { week: 11, topic: 'Object-Oriented Programming I', reading: 'Chapter 10', assignments: 'Project 2 Due, Lab 10: Classes' },
            { week: 12, topic: 'Object-Oriented Programming II', reading: 'Chapter 11', assignments: 'Lab 11: Inheritance, Project 3 Assigned' },
            { week: 13, topic: 'Recursion', reading: 'Chapter 12', assignments: 'Lab 12: Recursion, HW 8: Recursive Solutions' },
            { week: 14, topic: 'Algorithm Analysis', reading: 'Chapter 13', assignments: 'Lab 13: Complexity, HW 9: Big-O' },
            { week: 15, topic: 'Advanced Topics and Review', reading: 'Selected Topics', assignments: 'Project 3 Due, Final Review' },
            { week: 16, topic: 'Final Exam Week', reading: 'Comprehensive Review', assignments: 'Final Exam' }
        ]
    },
    
    'MATH101': {
        courseId: 'MATH101',
        courseName: 'Calculus I',
        credits: 4,
        instructor: 'Dr. Emily Rodriguez',
        email: 'erodriguez@university.edu',
        officeHours: 'MWF 1:00-2:30 PM, Mathematics Building 412',
        meetingTime: 'MWF 9:00-9:50 AM, Th 9:00-9:50 AM (Recitation)',
        location: 'Mathematics Building 201',
        
        description: 'Introduction to differential and integral calculus. Topics include limits, derivatives, applications of derivatives, definite and indefinite integrals, and the Fundamental Theorem of Calculus.',
        
        objectives: [
            'Evaluate limits using various techniques',
            'Compute derivatives using differentiation rules',
            'Apply derivatives to solve optimization problems',
            'Understand and use the Mean Value Theorem',
            'Evaluate definite and indefinite integrals',
            'Apply integration to find areas and volumes',
            'Model real-world problems using calculus',
            'Communicate mathematical ideas clearly'
        ],
        
        prerequisites: 'Pre-calculus or placement exam',
        
        textbooks: [
            {
                title: 'Calculus: Early Transcendentals',
                authors: 'James Stewart',
                edition: '8th Edition',
                isbn: '978-1285741550',
                required: true,
                price: '$290'
            }
        ],
        
        gradingBreakdown: {
            'Midterm Exams (3)': 45,
            'Final Exam': 25,
            'Homework': 15,
            'Quizzes': 10,
            'Participation': 5
        },
        
        weeklySchedule: [
            { week: 1, topic: 'Review of Functions and Introduction to Limits', reading: 'Sections 1.1-2.2', assignments: 'HW 1: Functions and Limits' },
            { week: 2, topic: 'Limit Laws and Continuity', reading: 'Sections 2.3-2.5', assignments: 'HW 2: Limit Calculations, Quiz 1' },
            { week: 3, topic: 'Derivatives and Rates of Change', reading: 'Sections 2.6-2.8', assignments: 'HW 3: Introduction to Derivatives' },
            { week: 4, topic: 'Differentiation Rules', reading: 'Sections 3.1-3.4', assignments: 'HW 4: Differentiation, Quiz 2' },
            { week: 5, topic: 'Chain Rule and Implicit Differentiation', reading: 'Sections 3.5-3.6', assignments: 'HW 5: Chain Rule, Exam 1' },
            { week: 6, topic: 'Related Rates and Linear Approximation', reading: 'Sections 3.9-3.10', assignments: 'HW 6: Applications' },
            { week: 7, topic: 'Maximum and Minimum Values', reading: 'Sections 4.1-4.3', assignments: 'HW 7: Optimization, Quiz 3' },
            { week: 8, topic: 'Mean Value Theorem and Curve Sketching', reading: 'Sections 4.2, 4.5', assignments: 'HW 8: Graphing' },
            { week: 9, topic: 'Optimization Problems', reading: 'Section 4.7', assignments: 'HW 9: Optimization, Exam 2' },
            { week: 10, topic: 'Antiderivatives', reading: 'Section 4.9', assignments: 'HW 10: Antiderivatives' },
            { week: 11, topic: 'The Definite Integral', reading: 'Sections 5.1-5.3', assignments: 'HW 11: Definite Integrals, Quiz 4' },
            { week: 12, topic: 'Fundamental Theorem of Calculus', reading: 'Sections 5.4-5.5', assignments: 'HW 12: FTC' },
            { week: 13, topic: 'Substitution Rule', reading: 'Section 5.5', assignments: 'HW 13: Integration, Exam 3' },
            { week: 14, topic: 'Areas Between Curves', reading: 'Section 6.1', assignments: 'HW 14: Applications of Integration' },
            { week: 15, topic: 'Volumes', reading: 'Sections 6.2-6.3', assignments: 'HW 15: Volumes, Review' },
            { week: 16, topic: 'Final Exam Week', reading: 'Comprehensive Review', assignments: 'Final Exam' }
        ]
    }
};

// Function to generate syllabus HTML
function generateSyllabusHTML(courseId) {
    // Try to get syllabus from database
    let syllabus = syllabusDatabase[courseId];
    
    // If not found, generate a generic syllabus
    if (!syllabus) {
        syllabus = generateGenericSyllabus(courseId);
    }
    
    // Populate the HTML
    document.getElementById('course-title').textContent = `${syllabus.courseId}: ${syllabus.courseName}`;
    document.getElementById('course-subtitle').innerHTML = `
        <div style="opacity: 0.9; margin-top: 0.5rem;">
            ${syllabus.credits} Credit Hours | ${syllabus.instructor || 'TBD'}
        </div>
    `;
    
    document.getElementById('course-meta').innerHTML = `
        <div>
            <strong>Meeting Time:</strong><br>
            ${syllabus.meetingTime || 'TBD'}
        </div>
        <div>
            <strong>Location:</strong><br>
            ${syllabus.location || 'TBD'}
        </div>
        <div>
            <strong>Instructor Email:</strong><br>
            ${syllabus.email || 'instructor@university.edu'}
        </div>
    `;
    
    document.getElementById('course-description').textContent = syllabus.description;
    
    // Learning objectives
    const objectivesList = document.getElementById('learning-objectives');
    objectivesList.innerHTML = syllabus.objectives.map(obj => `<li>${obj}</li>`).join('');
    
    // Prerequisites
    document.getElementById('prerequisites').textContent = syllabus.prerequisites || 'None';
    
    // Textbooks
    const textbooksDiv = document.getElementById('textbooks');
    textbooksDiv.innerHTML = syllabus.textbooks.map(book => `
        <div class="textbook-card">
            <strong>${book.title}</strong> ${book.required ? '<span class="badge">Required</span>' : '<span class="badge" style="background: #718096;">Optional</span>'}<br>
            Authors: ${book.authors}<br>
            Edition: ${book.edition} | ISBN: ${book.isbn}<br>
            ${book.price ? `Approximate Price: ${book.price}` : ''}
            ${book.url ? `<br><a href="${book.url}" target="_blank" style="color: var(--primary-color);">Access Online</a>` : ''}
        </div>
    `).join('');
    
    // Grading breakdown
    const gradingBody = document.getElementById('grading-breakdown');
    gradingBody.innerHTML = Object.entries(syllabus.gradingBreakdown).map(([component, weight]) => `
        <tr>
            <td>${component}</td>
            <td>${weight}%</td>
        </tr>
    `).join('');
    
    // Weekly schedule
    const scheduleDiv = document.getElementById('weekly-schedule');
    scheduleDiv.innerHTML = syllabus.weeklySchedule.map(week => `
        <div class="week-card">
            <h4>Week ${week.week}: ${week.topic}</h4>
            <p><strong>Reading:</strong> ${week.reading}</p>
            <p><strong>Assignments:</strong> ${week.assignments}</p>
        </div>
    `).join('');
    
    // Office hours
    document.getElementById('office-hours').textContent = syllabus.officeHours || 'By appointment';
}

// Generate generic syllabus for courses not in database
function generateGenericSyllabus(courseId) {
    const majorPrefix = courseId.match(/^[A-Z]+/)[0];
    const courseNumber = courseId.match(/\d+/)[0];
    const level = parseInt(courseNumber[0]);
    
    const levelNames = {
        1: 'Introduction to',
        2: 'Intermediate',
        3: 'Advanced',
        4: 'Special Topics in'
    };
    
    const majorNames = {
        'CS': 'Computer Science',
        'CHEM': 'Chemistry',
        'PHYS': 'Physics',
        'MATH': 'Mathematics',
        'BIO': 'Biology',
        'EE': 'Electrical Engineering',
        'ME': 'Mechanical Engineering',
        'CE': 'Civil Engineering',
        'ENV': 'Environmental Science',
        'ECON': 'Economics',
        'PSY': 'Psychology',
        'POL': 'Political Science',
        'NURS': 'Nursing',
        'MED': 'Medicine',
        'PHAR': 'Pharmacy'
    };
    
    const courseName = `${levelNames[level] || 'Topics in'} ${majorNames[majorPrefix] || majorPrefix}`;
    
    return {
        courseId: courseId,
        courseName: courseName,
        credits: level >= 3 ? 3 : 4,
        instructor: 'Dr. Faculty Member',
        email: 'instructor@university.edu',
        officeHours: 'TBD',
        meetingTime: 'TBD',
        location: 'TBD',
        
        description: `This course covers ${level >= 3 ? 'advanced' : 'fundamental'} topics in ${majorNames[majorPrefix] || majorPrefix}. Students will develop theoretical understanding and practical skills relevant to the field.`,
        
        objectives: [
            `Master fundamental concepts in ${majorNames[majorPrefix] || majorPrefix}`,
            'Apply theoretical knowledge to solve practical problems',
            'Develop critical thinking and analytical skills',
            'Communicate ideas effectively in written and oral form',
            'Work collaboratively on projects and assignments',
            'Demonstrate professional and ethical behavior'
        ],
        
        prerequisites: level > 1 ? `${majorPrefix}${(level-1)}01 or instructor permission` : 'None',
        
        textbooks: [
            {
                title: `${courseName} Textbook`,
                authors: 'Various Authors',
                edition: 'Latest Edition',
                isbn: 'TBD',
                required: true,
                price: 'TBD'
            }
        ],
        
        gradingBreakdown: {
            'Exams': 40,
            'Assignments': 25,
            'Projects': 20,
            'Participation': 10,
            'Quizzes': 5
        },
        
        weeklySchedule: Array.from({length: 16}, (_, i) => ({
            week: i + 1,
            topic: i === 15 ? 'Final Exam Week' : i === 7 ? 'Midterm Exam' : `Week ${i + 1} Topics`,
            reading: i === 15 ? 'Comprehensive Review' : `Chapter ${i + 1}`,
            assignments: i === 7 ? 'Midterm Exam' : i === 15 ? 'Final Exam' : `Assignment ${i + 1}`
        }))
    };
}

// Get course ID from URL parameters
function getCourseIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('course') || 'CS101';
}

// Load syllabus on page load
document.addEventListener('DOMContentLoaded', function() {
    const courseId = getCourseIdFromURL();
    generateSyllabusHTML(courseId);
});

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { syllabusDatabase, generateGenericSyllabus };
}