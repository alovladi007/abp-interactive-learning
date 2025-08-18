-- QBank Complete Database Schema
-- PostgreSQL 15+ with extensions

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create database
CREATE DATABASE qbank_production;
\c qbank_production;

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'student',
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Topics table
CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_id INTEGER REFERENCES topics(id),
    description TEXT,
    icon VARCHAR(50),
    order_index INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Questions table with full metadata
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    external_id VARCHAR(100) UNIQUE,
    topic_id INTEGER REFERENCES topics(id),
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) DEFAULT 'multiple_choice',
    difficulty_level VARCHAR(20),
    points INTEGER DEFAULT 1,
    time_limit_seconds INTEGER,
    explanation TEXT,
    hints TEXT[],
    tags TEXT[],
    media_url TEXT,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT true,
    review_status VARCHAR(50) DEFAULT 'pending'
);

-- Question options table
CREATE TABLE question_options (
    id SERIAL PRIMARY KEY,
    question_id INTEGER REFERENCES questions(id) ON DELETE CASCADE,
    option_text TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT false,
    explanation TEXT,
    order_index INTEGER DEFAULT 0
);

-- IRT parameters table
CREATE TABLE irt_parameters (
    id SERIAL PRIMARY KEY,
    question_id INTEGER REFERENCES questions(id) ON DELETE CASCADE,
    model_type VARCHAR(10) DEFAULT '3PL',
    a_discrimination FLOAT DEFAULT 1.0,
    b_difficulty FLOAT DEFAULT 0.0,
    c_guessing FLOAT DEFAULT 0.2,
    d_upper_asymptote FLOAT DEFAULT 1.0,
    standard_error_a FLOAT,
    standard_error_b FLOAT,
    standard_error_c FLOAT,
    fit_statistic FLOAT,
    sample_size INTEGER,
    last_calibrated TIMESTAMP,
    UNIQUE(question_id, model_type)
);

-- Quiz sessions table
CREATE TABLE quiz_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    session_type VARCHAR(50) DEFAULT 'practice',
    topic_id INTEGER REFERENCES topics(id),
    config JSONB,
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    time_spent_seconds INTEGER,
    score FLOAT,
    theta_initial FLOAT DEFAULT 0.0,
    theta_final FLOAT,
    status VARCHAR(50) DEFAULT 'active'
);

-- User responses table
CREATE TABLE user_responses (
    id SERIAL PRIMARY KEY,
    session_id UUID REFERENCES quiz_sessions(id),
    question_id INTEGER REFERENCES questions(id),
    selected_option_id INTEGER REFERENCES question_options(id),
    is_correct BOOLEAN,
    time_taken_seconds INTEGER,
    confidence_level INTEGER CHECK (confidence_level >= 1 AND confidence_level <= 5),
    theta_before FLOAT,
    theta_after FLOAT,
    information_value FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Question exposure control
CREATE TABLE exposure_control (
    id SERIAL PRIMARY KEY,
    question_id INTEGER REFERENCES questions(id),
    date DATE DEFAULT CURRENT_DATE,
    exposure_count INTEGER DEFAULT 0,
    selection_count INTEGER DEFAULT 0,
    exposure_rate FLOAT,
    sympson_hetter_k FLOAT DEFAULT 1.0,
    max_exposure_rate FLOAT DEFAULT 0.2,
    UNIQUE(question_id, date)
);

-- User ability tracking
CREATE TABLE user_abilities (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    topic_id INTEGER REFERENCES topics(id),
    theta FLOAT DEFAULT 0.0,
    theta_se FLOAT DEFAULT 1.0,
    num_responses INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT NOW(),
    percentile_rank FLOAT,
    UNIQUE(user_id, topic_id)
);

-- Analytics events table
CREATE TABLE analytics_events (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    event_type VARCHAR(100),
    event_data JSONB,
    session_id UUID,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Question performance metrics (materialized view)
CREATE MATERIALIZED VIEW question_metrics AS
SELECT 
    q.id,
    q.question_text,
    COUNT(ur.id) as total_responses,
    AVG(CASE WHEN ur.is_correct THEN 1.0 ELSE 0.0 END) as p_value,
    STDDEV(CASE WHEN ur.is_correct THEN 1.0 ELSE 0.0 END) as discrimination,
    AVG(ur.time_taken_seconds) as avg_time,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY ur.time_taken_seconds) as median_time,
    AVG(ur.confidence_level) as avg_confidence
FROM questions q
LEFT JOIN user_responses ur ON q.id = ur.question_id
GROUP BY q.id, q.question_text;

-- Indexes for performance
CREATE INDEX idx_questions_topic ON questions(topic_id);
CREATE INDEX idx_questions_difficulty ON questions(difficulty_level);
CREATE INDEX idx_questions_tags ON questions USING GIN(tags);
CREATE INDEX idx_user_responses_session ON user_responses(session_id);
CREATE INDEX idx_user_responses_question ON user_responses(question_id);
CREATE INDEX idx_quiz_sessions_user ON quiz_sessions(user_id);
CREATE INDEX idx_exposure_control_date ON exposure_control(date);
CREATE INDEX idx_analytics_events_user ON analytics_events(user_id);
CREATE INDEX idx_analytics_events_created ON analytics_events(created_at);

-- Full text search
CREATE INDEX idx_questions_fulltext ON questions USING GIN(to_tsvector('english', question_text));

-- Functions and triggers
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_questions_updated_at
BEFORE UPDATE ON questions
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();

-- Function to calculate IRT probability
CREATE OR REPLACE FUNCTION calculate_irt_probability(
    theta FLOAT,
    a FLOAT,
    b FLOAT,
    c FLOAT
) RETURNS FLOAT AS $$
BEGIN
    RETURN c + (1 - c) / (1 + EXP(-a * (theta - b)));
END;
$$ LANGUAGE plpgsql;

-- Function to update user ability after response
CREATE OR REPLACE FUNCTION update_user_ability()
RETURNS TRIGGER AS $$
DECLARE
    v_topic_id INTEGER;
    v_current_theta FLOAT;
    v_current_se FLOAT;
    v_irt_params RECORD;
BEGIN
    -- Get question topic
    SELECT topic_id INTO v_topic_id FROM questions WHERE id = NEW.question_id;
    
    -- Get current ability
    SELECT theta, theta_se INTO v_current_theta, v_current_se
    FROM user_abilities
    WHERE user_id = (SELECT user_id FROM quiz_sessions WHERE id = NEW.session_id)
    AND topic_id = v_topic_id;
    
    IF NOT FOUND THEN
        v_current_theta := 0.0;
        v_current_se := 1.0;
    END IF;
    
    -- Get IRT parameters
    SELECT * INTO v_irt_params FROM irt_parameters WHERE question_id = NEW.question_id;
    
    -- Simple EAP update (can be replaced with more sophisticated method)
    NEW.theta_before := v_current_theta;
    NEW.theta_after := v_current_theta + 
        CASE WHEN NEW.is_correct THEN 0.1 ELSE -0.1 END * 
        (1.0 / (1.0 + EXP(-v_irt_params.a_discrimination * (v_current_theta - v_irt_params.b_difficulty))));
    
    -- Update user ability
    INSERT INTO user_abilities (user_id, topic_id, theta, theta_se, num_responses)
    VALUES (
        (SELECT user_id FROM quiz_sessions WHERE id = NEW.session_id),
        v_topic_id,
        NEW.theta_after,
        v_current_se * 0.95, -- Decrease SE with more responses
        1
    )
    ON CONFLICT (user_id, topic_id)
    DO UPDATE SET
        theta = NEW.theta_after,
        theta_se = user_abilities.theta_se * 0.95,
        num_responses = user_abilities.num_responses + 1,
        last_updated = NOW();
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_ability
BEFORE INSERT ON user_responses
FOR EACH ROW
EXECUTE FUNCTION update_user_ability();

-- Initial data seed
INSERT INTO topics (name, description) VALUES
('Mathematics', 'Mathematical concepts and problem solving'),
('Algebra', 'Algebraic expressions and equations'),
('Geometry', 'Shapes, angles, and spatial reasoning'),
('Calculus', 'Derivatives, integrals, and limits'),
('Science', 'Natural sciences and scientific method'),
('Physics', 'Matter, energy, and forces'),
('Chemistry', 'Elements, compounds, and reactions'),
('Biology', 'Life sciences and organisms'),
('English', 'Language arts and communication'),
('Grammar', 'Language structure and rules'),
('Reading Comprehension', 'Understanding and analyzing texts'),
('Writing', 'Composition and expression');

-- Update parent relationships
UPDATE topics SET parent_id = 1 WHERE name IN ('Algebra', 'Geometry', 'Calculus');
UPDATE topics SET parent_id = 5 WHERE name IN ('Physics', 'Chemistry', 'Biology');
UPDATE topics SET parent_id = 9 WHERE name IN ('Grammar', 'Reading Comprehension', 'Writing');