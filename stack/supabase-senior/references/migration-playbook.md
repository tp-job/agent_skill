# Migration Playbook — Postgres → Supabase

Moving an existing Postgres database onto Supabase: checklist, the three paths, pg_dump/pg_restore, and the post-migration steps.

## 4. MIGRATION PLAYBOOK — POSTGRES → SUPABASE

### Pre-Migration Checklist

```sql
-- Run on SOURCE database before anything
SELECT pg_size_pretty(pg_database_size(current_database())) AS db_size;
SELECT version();
SELECT extname FROM pg_extension ORDER BY extname;
SELECT count(*) FROM pg_stat_activity;
-- Compare extensions against Supabase's available list
SELECT name FROM pg_available_extensions ORDER BY name; -- (run on Supabase target)
```

### Three Migration Paths

|Method|Downtime|Complexity|Best For|
|---|---|---|---|
|**Google Colab notebook**|~hours|Low|< 10 GB, guided|
|**pg_dump / pg_restore**|Maintenance window|Medium|Any size|
|**Logical Replication**|Near-zero|High|Postgres 10+, large prod DBs|

### pg_dump / pg_restore (canonical)

```bash
# Step 1: Dump (always use --no-owner --no-privileges for Supabase)
pg_dump \
  --host=<source_host> --port=5432 \
  --username=<user> --dbname=<db> \
  --jobs=4 --format=directory \
  --no-owner --no-privileges --no-subscriptions \
  --verbose --file=./db_dump 2>&1 | tee dump.log

# Step 2: Restore to Supabase (use session pooler port 5432)
export SUPABASE_URL="postgresql://postgres.[ref]:[pw]@aws-0-[region].pooler.supabase.com:5432/postgres"
pg_restore \
  --host=... --port=5432 \
  --username=postgres --dbname=postgres \
  --jobs=4 --format=directory \
  --no-owner --no-privileges \
  --verbose ./db_dump 2>&1 | tee restore.log
```

### Post-Migration (always required)

```sql
-- 1. Re-enable RLS on all tables (not migrated by pg_dump)
SELECT 'ALTER TABLE "' || tablename || '" ENABLE ROW LEVEL SECURITY;'
FROM pg_tables WHERE schemaname = 'public';

-- 2. Recreate roles / grants (not migrated)
-- 3. Re-create auth triggers
-- 4. Verify extensions installed on Supabase target
-- 5. Test RLS policies with anon key (not service_role)
```
