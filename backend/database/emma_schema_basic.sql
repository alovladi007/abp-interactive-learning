-- EMMA Database Schema
-- AI STEM Tutor - User progress, quiz questions, and study sessions

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (shared with Dr. Sarah)
-- If not exists from main schema
CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- EMMA-specific user profile
CREATE TABLE emma_user_profiles (
    profile_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    grade_level VARCHAR(50),
    subjects_of_interest TEXT[],
    learning_goals TEXT,
    target_hours_per_week INT DEFAULT 5,
    timezone VARCHAR(50) DEFAULT 'UTC',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id)
);

-- Problem solving history
CREATE TABLE emma_solutions (
    solution_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    problem_type VARCHAR(50) NOT NULL,
    difficulty VARCHAR(20) NOT NULL,
    question TEXT NOT NULL,
    solution JSONB NOT NULL,
    steps JSONB,
    final_answer TEXT,
    latex_answer TEXT,
    computation_time_ms INT,
    tags TEXT[],
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX idx_emma_solutions_user_id ON emma_solutions(user_id);
CREATE INDEX idx_emma_solutions_type ON emma_solutions(problem_type);
CREATE INDEX idx_emma_solutions_created_at ON emma_solutions(created_at DESC);

-- Quiz question bank
CREATE TABLE emma_quiz_questions (
    question_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    topic VARCHAR(100) NOT NULL,
    subtopic VARCHAR(100),
    difficulty VARCHAR(20) NOT NULL,
    question TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    distractors JSONB NOT NULL,
    explanation TEXT,
    latex_representation TEXT,
    problem_type VARCHAR(50),
    tags TEXT[],
    created_by UUID REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- Create indexes for quiz questions
CREATE INDEX idx_quiz_topic ON emma_quiz_questions(topic);
CREATE INDEX idx_quiz_difficulty ON emma_quiz_questions(difficulty);
CREATE INDEX idx_quiz_active ON emma_quiz_questions(is_active);

-- Spaced repetition user progress
CREATE TABLE emma_user_progress (
    progress_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    question_id UUID REFERENCES emma_quiz_questions(question_id) ON DELETE CASCADE,
    ease_factor FLOAT DEFAULT 2.5 CHECK (ease_factor >= 1.3),
    interval_days INT DEFAULT 1 CHECK (interval_days >= 0),
    repetitions INT DEFAULT 0 CHECK (repetitions >= 0),
    last_reviewed TIMESTAMP,
    next_review TIMESTAMP,
    total_reviews INT DEFAULT 0,
    correct_reviews INT DEFAULT 0,
    accuracy_percentage FLOAT GENERATED ALWAYS AS (
        CASE
            WHEN total_reviews > 0 THEN (correct_reviews::FLOAT / total_reviews::FLOAT * 100)
            ELSE 0
        END
    ) STORED,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, question_id)
);

-- Create indexes for spaced repetition
CREATE INDEX idx_progress_user_id ON emma_user_progress(user_id);
CREATE INDEX idx_progress_next_review ON emma_user_progress(next_review);
CREATE INDEX idx_progress_user_next_review ON emma_user_progress(user_id, next_review);

-- Study sessions
CREATE TABLE emma_study_sessions (
    session_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    topic VARCHAR(100),
    problem_type VARCHAR(50),
    duration_minutes INT,
    problems_attempted INT DEFAULT 0,
    problems_solved INT DEFAULT 0,
    accuracy_percentage FLOAT GENERATED ALWAYS AS (
        CASE
            WHEN problems_attempted > 0 THEN (problems_solved::FLOAT / problems_attempted::FLOAT * 100)
            ELSE 0
        END
    ) STORED,
    started_at TIMESTAMP DEFAULT NOW(),
    ended_at TIMESTAMP,
    notes TEXT
);

-- Create indexes for study sessions
CREATE INDEX idx_sessions_user_id ON emma_study_sessions(user_id);
CREATE INDEX idx_sessions_started_at ON emma_study_sessions(started_at DESC);

-- Answer submissions (detailed tracking)
CREATE TABLE emma_answer_submissions (
    submission_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    question_id UUID REFERENCES emma_quiz_questions(question_id) ON DELETE CASCADE,
    session_id UUID REFERENCES emma_study_sessions(session_id) ON DELETE SET NULL,
    selected_answer TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL,
    time_taken_seconds INT,
    quality_score INT CHECK (quality_score BETWEEN 0 AND 5),
    submitted_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for answer submissions
CREATE INDEX idx_submissions_user_id ON emma_answer_submissions(user_id);
CREATE INDEX idx_submissions_question_id ON emma_answer_submissions(question_id);
CREATE INDEX idx_submissions_submitted_at ON emma_answer_submissions(submitted_at DESC);

-- Topic mastery tracking
CREATE TABLE emma_topic_mastery (
    mastery_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    topic VARCHAR(100) NOT NULL,
    subtopic VARCHAR(100),
    total_questions INT DEFAULT 0,
    mastered_questions INT DEFAULT 0,
    mastery_percentage FLOAT GENERATED ALWAYS AS (
        CASE
            WHEN total_questions > 0 THEN (mastered_questions::FLOAT / total_questions::FLOAT * 100)
            ELSE 0
        END
    ) STORED,
    average_ease_factor FLOAT,
    last_studied TIMESTAMP,
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, topic, subtopic)
);

-- Create indexes for topic mastery
CREATE INDEX idx_mastery_user_id ON emma_topic_mastery(user_id);
CREATE INDEX idx_mastery_topic ON emma_topic_mastery(topic);
CREATE INDEX idx_mastery_percentage ON emma_topic_mastery(mastery_percentage);

-- Visualizations cache
CREATE TABLE emma_visualizations (
    viz_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    expression TEXT NOT NULL,
    plot_type VARCHAR(50) NOT NULL,
    parameters JSONB,
    image_data TEXT NOT NULL, -- Base64 encoded
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP DEFAULT NOW() + INTERVAL '7 days'
);

-- Create index for visualization cache
CREATE INDEX idx_viz_expression ON emma_visualizations(expression, plot_type);
CREATE INDEX idx_viz_expires_at ON emma_visualizations(expires_at);

-- Achievement system
CREATE TABLE emma_achievements (
    achievement_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    icon VARCHAR(100),
    requirement JSONB NOT NULL, -- Flexible requirement definition
    points INT DEFAULT 0,
    rarity VARCHAR(20) DEFAULT 'common' CHECK (rarity IN ('common', 'uncommon', 'rare', 'epic', 'legendary'))
);

-- User achievements
CREATE TABLE emma_user_achievements (
    user_achievement_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    achievement_id UUID REFERENCES emma_achievements(achievement_id) ON DELETE CASCADE,
    earned_at TIMESTAMP DEFAULT NOW(),
    progress INT DEFAULT 0,
    UNIQUE(user_id, achievement_id)
);

-- Create indexes for achievements
CREATE INDEX idx_user_achievements_user_id ON emma_user_achievements(user_id);
CREATE INDEX idx_user_achievements_earned_at ON emma_user_achievements(earned_at DESC);

-- Functions and Triggers

-- Update timestamp function
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for user progress
CREATE TRIGGER update_emma_progress_timestamp
BEFORE UPDATE ON emma_user_progress
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- Trigger for topic mastery
CREATE TRIGGER update_emma_mastery_timestamp
BEFORE UPDATE ON emma_topic_mastery
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- Trigger for user profiles
CREATE TRIGGER update_emma_profile_timestamp
BEFORE UPDATE ON emma_user_profiles
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- Function to update topic mastery
CREATE OR REPLACE FUNCTION update_topic_mastery()
RETURNS TRIGGER AS $$
BEGIN
    -- Update or insert topic mastery
    INSERT INTO emma_topic_mastery (user_id, topic, subtopic, total_questions, mastered_questions)
    SELECT
        NEW.user_id,
        q.topic,
        q.subtopic,
        COUNT(*),
        SUM(CASE WHEN up.repetitions >= 5 THEN 1 ELSE 0 END)
    FROM emma_user_progress up
    JOIN emma_quiz_questions q ON up.question_id = q.question_id
    WHERE up.user_id = NEW.user_id AND q.topic = (SELECT topic FROM emma_quiz_questions WHERE question_id = NEW.question_id)
    GROUP BY q.topic, q.subtopic
    ON CONFLICT (user_id, topic, subtopic)
    DO UPDATE SET
        total_questions = EXCLUDED.total_questions,
        mastered_questions = EXCLUDED.mastered_questions,
        last_studied = NOW();

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to update topic mastery after answer
CREATE TRIGGER update_mastery_after_answer
AFTER INSERT OR UPDATE ON emma_user_progress
FOR EACH ROW
EXECUTE FUNCTION update_topic_mastery();

-- Views for analytics

-- User performance summary view
CREATE OR REPLACE VIEW emma_user_performance AS
SELECT
    u.user_id,
    u.username,
    COUNT(DISTINCT es.solution_id) as total_problems_solved,
    COUNT(DISTINCT eas.submission_id) as total_quiz_answers,
    ROUND(AVG(CASE WHEN eas.is_correct THEN 100.0 ELSE 0.0 END), 2) as overall_accuracy,
    COUNT(DISTINCT ess.session_id) as total_study_sessions,
    COALESCE(SUM(ess.duration_minutes), 0) as total_study_minutes,
    COUNT(DISTINCT eua.achievement_id) as achievements_earned,
    ROUND(AVG(etm.mastery_percentage), 2) as average_mastery_percentage
FROM users u
LEFT JOIN emma_solutions es ON u.user_id = es.user_id
LEFT JOIN emma_answer_submissions eas ON u.user_id = eas.user_id
LEFT JOIN emma_study_sessions ess ON u.user_id = ess.user_id
LEFT JOIN emma_user_achievements eua ON u.user_id = eua.user_id
LEFT JOIN emma_topic_mastery etm ON u.user_id = etm.user_id
GROUP BY u.user_id, u.username;

-- Daily activity view
CREATE OR REPLACE VIEW emma_daily_activity AS
SELECT
    user_id,
    DATE(created_at) as activity_date,
    COUNT(DISTINCT solution_id) as problems_solved,
    COUNT(DISTINCT CASE WHEN problem_type = 'algebra' THEN solution_id END) as algebra_problems,
    COUNT(DISTINCT CASE WHEN problem_type = 'calculus' THEN solution_id END) as calculus_problems,
    ROUND(AVG(computation_time_ms)::NUMERIC, 2) as avg_computation_time
FROM emma_solutions
GROUP BY user_id, DATE(created_at);

-- Insert sample achievements
INSERT INTO emma_achievements (name, description, icon, requirement, points, rarity) VALUES
('First Steps', 'Solve your first problem', '🎯', '{"problems_solved": 1}', 10, 'common'),
('Problem Solver', 'Solve 10 problems', '⭐', '{"problems_solved": 10}', 50, 'common'),
('Math Whiz', 'Solve 100 problems', '🌟', '{"problems_solved": 100}', 200, 'uncommon'),
('Calculus Master', 'Solve 50 calculus problems', '📐', '{"calculus_problems": 50}', 150, 'rare'),
('Algebra Expert', 'Solve 50 algebra problems', '🔢', '{"algebra_problems": 50}', 150, 'rare'),
('Study Streak', 'Study for 7 consecutive days', '🔥', '{"streak_days": 7}', 100, 'uncommon'),
('Speed Demon', 'Solve 10 problems in under 30 seconds each', '⚡', '{"fast_solves": 10}', 75, 'uncommon'),
('Perfect Score', 'Get 100% on a 20-question quiz', '💯', '{"perfect_quiz": 20}', 200, 'rare'),
('Topic Master', 'Achieve 90% mastery in any topic', '🏆', '{"topic_mastery": 90}', 250, 'epic'),
('Renaissance Scholar', 'Achieve 70% mastery in 5 different topics', '👑', '{"topics_mastered": 5}', 500, 'legendary')
ON CONFLICT (name) DO NOTHING;

-- Sample quiz questions (basic algebra)
INSERT INTO emma_quiz_questions (topic, subtopic, difficulty, question, correct_answer, distractors, explanation, problem_type, tags) VALUES
('algebra', 'linear_equations', 'beginner', 'Solve for x: 2x + 5 = 13', 'x = 4', '["x = 3", "x = 5", "x = 6"]', 'Subtract 5 from both sides: 2x = 8. Divide by 2: x = 4', 'algebra', ARRAY['linear', 'equations']),
('algebra', 'quadratic_equations', 'intermediate', 'Solve: x² - 5x + 6 = 0', 'x = 2 or x = 3', '["x = 1 or x = 6", "x = -2 or x = -3", "x = 0 or x = 5"]', 'Factor: (x - 2)(x - 3) = 0. Solutions are x = 2 and x = 3', 'algebra', ARRAY['quadratic', 'factoring']),
('calculus', 'derivatives', 'intermediate', 'Find d/dx(x³)', '3x²', '["x²", "3x³", "x³/3"]', 'Using the power rule: d/dx(xⁿ) = nxⁿ⁻¹, so d/dx(x³) = 3x²', 'calculus', ARRAY['derivatives', 'power_rule']),
('calculus', 'integrals', 'intermediate', 'Integrate: ∫2x dx', 'x² + C', '["2x² + C", "x²/2 + C", "2x + C"]', 'Using the power rule for integration: ∫xⁿ dx = xⁿ⁺¹/(n+1) + C', 'calculus', ARRAY['integrals', 'power_rule']),
('algebra', 'exponents', 'beginner', 'Simplify: (x²)³', 'x⁶', '["x⁵", "x⁸", "3x²"]', 'When raising a power to a power, multiply the exponents: (x²)³ = x²ˣ³ = x⁶', 'algebra', ARRAY['exponents', 'simplification'])
ON CONFLICT DO NOTHING;

-- Comments
COMMENT ON TABLE emma_user_profiles IS 'User-specific EMMA profiles with learning preferences';
COMMENT ON TABLE emma_solutions IS 'History of problems solved by users';
COMMENT ON TABLE emma_quiz_questions IS 'Bank of quiz questions across all topics';
COMMENT ON TABLE emma_user_progress IS 'Spaced repetition progress tracking for each user-question pair';
COMMENT ON TABLE emma_study_sessions IS 'Study session tracking with duration and performance metrics';
COMMENT ON TABLE emma_answer_submissions IS 'Detailed tracking of quiz answer submissions';
COMMENT ON TABLE emma_topic_mastery IS 'Aggregated mastery levels for topics and subtopics';
COMMENT ON TABLE emma_achievements IS 'Achievement definitions';
COMMENT ON TABLE emma_user_achievements IS 'Achievements earned by users';
