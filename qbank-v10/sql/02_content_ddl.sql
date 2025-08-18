-- =====================================================
-- sql/02_content_ddl.sql
-- Content management tables with versioning
-- =====================================================

-- Topic hierarchy with ltree for efficient queries
CREATE TABLE topics (
    id BIGSERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL DEFAULT '00000000-0000-0000-0000-000000000001'::uuid,
    parent_id BIGINT REFERENCES topics(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    blueprint_code VARCHAR(50),
    description TEXT,
    weight DECIMAL(3,2) DEFAULT 1.0 CHECK (weight BETWEEN 0 AND 1),
    path LTREE,
    is_active BOOLEAN DEFAULT TRUE,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT uq_topic_blueprint UNIQUE(tenant_id, blueprint_code)
);

CREATE INDEX idx_topics_tenant ON topics(tenant_id);
CREATE INDEX idx_topics_parent ON topics(parent_id);
CREATE INDEX idx_topics_blueprint ON topics(blueprint_code) WHERE blueprint_code IS NOT NULL;
CREATE INDEX idx_topics_path ON topics USING GIST(path);
CREATE INDEX idx_topics_metadata ON topics USING GIN(metadata);

-- Questions with soft delete and audit trail
CREATE TABLE questions (
    id BIGSERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL DEFAULT '00000000-0000-0000-0000-000000000001'::uuid,
    external_ref VARCHAR(100),
    created_by VARCHAR(255) NOT NULL,
    reviewed_by VARCHAR(255),
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_by VARCHAR(255),
    deleted_at TIMESTAMPTZ,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT uq_question_external_ref UNIQUE(tenant_id, external_ref)
);

CREATE INDEX idx_questions_tenant ON questions(tenant_id);
CREATE INDEX idx_questions_external_ref ON questions(external_ref) WHERE external_ref IS NOT NULL;
CREATE INDEX idx_questions_created_by ON questions(created_by);
CREATE INDEX idx_questions_deleted ON questions(is_deleted, deleted_at) WHERE is_deleted = TRUE;

-- Question versions with full-text search and embeddings
CREATE TABLE question_versions (
    id BIGSERIAL PRIMARY KEY,
    question_id BIGINT NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    version INT NOT NULL CHECK (version > 0),
    state VARCHAR(20) NOT NULL DEFAULT 'draft',
    stem_md TEXT NOT NULL,
    lead_in TEXT NOT NULL,
    rationale_md TEXT NOT NULL,
    difficulty_label VARCHAR(20),
    bloom_level INT CHECK (bloom_level BETWEEN 1 AND 6),
    topic_id BIGINT REFERENCES topics(id) ON DELETE SET NULL,
    tags TEXT[] DEFAULT '{}',
    assets JSONB DEFAULT '[]',
    references JSONB DEFAULT '[]',
    search_vector TSVECTOR,
    -- embedding vector(768),  -- For semantic search (requires pgvector)
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    reviewed_by VARCHAR(255),
    reviewed_at TIMESTAMPTZ,
    approved_by VARCHAR(255),
    approved_at TIMESTAMPTZ,
    
    CONSTRAINT uq_question_version UNIQUE(question_id, version),
    CONSTRAINT ck_question_state CHECK (state IN ('draft', 'in_review', 'approved', 'published', 'archived'))
);

CREATE INDEX idx_qv_question ON question_versions(question_id);
CREATE INDEX idx_qv_topic ON question_versions(topic_id);
CREATE INDEX idx_qv_state ON question_versions(state);
CREATE INDEX idx_qv_version ON question_versions(version);
CREATE INDEX idx_qv_tags ON question_versions USING GIN(tags);
CREATE INDEX idx_qv_search ON question_versions USING GIN(search_vector);
-- CREATE INDEX idx_qv_embedding ON question_versions USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX idx_qv_metadata ON question_versions USING GIN(metadata);

-- Trigger to update search vector
CREATE OR REPLACE FUNCTION update_question_search_vector() RETURNS trigger AS $$
BEGIN
    NEW.search_vector := 
        setweight(to_tsvector('english', COALESCE(NEW.stem_md, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.lead_in, '')), 'B') ||
        setweight(to_tsvector('english', COALESCE(NEW.rationale_md, '')), 'C') ||
        setweight(to_tsvector('english', COALESCE(array_to_string(NEW.tags, ' '), '')), 'D');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_question_search_vector
    BEFORE INSERT OR UPDATE ON question_versions
    FOR EACH ROW EXECUTE FUNCTION update_question_search_vector();

-- Question options with distractor analysis support
CREATE TABLE question_options (
    id BIGSERIAL PRIMARY KEY,
    question_version_id BIGINT NOT NULL REFERENCES question_versions(id) ON DELETE CASCADE,
    option_label CHAR(1) NOT NULL CHECK (option_label IN ('A', 'B', 'C', 'D', 'E', 'F')),
    option_text_md TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL DEFAULT FALSE,
    explanation_md TEXT,
    metadata JSONB DEFAULT '{}',
    
    CONSTRAINT uq_question_option UNIQUE(question_version_id, option_label)
);

CREATE INDEX idx_qo_question_version ON question_options(question_version_id);
CREATE INDEX idx_qo_correct ON question_options(is_correct) WHERE is_correct = TRUE;

-- Question publications for exam management
CREATE TABLE question_publications (
    id BIGSERIAL PRIMARY KEY,
    question_id BIGINT NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    live_version INT NOT NULL,
    exam_code VARCHAR(50) NOT NULL,
    tenant_id UUID NOT NULL DEFAULT '00000000-0000-0000-0000-000000000001'::uuid,
    published_at TIMESTAMPTZ DEFAULT NOW(),
    published_by VARCHAR(255) NOT NULL,
    expires_at TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT TRUE,
    metadata JSONB DEFAULT '{}',
    
    CONSTRAINT uq_question_publication UNIQUE(question_id, exam_code),
    CONSTRAINT fk_publication_version FOREIGN KEY (question_id, live_version) 
        REFERENCES question_versions(question_id, version)
);

CREATE INDEX idx_qp_question ON question_publications(question_id);
CREATE INDEX idx_qp_exam_code ON question_publications(exam_code);
CREATE INDEX idx_qp_tenant ON question_publications(tenant_id);
CREATE INDEX idx_qp_active ON question_publications(is_active, expires_at) WHERE is_active = TRUE;