-- ==============================================================================
-- Oogway / Lenny Growth Assistant - Supabase PostgreSQL Schema
-- ==============================================================================

-- 1. Enable UUID Extension (standard for PostgreSQL / Supabase)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ==============================================================================
-- Table 1: sessions
-- Purpose: Tracks conversation threads, model used, and user metadata
-- ==============================================================================
CREATE TABLE IF NOT EXISTS public.sessions (
    id VARCHAR(64) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    title VARCHAR(255) NOT NULL DEFAULT 'New Strategy Chat',
    model_provider VARCHAR(64) NOT NULL DEFAULT 'ollama',
    model_name VARCHAR(128) NOT NULL DEFAULT 'llama3:latest',
    session_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT timezone('utc'::text, now()),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT timezone('utc'::text, now())
);

-- ==============================================================================
-- Table 2: messages
-- Purpose: Stores individual user queries, assistant responses, and grounding telemetry
-- ==============================================================================
CREATE TABLE IF NOT EXISTS public.messages (
    id VARCHAR(64) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    session_id VARCHAR(64) NOT NULL REFERENCES public.sessions(id) ON DELETE CASCADE,
    role VARCHAR(32) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    sources JSONB NOT NULL DEFAULT '[]'::jsonb,
    token_count INTEGER NULL,
    latency_ms INTEGER NULL,
    skill_used VARCHAR(64) NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT timezone('utc'::text, now())
);

-- ==============================================================================
-- Table 3: artifacts
-- Purpose: Interactive generated artifacts (HTML, Markdown, SVG, Mermaid)
-- ==============================================================================
CREATE TABLE IF NOT EXISTS public.artifacts (
    id VARCHAR(64) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    session_id VARCHAR(64) NOT NULL REFERENCES public.sessions(id) ON DELETE CASCADE,
    message_id VARCHAR(64) NULL REFERENCES public.messages(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    artifact_type VARCHAR(32) NOT NULL DEFAULT 'html' CHECK (artifact_type IN ('html', 'markdown', 'svg')),
    content TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT timezone('utc'::text, now())
);

-- ==============================================================================
-- Performance Indexes
-- ==============================================================================
CREATE INDEX IF NOT EXISTS idx_sessions_updated_at ON public.sessions (updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_messages_session_id ON public.messages (session_id);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON public.messages (created_at ASC);
CREATE INDEX IF NOT EXISTS idx_artifacts_session_id ON public.artifacts (session_id);
CREATE INDEX IF NOT EXISTS idx_artifacts_message_id ON public.artifacts (message_id);

-- ==============================================================================
-- Automated updated_at Trigger for sessions
-- ==============================================================================
CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = timezone('utc'::text, now());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_sessions_updated_at ON public.sessions;
CREATE TRIGGER trigger_sessions_updated_at
BEFORE UPDATE ON public.sessions
FOR EACH ROW
EXECUTE FUNCTION public.set_updated_at();

-- ==============================================================================
-- Supabase Row Level Security (RLS) & Access Control
-- ==============================================================================
ALTER TABLE public.sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.artifacts ENABLE ROW LEVEL SECURITY;

-- Allow full CRUD for anon and authenticated API clients (development & app backend)
CREATE POLICY "Allow public full access to sessions"
    ON public.sessions
    FOR ALL
    TO anon, authenticated, service_role
    USING (true)
    WITH CHECK (true);

CREATE POLICY "Allow public full access to messages"
    ON public.messages
    FOR ALL
    TO anon, authenticated, service_role
    USING (true)
    WITH CHECK (true);

CREATE POLICY "Allow public full access to artifacts"
    ON public.artifacts
    FOR ALL
    TO anon, authenticated, service_role
    USING (true)
    WITH CHECK (true);
