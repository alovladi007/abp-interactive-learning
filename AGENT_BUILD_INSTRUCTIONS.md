# AI Agent Instructions: Build EUREKA Landing Page Frontend

**Target Agent:** Claude Code, ChatGPT Code Interpreter, or similar AI coding assistant

**Task:** Build a complete, modern landing page matching the EUREKA platform specifications

**Complexity:** Intermediate

**Estimated Time:** 30-45 minutes (agent execution time)

---

## Agent Mission Brief

You are tasked with building a professional, modern landing page for an educational platform. The page must be responsive, animated, and visually stunning. You will build this from scratch using only HTML, CSS, and vanilla JavaScript.

**Success Criteria:**
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Smooth animations on scroll
- ✅ Professional UI matching specifications
- ✅ All interactive elements functional
- ✅ No frameworks (pure HTML/CSS/JS)
- ✅ Cross-browser compatible

---

## Phase 1: Project Setup & Structure

### Task 1.1: Create Project Structure

Create the following directory structure:

```
landing-page/
├── index.html
├── styles.css
├── script.js
├── images/
│   ├── hero-image.jpg (placeholder)
│   ├── feature-1.jpg (placeholder)
│   └── feature-2.jpg (placeholder)
└── README.md
```

### Task 1.2: Initialize HTML Boilerplate

Create `index.html` with:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="E.U.R.E.K.A - Empowering Universal Research, Education, Knowledge & Achievement">
    <title>E.U.R.E.K.A - Educational Platform</title>

    <!-- External Dependencies -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <!-- Custom Styles -->
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Content will be added in subsequent tasks -->

    <!-- Scripts -->
    <script src="script.js"></script>
</body>
</html>
```

**Validation:**
- [ ] HTML5 doctype present
- [ ] Meta viewport for responsiveness
- [ ] Font Awesome 6.4.0 CDN loaded
- [ ] Links to styles.css and script.js

---

## Phase 2: CSS Foundation & Variables

### Task 2.1: Create CSS Variables

In `styles.css`, define the design system:

```css
:root {
    /* Primary Colors */
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --accent-color: #f093fb;
    --accent-secondary: #f5576c;

    /* Background Colors */
    --dark-bg: #0a0a0a;
    --card-bg: #1a1a1a;
    --secondary-bg: #141414;

    /* Text Colors */
    --text-primary: #ffffff;
    --text-secondary: #b0b0b0;
    --text-muted: #666666;

    /* Borders */
    --border-color: #2a2a2a;
    --border-radius: 12px;

    /* Spacing */
    --spacing-xs: 0.5rem;
    --spacing-sm: 1rem;
    --spacing-md: 1.5rem;
    --spacing-lg: 2rem;
    --spacing-xl: 3rem;

    /* Transitions */
    --transition-fast: 0.2s ease;
    --transition-normal: 0.3s ease;
    --transition-slow: 0.5s ease;

    /* Shadows */
    --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.1);
    --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.2);
    --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.3);

    /* Gradients */
    --gradient-primary: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    --gradient-accent: linear-gradient(135deg, var(--accent-color) 0%, var(--accent-secondary) 100%);
}
```

### Task 2.2: Reset & Base Styles

```css
/* Reset */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Base Styles */
html {
    scroll-behavior: smooth;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    background-color: var(--dark-bg);
    color: var(--text-primary);
    line-height: 1.6;
    overflow-x: hidden;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    font-weight: 600;
    line-height: 1.2;
    margin-bottom: var(--spacing-md);
}

h1 { font-size: 3rem; }
h2 { font-size: 2.5rem; }
h3 { font-size: 2rem; }
h4 { font-size: 1.5rem; }

p {
    margin-bottom: var(--spacing-sm);
}

a {
    color: var(--primary-color);
    text-decoration: none;
    transition: var(--transition-normal);
}

a:hover {
    color: var(--accent-color);
}

/* Container */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--spacing-lg);
}

/* Utility Classes */
.text-center { text-align: center; }
.text-accent { color: var(--accent-color); }
.text-secondary { color: var(--text-secondary); }
.mt-4 { margin-top: var(--spacing-xl); }
.mb-4 { margin-bottom: var(--spacing-xl); }
```

**Validation:**
- [ ] CSS variables defined
- [ ] Reset styles applied
- [ ] Typography hierarchy established
- [ ] Utility classes created

---

## Phase 3: Navigation Bar Component

### Task 3.1: Build Navigation HTML

Add to `index.html` body:

```html
<nav class="navbar">
    <div class="nav-container">
        <!-- Logo -->
        <a href="#" class="nav-logo">
            <div class="logo-icon">
                <i class="fas fa-lightbulb"></i>
            </div>
            <span class="logo-text">E.U.R.E.K.A</span>
        </a>

        <!-- Search Bar -->
        <div class="search-bar">
            <i class="fas fa-search"></i>
            <input type="text" placeholder="Search courses, videos, topics...">
        </div>

        <!-- Navigation Menu -->
        <ul class="nav-menu">
            <li class="nav-item">
                <a href="#" class="nav-link active">
                    <i class="fas fa-home"></i>
                    <span>Home</span>
                </a>
            </li>
            <li class="nav-item">
                <a href="#features" class="nav-link">
                    <i class="fas fa-star"></i>
                    <span>Features</span>
                </a>
            </li>
            <li class="nav-item">
                <a href="#samples" class="nav-link">
                    <i class="fas fa-play-circle"></i>
                    <span>Learning Samples</span>
                </a>
            </li>
            <li class="nav-item">
                <a href="#pricing" class="nav-link">
                    <i class="fas fa-tags"></i>
                    <span>Pricing</span>
                </a>
            </li>
            <li class="nav-item">
                <a href="#contact" class="nav-link">
                    <i class="fas fa-envelope"></i>
                    <span>Contact</span>
                </a>
            </li>
        </ul>

        <!-- Action Buttons -->
        <div class="nav-actions">
            <button class="btn btn-outline">
                <i class="fas fa-sign-in-alt"></i>
                Login
            </button>
            <button class="btn btn-primary">
                <i class="fas fa-rocket"></i>
                Get Started
            </button>
        </div>

        <!-- Mobile Menu Toggle -->
        <button class="mobile-menu-toggle">
            <i class="fas fa-bars"></i>
        </button>
    </div>
</nav>
```

### Task 3.2: Style Navigation Bar

Add to `styles.css`:

```css
/* Navigation Bar */
.navbar {
    position: sticky;
    top: 0;
    width: 100%;
    background: rgba(10, 10, 10, 0.95);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--border-color);
    z-index: 1000;
    padding: 1rem 0;
}

.nav-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    align-items: center;
    gap: 2rem;
}

/* Logo */
.nav-logo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 1.5rem;
    font-weight: 700;
    text-decoration: none;
    color: var(--text-primary);
}

.logo-icon {
    width: 40px;
    height: 40px;
    background: var(--gradient-primary);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
}

/* Search Bar */
.search-bar {
    flex: 1;
    max-width: 500px;
    position: relative;
}

.search-bar i {
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-muted);
}

.search-bar input {
    width: 100%;
    padding: 0.75rem 1rem 0.75rem 3rem;
    background: var(--secondary-bg);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    color: var(--text-primary);
    font-size: 0.9rem;
    transition: var(--transition-normal);
}

.search-bar input:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* Navigation Menu */
.nav-menu {
    display: flex;
    list-style: none;
    gap: 0.5rem;
    margin: 0;
}

.nav-link {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    color: var(--text-secondary);
    text-decoration: none;
    border-radius: 8px;
    transition: var(--transition-normal);
    font-size: 0.9rem;
}

.nav-link:hover {
    color: var(--text-primary);
    background: rgba(102, 126, 234, 0.1);
}

.nav-link.active {
    color: var(--primary-color);
    background: rgba(102, 126, 234, 0.15);
}

.nav-link i {
    font-size: 1rem;
}

/* Action Buttons */
.nav-actions {
    display: flex;
    gap: 1rem;
}

.btn {
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    transition: var(--transition-normal);
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    border: none;
}

.btn-primary {
    background: var(--gradient-primary);
    color: white;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

.btn-outline {
    background: transparent;
    color: var(--text-primary);
    border: 1px solid var(--border-color);
}

.btn-outline:hover {
    border-color: var(--primary-color);
    background: rgba(102, 126, 234, 0.1);
}

/* Mobile Menu Toggle */
.mobile-menu-toggle {
    display: none;
    background: none;
    border: none;
    color: var(--text-primary);
    font-size: 1.5rem;
    cursor: pointer;
}

/* Responsive */
@media (max-width: 1024px) {
    .nav-menu {
        display: none;
    }

    .mobile-menu-toggle {
        display: block;
    }
}

@media (max-width: 768px) {
    .search-bar {
        max-width: 200px;
    }

    .nav-actions .btn span {
        display: none;
    }
}
```

**Validation:**
- [ ] Navigation bar is sticky
- [ ] Logo displays with icon
- [ ] Search bar functional
- [ ] Menu items aligned properly
- [ ] Buttons styled correctly
- [ ] Responsive on mobile

---

## Phase 4: Hero Section

### Task 4.1: Build Hero HTML

Add after navigation in `index.html`:

```html
<section class="hero">
    <div class="hero-container">
        <div class="hero-content fade-in">
            <h1>Empowering Universal Research, Education, Knowledge & Achievement</h1>
            <p class="hero-subtitle">Explore Ideas. Master Knowledge. Drive Innovation.</p>

            <div class="hero-buttons">
                <button class="btn btn-primary btn-lg">
                    <i class="fas fa-play"></i>
                    Start Learning Free
                </button>
                <button class="btn btn-outline btn-lg">
                    <i class="fas fa-video"></i>
                    Watch Demo
                </button>
            </div>

            <!-- Statistics -->
            <div class="hero-stats">
                <div class="stat-item">
                    <span class="stat-number">500K+</span>
                    <span class="stat-label">Active Learners</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">10K+</span>
                    <span class="stat-label">Video Courses</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">95%</span>
                    <span class="stat-label">Success Rate</span>
                </div>
            </div>
        </div>

        <div class="hero-visual scale-in">
            <div class="hero-card">
                <div class="video-preview">
                    <img src="images/hero-image.jpg" alt="AI Learning Platform">
                    <div class="play-overlay">
                        <i class="fas fa-play-circle"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
```

### Task 4.2: Style Hero Section

```css
/* Hero Section */
.hero {
    min-height: calc(100vh - 80px);
    display: flex;
    align-items: center;
    padding: 4rem 0;
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(240, 147, 251, 0.1) 0%, transparent 50%);
    z-index: -1;
}

.hero-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 2rem;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    align-items: center;
}

.hero-content h1 {
    font-size: 3.5rem;
    line-height: 1.2;
    margin-bottom: 1.5rem;
    background: linear-gradient(135deg, var(--text-primary) 0%, var(--accent-color) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 1.25rem;
    color: var(--text-secondary);
    margin-bottom: 2rem;
}

.hero-buttons {
    display: flex;
    gap: 1rem;
    margin-bottom: 3rem;
}

.btn-lg {
    padding: 1rem 2rem;
    font-size: 1rem;
}

/* Hero Stats */
.hero-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
    padding-top: 2rem;
    border-top: 1px solid var(--border-color);
}

.stat-item {
    text-align: left;
}

.stat-number {
    display: block;
    font-size: 2.5rem;
    font-weight: 700;
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

.stat-label {
    display: block;
    color: var(--text-secondary);
    font-size: 0.9rem;
}

/* Hero Visual */
.hero-visual {
    position: relative;
}

.hero-card {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: var(--shadow-lg);
}

.video-preview {
    position: relative;
    border-radius: 12px;
    overflow: hidden;
    aspect-ratio: 16/9;
}

.video-preview img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.play-overlay {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 80px;
    height: 80px;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: var(--transition-normal);
}

.play-overlay:hover {
    transform: translate(-50%, -50%) scale(1.1);
    background: white;
}

.play-overlay i {
    font-size: 2rem;
    color: var(--primary-color);
    margin-left: 5px;
}

/* Animations */
.fade-in {
    animation: fadeIn 1s ease forwards;
}

.scale-in {
    animation: scaleIn 1s ease forwards;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes scaleIn {
    from {
        opacity: 0;
        transform: scale(0.9);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

/* Responsive */
@media (max-width: 1024px) {
    .hero-container {
        grid-template-columns: 1fr;
        gap: 3rem;
    }

    .hero-content h1 {
        font-size: 2.5rem;
    }
}

@media (max-width: 768px) {
    .hero-stats {
        grid-template-columns: 1fr;
        gap: 1rem;
    }

    .hero-buttons {
        flex-direction: column;
    }

    .hero-content h1 {
        font-size: 2rem;
    }
}
```

**Validation:**
- [ ] Hero section full viewport height
- [ ] Grid layout with text and image
- [ ] Gradient text effects applied
- [ ] Stats display in grid
- [ ] Play button overlay on image
- [ ] Animations trigger on load

---

## Phase 5: Features Section

### Task 5.1: Build Features HTML

```html
<section id="features" class="features">
    <div class="container">
        <h2 class="text-center">Powerful Features for Modern Learning</h2>
        <p class="text-center text-secondary section-subtitle">
            Everything you need to master any subject
        </p>

        <div class="features-grid">
            <!-- Feature 1 -->
            <div class="feature-card animate-on-scroll">
                <div class="feature-icon">
                    <i class="fas fa-video"></i>
                </div>
                <h3>AI Video Generator</h3>
                <p>Transform any text, document, or idea into engaging video lectures using advanced AI technology.</p>
                <span class="feature-badge">NEW</span>
            </div>

            <!-- Feature 2 -->
            <div class="feature-card animate-on-scroll">
                <div class="feature-icon">
                    <i class="fas fa-graduation-cap"></i>
                </div>
                <h3>Academic Setup</h3>
                <p>Complete curriculum management with syllabus tracking, assignment scheduling, and grade analytics.</p>
                <span class="feature-badge badge-popular">POPULAR</span>
            </div>

            <!-- Feature 3 -->
            <div class="feature-card animate-on-scroll">
                <div class="feature-icon">
                    <i class="fas fa-book"></i>
                </div>
                <h3>Digital Library</h3>
                <p>Access millions of books, research papers, and educational resources in one centralized location.</p>
                <span class="feature-badge">500K+ Books</span>
            </div>

            <!-- Feature 4 -->
            <div class="feature-card animate-on-scroll">
                <div class="feature-icon">
                    <i class="fas fa-shopping-cart"></i>
                </div>
                <h3>Course Marketplace</h3>
                <p>Buy, sell, and share educational content with millions of learners worldwide.</p>
                <span class="feature-badge">Amazon-style</span>
            </div>

            <!-- Feature 5 -->
            <div class="feature-card animate-on-scroll">
                <div class="feature-icon">
                    <i class="fas fa-clipboard-check"></i>
                </div>
                <h3>Smart Assessments</h3>
                <p>Advanced testing system with detailed explanations, performance tracking, and adaptive learning.</p>
                <span class="feature-badge">UWorld Quality</span>
            </div>

            <!-- Feature 6 -->
            <div class="feature-card animate-on-scroll">
                <div class="feature-icon">
                    <i class="fas fa-certificate"></i>
                </div>
                <h3>Certifications</h3>
                <p>Earn industry-recognized certificates and boost your career with verified credentials.</p>
                <span class="feature-badge badge-popular">TOP RATED</span>
            </div>
        </div>
    </div>
</section>
```

### Task 5.2: Style Features Section

```css
/* Features Section */
.features {
    padding: 6rem 0;
    background: var(--secondary-bg);
}

.section-subtitle {
    font-size: 1.1rem;
    margin-bottom: 3rem;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2rem;
    margin-top: 3rem;
}

.feature-card {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius);
    padding: 2rem;
    position: relative;
    transition: var(--transition-normal);
    opacity: 0;
    transform: translateY(30px);
}

.feature-card.visible {
    opacity: 1;
    transform: translateY(0);
}

.feature-card:hover {
    transform: translateY(-8px);
    border-color: var(--primary-color);
    box-shadow: var(--shadow-lg);
}

.feature-icon {
    width: 60px;
    height: 60px;
    background: var(--gradient-primary);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1.5rem;
    color: white;
    font-size: 1.5rem;
}

.feature-card h3 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
}

.feature-card p {
    color: var(--text-secondary);
    line-height: 1.6;
}

.feature-badge {
    position: absolute;
    top: 1.5rem;
    right: 1.5rem;
    background: var(--primary-color);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
}

.badge-popular {
    background: var(--accent-secondary);
}

/* Responsive */
@media (max-width: 768px) {
    .features-grid {
        grid-template-columns: 1fr;
    }
}
```

**Validation:**
- [ ] 6 feature cards in responsive grid
- [ ] Icons with gradient backgrounds
- [ ] Badges positioned correctly
- [ ] Hover effects working
- [ ] Cards animate on scroll

---

## Phase 6: Pricing Section

### Task 6.1: Build Pricing HTML

```html
<section id="pricing" class="pricing">
    <div class="container">
        <h2 class="text-center">Choose Your Learning Path</h2>
        <p class="text-center text-secondary section-subtitle">
            Flexible plans for every learner
        </p>

        <div class="pricing-grid">
            <!-- Free Plan -->
            <div class="pricing-card animate-on-scroll">
                <div class="pricing-header">
                    <h3>Free</h3>
                    <div class="price">
                        <span class="currency">$</span>
                        <span class="amount">0</span>
                        <span class="period">/month</span>
                    </div>
                </div>
                <ul class="pricing-features">
                    <li><i class="fas fa-check"></i> Access to 100 free videos</li>
                    <li><i class="fas fa-check"></i> Basic quizzes & tests</li>
                    <li><i class="fas fa-check"></i> Community forum access</li>
                    <li><i class="fas fa-check"></i> Mobile app access</li>
                    <li class="disabled"><i class="fas fa-times"></i> AI tutoring</li>
                    <li class="disabled"><i class="fas fa-times"></i> Certificates</li>
                </ul>
                <button class="btn btn-outline btn-block">Get Started</button>
            </div>

            <!-- Pro Plan -->
            <div class="pricing-card featured animate-on-scroll">
                <div class="popular-badge">MOST POPULAR</div>
                <div class="pricing-header">
                    <h3>Pro</h3>
                    <div class="price">
                        <span class="currency">$</span>
                        <span class="amount">19</span>
                        <span class="period">/month</span>
                    </div>
                </div>
                <ul class="pricing-features">
                    <li><i class="fas fa-check"></i> Access to 5,000+ videos</li>
                    <li><i class="fas fa-check"></i> Advanced assessments</li>
                    <li><i class="fas fa-check"></i> AI tutor assistance</li>
                    <li><i class="fas fa-check"></i> Downloadable resources</li>
                    <li><i class="fas fa-check"></i> Progress analytics</li>
                    <li class="disabled"><i class="fas fa-times"></i> 1-on-1 coaching</li>
                </ul>
                <button class="btn btn-primary btn-block">Start Free Trial</button>
            </div>

            <!-- ProMax Plan -->
            <div class="pricing-card animate-on-scroll">
                <div class="pricing-header">
                    <h3>ProMax</h3>
                    <div class="price">
                        <span class="currency">$</span>
                        <span class="amount">49</span>
                        <span class="period">/month</span>
                    </div>
                </div>
                <ul class="pricing-features">
                    <li><i class="fas fa-check"></i> Unlimited access to all content</li>
                    <li><i class="fas fa-check"></i> Priority AI tutoring</li>
                    <li><i class="fas fa-check"></i> 1-on-1 coaching sessions</li>
                    <li><i class="fas fa-check"></i> Custom learning paths</li>
                    <li><i class="fas fa-check"></i> All certifications included</li>
                    <li><i class="fas fa-check"></i> Lifetime access</li>
                </ul>
                <button class="btn btn-outline btn-block">Contact Sales</button>
            </div>
        </div>
    </div>
</section>
```

### Task 6.2: Style Pricing Section

```css
/* Pricing Section */
.pricing {
    padding: 6rem 0;
}

.pricing-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 3rem;
}

.pricing-card {
    background: var(--card-bg);
    border: 2px solid var(--border-color);
    border-radius: var(--border-radius);
    padding: 2rem;
    position: relative;
    transition: var(--transition-normal);
    opacity: 0;
    transform: translateY(30px);
}

.pricing-card.visible {
    opacity: 1;
    transform: translateY(0);
}

.pricing-card:hover {
    transform: translateY(-8px);
    border-color: var(--primary-color);
    box-shadow: var(--shadow-lg);
}

.pricing-card.featured {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
}

.popular-badge {
    position: absolute;
    top: -12px;
    left: 50%;
    transform: translateX(-50%);
    background: var(--gradient-accent);
    color: white;
    padding: 0.5rem 1.5rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
}

.pricing-header {
    text-align: center;
    padding-bottom: 2rem;
    border-bottom: 1px solid var(--border-color);
    margin-bottom: 2rem;
}

.pricing-header h3 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
}

.price {
    display: flex;
    align-items: flex-start;
    justify-content: center;
    gap: 0.25rem;
}

.currency {
    font-size: 1.5rem;
    color: var(--text-secondary);
    margin-top: 0.5rem;
}

.amount {
    font-size: 4rem;
    font-weight: 700;
    line-height: 1;
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.period {
    color: var(--text-secondary);
    margin-top: 2rem;
}

.pricing-features {
    list-style: none;
    margin-bottom: 2rem;
}

.pricing-features li {
    padding: 0.75rem 0;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: var(--text-primary);
}

.pricing-features li i {
    color: var(--primary-color);
    font-size: 1rem;
}

.pricing-features li.disabled {
    color: var(--text-muted);
    opacity: 0.5;
}

.pricing-features li.disabled i {
    color: var(--text-muted);
}

.btn-block {
    width: 100%;
}

/* Responsive */
@media (max-width: 768px) {
    .pricing-grid {
        grid-template-columns: 1fr;
    }
}
```

**Validation:**
- [ ] 3 pricing cards displayed
- [ ] Featured card has special styling
- [ ] Price typography correct
- [ ] Feature lists with checkmarks
- [ ] Buttons full width
- [ ] Cards animate on scroll

---

## Phase 7: Footer Section

### Task 7.1: Build Footer HTML

```html
<footer class="footer">
    <div class="container">
        <div class="footer-grid">
            <!-- Company Info -->
            <div class="footer-section">
                <div class="footer-logo">
                    <div class="logo-icon">
                        <i class="fas fa-lightbulb"></i>
                    </div>
                    <span class="logo-text">E.U.R.E.K.A</span>
                </div>
                <p class="text-secondary">
                    Empowering Universal Research, Education, Knowledge & Achievement.
                </p>
                <div class="social-links">
                    <a href="#" class="social-link"><i class="fab fa-facebook"></i></a>
                    <a href="#" class="social-link"><i class="fab fa-twitter"></i></a>
                    <a href="#" class="social-link"><i class="fab fa-linkedin"></i></a>
                    <a href="#" class="social-link"><i class="fab fa-youtube"></i></a>
                    <a href="#" class="social-link"><i class="fab fa-instagram"></i></a>
                </div>
            </div>

            <!-- Quick Links -->
            <div class="footer-section">
                <h4>Platform</h4>
                <ul class="footer-links">
                    <li><a href="#features">Features</a></li>
                    <li><a href="#pricing">Pricing</a></li>
                    <li><a href="#">About Us</a></li>
                    <li><a href="#">Careers</a></li>
                </ul>
            </div>

            <!-- Resources -->
            <div class="footer-section">
                <h4>Resources</h4>
                <ul class="footer-links">
                    <li><a href="#">Documentation</a></li>
                    <li><a href="#">API</a></li>
                    <li><a href="#">Blog</a></li>
                    <li><a href="#">Help Center</a></li>
                </ul>
            </div>

            <!-- Newsletter -->
            <div class="footer-section">
                <h4>Stay Updated</h4>
                <p class="text-secondary">Get the latest updates and offers.</p>
                <form class="newsletter-form">
                    <input type="email" placeholder="Enter your email">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-paper-plane"></i>
                    </button>
                </form>
            </div>
        </div>

        <div class="footer-bottom">
            <p class="text-secondary">
                © 2025 E.U.R.E.K.A. All rights reserved.
            </p>
            <div class="footer-bottom-links">
                <a href="#">Privacy Policy</a>
                <a href="#">Terms of Service</a>
                <a href="#">Cookie Policy</a>
            </div>
        </div>
    </div>
</footer>
```

### Task 7.2: Style Footer

```css
/* Footer */
.footer {
    background: var(--secondary-bg);
    border-top: 1px solid var(--border-color);
    padding: 4rem 0 2rem;
    margin-top: 6rem;
}

.footer-grid {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1.5fr;
    gap: 3rem;
    margin-bottom: 3rem;
}

.footer-logo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
    font-size: 1.5rem;
    font-weight: 700;
}

.footer-section h4 {
    margin-bottom: 1.5rem;
    font-size: 1.1rem;
}

.footer-links {
    list-style: none;
}

.footer-links li {
    margin-bottom: 0.75rem;
}

.footer-links a {
    color: var(--text-secondary);
    transition: var(--transition-normal);
}

.footer-links a:hover {
    color: var(--primary-color);
}

.social-links {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
}

.social-link {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-secondary);
    transition: var(--transition-normal);
}

.social-link:hover {
    background: var(--primary-color);
    color: white;
    border-color: var(--primary-color);
    transform: translateY(-3px);
}

.newsletter-form {
    display: flex;
    gap: 0.5rem;
    margin-top: 1rem;
}

.newsletter-form input {
    flex: 1;
    padding: 0.75rem 1rem;
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    color: var(--text-primary);
}

.newsletter-form input:focus {
    outline: none;
    border-color: var(--primary-color);
}

.newsletter-form button {
    padding: 0.75rem 1.5rem;
}

.footer-bottom {
    padding-top: 2rem;
    border-top: 1px solid var(--border-color);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.footer-bottom-links {
    display: flex;
    gap: 2rem;
}

.footer-bottom-links a {
    color: var(--text-secondary);
    font-size: 0.9rem;
}

.footer-bottom-links a:hover {
    color: var(--primary-color);
}

/* Responsive */
@media (max-width: 1024px) {
    .footer-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 768px) {
    .footer-grid {
        grid-template-columns: 1fr;
    }

    .footer-bottom {
        flex-direction: column;
        gap: 1rem;
        text-align: center;
    }
}
```

**Validation:**
- [ ] 4-column footer grid
- [ ] Social icons with hover effects
- [ ] Newsletter form functional
- [ ] Bottom section with copyright
- [ ] Responsive on mobile

---

## Phase 8: JavaScript Interactivity

### Task 8.1: Smooth Scroll Navigation

Add to `script.js`:

```javascript
// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));

        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
```

### Task 8.2: Active Navigation State

```javascript
// Update active navigation link on scroll
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-link');

window.addEventListener('scroll', () => {
    let current = '';

    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;

        if (window.pageYOffset >= sectionTop - 100) {
            current = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
});
```

### Task 8.3: Scroll Animations

```javascript
// Intersection Observer for scroll animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe all elements with animate-on-scroll class
document.querySelectorAll('.animate-on-scroll').forEach(el => {
    observer.observe(el);
});
```

### Task 8.4: Mobile Menu Toggle

```javascript
// Mobile menu functionality
const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
const navMenu = document.querySelector('.nav-menu');

if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');

        // Toggle icon
        const icon = mobileMenuToggle.querySelector('i');
        icon.classList.toggle('fa-bars');
        icon.classList.toggle('fa-times');
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.navbar')) {
            navMenu.classList.remove('active');
            const icon = mobileMenuToggle.querySelector('i');
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
        }
    });
}
```

### Task 8.5: Search Functionality

```javascript
// Search bar functionality
const searchInput = document.querySelector('.search-bar input');

if (searchInput) {
    searchInput.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        console.log('Searching for:', searchTerm);

        // Add your search logic here
        // For now, just log to console
    });
}
```

### Task 8.6: Newsletter Form

```javascript
// Newsletter form submission
const newsletterForm = document.querySelector('.newsletter-form');

if (newsletterForm) {
    newsletterForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const email = newsletterForm.querySelector('input[type="email"]').value;

        // Basic email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (emailRegex.test(email)) {
            console.log('Newsletter signup:', email);
            alert('Thank you for subscribing!');
            newsletterForm.reset();
        } else {
            alert('Please enter a valid email address.');
        }
    });
}
```

**Validation:**
- [ ] Smooth scroll working
- [ ] Active nav updates on scroll
- [ ] Scroll animations trigger
- [ ] Mobile menu toggles
- [ ] Search input responsive
- [ ] Newsletter form validates

---

## Phase 9: Responsive Design

### Task 9.1: Mobile Menu Styles

Add to `styles.css`:

```css
/* Mobile Menu */
@media (max-width: 1024px) {
    .nav-menu {
        position: fixed;
        top: 80px;
        left: -100%;
        width: 300px;
        height: calc(100vh - 80px);
        background: var(--card-bg);
        border-right: 1px solid var(--border-color);
        flex-direction: column;
        padding: 2rem;
        transition: var(--transition-normal);
        z-index: 999;
    }

    .nav-menu.active {
        left: 0;
    }

    .nav-item {
        width: 100%;
    }

    .nav-link {
        width: 100%;
        padding: 1rem;
    }
}
```

### Task 9.2: Tablet Optimizations

```css
@media (max-width: 768px) {
    /* Typography */
    h1 { font-size: 2rem; }
    h2 { font-size: 1.75rem; }
    h3 { font-size: 1.5rem; }

    /* Spacing */
    .container {
        padding: 0 1rem;
    }

    section {
        padding: 3rem 0;
    }

    /* Hero */
    .hero-buttons {
        flex-direction: column;
    }

    .btn-lg {
        width: 100%;
    }
}
```

### Task 9.3: Mobile Optimizations

```css
@media (max-width: 480px) {
    /* Navigation */
    .search-bar {
        display: none;
    }

    .nav-actions {
        gap: 0.5rem;
    }

    .nav-actions .btn {
        padding: 0.5rem 1rem;
        font-size: 0.85rem;
    }

    /* Hero */
    .hero {
        min-height: auto;
        padding: 2rem 0;
    }

    .hero-content h1 {
        font-size: 1.75rem;
    }

    .stat-number {
        font-size: 2rem;
    }

    /* Features */
    .features-grid {
        gap: 1.5rem;
    }

    .feature-card {
        padding: 1.5rem;
    }
}
```

**Validation:**
- [ ] Mobile menu slides in/out
- [ ] Typography scales appropriately
- [ ] Grids stack on mobile
- [ ] Buttons full width on mobile
- [ ] All content readable

---

## Phase 10: Performance & Polish

### Task 10.1: Image Optimization

Create placeholder images or add instructions:

```javascript
// Add to script.js - Lazy load images
document.addEventListener('DOMContentLoaded', () => {
    const images = document.querySelectorAll('img[data-src]');

    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
});
```

### Task 10.2: Loading States

```css
/* Loading Animation */
@keyframes shimmer {
    0% {
        background-position: -1000px 0;
    }
    100% {
        background-position: 1000px 0;
    }
}

.skeleton {
    background: linear-gradient(
        90deg,
        var(--card-bg) 0%,
        rgba(255, 255, 255, 0.05) 50%,
        var(--card-bg) 100%
    );
    background-size: 1000px 100%;
    animation: shimmer 2s infinite;
}
```

### Task 10.3: Accessibility Enhancements

Add to HTML elements:

```html
<!-- Example: Add ARIA labels -->
<button class="btn btn-primary" aria-label="Start learning for free">
    Start Learning Free
</button>

<nav class="navbar" role="navigation" aria-label="Main navigation">
    <!-- nav content -->
</nav>
```

### Task 10.4: SEO Meta Tags

Add to `<head>`:

```html
<!-- SEO -->
<meta name="description" content="E.U.R.E.K.A - Empowering Universal Research, Education, Knowledge & Achievement. Learn from 10K+ courses with AI-powered tutoring.">
<meta name="keywords" content="online learning, education, courses, AI tutoring, certifications">
<meta name="author" content="E.U.R.E.K.A">

<!-- Open Graph -->
<meta property="og:title" content="E.U.R.E.K.A - Educational Platform">
<meta property="og:description" content="Explore Ideas. Master Knowledge. Drive Innovation.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://yoursite.com">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="E.U.R.E.K.A - Educational Platform">
```

**Validation:**
- [ ] Images lazy load
- [ ] Loading states present
- [ ] ARIA labels added
- [ ] Meta tags complete

---

## Phase 11: Testing & Quality Assurance

### Task 11.1: Browser Testing Checklist

Test in:
- [ ] Chrome/Edge (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Mobile Chrome (Android)
- [ ] Mobile Safari (iOS)

### Task 11.2: Responsiveness Testing

Test at breakpoints:
- [ ] 1920px (Desktop)
- [ ] 1024px (Tablet landscape)
- [ ] 768px (Tablet portrait)
- [ ] 480px (Mobile landscape)
- [ ] 375px (Mobile portrait)

### Task 11.3: Performance Testing

Run checks:
- [ ] Google Lighthouse (aim for 90+ score)
- [ ] Page load under 3 seconds
- [ ] First Contentful Paint under 1.5s
- [ ] No console errors
- [ ] All images optimized

### Task 11.4: Accessibility Testing

Verify:
- [ ] Keyboard navigation works
- [ ] Focus indicators visible
- [ ] Alt text on all images
- [ ] Color contrast passes WCAG AA
- [ ] Screen reader compatible

### Task 11.5: Functionality Testing

Confirm:
- [ ] All navigation links work
- [ ] Smooth scroll functions
- [ ] Mobile menu toggles
- [ ] Forms validate properly
- [ ] Hover effects smooth
- [ ] Animations trigger correctly

---

## Phase 12: Documentation & Deployment

### Task 12.1: Create README

Create `README.md`:

```markdown
# E.U.R.E.K.A Landing Page

Modern, responsive landing page for educational platform.

## Features
- Responsive design (mobile-first)
- Smooth scroll animations
- Modern UI with gradients
- No frameworks (pure HTML/CSS/JS)

## Quick Start
1. Clone repository
2. Open `index.html` in browser
3. Or serve with: `python3 -m http.server 8000`

## File Structure
- `index.html` - Main page
- `styles.css` - All styles
- `script.js` - Interactivity
- `images/` - Image assets

## Browser Support
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## License
MIT
```

### Task 12.2: Deployment Instructions

Add deployment guide to README:

```markdown
## Deployment

### GitHub Pages
1. Push to GitHub
2. Settings → Pages → Deploy from main branch
3. Site live at: `username.github.io/repo`

### Netlify
1. Drag folder to netlify.com/drop
2. Instant deployment

### Vercel
```bash
npm i -g vercel
vercel --prod
```
```

---

## Final Validation Checklist

### Code Quality
- [ ] HTML validates (W3C validator)
- [ ] CSS validates
- [ ] No JavaScript errors
- [ ] Code is commented
- [ ] Files properly organized

### Design
- [ ] Matches specifications
- [ ] Consistent spacing
- [ ] Typography hierarchy clear
- [ ] Colors from design system
- [ ] Icons display correctly

### Functionality
- [ ] All sections present
- [ ] Navigation works
- [ ] Forms validate
- [ ] Animations smooth
- [ ] Mobile menu functional

### Performance
- [ ] Page loads quickly
- [ ] Images optimized
- [ ] No render-blocking resources
- [ ] Smooth scrolling
- [ ] No layout shifts

### Accessibility
- [ ] Keyboard navigable
- [ ] Screen reader friendly
- [ ] Good color contrast
- [ ] Alt text present
- [ ] Focus indicators visible

### Responsive
- [ ] Works on all screen sizes
- [ ] No horizontal scroll
- [ ] Touch targets adequate
- [ ] Text readable
- [ ] Images scale properly

---

## Success Criteria Summary

Your landing page is complete when:

✅ **Structure**
- All sections implemented (nav, hero, features, pricing, footer)
- Semantic HTML throughout
- Proper heading hierarchy

✅ **Styling**
- CSS variables for theming
- Responsive grid layouts
- Smooth animations
- Modern design aesthetic

✅ **Interactivity**
- Smooth scroll navigation
- Active state updates
- Mobile menu works
- Forms validate

✅ **Quality**
- No console errors
- Cross-browser compatible
- Mobile-optimized
- Passes Lighthouse audit

✅ **Documentation**
- README complete
- Code commented
- Deployment guide included

---

## Agent Deliverables

Upon completion, provide:

1. **Complete source code**
   - `index.html`
   - `styles.css`
   - `script.js`
   - `README.md`

2. **Test results**
   - Browser compatibility report
   - Lighthouse scores
   - Responsiveness screenshots

3. **Deployment URL**
   - Live demo link
   - GitHub repository (optional)

4. **Summary report**
   - Features implemented
   - Known issues (if any)
   - Recommendations for improvement

---

## Estimated Completion Time

- **Phase 1-2** (Setup & Foundation): 5 minutes
- **Phase 3** (Navigation): 5 minutes
- **Phase 4** (Hero): 5 minutes
- **Phase 5** (Features): 8 minutes
- **Phase 6** (Pricing): 5 minutes
- **Phase 7** (Footer): 5 minutes
- **Phase 8** (JavaScript): 8 minutes
- **Phase 9** (Responsive): 5 minutes
- **Phase 10** (Polish): 5 minutes
- **Phase 11** (Testing): 10 minutes
- **Phase 12** (Documentation): 3 minutes

**Total: ~60 minutes** (agent execution time)

---

## Notes for Agent

- Follow phases sequentially for best results
- Test each component before moving to next phase
- Use provided code examples as templates
- Validate frequently using checklists
- Document any deviations from spec
- Optimize for performance throughout
- Prioritize accessibility
- Keep code clean and commented

---

## Support Resources

If you encounter issues:

1. **HTML Validation**: https://validator.w3.org/
2. **CSS Validation**: https://jigsaw.w3.org/css-validator/
3. **Lighthouse**: Chrome DevTools → Lighthouse tab
4. **Font Awesome Icons**: https://fontawesome.com/icons
5. **Can I Use**: https://caniuse.com/ (browser support)

---

**End of Agent Instructions**

*You may now proceed with building the landing page. Follow each phase sequentially and validate before moving forward. Good luck!*
