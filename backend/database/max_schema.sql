-- MAX AI Research Assistant - Complete Database Schema
-- PostgreSQL 15+ with pgvector extension for embeddings
-- Comprehensive research management, citation analysis, and collaboration

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "vector";

-- ============================================================================
-- USERS & AUTHENTICATION
-- ============================================================================

CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    affiliation VARCHAR(255),
    research_interests TEXT[],
    orcid VARCHAR(50),
    google_scholar_id VARCHAR(100),
    profile_image_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT true,
    subscription_tier VARCHAR(20) DEFAULT 'free' CHECK (subscription_tier IN ('free', 'pro', 'enterprise'))
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);

-- ============================================================================
-- PAPERS & RESEARCH CONTENT
-- ============================================================================

CREATE TABLE IF NOT EXISTS papers (
    paper_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    external_id VARCHAR(255) UNIQUE, -- S2, arXiv, DOI, etc.
    source VARCHAR(50) NOT NULL CHECK (source IN ('semantic_scholar', 'arxiv', 'pubmed', 'crossref', 'scispace', 'manual')),
    title TEXT NOT NULL,
    abstract TEXT,
    authors JSONB NOT NULL DEFAULT '[]', -- [{name, affiliation, ids}]
    publication_year INTEGER,
    publication_date DATE,
    venue VARCHAR(500),
    venue_type VARCHAR(50) CHECK (venue_type IN ('journal', 'conference', 'preprint', 'workshop', 'book')),
    doi VARCHAR(255),
    arxiv_id VARCHAR(50),
    pubmed_id VARCHAR(50),
    url TEXT,
    pdf_url TEXT,
    citations_count INTEGER DEFAULT 0,
    references_count INTEGER DEFAULT 0,
    influential_citation_count INTEGER DEFAULT 0,
    fields_of_study TEXT[],
    keywords TEXT[],
    embedding VECTOR(768), -- Sentence embeddings for semantic search
    tldr TEXT, -- AI-generated summary
    credibility_score FLOAT CHECK (credibility_score >= 0 AND credibility_score <= 100),
    h_index INTEGER,
    is_open_access BOOLEAN DEFAULT false,
    language VARCHAR(10) DEFAULT 'en',
    metadata JSONB DEFAULT '{}',
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    indexed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_papers_external_id ON papers(external_id);
CREATE INDEX idx_papers_doi ON papers(doi);
CREATE INDEX idx_papers_arxiv ON papers(arxiv_id);
CREATE INDEX idx_papers_title_trgm ON papers USING gin(title gin_trgm_ops);
CREATE INDEX idx_papers_abstract_trgm ON papers USING gin(abstract gin_trgm_ops);
CREATE INDEX idx_papers_year ON papers(publication_year DESC);
CREATE INDEX idx_papers_citations ON papers(citations_count DESC);
CREATE INDEX idx_papers_credibility ON papers(credibility_score DESC);
CREATE INDEX idx_papers_fields ON papers USING gin(fields_of_study);
CREATE INDEX idx_papers_embedding ON papers USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- ============================================================================
-- CITATIONS & REFERENCES
-- ============================================================================

CREATE TABLE IF NOT EXISTS citations (
    citation_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    citing_paper_id UUID NOT NULL REFERENCES papers(paper_id) ON DELETE CASCADE,
    cited_paper_id UUID NOT NULL REFERENCES papers(paper_id) ON DELETE CASCADE,
    context TEXT, -- Text surrounding the citation
    intent VARCHAR(50), -- background, method, result_comparison, etc.
    is_influential BOOLEAN DEFAULT false,
    citation_count INTEGER DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(citing_paper_id, cited_paper_id)
);

CREATE INDEX idx_citations_citing ON citations(citing_paper_id);
CREATE INDEX idx_citations_cited ON citations(cited_paper_id);
CREATE INDEX idx_citations_influential ON citations(is_influential) WHERE is_influential = true;

-- ============================================================================
-- AUTHORS
-- ============================================================================

CREATE TABLE IF NOT EXISTS authors (
    author_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    normalized_name VARCHAR(255) NOT NULL,
    affiliations TEXT[],
    email VARCHAR(255),
    orcid VARCHAR(50) UNIQUE,
    google_scholar_id VARCHAR(100) UNIQUE,
    semantic_scholar_id VARCHAR(100) UNIQUE,
    h_index INTEGER,
    i10_index INTEGER,
    total_citations INTEGER DEFAULT 0,
    total_papers INTEGER DEFAULT 0,
    research_interests TEXT[],
    homepage_url TEXT,
    profile_image_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_authors_name_trgm ON authors USING gin(name gin_trgm_ops);
CREATE INDEX idx_authors_normalized ON authors(normalized_name);
CREATE INDEX idx_authors_orcid ON authors(orcid);

CREATE TABLE IF NOT EXISTS paper_authors (
    paper_id UUID NOT NULL REFERENCES papers(paper_id) ON DELETE CASCADE,
    author_id UUID NOT NULL REFERENCES authors(author_id) ON DELETE CASCADE,
    author_position INTEGER NOT NULL, -- 0 for first author, etc.
    is_corresponding BOOLEAN DEFAULT false,
    PRIMARY KEY (paper_id, author_id)
);

CREATE INDEX idx_paper_authors_paper ON paper_authors(paper_id);
CREATE INDEX idx_paper_authors_author ON paper_authors(author_id);

-- ============================================================================
-- RESEARCH COLLECTIONS & LIBRARIES
-- ============================================================================

CREATE TABLE IF NOT EXISTS collections (
    collection_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    is_public BOOLEAN DEFAULT false,
    color VARCHAR(7), -- Hex color code
    icon VARCHAR(50),
    paper_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_collections_user ON collections(user_id);

CREATE TABLE IF NOT EXISTS collection_papers (
    collection_id UUID NOT NULL REFERENCES collections(collection_id) ON DELETE CASCADE,
    paper_id UUID NOT NULL REFERENCES papers(paper_id) ON DELETE CASCADE,
    added_by UUID REFERENCES users(user_id),
    notes TEXT,
    tags TEXT[],
    reading_status VARCHAR(20) DEFAULT 'to_read' CHECK (reading_status IN ('to_read', 'reading', 'read', 'referenced')),
    importance_rating INTEGER CHECK (importance_rating >= 1 AND importance_rating <= 5),
    added_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (collection_id, paper_id)
);

CREATE INDEX idx_collection_papers_collection ON collection_papers(collection_id);
CREATE INDEX idx_collection_papers_paper ON collection_papers(paper_id);

-- ============================================================================
-- SAVED SEARCHES & ALERTS
-- ============================================================================

CREATE TABLE IF NOT EXISTS saved_searches (
    search_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    query TEXT NOT NULL,
    filters JSONB DEFAULT '{}', -- {year_min, year_max, fields, venues, etc}
    alert_enabled BOOLEAN DEFAULT false,
    alert_frequency VARCHAR(20) CHECK (alert_frequency IN ('daily', 'weekly', 'monthly')),
    last_alerted TIMESTAMP WITH TIME ZONE,
    results_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_saved_searches_user ON saved_searches(user_id);
CREATE INDEX idx_saved_searches_alerts ON saved_searches(alert_enabled) WHERE alert_enabled = true;

-- ============================================================================
-- RESEARCH SYNTHESIS & SUMMARIES
-- ============================================================================

CREATE TABLE IF NOT EXISTS syntheses (
    synthesis_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    research_question TEXT,
    paper_ids UUID[] NOT NULL,
    synthesis_text TEXT,
    key_findings JSONB DEFAULT '[]', -- [{finding, papers, confidence}]
    methodologies JSONB DEFAULT '[]',
    gaps_identified TEXT[],
    future_directions TEXT[],
    citation_graph JSONB, -- Network data for visualization
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_syntheses_user ON syntheses(user_id);

-- ============================================================================
-- ANNOTATIONS & HIGHLIGHTS
-- ============================================================================

CREATE TABLE IF NOT EXISTS annotations (
    annotation_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    paper_id UUID NOT NULL REFERENCES papers(paper_id) ON DELETE CASCADE,
    annotation_type VARCHAR(20) CHECK (annotation_type IN ('highlight', 'note', 'question', 'idea')),
    content TEXT NOT NULL,
    page_number INTEGER,
    position JSONB, -- {start, end, rect} for PDF coordinates
    color VARCHAR(7),
    is_private BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_annotations_user ON annotations(user_id);
CREATE INDEX idx_annotations_paper ON annotations(paper_id);

-- ============================================================================
-- COLLABORATION & SHARING
-- ============================================================================

CREATE TABLE IF NOT EXISTS teams (
    team_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_by UUID NOT NULL REFERENCES users(user_id),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS team_members (
    team_id UUID NOT NULL REFERENCES teams(team_id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    role VARCHAR(20) DEFAULT 'member' CHECK (role IN ('owner', 'admin', 'member', 'viewer')),
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (team_id, user_id)
);

CREATE INDEX idx_team_members_team ON team_members(team_id);
CREATE INDEX idx_team_members_user ON team_members(user_id);

-- ============================================================================
-- READING PROGRESS & ANALYTICS
-- ============================================================================

CREATE TABLE IF NOT EXISTS reading_progress (
    progress_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    paper_id UUID NOT NULL REFERENCES papers(paper_id) ON DELETE CASCADE,
    progress_percentage INTEGER DEFAULT 0 CHECK (progress_percentage >= 0 AND progress_percentage <= 100),
    time_spent_minutes INTEGER DEFAULT 0,
    last_page INTEGER,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, paper_id)
);

CREATE INDEX idx_reading_progress_user ON reading_progress(user_id);

CREATE TABLE IF NOT EXISTS user_activity (
    activity_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    activity_type VARCHAR(50) NOT NULL, -- search, read, annotate, cite, share, etc.
    entity_type VARCHAR(50), -- paper, collection, synthesis
    entity_id UUID,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_user_activity_user ON user_activity(user_id);
CREATE INDEX idx_user_activity_type ON user_activity(activity_type);
CREATE INDEX idx_user_activity_created ON user_activity(created_at DESC);

-- ============================================================================
-- CITATION EXPORT & FORMATTING
-- ============================================================================

CREATE TABLE IF NOT EXISTS citation_styles (
    style_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL,
    display_name VARCHAR(255) NOT NULL,
    csl_content TEXT NOT NULL, -- Citation Style Language JSON
    is_default BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert default citation styles
INSERT INTO citation_styles (name, display_name, csl_content, is_default) VALUES
('apa', 'APA 7th Edition', '{}', true),
('mla', 'MLA 9th Edition', '{}', false),
('chicago', 'Chicago 17th Edition', '{}', false),
('ieee', 'IEEE', '{}', false),
('vancouver', 'Vancouver', '{}', false)
ON CONFLICT (name) DO NOTHING;

-- ============================================================================
-- RESEARCH TRENDS & ANALYTICS
-- ============================================================================

CREATE TABLE IF NOT EXISTS research_trends (
    trend_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    topic VARCHAR(255) NOT NULL,
    field_of_study VARCHAR(100),
    time_period VARCHAR(20), -- 'last_month', 'last_year', 'all_time'
    paper_count INTEGER DEFAULT 0,
    citation_velocity FLOAT, -- Average citations per month
    top_papers UUID[],
    top_authors UUID[],
    emerging_keywords TEXT[],
    trend_score FLOAT,
    computed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(topic, field_of_study, time_period)
);

CREATE INDEX idx_research_trends_topic ON research_trends(topic);
CREATE INDEX idx_research_trends_field ON research_trends(field_of_study);

-- ============================================================================
-- TRIGGERS & FUNCTIONS
-- ============================================================================

-- Update paper count in collections
CREATE OR REPLACE FUNCTION update_collection_paper_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE collections SET paper_count = paper_count + 1 WHERE collection_id = NEW.collection_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE collections SET paper_count = paper_count - 1 WHERE collection_id = OLD.collection_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_collection_paper_count
AFTER INSERT OR DELETE ON collection_papers
FOR EACH ROW EXECUTE FUNCTION update_collection_paper_count();

-- Update timestamps
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_collections_timestamp
BEFORE UPDATE ON collections
FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trigger_update_syntheses_timestamp
BEFORE UPDATE ON syntheses
FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- Most cited papers in collections
CREATE OR REPLACE VIEW v_popular_papers AS
SELECT
    p.paper_id,
    p.title,
    p.publication_year,
    p.citations_count,
    p.credibility_score,
    COUNT(DISTINCT cp.collection_id) as collections_count
FROM papers p
LEFT JOIN collection_papers cp ON p.paper_id = cp.paper_id
GROUP BY p.paper_id
ORDER BY p.citations_count DESC, collections_count DESC;

-- User research statistics
CREATE OR REPLACE VIEW v_user_stats AS
SELECT
    u.user_id,
    u.username,
    COUNT(DISTINCT c.collection_id) as collections_count,
    COUNT(DISTINCT cp.paper_id) as papers_saved,
    COUNT(DISTINCT a.annotation_id) as annotations_count,
    COUNT(DISTINCT s.synthesis_id) as syntheses_count
FROM users u
LEFT JOIN collections c ON u.user_id = c.user_id
LEFT JOIN collection_papers cp ON c.collection_id = cp.collection_id
LEFT JOIN annotations a ON u.user_id = a.user_id
LEFT JOIN syntheses s ON u.user_id = s.user_id
GROUP BY u.user_id;

-- Grant permissions (adjust as needed for your setup)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO max_app_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO max_app_user;
-- GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO max_app_user;

COMMENT ON DATABASE CURRENT_DATABASE() IS 'MAX AI Research Assistant - Complete research management system';
