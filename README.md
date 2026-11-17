# Warik Labs

**India-first personal execution assistant.**

The primary user surface is planned to be WhatsApp. The web console is the owner's Mission Control for approvals, mission state, memory, integrations and audit evidence.

## Phase 1 scaffold

This branch introduces the monorepo foundation:

- `apps/console`: Next.js App Router dashboard shell.
- `apps/api`: FastAPI service, configuration, database foundation and health checks.
- `apps/api/alembic`: database migrations.
- PostgreSQL and Redis for local development.
- GitHub Actions CI for Python and TypeScript.
- Initial domain tables for users, tasks, actions, approvals, memories, integrations and ledger events.

No live WhatsApp, LLM, browser, payment, travel or commerce integration is enabled in this phase.

## Requirements

- Node.js 20.9 or newer.
- pnpm 12.21.0.
- Python 3.13.
- Docker Desktop with Docker Compose.

## Local setup

1. Copy the root `.env.example` to `.env.local` in the repository root for the API.
2. Copy `apps/console/.env.example` to `apps/console/.env.local` for the browser-visible API base URL.
3. Keep all real credentials in local ignored files or a secret manager. Do not commit them.
3. Start local infrastructure:

```bash
docker compose up -d postgres redis
```

4. Install JavaScript dependencies:

```bash
corepack enable
corepack prepare pnpm@12.21.0 --activate
pnpm install
```

5. Start the API:

```bash
cd apps/api
python3.13 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

6. In another terminal, start the dashboard:

```bash
pnpm --filter @warik/console dev
```

Open http://localhost:3000. API docs are at http://localhost:8000/docs.

## Database changes

Create a migration after model changes:

```bash
cd apps/api
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

Never rely on `create_all()` in a deployed environment. Review generated migrations before committing them.

## Verification

```bash
pnpm lint
pnpm typecheck
pnpm build

cd apps/api
ruff check app tests
pytest
```

## Security posture in this scaffold

- No old repository credentials are reused.
- No provider key is required for local startup.
- Payments and live browser actions default to disabled.
- The local Postgres password in Compose is a development-only value, not a production credential.
- Production must provide a new high-entropy JWT secret and managed database/Redis credentials.
- Health endpoints do not disclose environment values.
- Ledger events are designed as append-only audit records; application-level append-only enforcement and hash-chain verification are later hardening tasks.

## Current limitations

This is a Phase 1 foundation, not a production-ready agent. WhatsApp webhook verification, task orchestration, the universal approval gate, CDP browser worker, Markdown memory service, scheduler, vault, real provider skills, consent/deletion workflows and full observability are future phases.
