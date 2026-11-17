# Phase 0 — Architecture Notes

**Audit date:** 2026-11-17  
**Old repository (read-only reference):** [a1k7/warik-ai](https://github.com/a1k7/warik-ai)  
**New repository (target):** [a1k7/Warik-Labs](https://github.com/a1k7/Warik-Labs)

## 1. Repository state and audit scope

- The target repository's `main` branch is empty (GitHub reports an empty Git tree). This is the correct clean target for a new application.
- The reference repository is public and has eight branches: `main`, `codex/india-first-follow-through-2026-11-16`, `codex/india-first-voice-assistant-2026-11-16`, `codex/production-readiness-2026-11-16`, `codex/warik-intelligence-workspace-2026-11-16`, `fix/postgres-workflow-json-cas`, `fix/warik-ai-reliability-audit`, and `integration/warik-ai-redesign`.
- `main` had 210 tracked files and its latest listed commit was 2026-11-14. The two advanced November 16 branches have 229 and 232 tracked files respectively, and each has diverged from main. The workspace branch contains a product thesis updated 2026-11-17.
- The review inspected main's tree, configuration and representative application files, plus both advanced branch heads' configuration, production templates, README and architecture/provider documents. It also compared their file-level changes against main.
- A full historical secret scan, provider-dashboard audit, cloud-environment audit, and local ignored-file audit have not been performed.

## 2. Existing stack and application shape

### Main branch

- **Frontend:** React 18, TypeScript, Vite, Tailwind CSS, React Router.
- **Backend:** Python, FastAPI, Pydantic / pydantic-settings, SQLAlchemy.
- **Persistence:** SQLite for local use with PostgreSQL support/configuration.
- **Inference:** Ollama and Groq provider paths.
- **Voice:** Gnani and Groq speech-provider paths.
- **Authentication:** JWT bearer tokens and password hashing.
- **Tests:** pytest suite covering API, parsing, workflow governance, confirmation, travel, provider selection, voice and database behavior.

### Advanced workspace / follow-through branches

The newer branches add or refine:

- Dockerfiles, a production Compose stack with PostgreSQL and Nginx, and GitHub Actions CI for backend tests, frontend build and container build.
- A more mature orchestrator, deterministic parser, universal planner, provider fallbacks and a capability-readiness endpoint.
- A commitment/action-ledger domain model and API; contextual next-step advice; a Memory page and Action Ledger page.
- A provider setup guide and India-first product strategy / execution thesis.
- Additional test coverage around capability readiness, commitment detection, workflow fallback, provider behavior and planning.

The advanced workspace branch is the recommended design reference because its README and product thesis explicitly describe the latest product boundary and execution-oriented direction. The two advanced branches are divergent; do not merge them wholesale or assume one is a clean superset.

## 3. Existing domain logic and integrations

| Area | What exists in the reference repository | Actual boundary / limitation to preserve |
|---|---|---|
| Agent orchestration | Deterministic parsing, goal interpretation, orchestrator, universal planner, workflow engine, tool registry | This is a tool-driven assistant workflow, not a general browser-control agent. |
| Workflow state | Multi-step workflows, dependencies/input bindings, optional steps, retry/partial-failure paths and persisted state | Rebuild with explicit idempotency, durable checkpoints and side-effect recovery. |
| Approval | Confirmation service and confirmation-aware tools | Not yet a universal policy gate for every external action. New design must enforce one central default-deny gate. |
| Audit | Action logs and workflow/commitment records | Not a full immutable, replay-complete browser action/observation ledger. |
| Memory | User memory records and context retrieval from the application database | Not a Markdown filesystem, not git-tracked memory, and not an isolated background compactor. |
| Browser | HTTP research/search utilities and HTML parsing | No dedicated Playwright/CDP browser driver, visual grounding loop, persistent logged-in browser profile, or browser sandbox was found in the reviewed trees. |
| Messaging | Web application chat / API | No WhatsApp Cloud API webhook, SMS/Exotel/Twilio adapter, or iMessage channel was found. |
| Scheduling | Tasks and reminders | No durable proactive event scheduler/cron integration for email, calendar, location or external webhooks was found. |
| Vault | Environment-backed settings and encrypted Swiggy OAuth-token support | No general-purpose Vault/capability-token broker or secret injection into an ephemeral browser sandbox. |
| Sandbox | Local application runtime and Docker deployment | No E2B, Firecracker, per-task microVM, or remote desktop/browser isolation found. |
| Payments | No UPI, BBPS, autopay/mandate or payment orchestration implementation found | Payment work must be a separately gated and sandbox-only subsystem. |
| Food | Restaurant discovery, provider/handoff patterns, Swiggy integration code | Newer documentation says Swiggy defaults to mock mode; do not present mock output as live data. |
| Travel | Flight offer search via configured Duffel path; optional Booking.com Demand API search/redirect; travel/geospatial provider adapters; Uber/Ola links | Flight search/refresh is not ticketing. Hotel search/redirect is not booking/payment. Cab/rail/IRCTC paths are handoffs, not live fares or reservations. |
| Voice | Browser voice capture/transcription with transcript review, Gnani/Groq provider paths | Voice is disabled unless configured; credentials must remain backend-only. |
| Dashboard | Chat, tasks, reminders, expenses, travel, food, settings, memory and action-ledger views on advanced branches | Useful product/domain references, not the requested WhatsApp-first management/observability console. |

### Important provider boundaries documented by the newer reference branch

- Duffel is used for flight offer search and offer refresh; the code does not create orders, issue tickets or collect payment.
- Booking.com Demand API is an optional partner-access search-and-redirect integration; it is not a Warik booking or payment.
- Uber/Ola, IRCTC, RedBus and MakeMyTrip are described as external handoffs, not bookings or live fare/seat inventory.
- Swiggy's default mode is mock; account connection and MCP permissions are managed separately.
- Restaurant results are candidates; menu, price, dietary suitability and availability are not independently guaranteed.

The source guide is [docs/PROVIDER_SETUP.md on the workspace branch](https://github.com/a1k7/warik-ai/blob/codex/warik-intelligence-workspace-2026-11-16/docs/PROVIDER_SETUP.md). These boundaries must be revalidated against current official provider documentation and actual partner access before implementing any skill.

## 4. Gap against the requested Instinct-like architecture

The old repository offers reusable domain patterns, but does not implement the defining subsystems in the mission:

1. **Loop:** no perception/action state machine around browser actions, DOM/CDP plus screenshot fallback, context/token budgeting per frame, or full replayable observation/action ledger.
2. **Browser identity:** no persistent browser session store designed as a high-value credential vault.
3. **Memory:** no structured Markdown memory hierarchy, auditable alias/grep retrieval, or separate writer/compaction worker.
4. **Scheduler:** no source-driven proactive trigger engine.
5. **Vault:** no general credential broker with short-lived per-skill capability tokens.
6. **Gate:** confirmation logic exists, but it is not yet a central policy engine covering all external side effects, timeouts and default-deny semantics.
7. **Sandbox:** no per-task isolated browser VM or durable separation between browser session data and disposable compute.
8. **WhatsApp:** no WhatsApp-first channel adapter or webhook lifecycle.
9. **India actions:** no UPI/BBPS execution, verified Blinkit grocery checkout, IRCTC ticketing, live ride booking or verified merchant order outcome.

## 5. Recommended new architecture (subject to approval)

### Core stack

- **Monorepo:** pnpm workspaces + Turborepo for JavaScript packages, with a separate Python workspace managed by `uv`. Keep the Python dependency graph independent of Node.
- **Web/dashboard:** Next.js App Router, TypeScript, Tailwind and shadcn/ui.
- **API/orchestrator:** Python FastAPI. This keeps one typed Python execution stack for the agent, browser tools and workers and provides the least conceptual migration from the reference backend. Do not port old modules verbatim.
- **Workers/queue:** Redis plus a Python-native durable worker framework (ARQ, Celery or Dramatiq; choose after load/retry requirements are confirmed). BullMQ is a natural fit for a Node worker, but would add a second job-runtime if the orchestrator remains Python.
- **Data:** PostgreSQL for users, tasks/missions, actions, approvals, memory metadata, integrations and append-only ledger events. Use explicit migrations from the first schema.
- **Browser:** Playwright using CDP where supported, with visual grounding as a controlled fallback. E2B or an equivalent isolated microVM can be evaluated after per-task cost and region are known; local Dockerized Chromium is for development only.
- **Memory:** Markdown documents with YAML front matter and wiki links, stored in a private, tenant-isolated encrypted data store. Do **not** commit personal memory to the application's source Git repository: deleting a file does not remove its contents from Git history. Retain an auditable version history outside the public source repo.
- **Vault:** local-only secrets via ignored `.env.local`; production through a managed secret store/KMS or Vault. Expose only short-lived, narrowly scoped capability tokens to workers; never inject raw secrets into model prompts.
- **Messaging:** a WhatsApp Cloud API adapter and verified webhook handler as the primary user channel; the dashboard is for owner operations, approvals and observability. Keep SMS/voice adapters separate and later.
- **Observability:** structured, redacted logs, OpenTelemetry traces, task/step cost accounting, durable action observations and ledger replay.

### Safety and integrity requirements

- Route browser access through an explicit domain allowlist and per-user authorization. Prefer official APIs and partner integrations over browser automation.
- Do not use rotating residential proxies or device-fingerprint spoofing to bypass a provider's anti-abuse systems, access controls or geographic restrictions. Use documented provider-approved egress and comply with each site's terms.
- Treat browser cookies, local storage, refresh tokens and session exports as root-equivalent credentials: encrypt at rest, isolate by tenant, restrict operators, audit access, support revocation, and never put them in prompts or logs.
- Use a policy gate for every side effect. Read-only/reversible actions may proceed within scope; irreversible actions require a one-time, expiring, task/action-bound approval. Timeout, malformed approval, replay or policy uncertainty must resolve to DENY.
- Add idempotency keys and external-effect reconciliation. Never automatically retry an action when the external outcome is uncertain.
- Keep a separate observation/action ledger with redacted PII in ordinary logs and restricted full-fidelity evidence only when strictly necessary.
- Implement consent, purpose-specific processing, data minimisation, access/export, correction, deletion and retention controls. Treat data residency as a deployment decision to verify, not as an automatic property of a provider.
- Never handle real money, create a real booking or send an irreversible message in development. Use test/sandbox provider accounts and explicit written approval before any live pilot.

### Proposed delivery sequence after approval

1. Scaffold monorepo, CI, typed configuration, migrations, PostgreSQL/Redis local compose and baseline security tests.
2. Build the agent state machine, tool contracts, browser/CDP driver, vision fallback, per-task budget controls and replay ledger.
3. Build WhatsApp webhook intake, message-to-mission orchestration, approval messages and default-deny timeout behavior.
4. Add Markdown memory service, auditable retrieval, read-only agent access, separate writer/compaction job and scheduler.
5. Add vault/capability tokens and only the approved 3–4 reference skills, in provider sandbox/test mode.
6. Add management dashboard, approvals inbox, ledger replay, memory viewer, integrations, cost/trace views, consent/deletion, rate limits and security hardening.

## 6. Compliance and provider documentation checkpoints

- Meta documents WhatsApp Business Platform as an API surface for sending/receiving messages and identifies webhooks, templates, pricing and authentication as separate platform topics: [Meta WhatsApp Business Platform overview](https://developers.facebook.com/documentation/business-messaging/whatsapp/overview/). Exact message types, template rules, pricing and webhook behavior must be checked against the approved app/version during implementation.
- India's Digital Personal Data Protection Rules, 2025 were published in the Gazette on 13 November 2025 and have staged commencement dates. The applicable provisions and dates must be mapped before launch; this is not a legal compliance opinion. [Official Gazette notification, G.S.R. 846(E)](https://egazette.gov.in/WriteReadData/2025/267650.pdf).
- Razorpay's official documentation distinguishes test and live modes and separate keys; test-mode actions do not move real money. This is suitable for a sandbox evaluation, not proof of production readiness: [Razorpay test/live modes](https://tfs.np.razorpay.in/docs/payments/dashboard/test-live-modes).
- No provider API contract, public rate limit, price, partner entitlement or production credential should be assumed from this audit. Obtain and pin the current first-party documentation and access grant for each selected skill before implementing it.

## 7. Audit conclusion

The reference repository is a useful source of product-domain knowledge and tested agent workflow patterns. It is not a ready-made foundation for the requested Instinct-like product. The new application must add the messaging channel, browser execution/sandbox, durable memory architecture, central gate, scheduler, vault, and complete audit/observability layer as first-class systems. The empty target repository is suitable for that clean implementation.
