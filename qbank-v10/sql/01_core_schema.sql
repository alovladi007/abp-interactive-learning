-- =====================================================
-- sql/01_core_schema.sql
-- Core database setup and extensions
-- =====================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";
CREATE EXTENSION IF NOT EXISTS "ltree";
-- CREATE EXTENSION IF NOT EXISTS "vector";  -- Requires pgvector

-- Create schemas
CREATE SCHEMA IF NOT EXISTS qbank;
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;

-- Set search path
SET search_path TO qbank, public;