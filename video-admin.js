// Video Admin Dashboard JavaScript
const API_BASE_URL = 'http://localhost:8001';

// State
let selectedFile = null;
let videos = [];

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    loadStatistics();
    loadVideos();
    loadPlaceholders();
});

// Setup event listeners
function setupEventListeners() {
    // Upload area
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('videoFile');
    
    uploadArea.addEventListener('click', () => fileInput.click());
    
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });
    
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });
    
    // Upload form
    const uploadForm = document.getElementById('uploadForm');
    uploadForm.addEventListener('submit', handleUpload);
    
    // Search
    const searchInput = document.getElementById('searchVideos');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            filterVideos(e.target.value);
        });
    }
}

// Handle file selection
function handleFileSelect(file) {
    const allowedTypes = ['video/mp4', 'video/webm', 'video/ogg', 'video/quicktime', 'video/x-msvideo', 'video/x-matroska'];
    const maxSize = 500 * 1024 * 1024; // 500MB
    
    if (!allowedTypes.includes(file.type) && !file.name.match(/\.(mp4|webm|ogg|mov|avi|mkv)$/i)) {
        showAlert('Invalid file type. Please select a video file.', 'error');
        return;
    }
    
    if (file.size > maxSize) {
        showAlert('File size exceeds 500MB limit.', 'error');
        return;
    }
    
    selectedFile = file;
    
    // Update upload area
    const uploadArea = document.getElementById('uploadArea');
    uploadArea.innerHTML = `
        <i class="fas fa-file-video" style="font-size: 3rem; color: var(--primary-accent); margin-bottom: 1rem;"></i>
        <h3 style="color: var(--text-primary); margin-bottom: 0.5rem;">${file.name}</h3>
        <p style="color: var(--text-secondary);">Size: ${formatFileSize(file.size)}</p>
        <p style="color: var(--primary-accent); margin-top: 1rem;">Click to change file</p>
    `;
}

// Handle upload
async function handleUpload(e) {
    e.preventDefault();
    
    if (!selectedFile) {
        showAlert('Please select a video file', 'error');
        return;
    }
    
    // Gather form data
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('title', document.getElementById('title').value);
    formData.append('description', document.getElementById('description').value);
    formData.append('category', document.getElementById('category').value);
    formData.append('subcategory', document.getElementById('subcategory').value);
    formData.append('instructor', document.getElementById('instructor').value);
    formData.append('level', document.getElementById('level').value);
    formData.append('is_premium', document.getElementById('isPremium').value === 'true');
    formData.append('tags', document.getElementById('tags').value);
    formData.append('topics', document.getElementById('topics').value);
    formData.append('prerequisites', document.getElementById('prerequisites').value);
    
    // Show progress
    const progressDiv = document.getElementById('uploadProgress');
    const progressFill = document.getElementById('progressFill');
    const uploadStatus = document.getElementById('uploadStatus');
    
    progressDiv.style.display = 'block';
    
    try {
        // Create XMLHttpRequest for progress tracking
        const xhr = new XMLHttpRequest();
        
        xhr.upload.addEventListener('progress', (e) => {
            if (e.lengthComputable) {
                const percentComplete = (e.loaded / e.total) * 100;
                progressFill.style.width = percentComplete + '%';
                progressFill.textContent = Math.round(percentComplete) + '%';
                uploadStatus.textContent = `Uploading... ${formatFileSize(e.loaded)} of ${formatFileSize(e.total)}`;
            }
        });
        
        xhr.addEventListener('load', () => {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                showAlert('Video uploaded successfully!', 'success');
                resetUploadForm();
                loadVideos();
                loadStatistics();
            } else {
                showAlert('Upload failed. Please try again.', 'error');
            }
        });
        
        xhr.addEventListener('error', () => {
            showAlert('Upload failed. Please check your connection.', 'error');
        });
        
        xhr.open('POST', `${API_BASE_URL}/api/videos/upload`);
        xhr.send(formData);
        
    } catch (error) {
        console.error('Upload error:', error);
        showAlert('Upload failed. Please try again.', 'error');
    }
}

// Reset upload form
function resetUploadForm() {
    document.getElementById('uploadForm').reset();
    selectedFile = null;
    
    const uploadArea = document.getElementById('uploadArea');
    uploadArea.innerHTML = `
        <i class="fas fa-cloud-upload-alt" style="font-size: 3rem; color: var(--primary-accent); margin-bottom: 1rem;"></i>
        <h3 style="color: var(--text-primary); margin-bottom: 0.5rem;">Drop video file here</h3>
        <p style="color: var(--text-secondary);">or click to browse</p>
        <p style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 1rem;">
            Supported formats: MP4, WebM, OGG, MOV, AVI, MKV (Max: 500MB)
        </p>
    `;
    
    document.getElementById('uploadProgress').style.display = 'none';
    document.getElementById('progressFill').style.width = '0%';
}

// Load statistics
async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/statistics`);
        const stats = await response.json();
        
        document.getElementById('total-videos').textContent = stats.total_videos || 0;
        document.getElementById('total-categories').textContent = stats.categories_count || 0;
        document.getElementById('total-views').textContent = formatNumber(stats.total_views || 0);
        document.getElementById('storage-used').textContent = formatFileSize(stats.total_size || 0);
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Load videos
async function loadVideos() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/videos/list`);
        const data = await response.json();
        videos = data.videos || [];
        displayVideos(videos);
    } catch (error) {
        console.error('Error loading videos:', error);
        // Show placeholder message
        const tableBody = document.getElementById('videoTableBody');
        if (tableBody) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="7" style="text-align: center; padding: 2rem; color: var(--text-secondary);">
                        No videos found or backend not running
                    </td>
                </tr>
            `;
        }
    }
}

// Display videos in table
function displayVideos(videoList) {
    const tableBody = document.getElementById('videoTableBody');
    if (!tableBody) return;
    
    if (videoList.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="7" style="text-align: center; padding: 2rem; color: var(--text-secondary);">
                    No videos uploaded yet
                </td>
            </tr>
        `;
        return;
    }
    
    tableBody.innerHTML = videoList.map(video => `
        <tr>
            <td>${video.title}</td>
            <td>${video.category}</td>
            <td>${video.instructor}</td>
            <td>${video.level}</td>
            <td>${formatNumber(video.views || 0)}</td>
            <td>
                <span class="status-badge status-${video.status}">
                    ${video.status}
                </span>
            </td>
            <td>
                <div class="action-buttons">
                    <button class="btn-small btn-edit" onclick="editVideo('${video.id}')">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn-small btn-delete" onclick="deleteVideo('${video.id}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

// Filter videos
function filterVideos(query) {
    const filtered = videos.filter(video => 
        video.title.toLowerCase().includes(query.toLowerCase()) ||
        video.category.toLowerCase().includes(query.toLowerCase()) ||
        video.instructor.toLowerCase().includes(query.toLowerCase())
    );
    displayVideos(filtered);
}

// Load placeholders
async function loadPlaceholders() {
    const categories = [
        'mathematics', 'computer-science', 'physics', 'chemistry', 'biology',
        'engineering', 'business', 'medicine', 'psychology', 'language',
        'history', 'art', 'music', 'philosophy', 'law',
        'environmental', 'data-science', 'test-prep', 'study-skills', 'career'
    ];
    
    const placeholdersGrid = document.getElementById('placeholders-grid');
    if (!placeholdersGrid) return;
    
    placeholdersGrid.innerHTML = categories.map(category => `
        <div class="placeholder-card" style="
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            cursor: pointer;
            transition: all 0.3s ease;
        " onclick="viewCategoryPlaceholders('${category}')">
            <h3 style="color: var(--primary-accent); margin-bottom: 1rem;">
                ${category.replace('-', ' ').charAt(0).toUpperCase() + category.slice(1).replace('-', ' ')}
            </h3>
            <p style="color: var(--text-secondary); margin-bottom: 1rem;">
                Click to view and fill placeholder slots
            </p>
            <div style="display: flex; justify-content: space-between; color: var(--text-secondary); font-size: 0.9rem;">
                <span><i class="fas fa-video"></i> 50 slots</span>
                <span><i class="fas fa-upload"></i> Upload</span>
            </div>
        </div>
    `).join('');
}

// View category placeholders
async function viewCategoryPlaceholders(category) {
    try {
        // For demonstration, we'll show a simple alert
        // In production, this would open a detailed view
        const response = await fetch(`${API_BASE_URL}/api/videos/placeholder/${category}/general`);
        const data = await response.json();
        
        alert(`Category: ${category}\nPlaceholder slots: ${data.placeholders.length}\n\nClick on individual slots to upload videos.`);
    } catch (error) {
        console.error('Error loading placeholders:', error);
    }
}

// Edit video
function editVideo(videoId) {
    // In production, this would open an edit modal
    alert(`Edit video: ${videoId}`);
}

// Delete video
async function deleteVideo(videoId) {
    if (!confirm('Are you sure you want to archive this video?')) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/videos/${videoId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showAlert('Video archived successfully', 'success');
            loadVideos();
            loadStatistics();
        } else {
            showAlert('Failed to delete video', 'error');
        }
    } catch (error) {
        console.error('Error deleting video:', error);
        showAlert('Failed to delete video', 'error');
    }
}

// Show tab
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all tab buttons
    document.querySelectorAll('.tab').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(`${tabName}-tab`).classList.add('active');
    
    // Add active class to clicked button
    event.target.closest('.tab').classList.add('active');
}

// Utility functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function formatNumber(num) {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
}

function showAlert(message, type) {
    // Simple alert for now, can be replaced with a better notification system
    alert(message);
}