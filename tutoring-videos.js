// Tutoring Videos Management System
// Handles 20 categories with 50 videos each

// Video categories data
const videoCategories = {
    'mathematics': {
        name: 'Mathematics',
        icon: '📐',
        description: 'From basic arithmetic to advanced calculus and statistics',
        totalVideos: 50,
        videos: generateVideoPlaceholders('Mathematics', 50)
    },
    'computer-science': {
        name: 'Computer Science',
        icon: '💻',
        description: 'Programming, algorithms, AI, and software development',
        totalVideos: 50,
        videos: generateVideoPlaceholders('Computer Science', 50)
    },
    'physics': {
        name: 'Physics',
        icon: '⚛️',
        description: 'Classical mechanics, quantum physics, and relativity',
        totalVideos: 50,
        videos: generateVideoPlaceholders('Physics', 50)
    },
    'chemistry': {
        name: 'Chemistry',
        icon: '🧪',
        description: 'Organic, inorganic, physical chemistry and lab techniques',
        totalVideos: 50,
        videos: generateVideoPlaceholders('Chemistry', 50)
    },
    'biology': {
        name: 'Biology',
        icon: '🧬',
        description: 'Cell biology, genetics, ecology, and human anatomy',
        totalVideos: 50,
        videos: generateVideoPlaceholders('Biology', 50)
    },
    'engineering': {
        name: 'Engineering',
        icon: '⚙️',
        description: 'Electrical, mechanical, civil, and software engineering',
        totalVideos: 50,
        videos: generateVideoPlaceholders('Engineering', 50)
    },
    'business': {
        name: 'Business & Economics',
        icon: '📊',
        description: 'Finance, marketing, management, and economic theory',
        totalVideos: 50,
        videos: generateVideoPlaceholders('Business', 50)
    },
    'medicine': {
        name: 'Medicine & Health',
        icon: '⚕️',
        description: 'Medical sciences, nursing, public health, and anatomy',
        totalVideos: 50,
        videos: generateVideoPlaceholders('Medicine', 50)
    },
    'psychology': {
        name: 'Psychology',
        icon: '🧠',
        description: 'Cognitive, clinical, social, and developmental psychology',
        totalVideos: 50,
        videos: generateVideoPlaceholders('Psychology', 50)
    },
    'language': {
        name: 'Language & Literature',
        icon: '📚',
        description: 'English, foreign languages, writing, and literary analysis',
        totalVideos: 50,
        videos: generateVideoPlaceholders('Language', 50)
    },
    'history': {
        name: 'History',
        icon: '📜',
        description: 'World history, American history, and historical analysis',
        totalVideos: 50,
        videos: generateVideoPlaceholders('History', 50)
    },
    'art': {
        name: 'Art & Design',
        icon: '🎨',
        description: 'Drawing, painting, graphic design, and art history',
        totalVideos: 50,
        videos: generateVideoPlaceholders('Art & Design', 50)
    },
    'music': {
        name: 'Music',
        icon: '🎵',
        description: 'Music theory, instruments, composition, and performance',
        totalVideos: 50,
        videos: generateVideoPlaceholders('Music', 50)
    },
    'philosophy': {
        name: 'Philosophy',
        icon: '💭',
        description: 'Ethics, logic, metaphysics, and philosophical thinking',
        totalVideos: 50,
        videos: generateVideoPlaceholders('Philosophy', 50)
    },
    'law': {
        name: 'Law',
        icon: '⚖️',
        description: 'Constitutional law, criminal law, and legal studies',
        totalVideos: 50,
        videos: generateVideoPlaceholders('Law', 50)
    },
    'environmental': {
        name: 'Environmental Science',
        icon: '🌍',
        description: 'Climate science, ecology, and sustainability',
        totalVideos: 50,
        videos: generateVideoPlaceholders('Environmental Science', 50)
    },
    'data-science': {
        name: 'Data Science',
        icon: '📈',
        description: 'Machine learning, statistics, and data analysis',
        totalVideos: 50,
        videos: generateVideoPlaceholders('Data Science', 50)
    },
    'test-prep': {
        name: 'Test Preparation',
        icon: '📝',
        description: 'SAT, ACT, GRE, GMAT, MCAT, and other standardized tests',
        totalVideos: 50,
        videos: generateVideoPlaceholders('Test Prep', 50)
    },
    'study-skills': {
        name: 'Study Skills',
        icon: '✏️',
        description: 'Note-taking, time management, and learning strategies',
        totalVideos: 50,
        videos: generateVideoPlaceholders('Study Skills', 50)
    },
    'career': {
        name: 'Career Development',
        icon: '🚀',
        description: 'Resume writing, interview skills, and professional growth',
        totalVideos: 50,
        videos: generateVideoPlaceholders('Career Development', 50)
    }
};

// Generate video placeholders for a category
function generateVideoPlaceholders(categoryName, count) {
    const videos = [];
    const topics = getTopicsForCategory(categoryName);
    const levels = ['Beginner', 'Intermediate', 'Advanced'];
    const instructors = [
        'Dr. Sarah Johnson', 'Prof. Michael Chen', 'Dr. Emily Rodriguez',
        'Prof. David Kim', 'Dr. Lisa Anderson', 'Prof. James Wilson',
        'Dr. Maria Garcia', 'Prof. Robert Brown', 'Dr. Jennifer Lee'
    ];
    
    for (let i = 1; i <= count; i++) {
        const topic = topics[Math.floor(Math.random() * topics.length)];
        const level = levels[Math.floor(Math.random() * levels.length)];
        const instructor = instructors[Math.floor(Math.random() * instructors.length)];
        const duration = Math.floor(Math.random() * 60) + 15; // 15-75 minutes
        const views = Math.floor(Math.random() * 50000) + 1000;
        const rating = (Math.random() * 2 + 3).toFixed(1); // 3.0-5.0
        
        videos.push({
            id: `${categoryName.toLowerCase().replace(/\s+/g, '-')}-video-${i}`,
            title: `${topic} - ${level} Level (Part ${i})`,
            instructor: instructor,
            duration: `${duration}:${Math.floor(Math.random() * 60).toString().padStart(2, '0')}`,
            views: views,
            rating: rating,
            level: level,
            description: `Comprehensive tutorial on ${topic} for ${level.toLowerCase()} learners. This video covers essential concepts and practical applications.`,
            thumbnail: null, // Placeholder for actual thumbnail
            uploadDate: getRandomDate(),
            isPremium: Math.random() > 0.7,
            tags: [categoryName, topic, level]
        });
    }
    
    return videos;
}

// Get topics for each category
function getTopicsForCategory(category) {
    const topicMap = {
        'Mathematics': ['Calculus', 'Linear Algebra', 'Statistics', 'Geometry', 'Trigonometry', 'Differential Equations'],
        'Computer Science': ['Python Programming', 'Data Structures', 'Algorithms', 'Machine Learning', 'Web Development', 'Databases'],
        'Physics': ['Mechanics', 'Thermodynamics', 'Electromagnetism', 'Quantum Physics', 'Optics', 'Relativity'],
        'Chemistry': ['Organic Chemistry', 'Inorganic Chemistry', 'Physical Chemistry', 'Biochemistry', 'Analytical Chemistry'],
        'Biology': ['Cell Biology', 'Genetics', 'Ecology', 'Evolution', 'Anatomy', 'Microbiology'],
        'Engineering': ['Circuit Analysis', 'Thermodynamics', 'Fluid Mechanics', 'Materials Science', 'Control Systems'],
        'Business': ['Finance', 'Marketing', 'Management', 'Accounting', 'Economics', 'Entrepreneurship'],
        'Medicine': ['Anatomy', 'Physiology', 'Pathology', 'Pharmacology', 'Clinical Medicine', 'Public Health'],
        'Psychology': ['Cognitive Psychology', 'Social Psychology', 'Clinical Psychology', 'Developmental Psychology', 'Neuroscience'],
        'Language': ['Grammar', 'Writing', 'Literature Analysis', 'Creative Writing', 'Public Speaking', 'Foreign Languages'],
        'History': ['Ancient History', 'Medieval History', 'Modern History', 'American History', 'World Wars', 'Cultural History'],
        'Art & Design': ['Drawing', 'Painting', 'Digital Art', 'Graphic Design', 'Art History', '3D Modeling'],
        'Music': ['Music Theory', 'Piano', 'Guitar', 'Composition', 'Music Production', 'Music History'],
        'Philosophy': ['Ethics', 'Logic', 'Metaphysics', 'Political Philosophy', 'Philosophy of Mind', 'Existentialism'],
        'Law': ['Constitutional Law', 'Criminal Law', 'Contract Law', 'Tort Law', 'International Law', 'Legal Writing'],
        'Environmental Science': ['Climate Change', 'Ecology', 'Conservation', 'Renewable Energy', 'Environmental Policy'],
        'Data Science': ['Machine Learning', 'Deep Learning', 'Data Visualization', 'Statistical Analysis', 'Big Data', 'AI'],
        'Test Prep': ['SAT Math', 'SAT Reading', 'ACT Science', 'GRE Verbal', 'GMAT Quant', 'MCAT Biology'],
        'Study Skills': ['Note Taking', 'Time Management', 'Memory Techniques', 'Speed Reading', 'Test Taking', 'Research Skills'],
        'Career Development': ['Resume Writing', 'Interview Skills', 'Networking', 'Leadership', 'Communication', 'Project Management']
    };
    
    return topicMap[category] || ['General Topics'];
}

// Get random date for upload
function getRandomDate() {
    const start = new Date(2023, 0, 1);
    const end = new Date();
    return new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
}

// Format number for display
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

// Format date for display
function formatDate(date) {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return `${months[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;
}

// State management
let currentCategory = null;
let currentPage = 1;
const videosPerPage = 12;

// Show category videos
function showCategoryVideos(categoryId) {
    currentCategory = categoryId;
    currentPage = 1;
    
    const category = videoCategories[categoryId];
    if (!category) return;
    
    // Hide categories, show videos
    document.getElementById('categories-section').style.display = 'none';
    document.getElementById('videos-section').classList.add('active');
    
    // Update title
    document.getElementById('category-title').innerHTML = `
        <i class="fas fa-folder-open"></i> ${category.name} Videos
    `;
    
    // Display videos
    displayVideos();
}

// Display videos for current page
function displayVideos() {
    const category = videoCategories[currentCategory];
    if (!category) return;
    
    const startIndex = (currentPage - 1) * videosPerPage;
    const endIndex = startIndex + videosPerPage;
    const videosToShow = category.videos.slice(startIndex, endIndex);
    
    const videosGrid = document.getElementById('videos-grid');
    videosGrid.innerHTML = videosToShow.map(video => `
        <div class="video-card" onclick="playVideo('${video.id}')">
            <div class="video-thumbnail">
                <i class="fas fa-play-circle"></i>
                <span class="video-duration">${video.duration}</span>
                ${video.isPremium ? '<span class="premium-badge">Premium</span>' : ''}
            </div>
            <div class="video-info">
                <h4 class="video-title">${video.title}</h4>
                <p class="video-instructor">${video.instructor}</p>
                <div class="video-meta">
                    <span class="video-views">
                        <i class="fas fa-eye"></i> ${formatNumber(video.views)}
                    </span>
                    <span class="video-rating">
                        <i class="fas fa-star"></i> ${video.rating}
                    </span>
                </div>
            </div>
        </div>
    `).join('');
    
    // Update pagination
    updatePagination();
}

// Update pagination controls
function updatePagination() {
    const category = videoCategories[currentCategory];
    if (!category) return;
    
    const totalPages = Math.ceil(category.videos.length / videosPerPage);
    const pageNumbers = document.getElementById('page-numbers');
    
    let paginationHTML = '';
    for (let i = 1; i <= totalPages; i++) {
        if (i === 1 || i === totalPages || (i >= currentPage - 2 && i <= currentPage + 2)) {
            paginationHTML += `
                <button class="page-btn ${i === currentPage ? 'active' : ''}" 
                        onclick="goToPage(${i})">${i}</button>
            `;
        } else if (i === currentPage - 3 || i === currentPage + 3) {
            paginationHTML += '<span style="color: var(--text-secondary);">...</span>';
        }
    }
    
    pageNumbers.innerHTML = paginationHTML;
}

// Change page
function changePage(direction) {
    const category = videoCategories[currentCategory];
    if (!category) return;
    
    const totalPages = Math.ceil(category.videos.length / videosPerPage);
    const newPage = currentPage + direction;
    
    if (newPage >= 1 && newPage <= totalPages) {
        currentPage = newPage;
        displayVideos();
        window.scrollTo(0, 0);
    }
}

// Go to specific page
function goToPage(page) {
    currentPage = page;
    displayVideos();
    window.scrollTo(0, 0);
}

// Show categories
function showCategories() {
    document.getElementById('categories-section').style.display = 'block';
    document.getElementById('videos-section').classList.remove('active');
    currentCategory = null;
    currentPage = 1;
}

// Play video (placeholder function)
function playVideo(videoId) {
    // Find the video
    let video = null;
    for (const category of Object.values(videoCategories)) {
        video = category.videos.find(v => v.id === videoId);
        if (video) break;
    }
    
    if (video) {
        alert(`Playing: ${video.title}\nInstructor: ${video.instructor}\nDuration: ${video.duration}\n\nNote: This is a placeholder. In production, this would open a video player.`);
    }
}

// Search functionality
function searchVideos(query) {
    if (!query) {
        showCategories();
        return;
    }
    
    const results = [];
    
    // Search through all categories
    for (const [categoryId, category] of Object.entries(videoCategories)) {
        for (const video of category.videos) {
            if (video.title.toLowerCase().includes(query.toLowerCase()) ||
                video.instructor.toLowerCase().includes(query.toLowerCase()) ||
                video.tags.some(tag => tag.toLowerCase().includes(query.toLowerCase()))) {
                results.push({...video, category: category.name});
            }
        }
    }
    
    // Display search results
    if (results.length > 0) {
        displaySearchResults(results);
    } else {
        displayNoResults(query);
    }
}

// Display search results
function displaySearchResults(results) {
    document.getElementById('categories-section').style.display = 'none';
    document.getElementById('videos-section').classList.add('active');
    
    document.getElementById('category-title').innerHTML = `
        <i class="fas fa-search"></i> Search Results (${results.length} videos found)
    `;
    
    const videosGrid = document.getElementById('videos-grid');
    videosGrid.innerHTML = results.slice(0, 24).map(video => `
        <div class="video-card" onclick="playVideo('${video.id}')">
            <div class="video-thumbnail">
                <i class="fas fa-play-circle"></i>
                <span class="video-duration">${video.duration}</span>
                <span class="category-badge">${video.category}</span>
            </div>
            <div class="video-info">
                <h4 class="video-title">${video.title}</h4>
                <p class="video-instructor">${video.instructor}</p>
                <div class="video-meta">
                    <span class="video-views">
                        <i class="fas fa-eye"></i> ${formatNumber(video.views)}
                    </span>
                    <span class="video-rating">
                        <i class="fas fa-star"></i> ${video.rating}
                    </span>
                </div>
            </div>
        </div>
    `).join('');
    
    // Hide pagination for search results
    document.querySelector('.pagination').style.display = 'none';
}

// Display no results message
function displayNoResults(query) {
    document.getElementById('categories-section').style.display = 'none';
    document.getElementById('videos-section').classList.add('active');
    
    document.getElementById('category-title').innerHTML = `
        <i class="fas fa-search"></i> No results found for "${query}"
    `;
    
    document.getElementById('videos-grid').innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 3rem;">
            <i class="fas fa-search" style="font-size: 3rem; color: var(--text-secondary); margin-bottom: 1rem;"></i>
            <p style="color: var(--text-secondary);">Try searching with different keywords or browse categories below.</p>
        </div>
    `;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Set up search
    const searchInput = document.querySelector('.search-input');
    const searchBtn = document.querySelector('.search-btn');
    
    if (searchInput && searchBtn) {
        searchBtn.addEventListener('click', () => searchVideos(searchInput.value));
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') searchVideos(searchInput.value);
        });
    }
    
    // Set up filter tags
    const filterTags = document.querySelectorAll('.filter-tag');
    filterTags.forEach(tag => {
        tag.addEventListener('click', function() {
            filterTags.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            // Apply filter logic here
            const filter = this.textContent.trim();
            console.log('Filter applied:', filter);
        });
    });
    
    // Initialize stats
    updateStats();
});

// Update statistics
function updateStats() {
    let totalVideos = 0;
    let totalHours = 0;
    
    for (const category of Object.values(videoCategories)) {
        totalVideos += category.videos.length;
        category.videos.forEach(video => {
            const [minutes] = video.duration.split(':').map(Number);
            totalHours += minutes / 60;
        });
    }
    
    // Update stat displays if they exist
    const videoStat = document.querySelector('.stat-value:nth-of-type(2)');
    const hourStat = document.querySelector('.stat-value:nth-of-type(3)');
    
    if (videoStat) videoStat.textContent = totalVideos.toString();
    if (hourStat) hourStat.textContent = Math.round(totalHours).toString() + '+';
}

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        videoCategories,
        showCategoryVideos,
        searchVideos
    };
}