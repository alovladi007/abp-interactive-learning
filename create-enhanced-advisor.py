#!/usr/bin/env python3
"""
Create the enhanced AI Path Advisor with all majors organized by category
"""

# HTML template with all majors and categories
html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Path Advisor - Personalized Learning Roadmap</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary-accent: #667eea;
            --secondary-accent: #764ba2;
            --success-color: #48bb78;
            --text-primary: #2d3748;
            --text-secondary: #718096;
            --border-color: #e2e8f0;
            --secondary-bg: #f7fafc;
            --card-bg: #ffffff;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.12);
            --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
            --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 2rem;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .wizard-header {
            text-align: center;
            color: white;
            margin-bottom: 3rem;
        }

        .wizard-header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }

        /* Category Selector */
        .category-selector {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: var(--shadow-lg);
        }

        .category-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 1.5rem;
        }

        .category-card {
            background: var(--secondary-bg);
            border: 2px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
        }

        .category-card:hover {
            border-color: var(--primary-accent);
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }

        .category-card.active {
            border-color: var(--primary-accent);
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        }

        .category-icon {
            width: 60px;
            height: 60px;
            margin: 0 auto 1rem;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.8rem;
            color: white;
        }

        /* Major Selection */
        .major-selection {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: var(--shadow-lg);
            display: none;
        }

        .major-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
            max-height: 400px;
            overflow-y: auto;
            padding: 0.5rem;
        }

        .major-card {
            background: var(--secondary-bg);
            border: 2px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
        }

        .major-card:hover {
            border-color: var(--primary-accent);
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }

        .major-card.selected {
            border-color: var(--primary-accent);
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        }

        .major-icon {
            width: 50px;
            height: 50px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1rem;
            font-size: 1.5rem;
            color: white;
        }

        /* Career Path Selection */
        .career-selection {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            display: none;
        }

        .career-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
        }

        .career-card {
            background: var(--secondary-bg);
            border: 2px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .career-card:hover {
            border-color: var(--primary-accent);
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }

        .career-card.selected {
            border-color: var(--primary-accent);
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        }

        /* Quick Setup Form */
        .quick-setup {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            display: none;
        }

        .form-group {
            margin-bottom: 1.5rem;
        }

        .form-label {
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--text-primary);
            display: block;
        }

        .form-select, .form-input {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            font-size: 1rem;
        }

        .range-slider {
            width: 100%;
            margin: 0.5rem 0;
        }

        .slider-value {
            text-align: center;
            color: var(--primary-accent);
            font-weight: 600;
            margin-top: 0.5rem;
        }

        /* Roadmap Display */
        .roadmap-display {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            display: none;
        }

        .roadmap-timeline {
            position: relative;
            padding-left: 3rem;
        }

        .roadmap-item {
            position: relative;
            margin-bottom: 2rem;
            background: var(--secondary-bg);
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid var(--border-color);
        }

        /* Navigation Buttons */
        .nav-buttons {
            display: flex;
            justify-content: space-between;
            margin-top: 2rem;
        }

        .btn {
            padding: 0.75rem 2rem;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .btn-secondary {
            background: var(--secondary-bg);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
        }

        /* Progress Steps */
        .progress-container {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: var(--shadow-md);
        }

        .progress-steps {
            display: flex;
            justify-content: space-between;
            position: relative;
        }

        .progress-step {
            display: flex;
            flex-direction: column;
            align-items: center;
            position: relative;
            z-index: 1;
        }

        .progress-step-circle {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: var(--card-bg);
            border: 2px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
        }

        .progress-step.active .progress-step-circle {
            background: var(--primary-accent);
            border-color: var(--primary-accent);
            color: white;
        }

        .progress-step.completed .progress-step-circle {
            background: var(--success-color);
            border-color: var(--success-color);
            color: white;
        }

        .progress-step-label {
            margin-top: 0.5rem;
            font-size: 0.85rem;
            color: var(--text-secondary);
            text-align: center;
        }

        /* Loading State */
        .loading {
            text-align: center;
            padding: 3rem;
        }

        .spinner {
            border: 4px solid var(--border-color);
            border-top: 4px solid var(--primary-accent);
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 1rem;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="academic-setup.html" style="color: white; text-decoration: none; display: inline-flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
            <i class="fas fa-arrow-left"></i> Back to Academic Setup
        </a>

        <div class="wizard-header">
            <h1>AI Path Advisor</h1>
            <p>Build your personalized learning roadmap with Louis, your AI advisor</p>
        </div>

        <!-- Progress Steps -->
        <div class="progress-container">
            <div class="progress-steps">
                <div class="progress-step active" id="step-1-progress">
                    <div class="progress-step-circle">1</div>
                    <div class="progress-step-label">Choose Field</div>
                </div>
                <div class="progress-step" id="step-2-progress">
                    <div class="progress-step-circle">2</div>
                    <div class="progress-step-label">Select Path</div>
                </div>
                <div class="progress-step" id="step-3-progress">
                    <div class="progress-step-circle">3</div>
                    <div class="progress-step-label">Preferences</div>
                </div>
                <div class="progress-step" id="step-4-progress">
                    <div class="progress-step-circle">4</div>
                    <div class="progress-step-label">Assessment</div>
                </div>
                <div class="progress-step" id="step-5-progress">
                    <div class="progress-step-circle">5</div>
                    <div class="progress-step-label">Roadmap</div>
                </div>
            </div>
        </div>

        <!-- Step 1: Category Selection -->
        <div class="category-selector" id="step-1">
            <h2>Step 1: Choose Your Field of Study</h2>
            <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">
                Select a category to explore available majors
            </p>

            <div class="category-grid">
                <div class="category-card" data-category="technology">
                    <div class="category-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                        <i class="fas fa-laptop-code"></i>
                    </div>
                    <h3>Technology</h3>
                    <p style="color: var(--text-secondary); font-size: 0.85rem;">2 majors</p>
                </div>

                <div class="category-card" data-category="engineering">
                    <div class="category-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                        <i class="fas fa-cogs"></i>
                    </div>
                    <h3>Engineering</h3>
                    <p style="color: var(--text-secondary); font-size: 0.85rem;">5 majors</p>
                </div>

                <div class="category-card" data-category="sciences">
                    <div class="category-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                        <i class="fas fa-flask"></i>
                    </div>
                    <h3>Sciences</h3>
                    <p style="color: var(--text-secondary); font-size: 0.85rem;">4 majors</p>
                </div>

                <div class="category-card" data-category="health">
                    <div class="category-icon" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
                        <i class="fas fa-heartbeat"></i>
                    </div>
                    <h3>Health & Medicine</h3>
                    <p style="color: var(--text-secondary); font-size: 0.85rem;">5 majors</p>
                </div>

                <div class="category-card" data-category="business">
                    <div class="category-icon" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
                        <i class="fas fa-chart-line"></i>
                    </div>
                    <h3>Business</h3>
                    <p style="color: var(--text-secondary); font-size: 0.85rem;">2 majors</p>
                </div>

                <div class="category-card" data-category="social">
                    <div class="category-icon" style="background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);">
                        <i class="fas fa-users"></i>
                    </div>
                    <h3>Social Sciences</h3>
                    <p style="color: var(--text-secondary); font-size: 0.85rem;">3 majors</p>
                </div>

                <div class="category-card" data-category="arts">
                    <div class="category-icon" style="background: linear-gradient(135deg, #f857a6 0%, #ff5858 100%);">
                        <i class="fas fa-palette"></i>
                    </div>
                    <h3>Arts & Design</h3>
                    <p style="color: var(--text-secondary); font-size: 0.85rem;">2 majors</p>
                </div>

                <div class="category-card" data-category="law">
                    <div class="category-icon" style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);">
                        <i class="fas fa-balance-scale"></i>
                    </div>
                    <h3>Law & Policy</h3>
                    <p style="color: var(--text-secondary); font-size: 0.85rem;">2 majors</p>
                </div>
            </div>
        </div>

        <!-- Major Selection (Hidden initially) -->
        <div class="major-selection" id="major-selection">
            <h3 id="category-title">Select Your Major</h3>
            <div class="major-grid" id="major-grid">
                <!-- Majors will be populated dynamically -->
            </div>
            <div class="nav-buttons">
                <button class="btn btn-secondary" onclick="backToCategories()">
                    <i class="fas fa-arrow-left"></i> Back
                </button>
            </div>
        </div>

        <!-- Step 2: Career Path Selection -->
        <div class="career-selection" id="step-2">
            <h2>Step 2: Choose Your Career Path</h2>
            <div class="career-grid" id="career-grid">
                <!-- Career paths will be populated dynamically -->
            </div>
        </div>

        <!-- Step 3: Preferences -->
        <div class="quick-setup" id="step-3">
            <h2>Step 3: Set Your Preferences</h2>
            <div class="form-group">
                <label class="form-label">Study Hours per Week</label>
                <input type="range" class="range-slider" id="hours-slider" min="5" max="40" value="15">
                <div class="slider-value" id="hours-value">15 hours/week</div>
            </div>
            
            <div class="form-group">
                <label class="form-label">Monthly Budget</label>
                <select class="form-select" id="budget-select">
                    <option value="0">Free resources only</option>
                    <option value="50">Up to $50/month</option>
                    <option value="100">Up to $100/month</option>
                    <option value="200">Up to $200/month</option>
                    <option value="unlimited">No budget limit</option>
                </select>
            </div>
            
            <div class="form-group">
                <label class="form-label">Learning Style</label>
                <select class="form-select" id="style-select">
                    <option value="visual">Visual (Videos, Diagrams)</option>
                    <option value="reading">Reading (Books, Articles)</option>
                    <option value="hands-on">Hands-on (Projects, Labs)</option>
                    <option value="mixed">Mixed Approach</option>
                </select>
            </div>
        </div>

        <!-- Step 4: Quiz -->
        <div class="quick-setup" id="step-4">
            <h2>Step 4: Baseline Assessment (Optional)</h2>
            <p style="text-align: center; padding: 2rem;">
                <button class="btn btn-primary" onclick="startQuiz()">Start Quiz</button>
                <button class="btn btn-secondary" onclick="skipQuiz()" style="margin-left: 1rem;">Skip</button>
            </p>
        </div>

        <!-- Step 5: Roadmap -->
        <div class="roadmap-display" id="step-5">
            <div class="loading">
                <div class="spinner"></div>
                <h3>Generating Your Roadmap...</h3>
            </div>
        </div>

        <!-- Navigation -->
        <div class="nav-buttons" id="main-nav" style="display: none;">
            <button class="btn btn-secondary" id="prev-btn" onclick="previousStep()">Previous</button>
            <button class="btn btn-primary" id="next-btn" onclick="nextStep()">Next</button>
        </div>
    </div>

    <script src="path-advisor-enhanced.js"></script>
</body>
</html>'''

# Write the HTML file
with open('ai-path-advisor.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("Enhanced AI Path Advisor HTML created successfully!")