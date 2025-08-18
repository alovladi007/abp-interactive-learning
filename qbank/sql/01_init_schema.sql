-- Advanced QBank System Database Schema
-- PostgreSQL schema for IRT-based adaptive testing platform

-- Create database if not exists
-- CREATE DATABASE qbank;

-- Use the database
-- \c qbank;

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS exposure_control CASCADE;
DROP TABLE IF EXISTS responses CASCADE;
DROP TABLE IF EXISTS test_sessions CASCADE;
DROP TABLE IF EXISTS questions CASCADE;
DROP TABLE IF EXISTS calibration_runs CASCADE;
DROP TABLE IF EXISTS item_banks CASCADE;

-- Create item_banks table
CREATE TABLE item_banks (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL UNIQUE,
    description TEXT,
    subject VARCHAR(100) NOT NULL,
    grade_level VARCHAR(50),
    test_type VARCHAR(50),
    total_items INTEGER DEFAULT 0,
    active_items INTEGER DEFAULT 0,
    average_difficulty FLOAT,
    average_discrimination FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100),
    config JSONB DEFAULT '{}'::jsonb
);

-- Create questions table with IRT parameters
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    subject VARCHAR(100) NOT NULL,
    topic VARCHAR(100) NOT NULL,
    difficulty_level VARCHAR(20) NOT NULL,
    
    -- IRT Parameters
    discrimination FLOAT DEFAULT 1.0 CHECK (discrimination > 0),
    difficulty FLOAT DEFAULT 0.0,
    guessing FLOAT DEFAULT 0.25 CHECK (guessing >= 0 AND guessing < 1),
    
    -- Sympson-Hetter Exposure Control
    exposure_rate FLOAT DEFAULT 0.0 CHECK (exposure_rate >= 0 AND exposure_rate <= 1),
    exposure_count INTEGER DEFAULT 0,
    selection_probability FLOAT DEFAULT 1.0 CHECK (selection_probability >= 0 AND selection_probability <= 1),
    last_exposed TIMESTAMP,
    
    -- Question metadata
    question_type VARCHAR(50) NOT NULL,
    options JSONB,
    correct_answer VARCHAR(500) NOT NULL,
    explanation TEXT,
    
    -- Statistics
    total_responses INTEGER DEFAULT 0,
    correct_responses INTEGER DEFAULT 0,
    average_response_time FLOAT DEFAULT 0.0,
    
    -- Calibration metadata
    last_calibrated TIMESTAMP,
    calibration_sample_size INTEGER DEFAULT 0,
    standard_error_a FLOAT,
    standard_error_b FLOAT,
    standard_error_c FLOAT,
    
    -- Content tags
    tags JSONB DEFAULT '[]'::jsonb,
    cognitive_level VARCHAR(50),
    
    -- Administrative
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    review_status VARCHAR(20) DEFAULT 'approved',
    item_bank_id INTEGER REFERENCES item_banks(id)
);

-- Create indexes for questions
CREATE INDEX idx_questions_subject_topic ON questions(subject, topic);
CREATE INDEX idx_questions_difficulty ON questions(difficulty);
CREATE INDEX idx_questions_exposure ON questions(exposure_rate);
CREATE INDEX idx_questions_active_subject ON questions(is_active, subject);
CREATE INDEX idx_questions_item_bank ON questions(item_bank_id);

-- Create test_sessions table
CREATE TABLE test_sessions (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    session_token VARCHAR(200) UNIQUE NOT NULL,
    
    -- Test configuration
    test_type VARCHAR(50) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    target_questions INTEGER DEFAULT 20,
    
    -- IRT estimates
    ability_estimate FLOAT DEFAULT 0.0,
    ability_se FLOAT DEFAULT 1.0,
    
    -- Session state
    status VARCHAR(20) DEFAULT 'active',
    questions_answered INTEGER DEFAULT 0,
    correct_answers INTEGER DEFAULT 0,
    
    -- Timing
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_time_seconds INTEGER DEFAULT 0,
    
    -- Session data
    ability_history JSONB DEFAULT '[]'::jsonb,
    question_sequence JSONB DEFAULT '[]'::jsonb
);

-- Create indexes for test_sessions
CREATE INDEX idx_sessions_user_id ON test_sessions(user_id);
CREATE INDEX idx_sessions_token ON test_sessions(session_token);
CREATE INDEX idx_sessions_status ON test_sessions(status);
CREATE INDEX idx_sessions_started ON test_sessions(started_at);

-- Create responses table
CREATE TABLE responses (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES test_sessions(id) ON DELETE CASCADE,
    question_id INTEGER REFERENCES questions(id) ON DELETE CASCADE,
    user_id VARCHAR(100) NOT NULL,
    
    -- Response data
    given_answer VARCHAR(500) NOT NULL,
    is_correct BOOLEAN NOT NULL,
    response_time FLOAT NOT NULL CHECK (response_time >= 0),
    
    -- IRT data at time of response
    ability_before FLOAT NOT NULL,
    ability_after FLOAT NOT NULL,
    information_value FLOAT,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    flagged_for_review BOOLEAN DEFAULT FALSE
);

-- Create indexes for responses
CREATE INDEX idx_responses_session_question ON responses(session_id, question_id);
CREATE INDEX idx_responses_user_created ON responses(user_id, created_at);
CREATE INDEX idx_responses_question ON responses(question_id);

-- Create calibration_runs table
CREATE TABLE calibration_runs (
    id SERIAL PRIMARY KEY,
    run_id VARCHAR(100) UNIQUE NOT NULL,
    
    -- Calibration details
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'running',
    
    -- Statistics
    questions_calibrated INTEGER DEFAULT 0,
    total_responses_used INTEGER DEFAULT 0,
    convergence_iterations INTEGER,
    log_likelihood FLOAT,
    
    -- Parameters
    calibration_method VARCHAR(50) NOT NULL,
    calibration_config JSONB,
    
    -- Results
    results_summary JSONB,
    error_message TEXT
);

-- Create exposure_control table
CREATE TABLE exposure_control (
    id SERIAL PRIMARY KEY,
    question_id INTEGER REFERENCES questions(id) ON DELETE CASCADE UNIQUE,
    
    -- Sympson-Hetter parameters
    target_exposure FLOAT DEFAULT 0.25,
    current_exposure FLOAT DEFAULT 0.0,
    selection_parameter FLOAT DEFAULT 1.0,
    
    -- Control statistics
    total_eligible INTEGER DEFAULT 0,
    total_administered INTEGER DEFAULT 0,
    
    -- Adaptive control
    control_parameter FLOAT DEFAULT 1.0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Phase tracking
    phase VARCHAR(20) DEFAULT 'initial',
    phase_iterations INTEGER DEFAULT 0
);

-- Create function to update timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_questions_updated_at BEFORE UPDATE ON questions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_item_banks_updated_at BEFORE UPDATE ON item_banks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create function to update exposure statistics
CREATE OR REPLACE FUNCTION update_exposure_stats()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.question_id IS NOT NULL THEN
        UPDATE questions 
        SET exposure_count = exposure_count + 1,
            last_exposed = CURRENT_TIMESTAMP,
            exposure_rate = CAST(exposure_count + 1 AS FLOAT) / GREATEST(total_responses, 1)
        WHERE id = NEW.question_id;
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for exposure updates
CREATE TRIGGER update_exposure_on_response AFTER INSERT ON responses
    FOR EACH ROW EXECUTE FUNCTION update_exposure_stats();

-- Create function to update question statistics
CREATE OR REPLACE FUNCTION update_question_stats()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE questions 
    SET total_responses = total_responses + 1,
        correct_responses = correct_responses + CASE WHEN NEW.is_correct THEN 1 ELSE 0 END,
        average_response_time = (average_response_time * total_responses + NEW.response_time) / (total_responses + 1)
    WHERE id = NEW.question_id;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for question statistics
CREATE TRIGGER update_question_stats_on_response AFTER INSERT ON responses
    FOR EACH ROW EXECUTE FUNCTION update_question_stats();

-- Create view for question performance metrics
CREATE VIEW question_performance AS
SELECT 
    q.id,
    q.subject,
    q.topic,
    q.difficulty_level,
    q.discrimination,
    q.difficulty,
    q.guessing,
    q.total_responses,
    q.correct_responses,
    CASE WHEN q.total_responses > 0 
         THEN CAST(q.correct_responses AS FLOAT) / q.total_responses 
         ELSE NULL END AS p_value,
    q.average_response_time,
    q.exposure_rate,
    q.last_calibrated,
    q.is_active
FROM questions q;

-- Create view for session analytics
CREATE VIEW session_analytics AS
SELECT 
    ts.id,
    ts.user_id,
    ts.test_type,
    ts.subject,
    ts.status,
    ts.questions_answered,
    ts.correct_answers,
    CASE WHEN ts.questions_answered > 0 
         THEN CAST(ts.correct_answers AS FLOAT) / ts.questions_answered 
         ELSE NULL END AS accuracy,
    ts.ability_estimate,
    ts.ability_se,
    ts.started_at,
    ts.completed_at,
    ts.total_time_seconds,
    CASE WHEN ts.questions_answered > 0 
         THEN ts.total_time_seconds / ts.questions_answered 
         ELSE NULL END AS avg_time_per_question
FROM test_sessions ts;

-- Grant permissions (adjust as needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO qbank_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO qbank_user;

-- Add comments for documentation
COMMENT ON TABLE questions IS 'Main question bank with IRT parameters and exposure control';
COMMENT ON TABLE test_sessions IS 'Adaptive testing sessions with ability tracking';
COMMENT ON TABLE responses IS 'Individual question responses with IRT calculations';
COMMENT ON TABLE calibration_runs IS 'History of item calibration runs';
COMMENT ON TABLE exposure_control IS 'Sympson-Hetter exposure control parameters';
COMMENT ON TABLE item_banks IS 'Organization of questions into item banks';

COMMENT ON COLUMN questions.discrimination IS 'IRT a-parameter: item discrimination';
COMMENT ON COLUMN questions.difficulty IS 'IRT b-parameter: item difficulty';
COMMENT ON COLUMN questions.guessing IS 'IRT c-parameter: pseudo-guessing';
COMMENT ON COLUMN questions.exposure_rate IS 'Current exposure rate for Sympson-Hetter control';
COMMENT ON COLUMN test_sessions.ability_estimate IS 'Current theta estimate using EAP or MLE';
COMMENT ON COLUMN test_sessions.ability_se IS 'Standard error of ability estimate';