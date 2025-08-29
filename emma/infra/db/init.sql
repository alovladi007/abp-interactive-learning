-- EMMA Database Schema with pgvector
-- PostgreSQL 16 with pgvector extension

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;  -- For text search

-- Create schemas
CREATE SCHEMA IF NOT EXISTS emma;
CREATE SCHEMA IF NOT EXISTS rag;

-- Set search path
SET search_path TO emma, rag, public;

-- =====================================================
-- Core Tables
-- =====================================================

-- Users table
CREATE TABLE emma.users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Sources table (documents, URLs, etc.)
CREATE TABLE rag.sources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    uri TEXT NOT NULL,
    kind VARCHAR(50) NOT NULL, -- 'pdf', 'web', 'markdown', 'code'
    title TEXT,
    sha256 VARCHAR(64) NOT NULL,
    file_size BIGINT,
    user_id UUID REFERENCES emma.users(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb,
    UNIQUE(sha256)
);

-- Chunks table with vector embeddings
CREATE TABLE rag.chunks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id UUID REFERENCES rag.sources(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    start_char INTEGER NOT NULL,
    end_char INTEGER NOT NULL,
    embedding vector(1536),  -- OpenAI ada-002 dimension
    token_count INTEGER,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(source_id, chunk_index)
);

-- Create vector similarity index
CREATE INDEX chunks_embedding_idx ON rag.chunks 
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

-- Create text search index
CREATE INDEX chunks_text_trgm_idx ON rag.chunks 
    USING gin (text gin_trgm_ops);

-- =====================================================
-- Problem Solving Tables
-- =====================================================

-- Runs table (problem-solving sessions)
CREATE TABLE emma.runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES emma.users(id) ON DELETE SET NULL,
    question TEXT NOT NULL,
    question_embedding vector(1536),
    flags JSONB DEFAULT '{}'::jsonb,  -- need_steps, need_citations, etc.
    status VARCHAR(50) DEFAULT 'pending',  -- pending, running, completed, failed
    created_at TIMESTAMPTZ DEFAULT NOW(),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    total_time_ms INTEGER,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Steps table (execution trace)
CREATE TABLE emma.steps (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    run_id UUID REFERENCES emma.runs(id) ON DELETE CASCADE,
    step_index INTEGER NOT NULL,
    role VARCHAR(50) NOT NULL,  -- planner, researcher, math, numeric, code, verifier, explainer
    thought TEXT,
    action TEXT,
    inputs JSONB DEFAULT '{}'::jsonb,
    outputs JSONB DEFAULT '{}'::jsonb,
    tool_calls JSONB DEFAULT '[]'::jsonb,
    citations JSONB DEFAULT '[]'::jsonb,
    status VARCHAR(50) DEFAULT 'pending',
    started_at TIMESTAMPTZ,
    finished_at TIMESTAMPTZ,
    duration_ms INTEGER,
    error TEXT,
    UNIQUE(run_id, step_index)
);

-- Tool calls table
CREATE TABLE emma.tool_calls (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    step_id UUID REFERENCES emma.steps(id) ON DELETE CASCADE,
    tool_name VARCHAR(100) NOT NULL,
    args JSONB NOT NULL,
    result JSONB,
    latency_ms INTEGER,
    error TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Citations table
CREATE TABLE emma.citations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    run_id UUID REFERENCES emma.runs(id) ON DELETE CASCADE,
    source_id UUID REFERENCES rag.sources(id) ON DELETE SET NULL,
    chunk_id UUID REFERENCES rag.chunks(id) ON DELETE SET NULL,
    text TEXT,
    score FLOAT,
    type VARCHAR(50),  -- web, file, kg, computation
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Artifacts table (plots, generated files)
CREATE TABLE emma.artifacts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    run_id UUID REFERENCES emma.runs(id) ON DELETE CASCADE,
    step_id UUID REFERENCES emma.steps(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,  -- plot, file, data
    mime_type VARCHAR(100),
    storage_path TEXT NOT NULL,  -- MinIO path
    size_bytes BIGINT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- =====================================================
-- Knowledge Graph Tables (for GraphRAG)
-- =====================================================

-- Entities table
CREATE TABLE rag.entities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL,  -- concept, equation, constant, material, etc.
    description TEXT,
    properties JSONB DEFAULT '{}'::jsonb,
    embedding vector(1536),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(name, type)
);

-- Relations table
CREATE TABLE rag.relations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_entity_id UUID REFERENCES rag.entities(id) ON DELETE CASCADE,
    target_entity_id UUID REFERENCES rag.entities(id) ON DELETE CASCADE,
    predicate VARCHAR(100) NOT NULL,  -- has_property, derives_from, used_in, etc.
    weight FLOAT DEFAULT 1.0,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(source_entity_id, target_entity_id, predicate)
);

-- Equations table (special entities)
CREATE TABLE rag.equations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_id UUID REFERENCES rag.entities(id) ON DELETE CASCADE,
    latex TEXT NOT NULL,
    sympy_form TEXT,
    variables JSONB DEFAULT '[]'::jsonb,
    domain VARCHAR(100),  -- physics, math, engineering, etc.
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- =====================================================
-- Analytics Tables
-- =====================================================

-- Evaluation results
CREATE TABLE emma.evaluations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    run_id UUID REFERENCES emma.runs(id) ON DELETE CASCADE,
    suite VARCHAR(100) NOT NULL,  -- gsm8k, math, physics, etc.
    problem_id VARCHAR(255) NOT NULL,
    expected_answer TEXT,
    actual_answer TEXT,
    is_correct BOOLEAN,
    score FLOAT,
    metrics JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- User feedback
CREATE TABLE emma.feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    run_id UUID REFERENCES emma.runs(id) ON DELETE CASCADE,
    user_id UUID REFERENCES emma.users(id) ON DELETE SET NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    issues JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- =====================================================
-- Indexes for Performance
-- =====================================================

-- Runs indexes
CREATE INDEX runs_user_id_idx ON emma.runs(user_id);
CREATE INDEX runs_status_idx ON emma.runs(status);
CREATE INDEX runs_created_at_idx ON emma.runs(created_at DESC);
CREATE INDEX runs_question_embedding_idx ON emma.runs 
    USING ivfflat (question_embedding vector_cosine_ops);

-- Steps indexes
CREATE INDEX steps_run_id_idx ON emma.steps(run_id);
CREATE INDEX steps_role_idx ON emma.steps(role);
CREATE INDEX steps_status_idx ON emma.steps(status);

-- Sources indexes
CREATE INDEX sources_kind_idx ON rag.sources(kind);
CREATE INDEX sources_user_id_idx ON rag.sources(user_id);
CREATE INDEX sources_created_at_idx ON rag.sources(created_at DESC);

-- Chunks indexes
CREATE INDEX chunks_source_id_idx ON rag.chunks(source_id);
CREATE INDEX chunks_token_count_idx ON rag.chunks(token_count);

-- Citations indexes
CREATE INDEX citations_run_id_idx ON emma.citations(run_id);
CREATE INDEX citations_source_id_idx ON emma.citations(source_id);
CREATE INDEX citations_score_idx ON emma.citations(score DESC);

-- Entities indexes
CREATE INDEX entities_type_idx ON rag.entities(type);
CREATE INDEX entities_embedding_idx ON rag.entities 
    USING ivfflat (embedding vector_cosine_ops);

-- Relations indexes
CREATE INDEX relations_source_entity_idx ON rag.relations(source_entity_id);
CREATE INDEX relations_target_entity_idx ON rag.relations(target_entity_id);
CREATE INDEX relations_predicate_idx ON rag.relations(predicate);

-- =====================================================
-- Functions and Triggers
-- =====================================================

-- Update timestamp trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply update trigger to relevant tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON emma.users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_sources_updated_at BEFORE UPDATE ON rag.sources
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Function to search similar chunks
CREATE OR REPLACE FUNCTION rag.search_similar_chunks(
    query_embedding vector(1536),
    match_count INT DEFAULT 10,
    match_threshold FLOAT DEFAULT 0.7
)
RETURNS TABLE (
    chunk_id UUID,
    source_id UUID,
    text TEXT,
    similarity FLOAT,
    metadata JSONB
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id AS chunk_id,
        c.source_id,
        c.text,
        1 - (c.embedding <=> query_embedding) AS similarity,
        c.metadata
    FROM rag.chunks c
    WHERE 1 - (c.embedding <=> query_embedding) > match_threshold
    ORDER BY c.embedding <=> query_embedding
    LIMIT match_count;
END;
$$ LANGUAGE plpgsql;

-- Function for hybrid search (vector + text)
CREATE OR REPLACE FUNCTION rag.hybrid_search(
    query_text TEXT,
    query_embedding vector(1536),
    match_count INT DEFAULT 10,
    vector_weight FLOAT DEFAULT 0.7
)
RETURNS TABLE (
    chunk_id UUID,
    source_id UUID,
    text TEXT,
    score FLOAT,
    metadata JSONB
) AS $$
BEGIN
    RETURN QUERY
    WITH vector_search AS (
        SELECT 
            c.id,
            1 - (c.embedding <=> query_embedding) AS vector_score
        FROM rag.chunks c
        ORDER BY c.embedding <=> query_embedding
        LIMIT match_count * 2
    ),
    text_search AS (
        SELECT 
            c.id,
            ts_rank(to_tsvector('english', c.text), 
                   plainto_tsquery('english', query_text)) AS text_score
        FROM rag.chunks c
        WHERE to_tsvector('english', c.text) @@ plainto_tsquery('english', query_text)
        LIMIT match_count * 2
    ),
    combined AS (
        SELECT 
            COALESCE(v.id, t.id) AS chunk_id,
            COALESCE(v.vector_score, 0) * vector_weight + 
            COALESCE(t.text_score, 0) * (1 - vector_weight) AS combined_score
        FROM vector_search v
        FULL OUTER JOIN text_search t ON v.id = t.id
    )
    SELECT 
        c.id AS chunk_id,
        c.source_id,
        c.text,
        co.combined_score AS score,
        c.metadata
    FROM combined co
    JOIN rag.chunks c ON c.id = co.chunk_id
    ORDER BY co.combined_score DESC
    LIMIT match_count;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- Initial Data
-- =====================================================

-- Insert default admin user (password: admin123)
INSERT INTO emma.users (email, username, password_hash, is_admin)
VALUES ('admin@emma.ai', 'admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5L2iGYjXyJFiG', TRUE);

-- Insert sample domains for equations
INSERT INTO rag.entities (name, type, description) VALUES
    ('Classical Mechanics', 'domain', 'Newtonian mechanics and dynamics'),
    ('Electromagnetism', 'domain', 'Electric and magnetic phenomena'),
    ('Thermodynamics', 'domain', 'Heat and energy transfer'),
    ('Quantum Mechanics', 'domain', 'Quantum physics and wave mechanics'),
    ('Linear Algebra', 'domain', 'Vector spaces and linear transformations'),
    ('Calculus', 'domain', 'Differential and integral calculus');

-- Grant permissions
GRANT ALL ON SCHEMA emma TO emma;
GRANT ALL ON SCHEMA rag TO emma;
GRANT ALL ON ALL TABLES IN SCHEMA emma TO emma;
GRANT ALL ON ALL TABLES IN SCHEMA rag TO emma;
GRANT ALL ON ALL SEQUENCES IN SCHEMA emma TO emma;
GRANT ALL ON ALL SEQUENCES IN SCHEMA rag TO emma;