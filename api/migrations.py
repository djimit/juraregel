"""Database migrations — RLS policies + seed data.

Run once to set up:
1. Row Level Security (RLS) on all tenant tables
2. RLS policies for tenant isolation
3. Seed data (demo organisation + templates)
"""

RLS_POLICIES = """
-- ─── Enable RLS on all tenant tables ────────────────────────

ALTER TABLE processing_activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE assessments ENABLE ROW LEVEL SECURITY;
ALTER TABLE evidence ENABLE ROW LEVEL SECURITY;
ALTER TABLE approvals ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_claims ENABLE ROW LEVEL SECURITY;

-- ─── Force RLS for table owners ─────────────────────────────

ALTER TABLE processing_activities FORCE ROW LEVEL SECURITY;
ALTER TABLE assessments FORCE ROW LEVEL SECURITY;
ALTER TABLE evidence FORCE ROW LEVEL SECURITY;
ALTER TABLE approvals FORCE ROW LEVEL SECURITY;
ALTER TABLE ai_claims FORCE ROW LEVEL SECURITY;

-- ─── RLS Policies ───────────────────────────────────────────

-- Processing Activities
CREATE POLICY pa_org_isolation ON processing_activities
    USING (organisation_id = current_setting('app.current_org')::uuid);

-- Assessments
CREATE POLICY a_org_isolation ON assessments
    USING (organisation_id = current_setting('app.current_org')::uuid);

-- Evidence
CREATE POLICY e_org_isolation ON evidence
    USING (assessment_id IN (
        SELECT id FROM assessments
        WHERE organisation_id = current_setting('app.current_org')::uuid
    ));

-- Approvals
CREATE POLICY ap_org_isolation ON approvals
    USING (assessment_id IN (
        SELECT id FROM assessments
        WHERE organisation_id = current_setting('app.current_org')::uuid
    ));

-- AI Claims
CREATE POLICY ai_org_isolation ON ai_claims
    USING (assessment_id IN (
        SELECT id FROM assessments
        WHERE organisation_id = current_setting('app.current_org')::uuid
    ));

-- ─── Audit Trail (no RLS — global visibility) ──────────────
-- Audit trail is intentionally not RLS-restricted for compliance

-- ─── Regulatory Changes (no RLS — global visibility) ───────
-- Regulatory changes are global and visible to all tenants
"""

SEED_DATA = """
-- ─── Demo Organisation ──────────────────────────────────────

INSERT INTO organisations (id, name, sector, size, contact_email)
VALUES (
    '00000000-0000-0000-0000-000000000001',
    'Gemeente Voorbeeld',
    'overheid',
    500,
    'fg@gemeente-voorbeeld.nl'
);

-- ─── Demo Processing Activity ───────────────────────────────

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
    ["Eigenaren", "Woningcorporaties"],
    '7 jaar',
    true
);
"""


async def apply_rls_policies(db_url: str | None = None) -> None:
    """Apply RLS policies to the database."""
    import asyncpg

    url = db_url or "postgresql://juraregel:juraregel@localhost:5432/juraregel"
    conn = await asyncpg.connect(url)

    try:
        for statement in RLS_POLICIES.split(";"):
            stmt = statement.strip()
            if stmt and not stmt.startswith("--"):
                await conn.execute(stmt)
        print("RLS policies applied successfully")
    finally:
        await conn.close()


async def seed_database(db_url: str | None = None) -> None:
    """Seed the database with demo data."""
    import asyncpg

    url = db_url or "postgresql://juraregel:juraregel@localhost:5432/juraregel"
    conn = await asyncpg.connect(url)

    try:
        for statement in SEED_DATA.split(";"):
            stmt = statement.strip()
            if stmt and not stmt.startswith("--"):
                try:
                    await conn.execute(stmt)
                except asyncpg.exceptions.UniqueViolationError:
                    pass  # Already seeded
        print("Seed data applied successfully")
    finally:
        await conn.close()
