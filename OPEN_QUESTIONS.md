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


---

# Owner selections received — 2026-11-17

The owner's uploaded screenshots show the following selections. These are recorded as decisions, not as permission to start Phase 1.

| Decision | Selected value | State |
|---|---|---|
| Canonical legacy reference | `codex/warik-intelligence-workspace-2026-11-16` | Resolved |
| Deployment target | AWS Mumbai (`ap-south-1`) | Selected; free-account eligibility and available services must be checked |
| Maximum task cost | ₹0 / free wherever possible | Hard constraint |
| First action skills | Flight search, grocery ordering (Blinkit/BigBasket), food ordering (Swiggy/Zomato), cab booking (Ola/Uber) | Selected; official API/partner access still unverified |
| Payment provider | Exclude payments from initial demo | Resolved; no PSP integration in initial demo |
| Browser sandbox | Local Docker Chromium first | Resolved for development; do not assume it is a production isolation boundary |
| Initial audience | Broad consumer audience | Selected as positioning; narrow pilot cohort still needs validation |

## Feasibility note: AWS Mumbai with a ₹0 hard budget

AWS currently documents a Free account plan for eligible new customers with up to USD $200 in credits over a period capped at six months; the plan only exposes selected services and ends when the credits are exhausted or the six-month period expires. Existing AWS customers or people who previously had an AWS account may be ineligible. This is a temporary proof-of-concept allowance, not a sustainable ₹0 production hosting commitment. See [AWS Free Tier](https://aws.amazon.com/free/), [AWS Free Tier FAQs](https://aws.amazon.com/free/free-tier-faqs/) and [AWS account plan documentation](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier-plans.html).

Before committing to AWS, confirm whether the account is eligible for the Free plan and confirm that every required resource/service can be used in `ap-south-1` under that plan. If it is not eligible, keep the first environment local and defer AWS deployment rather than incur charges.

## Remaining confirmations

1. Does the AWS account qualify as a **new-customer Free plan** account? Do not share billing/payment details in chat.
2. Is a WhatsApp Business Account / Meta developer app already available, or should the first demo use a local WhatsApp webhook simulator until access is configured?
3. Is the broad audience only a long-term product target, with a small opt-in pilot group for testing? A broad positioning statement is not a substitute for usability validation.
4. For any of the four selected skills, please confirm whether you already have approved partner/API access. No integration will be assumed available merely because the consumer website/app exists.

## Credentials and API endpoint supplied after the initial audit

- The Render URL supplied is recorded as the old backend's reference endpoint only. A browser-based request to its health path was not accessible in this audit; no uptime or correctness claim is made.
- Environment values supplied in chat and non-empty values found in the uploaded archive are classified as exposed and must not be reused. See the updated `SECRETS_INVENTORY.md`.
- No old credential was used to call the Render service or any provider API.
- Do not attach or paste another unredacted `.env`, token file, connection string or key. A redacted key-name-only export is sufficient for future configuration review.

## Phase 1 gate remains closed

The decisions above resolve the original architecture questions, but they do **not** constitute an explicit implementation approval. Phase 1 remains blocked until you say **“Approve Phase 1”** after addressing the exposed credentials and confirming the AWS account's no-cost eligibility (or choosing local-first).

