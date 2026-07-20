-- JuraRegel Database Initialization
-- Run automatically on first container start

-- ─── Extensions ─────────────────────────────────────────────

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ─── Application Role (for RLS) ─────────────────────────────

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'juraregel_app') THEN
        CREATE ROLE juraregel_app LOGIN PASSWORD 'juraregel';
    END IF;
END
$$;

-- ─── Grant permissions ──────────────────────────────────────

GRANT CONNECT ON DATABASE juraregel TO juraregel_app;
GRANT USAGE ON SCHEMA public TO juraregel_app;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO juraregel_app;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO juraregel_app;

-- ─── RLS Helper Function ────────────────────────────────────

CREATE OR REPLACE FUNCTION current_tenant_id() RETURNS uuid AS $$
BEGIN
    RETURN NULLIF(current_setting('app.current_org', true), '')::uuid;
END;
$$ LANGUAGE plpgsql STABLE;

-- ─── Seed: Demo Organisation ───────────────────────────────

INSERT INTO organisations (id, name, sector, size, contact_email)
VALUES (
    '00000000-0000-0000-0000-000000000001',
    'Gemeente Voorbeeld',
    'overheid',
    500,
    'fg@gemeente-voorbeeld.nl'
)
ON CONFLICT (id) DO NOTHING;

-- ─── Seed: Demo Processing Activity ────────────────────────

INSERT INTO processing_activities (
    id, organisation_id, name, purpose, legal_basis,
    data_categories, data_subjects, retention_period, dpia_required
) VALUES (
    '00000000-0000-0000-0000-000000000010',
    '00000000-0000-0000-0000-000000000001',
    'WOZ-AI Waardering',
    'Automatische waardering van onroerend goed met AI',
    'Art. 6(1)(e)',
    '["Naam", "Adres", "WOZ-waarde", "Woninggegevens"]',
    '["Eigenaren", "Woningcorporaties"]',
    '7 jaar',
    true
)
ON CONFLICT (id) DO NOTHING;
