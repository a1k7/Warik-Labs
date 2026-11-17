# Phase 0 — Reuse Plan

**Date:** 2026-11-17  
**Old repository:** [a1k7/warik-ai](https://github.com/a1k7/warik-ai) (read-only reference)  
**New repository:** [a1k7/Warik-Labs](https://github.com/a1k7/Warik-Labs) (target)

## Guiding rule

Reimplement the product in a clean architecture. Treat the old repository as a source of domain knowledge, tested edge cases, API usage patterns and product boundaries—not as a codebase to copy into the new application. No old application code has been copied into the target.

## Reuse by concept

| Reference area | Concepts worth carrying forward | New implementation approach |
|---|---|---|
| `deterministic_parser.py`, `goal_interpreter.py` | Extract intent, entities, dates, constraints and missing required information before tool execution | Create typed mission-intake schemas and a deterministic preflight layer; require provenance and confidence for extracted fields. |
| `orchestrator.py`, `universal_planner.py`, `workflow_engine.py` | Capability discovery, dependency-aware planning, input binding, optional steps, retries and partial failure | Build a provider-neutral planner over versioned tool contracts, durable checkpoints and idempotent task steps. |
| `registry.py`, `provider_selector.py` | Tool registry, provider selection, fallback and capability readiness | Create explicit capability manifests with required scopes, supported modes, side-effect class, cost estimates and evidence semantics. |
| `confirmation_service.py`, confirmation tests | User confirmation before consequential actions | Replace scattered confirmations with the central Gate: policy decision, one-time task/action-bound approval token, expiry and default-deny timeout. |
| `action_log.py`, workflow state and Action Ledger | Event history, pending work, counterparty, due date and user-recorded outcome | Create append-only action/observation events and a mission state projection. Keep evidence state separate from user-reported completion. |
| `memory.py`, `memory_context.py`, `conversation_context.py` | Explicitly stored user preferences and contextual retrieval | Rebuild as private Markdown memory with front matter, aliases, keyword retrieval, auditable read receipts, separate writer and compaction worker. |
| `travel_apis.py`, travel adapters | Provider abstraction, airport/geospatial resolution, offer refresh, clear search-vs-booking boundaries | Rebuild only the approved integrations behind isolated skill adapters; verify each current API contract and access permission first. |
| Swiggy integration package | OAuth callback, token storage/encryption, provider capability separation, mock mode | Reimplement only if current partner documentation and user-granted scopes support the intended flow. Keep mock and live modes impossible to confuse. |
| Gnani/Groq STT/TTS services | Provider abstraction, backend-only credentials, transcript review, usage accounting | Build a cost-metered speech interface with explicit user review and no secrets in browser code or model context. |
| React Settings, Memory, Action Ledger and task pages | Useful information architecture and operational visibility | Re-design in Next.js around WhatsApp-first interaction plus a mission/approval/ledger dashboard; do not port UI source. |
| Provider and workflow tests | Test cases for approval, isolation, provider fallback, missing inputs and partial failures | Write new unit, contract, integration and end-to-end tests around the new architecture and sandbox fakes. |

## Concepts to retain as product invariants

1. **A tool invocation is not success.** Record provider-returned, estimated, unverified and independently verified outcomes separately.
2. **The user remains in control.** Ask for missing information only when it blocks safe progress. Require approval for irreversible actions.
3. **Persist the mission, not only the transcript.** Preserve the original request, constraints, plan, evidence, decisions, blockers and next step.
4. **Keep providers replaceable.** No single model or merchant API should be embedded in the workflow planner.
5. **Failures are first-class.** Support provider timeouts, retries with idempotency, partial completion and manual recovery.
6. **Be honest about handoffs.** Opening a search link, deep link or provider checkout does not mean a booking/order/payment occurred.
7. **User memory must be inspectable and deletable.** The user should be able to see which memory file influenced an answer.

## Explicit non-reuse

- Do not copy old source files verbatim.
- Do not copy old database records, user data, browser cookies, local storage, access tokens or OAuth refresh tokens.
- Do not reuse old JWT signing secrets, token-encryption keys, database passwords or provider credentials.
- Do not treat legacy mock responses or handoff URLs as live provider integrations.
- Do not port the old SQLite schema as the final production schema; design Postgres migrations for the new domain.
- Do not carry forward an implicit trust model in which the model can choose arbitrary URLs, domains or tools.
- Do not use undocumented private consumer APIs, browser fingerprint spoofing or residential proxy rotation to evade access controls.

## Provider reuse decision gates

Before any adapter is implemented, record:

- Official API documentation URL and date/version reviewed.
- Evidence that the user/company has permission and the necessary partner account/scopes.
- Whether the provider exposes a sandbox/test environment and which credential class is in use.
- Exact read-only, reversible and irreversible operations available.
- Rate limits, pricing and billing ownership from official documentation.
- Idempotency, confirmation, cancellation, refund and reconciliation behavior.
- What constitutes authoritative evidence of success.
- Data sent to the provider, retention, region and deletion obligations.
- Fallback behavior when no supported API exists (usually a labelled user handoff, not a fabricated success).

## Recommended first reference implementation order (provisional)

1. WhatsApp Cloud API message intake and status/approval notifications (channel foundation, not one of the action skills).
2. One read-only skill with reliable structured responses and test credentials.
3. One user-approved reversible workflow with a verifiable provider receipt.
4. One irreversible action only after a proper sandbox, Gate and reconciliation tests exist.

The exact action skills remain open pending your selection and provider-access confirmation. Blinkit, IRCTC, BBPS, live ride booking and grocery checkout are **not** assumed to offer an open consumer API simply because a website/app exists.
