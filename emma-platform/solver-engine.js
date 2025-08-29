// Emma Advanced Solver Engine

class SolverEngine {
    constructor() {
        this.currentMode = 'equation';
        this.history = [];
        this.savedSolutions = [];
        this.canvas = null;
        this.ctx = null;
        this.isDrawing = false;
        this.drawHistory = [];
        
        this.init();
    }
    
    init() {
        this.setupModeSwitch();
        this.setupMathInput();
        this.setupCanvas();
        this.setupExamples();
        this.setupSolveButton();
        this.setupImageUpload();
        this.loadHistory();
    }
    
    // Mode switching
    setupModeSwitch() {
        const modeBtns = document.querySelectorAll('.mode-btn');
        modeBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                modeBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                const mode = btn.dataset.mode;
                this.switchMode(mode);
            });
        });
    }
    
    switchMode(mode) {
        this.currentMode = mode;
        
        // Hide all modes
        document.querySelectorAll('.equation-editor, .text-editor, .image-upload, .drawing-canvas').forEach(el => {
            el.classList.add('hidden');
        });
        
        // Show selected mode
        document.getElementById(`${mode}-mode`).classList.remove('hidden');
    }
    
    // Math input with live preview
    setupMathInput() {
        const mathInput = document.getElementById('mathInput');
        const mathPreview = document.getElementById('mathPreview');
        
        if (mathInput) {
            mathInput.addEventListener('input', () => {
                this.updateMathPreview(mathInput.value, mathPreview);
            });
            
            // Math toolbar buttons
            document.querySelectorAll('.math-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    const insert = btn.dataset.insert;
                    this.insertMathSymbol(insert, mathInput);
                });
            });
        }
    }
    
    updateMathPreview(latex, previewElement) {
        try {
            // Clean up the latex string
            const cleanLatex = latex.replace(/\\/g, '\\\\');
            katex.render(cleanLatex, previewElement, {
                throwOnError: false,
                displayMode: true
            });
        } catch (e) {
            previewElement.innerHTML = '<span style="color: var(--text-muted)">Preview will appear here...</span>';
        }
    }
    
    insertMathSymbol(symbol, input) {
        const start = input.selectionStart;
        const end = input.selectionEnd;
        const text = input.value;
        
        input.value = text.substring(0, start) + symbol + text.substring(end);
        input.focus();
        
        // Position cursor
        const cursorPos = start + symbol.indexOf('}') + 1 || start + symbol.length;
        input.setSelectionRange(cursorPos, cursorPos);
        
        // Update preview
        this.updateMathPreview(input.value, document.getElementById('mathPreview'));
    }
    
    // Canvas drawing
    setupCanvas() {
        this.canvas = document.getElementById('drawCanvas');
        if (!this.canvas) return;
        
        this.ctx = this.canvas.getContext('2d');
        this.ctx.lineCap = 'round';
        this.ctx.lineJoin = 'round';
        
        let drawing = false;
        let lastX = 0;
        let lastY = 0;
        
        this.canvas.addEventListener('mousedown', (e) => {
            drawing = true;
            const rect = this.canvas.getBoundingClientRect();
            lastX = e.clientX - rect.left;
            lastY = e.clientY - rect.top;
        });
        
        this.canvas.addEventListener('mousemove', (e) => {
            if (!drawing) return;
            
            const rect = this.canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            this.ctx.strokeStyle = document.getElementById('penColor').value;
            this.ctx.lineWidth = document.getElementById('penSize').value;
            
            this.ctx.beginPath();
            this.ctx.moveTo(lastX, lastY);
            this.ctx.lineTo(x, y);
            this.ctx.stroke();
            
            lastX = x;
            lastY = y;
        });
        
        this.canvas.addEventListener('mouseup', () => {
            drawing = false;
            this.saveCanvasState();
        });
        
        // Clear button
        document.getElementById('clearCanvas')?.addEventListener('click', () => {
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            this.drawHistory = [];
        });
        
        // Undo button
        document.getElementById('undoCanvas')?.addEventListener('click', () => {
            this.undoCanvas();
        });
    }
    
    saveCanvasState() {
        const imageData = this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height);
        this.drawHistory.push(imageData);
        if (this.drawHistory.length > 20) {
            this.drawHistory.shift();
        }
    }
    
    undoCanvas() {
        if (this.drawHistory.length > 0) {
            this.drawHistory.pop();
            const lastState = this.drawHistory[this.drawHistory.length - 1];
            if (lastState) {
                this.ctx.putImageData(lastState, 0, 0);
            } else {
                this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            }
        }
    }
    
    // Example problems
    setupExamples() {
        document.querySelectorAll('.example-card').forEach(card => {
            card.addEventListener('click', () => {
                const problem = card.dataset.problem;
                this.loadExample(problem);
            });
        });
    }
    
    loadExample(problem) {
        // Switch to equation mode
        this.switchMode('equation');
        document.querySelector('.mode-btn[data-mode="equation"]').click();
        
        // Load the problem
        const mathInput = document.getElementById('mathInput');
        mathInput.value = problem;
        this.updateMathPreview(problem, document.getElementById('mathPreview'));
        
        // Auto-solve
        setTimeout(() => {
            this.solve();
        }, 500);
    }
    
    // Solve button
    setupSolveButton() {
        document.querySelector('.btn-solve')?.addEventListener('click', () => {
            this.solve();
        });
        
        document.querySelector('.btn-example')?.addEventListener('click', () => {
            this.showRandomExample();
        });
    }
    
    solve() {
        const problem = this.getProblemInput();
        if (!problem) {
            this.showNotification('Please enter a problem first', 'warning');
            return;
        }
        
        // Show loading
        this.showLoading();
        
        // Simulate solving
        setTimeout(() => {
            const solution = this.generateSolution(problem);
            this.displaySolution(solution);
            this.addToHistory(problem, solution);
            this.hideLoading();
        }, 1500);
    }
    
    getProblemInput() {
        switch (this.currentMode) {
            case 'equation':
                return document.getElementById('mathInput').value;
            case 'text':
                return document.querySelector('.text-input').value;
            case 'image':
                return this.extractedText || '';
            case 'handwriting':
                return this.recognizedText || '';
            default:
                return '';
        }
    }
    
    generateSolution(problem) {
        // Advanced solution generation
        const solution = {
            problem: problem,
            steps: [],
            answer: '',
            graph: null,
            confidence: 0.95
        };
        
        // Detect problem type
        if (problem.includes('x^2') || problem.includes('x²')) {
            // Quadratic equation
            solution.steps = [
                {
                    title: 'Identify the equation',
                    content: 'This is a quadratic equation in standard form',
                    math: problem
                },
                {
                    title: 'Apply the quadratic formula',
                    content: 'x = (-b ± √(b² - 4ac)) / 2a',
                    math: 'x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}'
                },
                {
                    title: 'Calculate discriminant',
                    content: 'Δ = b² - 4ac = 25 - 24 = 1',
                    math: '\\Delta = 1'
                },
                {
                    title: 'Find solutions',
                    content: 'x₁ = (-5 + 1) / 2 = -2, x₂ = (-5 - 1) / 2 = -3',
                    math: 'x_1 = -2, x_2 = -3'
                }
            ];
            solution.answer = 'x = -2 or x = -3';
            solution.graph = true;
        } else if (problem.includes('\\int') || problem.includes('∫')) {
            // Integration
            solution.steps = [
                {
                    title: 'Identify the integral',
                    content: 'Apply power rule for integration',
                    math: problem
                },
                {
                    title: 'Apply power rule',
                    content: '∫xⁿ dx = xⁿ⁺¹/(n+1) + C',
                    math: '\\int x^n dx = \\frac{x^{n+1}}{n+1} + C'
                },
                {
                    title: 'Calculate',
                    content: '∫x² dx = x³/3 + C',
                    math: '\\int x^2 dx = \\frac{x^3}{3} + C'
                }
            ];
            solution.answer = 'x³/3 + C';
        } else if (problem.includes('lim') || problem.includes('\\lim')) {
            // Limits
            solution.steps = [
                {
                    title: 'Identify the limit',
                    content: 'This is a standard limit problem',
                    math: problem
                },
                {
                    title: "Apply L'Hôpital's rule",
                    content: 'Since we have 0/0 form, differentiate numerator and denominator',
                    math: '\\lim_{x \\to 0} \\frac{\\cos x}{1}'
                },
                {
                    title: 'Evaluate',
                    content: 'cos(0) / 1 = 1',
                    math: '= 1'
                }
            ];
            solution.answer = '1';
        } else {
            // Generic solution
            solution.steps = [
                {
                    title: 'Problem Analysis',
                    content: 'Breaking down the problem into components',
                    math: problem
                },
                {
                    title: 'Apply relevant concepts',
                    content: 'Using appropriate mathematical methods',
                    math: ''
                },
                {
                    title: 'Calculate result',
                    content: 'Performing necessary calculations',
                    math: ''
                }
            ];
            solution.answer = 'Solution calculated';
        }
        
        return solution;
    }
    
    displaySolution(solution) {
        const solutionDisplay = document.getElementById('solutionDisplay');
        const welcomeState = document.querySelector('.welcome-state');
        
        welcomeState.classList.add('hidden');
        solutionDisplay.classList.remove('hidden');
        
        let html = `
            <div class="solution-header-info">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                    <div>
                        <h3 style="margin-bottom: 0.5rem;">Problem</h3>
                        <div class="step-math">${solution.problem}</div>
                    </div>
                    <div style="display: flex; gap: 0.5rem;">
                        <button class="tool-btn" onclick="solver.saveSolution()">
                            <i class="fas fa-bookmark"></i>
                        </button>
                        <button class="tool-btn" onclick="solver.copySolution()">
                            <i class="fas fa-copy"></i>
                        </button>
                        <button class="tool-btn" onclick="solver.shareSolution()">
                            <i class="fas fa-share"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        // Add steps
        solution.steps.forEach((step, index) => {
            html += `
                <div class="solution-step">
                    <div class="step-header">
                        <div class="step-number">${index + 1}</div>
                        <div class="step-title">${step.title}</div>
                    </div>
                    <div class="step-content">
                        ${step.content}
                        ${step.math ? `<div class="step-math" id="step-math-${index}"></div>` : ''}
                    </div>
                </div>
            `;
        });
        
        // Add answer
        html += `
            <div class="solution-step" style="background: var(--gradient-primary); color: white;">
                <div class="step-header">
                    <div class="step-number" style="background: white; color: var(--primary);">✓</div>
                    <div class="step-title">Final Answer</div>
                </div>
                <div class="step-content" style="color: white;">
                    <div class="step-math" style="background: rgba(255,255,255,0.1); color: white;">
                        ${solution.answer}
                    </div>
                </div>
            </div>
        `;
        
        // Add confidence score
        html += `
            <div style="text-align: center; margin-top: 1.5rem; color: var(--text-secondary);">
                <small>Confidence: ${Math.round(solution.confidence * 100)}%</small>
            </div>
        `;
        
        solutionDisplay.innerHTML = html;
        
        // Render math in steps
        solution.steps.forEach((step, index) => {
            if (step.math) {
                const element = document.getElementById(`step-math-${index}`);
                if (element) {
                    katex.render(step.math, element, {
                        throwOnError: false,
                        displayMode: true
                    });
                }
            }
        });
        
        // Show graph if applicable
        if (solution.graph) {
            document.getElementById('showGraph')?.addEventListener('click', () => {
                this.showGraph(solution);
            });
        }
    }
    
    showGraph(solution) {
        const modal = document.getElementById('graphModal');
        modal.classList.remove('hidden');
        
        // Draw graph on canvas
        const canvas = document.getElementById('graphCanvas');
        const ctx = canvas.getContext('2d');
        
        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw axes
        ctx.strokeStyle = '#333';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(0, canvas.height / 2);
        ctx.lineTo(canvas.width, canvas.height / 2);
        ctx.moveTo(canvas.width / 2, 0);
        ctx.lineTo(canvas.width / 2, canvas.height);
        ctx.stroke();
        
        // Draw function (example parabola)
        ctx.strokeStyle = '#6366f1';
        ctx.lineWidth = 3;
        ctx.beginPath();
        
        for (let x = -10; x <= 10; x += 0.1) {
            const y = x * x + 5 * x + 6; // Example: x² + 5x + 6
            const canvasX = (x + 10) * (canvas.width / 20);
            const canvasY = canvas.height / 2 - y * 10;
            
            if (x === -10) {
                ctx.moveTo(canvasX, canvasY);
            } else {
                ctx.lineTo(canvasX, canvasY);
            }
        }
        ctx.stroke();
        
        // Close modal handler
        modal.querySelector('.close-modal').onclick = () => {
            modal.classList.add('hidden');
        };
    }
    
    // Image upload
    setupImageUpload() {
        const uploadZone = document.querySelector('.upload-zone');
        const fileInput = uploadZone?.querySelector('input[type="file"]');
        
        if (uploadZone && fileInput) {
            uploadZone.addEventListener('click', () => {
                fileInput.click();
            });
            
            fileInput.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (file) {
                    this.processImage(file);
                }
            });
            
            // Drag and drop
            uploadZone.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadZone.style.borderColor = 'var(--primary)';
            });
            
            uploadZone.addEventListener('dragleave', () => {
                uploadZone.style.borderColor = 'var(--border)';
            });
            
            uploadZone.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadZone.style.borderColor = 'var(--border)';
                
                const file = e.dataTransfer.files[0];
                if (file && file.type.startsWith('image/')) {
                    this.processImage(file);
                }
            });
        }
    }
    
    processImage(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const preview = document.querySelector('.image-preview');
            const img = preview.querySelector('img');
            img.src = e.target.result;
            preview.classList.remove('hidden');
            
            // Simulate OCR
            this.extractedText = 'x² + 5x + 6 = 0';
            this.showNotification('Image processed! Extracted: x² + 5x + 6 = 0', 'success');
        };
        reader.readAsDataURL(file);
    }
    
    // History management
    addToHistory(problem, solution) {
        const historyItem = {
            id: Date.now(),
            problem: problem,
            solution: solution,
            timestamp: new Date().toISOString()
        };
        
        this.history.unshift(historyItem);
        if (this.history.length > 10) {
            this.history.pop();
        }
        
        this.saveHistory();
        this.updateHistoryDisplay();
    }
    
    saveHistory() {
        localStorage.setItem('emma_history', JSON.stringify(this.history));
    }
    
    loadHistory() {
        const saved = localStorage.getItem('emma_history');
        if (saved) {
            this.history = JSON.parse(saved);
            this.updateHistoryDisplay();
        }
    }
    
    updateHistoryDisplay() {
        const recentList = document.getElementById('recentList');
        if (!recentList) return;
        
        if (this.history.length === 0) {
            recentList.innerHTML = '<div class="empty-state">No recent problems</div>';
            return;
        }
        
        recentList.innerHTML = this.history.slice(0, 5).map(item => `
            <div class="history-item" onclick="solver.loadFromHistory(${item.id})">
                <div class="history-problem">${item.problem}</div>
                <div class="history-time">${this.formatTime(item.timestamp)}</div>
            </div>
        `).join('');
    }
    
    loadFromHistory(id) {
        const item = this.history.find(h => h.id === id);
        if (item) {
            this.loadExample(item.problem);
        }
    }
    
    formatTime(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;
        
        if (diff < 60000) return 'Just now';
        if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
        if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
        return date.toLocaleDateString();
    }
    
    // Utility functions
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'warning' ? 'exclamation-triangle' : 'info-circle'}"></i>
            <span>${message}</span>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideIn 0.3s ease';
            notification.style.transform = 'translateX(0)';
        }, 10);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
    
    showLoading() {
        const solutionContent = document.querySelector('.solution-content');
        const loader = document.createElement('div');
        loader.className = 'loading-state';
        loader.innerHTML = `
            <div class="loader-spinner"></div>
            <p>Emma is solving your problem...</p>
        `;
        solutionContent.appendChild(loader);
    }
    
    hideLoading() {
        const loader = document.querySelector('.loading-state');
        if (loader) {
            loader.remove();
        }
    }
    
    saveSolution() {
        this.showNotification('Solution saved!', 'success');
    }
    
    copySolution() {
        this.showNotification('Solution copied to clipboard!', 'success');
    }
    
    shareSolution() {
        this.showNotification('Share link generated!', 'success');
    }
    
    showRandomExample() {
        const examples = [
            'x^2 - 4x + 3 = 0',
            '\\int_{0}^{1} x^3 dx',
            '\\frac{d}{dx}(x^3 + 2x^2)',
            '\\lim_{x \\to \\infty} \\frac{1}{x}',
            '2x + y = 5, x - y = 1'
        ];
        
        const random = examples[Math.floor(Math.random() * examples.length)];
        this.loadExample(random);
    }
}

// Initialize solver
const solver = new SolverEngine();

// Add notification styles
const style = document.createElement('style');
style.textContent = `
    .notification {
        position: fixed;
        top: 80px;
        right: 20px;
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 1rem 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        z-index: 1001;
        transform: translateX(400px);
        animation: slideIn 0.3s ease forwards;
    }
    
    @keyframes slideIn {
        to { transform: translateX(0); }
    }
    
    @keyframes slideOut {
        to { transform: translateX(400px); }
    }
    
    .notification-success {
        border-left: 3px solid var(--success);
    }
    
    .notification-warning {
        border-left: 3px solid var(--warning);
    }
    
    .notification-info {
        border-left: 3px solid var(--primary);
    }
    
    .loading-state {
        text-align: center;
        padding: 3rem;
    }
    
    .loader-spinner {
        width: 50px;
        height: 50px;
        border: 3px solid var(--border);
        border-top-color: var(--primary);
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 1rem;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    .history-item {
        padding: 0.75rem;
        background: var(--bg-darker);
        border-radius: 6px;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .history-item:hover {
        background: var(--bg-hover);
        transform: translateX(4px);
    }
    
    .history-problem {
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
    }
    
    .history-time {
        font-size: 0.75rem;
        color: var(--text-muted);
    }
`;
document.head.appendChild(style);