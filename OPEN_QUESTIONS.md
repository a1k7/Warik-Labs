# Phase 0 — Open Questions and Approval Gate

**Date:** 2026-11-17  
**Target repository:** [a1k7/Warik-Labs](https://github.com/a1k7/Warik-Labs)

Phase 0 audit documents are now the only files intended for this repository. No application code has been started. Phase 1 remains blocked until the owner approves the architecture and answers the decisions below.

## Decisions needed

### 1. Canonical old-repository branch

The old repository has divergent branches. My recommended reference is:

`codex/warik-intelligence-workspace-2026-11-16`

It contains the newer execution thesis, Action Ledger/Memory workspace and expanded planning/provider work. `codex/india-first-follow-through-2026-11-16` is also substantially ahead of `main` and has a different set of commits. Should the workspace branch be the primary reference, with the follow-through branch used only for comparison?

### 2. Deployment target and data residency

Where should the first deployable environment run?

- Local-only demo on your machine.
- Managed platform with an India region, if available for the required services.
- AWS Mumbai (`ap-south-1`) or another cloud region.
- Another target you already have access to.

Also confirm whether India-region storage is a strict requirement for all personal data, or a preference where technically and commercially feasible. WhatsApp, model and provider processing may involve separate data flows that need to be documented.

### 3. Cost ceiling

What is the hard budget per completed task, in INR, for model inference, browser VM time, database/queue, messaging and provider charges? Please also specify the acceptable monthly infrastructure ceiling for the first pilot. The design should enforce per-task and per-user budgets rather than merely estimate them.

### 4. First 3–4 action skills

Which 3–4 skills should be built first?

Candidate set from your brief:
- Blinkit / grocery ordering
- IRCTC train search and booking
- Flight search (MakeMyTrip/Goibibo or an approved flight API)
- Hotel search
- Ola/Uber cab booking
- Swiggy / Zomato food ordering
- Restaurant reservations
- BBPS bill fetch/payment
- Mobile recharge

My recommendation is to start with read-only/search capabilities where a documented API and test account can be obtained, then add one reversible action, and only later an irreversible transaction. For any provider without documented partner access or a sandbox, the first release should provide an honest handoff rather than claim an order or booking was completed.

### 5. Payment service provider

Choose the initial payment integration: **Razorpay or Cashfree**. Development will use test/sandbox credentials only; no live UPI transaction, mandate, recharge or bill payment will run without your explicit written approval. Also confirm whether payments should be excluded completely from the first public demo.

### 6. Browser sandbox

Do you already have an E2B account/credits or another approved microVM provider? If not, should Phase 2 begin with local Dockerized Chromium and a provider interface, with remote per-task VMs added only when budget and region are approved?

### 7. Initial user and language scope

Who is the first user cohort: students, young professionals, households, or another group? Confirm whether English + Hinglish is sufficient for the first pilot, or name the first additional Indian language.

## Access required

The GitHub connection can read both repositories and has write/admin permissions. The target repository is empty, so no more repository access is currently required.

The following are **not** visible through GitHub and are not required to complete Phase 0:

- Ignored local `.env` files on your Mac.
- Render, Vercel, AWS or other deployment environment values.
- Provider dashboard keys, partner approvals or account scopes.
- Meta Business Manager / WhatsApp Business Account configuration.

Do not paste secrets into chat. When the new provider configuration is approved, copy only the credentials you explicitly authorise, locally, into the new gitignored `.env.local` or into the selected deployment's secret manager. For development, use separate test/sandbox keys only. I will not make live provider calls using credentials from the old repository unless you explicitly approve that specific provider and operation.

## Phase 0 exit checklist

- [x] Confirm old/new repository access and target branch state.
- [x] Enumerate old repository branches and identify divergent advanced references.
- [x] Inspect source tree, framework/dependency files, configuration, environment templates, deployment template and provider guide.
- [x] Inventory environment-variable names and secret-bearing settings without displaying values.
- [x] Identify reusable domain patterns and missing requested subsystems.
- [x] Produce Phase 0 audit documents in the new repository.
- [ ] Owner confirms canonical legacy branch.
- [ ] Owner answers deployment, budget, skills, PSP, sandbox and initial audience questions.
- [ ] Owner explicitly approves Phase 1.

## Approval required

Reply with your decisions and explicitly say **“Approve Phase 1”** when you want the scaffold to begin. Until then, keep the target limited to these Phase 0 documents.
