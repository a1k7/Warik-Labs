# Secrets and Environment Inventory

**Audit date:** 2026-11-17  
**Reference repository:** [a1k7/warik-ai](https://github.com/a1k7/warik-ai)  
**Reference branches inspected:** `main`, `codex/india-first-follow-through-2026-11-16`, `codex/warik-intelligence-workspace-2026-11-16`, plus the remaining five listed in the Phase 0 architecture notes.  
**Target repository:** [a1k7/Warik-Labs](https://github.com/a1k7/Warik-Labs)

## Executive finding

No populated provider credential was found in the checked-in `.env.example`, `.env.production.example`, or the inspected settings defaults. Sensitive settings are blank/None, except for a development JWT placeholder and test-only CI configuration. The production example contains placeholders, not a usable production password or token.

This is **not** a certification that the repository has never contained a secret. This pass did not inspect every historical Git blob, GitHub Actions secret, Render/deployment environment, or local ignored file. Since the old repository is public, any credential ever committed to any reachable or historical revision must be treated as exposed and rotated—even if later deleted.

No old key was used to contact a provider. No key value is reproduced in this document.

## Source and status legend

- **Blank / None:** the committed template or settings default contains no credential value.
- **Placeholder:** a human-readable development or deployment placeholder, not a safe production secret.
- **Config-only:** a setting exists in the application configuration but is absent from the root environment template; no value was observed in the inspected defaults.
- **Unknown environment:** the variable can carry a test or production credential, but its type cannot be determined without inspecting the private local/deployment value. Do not assume it is sandbox.
- **Non-secret configuration:** URL, feature flag, model name, timeout, port, partner identifier, or similar metadata. Some URLs/IDs can still reveal infrastructure details and should be handled sensibly.

## Credential and secret-bearing inventory

| Name | Service / purpose | Observed state in inspected refs | Test or production assessment |
|---|---|---|---|
| `JWT_SECRET` | Application authentication; signs JWTs | Development placeholder in settings, dummy test value in CI, placeholder in production example; no real value in checked-in env templates | **High risk if deployed unchanged.** Generate a unique high-entropy production secret. Rotate if a real value was ever committed or shared. |
| `DATABASE_URL` | SQLAlchemy database connection | Local SQLite example; production Compose constructs a PostgreSQL DSN from deployment variables | Treat as secret-bearing in production because it can contain username/password. No production DSN observed. |
| `POSTGRES_PASSWORD` | Production PostgreSQL container | Placeholder in `.env.production.example` | Production-intended template variable, not an observed live password. Generate a new value at deployment. |
| `GNANI_API_KEY` | Gnani speech-to-text / text-to-speech provider | Blank in `.env.example` and production example; settings default empty/None | No test or production key observed. Use a dedicated test credential first. |
| `GNANI_ORG_ID` | Gnani account/organisation identifier | Blank in templates | Identifier, not necessarily an authentication secret. Treat as account metadata. |
| `GNANI_USER_ID` | Gnani account/user identifier | Blank in templates | Identifier, not necessarily an authentication secret. Treat as account metadata. |
| `GROQ_API_KEY` | Groq hosted inference / speech provider | Blank in templates; settings default empty/None | No test or production key observed. Any configured key must remain server-side. |
| `GEOAPIFY_API_KEY` | Geoapify geocoding / places provider | Config-only; empty/None default; omitted from the root sample template | No key observed. Add an explicit placeholder to the new template only if this provider is retained. |
| `DUFFEL_API_KEY` | Duffel flight-offer API | Blank in newer branch templates; empty/None default | No key observed. Test/live mode cannot be inferred; use a sandbox/test key for development. |
| `STAYAPI_KEY` | StayAPI hotel provider setting | Config-only; empty/None default | No key observed; active provider contract and intended use require validation. |
| `REEF_API_KEY` | Reef provider setting | Config-only; empty/None default | No key observed; active provider contract and intended use require validation. |
| `BOOKING_API_TOKEN` | Booking.com Demand API | Blank in newer branch templates; empty/None default | No partner token observed. Partner access and environment must be confirmed before use. |
| `AGODA_API_KEY` | Agoda provider setting | Config-only; empty/None default | No key observed; active provider contract and intended use require validation. |
| `SWIGGY_TOKEN_ENCRYPTION_KEY` | Encryption key for stored Swiggy OAuth tokens | Blank in templates; empty/None default | No key observed. Generate a new, independent key for the new system; never reuse JWT or application secrets. |
| `SWIGGY_CLIENT_ID` | Swiggy OAuth client identifier | Blank in templates; empty/None default | No client ID observed. A client ID is not always secret, but keep integration configuration server-side unless the approved flow says otherwise. |

### Partner identifiers (not assumed to be secrets)

| Name | Service / purpose | Observed state |
|---|---|---|
| `BOOKING_AFFILIATE_ID` | Booking.com affiliate identifier | Blank in newer templates; not a password/token. |
| `AGODA_AFFILIATE_ID` | Agoda affiliate identifier | Config-only; empty/None default. |
| `GNANI_ORG_ID`, `GNANI_USER_ID` | Gnani tenant/user identifiers | Blank in templates. |

## Complete environment-variable inventory

The following is the union of settings discovered in the inspected application configuration, root templates, production template, Compose file, CI configuration, and setup documentation. Pydantic settings fields are listed in their conventional uppercase environment-variable form.

| Name | Service / purpose | Classification |
|---|---|---|
| `APP_NAME` | Application display/configuration name | Non-secret configuration |
| `ENVIRONMENT` | Runtime environment selector | Non-secret configuration; security-sensitive behavior switch |
| `DATABASE_URL` | Application database DSN | Secret-bearing in production |
| `CORS_ORIGINS` | Allowed browser origins | Non-secret security configuration |
| `JWT_SECRET` | JWT signing secret | Secret |
| `JWT_ALGORITHM` | JWT signing algorithm | Non-secret security configuration |
| `JWT_EXPIRE_MINUTES` | JWT expiry | Non-secret security configuration |
| `GNANI_API_KEY` | Gnani API credential | Secret |
| `GNANI_ORG_ID` | Gnani organisation identifier | Account metadata |
| `GNANI_USER_ID` | Gnani user identifier | Account metadata |
| `GNANI_STT_URL` | Gnani speech-to-text endpoint | Endpoint configuration |
| `GNANI_TTS_URL` | Gnani text-to-speech endpoint | Endpoint configuration |
| `VOICE_ENABLED` | Voice feature switch | Feature configuration |
| `VOICE_USAGE_LIMIT_SECONDS` | Voice usage cap | Limit configuration |
| `VOICE_MAX_UPLOAD_BYTES` | Voice upload limit | Limit configuration |
| `VOICE_MAX_DURATION_SECONDS` | Voice duration limit | Limit configuration |
| `VOICE_TTS_CHAR_LIMIT` | TTS character limit | Limit configuration |
| `LLM_PROVIDER` | Hosted/local LLM provider selector | Provider configuration |
| `OLLAMA_BASE_URL` | Ollama endpoint | Endpoint configuration |
| `OLLAMA_MODEL` | Ollama model name | Model configuration |
| `OLLAMA_PLANNER_MODEL` | Planner model on workspace branch | Model configuration |
| `OLLAMA_NUM_CTX` | Ollama context-window setting | Model configuration |
| `OLLAMA_NUM_PREDICT` | Ollama output-token setting | Model configuration |
| `GROQ_API_KEY` | Groq API credential | Secret |
| `GROQ_MODEL` | Groq model name | Model configuration |
| `NOMINATIM_URL` | Nominatim endpoint | Endpoint configuration |
| `OVERPASS_URL` | Overpass API endpoint | Endpoint configuration |
| `GEO_USER_AGENT` | Geospatial service user-agent | Service identification |
| `GEO_TIMEOUT_SECONDS` | Geospatial HTTP timeout | Runtime configuration |
| `OVERPASS_TIMEOUT_SECONDS` | Overpass timeout | Runtime configuration |
| `NOMINATIM_MIN_INTERVAL_SECONDS` | Nominatim request pacing | Runtime configuration |
| `AIRPORT_SEARCH_RADIUS_M` | Airport resolution radius | Domain configuration |
| `GEOAPIFY_API_KEY` | Geoapify API credential | Secret; config-only |
| `DUFFEL_API_KEY` | Duffel API credential | Secret |
| `STAYAPI_KEY` | StayAPI credential | Secret; config-only |
| `REEF_API_KEY` | Reef credential | Secret; config-only |
| `SWIGGY_TOKEN_ENCRYPTION_KEY` | Swiggy token-at-rest encryption key | Secret |
| `SWIGGY_CLIENT_ID` | Swiggy OAuth client identifier | Integration credential/config |
| `SWIGGY_REDIRECT_URI` | Swiggy OAuth callback | Endpoint configuration |
| `SWIGGY_FRONTEND_RETURN_URL` | Post-OAuth frontend return URL | Endpoint configuration |
| `SWIGGY_AUTHORIZE_URL` | Swiggy OAuth authorisation endpoint | Endpoint configuration |
| `SWIGGY_TOKEN_URL` | Swiggy OAuth token endpoint | Endpoint configuration; not itself a token |
| `SWIGGY_LOGOUT_URL` | Swiggy logout endpoint | Endpoint configuration |
| `SWIGGY_OAUTH_SCOPE` | Swiggy OAuth scopes | Permission configuration |
| `SWIGGY_MODE` | Swiggy mock/live mode selector | Environment/feature configuration |
| `SWIGGY_FOOD_MCP_URL` | Swiggy food MCP endpoint | Endpoint configuration |
| `SWIGGY_INSTAMART_MCP_URL` | Swiggy Instamart MCP endpoint | Endpoint configuration |
| `SWIGGY_DINEOUT_MCP_URL` | Swiggy Dineout MCP endpoint | Endpoint configuration |
| `SWIGGY_SCENES_MCP_URL` | Swiggy Scenes MCP endpoint | Endpoint configuration |
| `AGODA_MODE` | Agoda provider mode | Environment/feature configuration |
| `AGODA_AFFILIATE_URL` | Agoda affiliate URL | Endpoint/configuration |
| `AGODA_AFFILIATE_ID` | Agoda affiliate identifier | Partner metadata |
| `AGODA_API_KEY` | Agoda API credential | Secret; config-only |
| `BOOKING_MODE` | Booking.com provider mode | Environment/feature configuration |
| `BOOKING_API_BASE_URL` | Booking.com API base endpoint | Endpoint configuration |
| `BOOKING_API_TOKEN` | Booking.com Demand API token | Secret |
| `BOOKING_AFFILIATE_ID` | Booking.com affiliate identifier | Partner metadata |
| `POSTGRES_DB` | Production PostgreSQL database name | Non-secret deployment configuration |
| `POSTGRES_USER` | Production PostgreSQL username | Deployment credential metadata |
| `POSTGRES_PASSWORD` | Production PostgreSQL password | Secret |
| `VITE_API_BASE_URL` | Frontend API base URL | Public frontend configuration; never put secrets in `VITE_*` |
| `FRONTEND_BIND` | Frontend host bind address | Deployment configuration |
| `FRONTEND_PORT` | Frontend published port | Deployment configuration |
| `BACKEND_BIND` | Backend host bind address | Deployment configuration |
| `BACKEND_PORT` | Backend published port | Deployment configuration |

## Repository hygiene findings

- The current `main` tree contains `.env.example`, but no tracked `.env`, `.env.local`, token JSON, or credential-named file.
- The two reviewed November 16 branches also contain `.env.production.example`; it contains placeholders, not observed live values.
- The old `.gitignore` excludes `.env`, `.env.local`, `.env.*.local`, and token files.
- Some provider settings in `backend/app/core/config.py` are missing from the root `.env.example`. The new repository must maintain one authoritative, complete `.env.example`.
- The production example is not a production secret store. Never deploy its placeholders unchanged.
- `VITE_*` values are bundled into browser code and must never contain API keys or private tokens.

## Rotation recommendation

**No production credential can be positively identified in the inspected checked-in configuration.** Do not rotate a key solely because its variable name exists. However:

1. Rotate any provider key that was ever committed in any historical revision, pasted into public logs, or otherwise exposed.
2. Replace any deployed JWT signing secret that matches a source-code/development placeholder or has been shared between environments.
3. Generate a new, unique Swiggy token-encryption key for the new application; do not reuse the old database-encryption key.
4. Create separate test and production credentials for each provider, and keep development restricted to test/sandbox keys.
5. Revoke old credentials that are no longer needed after the new app has been validated.

## Items not visible through the GitHub repository

The audit cannot see ignored local files on the user's Mac, GitHub Actions secret values, Render/other cloud environment variables, provider dashboards, or production database credentials. These require owner-side inspection. **Do not paste secret values into chat.** A local copy operation can move approved values into a gitignored `.env.local` after the new configuration is finalised.


---

# Security addendum — evidence from uploaded local archives and Render production configuration

**Updated:** 2026-11-17  
**Source material:** user-uploaded `warik-ai.zip`, `warik-ai-safety-backups(2).zip`, Render Production environment screenshot, and environment configuration text supplied in this conversation.

This addendum supersedes any earlier statement that only blank example credentials were observed. The earlier GitHub-only inspection did not include ignored local files; the uploaded ZIP revealed additional material.

## Confirmed exposed configuration

The Render screenshot is the **Production** environment for the old `warik-ai-backend` service. Its masked variable list includes `DATABASE_URL`, `GROQ_API_KEY`, and `JWT_SECRET`. The accompanying text supplied non-empty values for those fields. These must be treated as production credentials, not as harmless free-tier demo values.

The uploaded `warik-ai.zip` also contains:

| Archive path | Non-empty credential-bearing fields found | Assessment |
|---|---|---|
| `warik-ai/backend/.env` | `DATABASE_URL` | Non-empty database DSN with embedded authentication. Environment/usage not independently verified. Treat as exposed. |
| `warik-ai/backend-backup/.env` | `GROQ_API_KEY`, `GNANI_API_KEY`, `GEOAPIFY_API_KEY`, `IGNAV_API_KEY`, `STAYAPI_KEY`, `VISTALINK_API_KEY`, `OLA_MAPS_API_KEY`, `DUFFEL_API_KEY`, `REEFAPI_KEY` | Non-empty values were present in the archive. Active/test/production status is unknown; treat every still-valid credential as compromised and rotate or revoke. |
| `warik-ai/backend-backup/token.json` | `access_token` (non-empty), `token_type` | Bearer/access-token-shaped material; provider/service could not be established from the inspected archive. Identify the issuing service privately, then revoke it. |
| `warik-ai/backend-backup-operator-phase1/backend/token.json` (inside nested `warik-ai-backend.zip`) | A `token.json` file is present | The nested copy requires the same private local review and revocation decision. |

The archive also includes a root `.env.example` containing placeholders and a nested `backend.zip` whose `.env` contained only non-secret application metadata. The separate `warik-ai-safety-backups(2).zip` had no files named `.env`, `token.json`, credential JSON or private-key files in its inspected archive listing.

## Rotation priority

| Priority | Credential | Required action |
|---|---|---|
| **Immediate** | Render Production `GROQ_API_KEY` and any non-empty Groq key in the backup archive | Revoke the old key(s), create a fresh key in Groq, update Render only after verifying the new key, and check provider usage for unexpected activity. |
| **Immediate** | Render Production `DATABASE_URL` and archive `backend/.env` database DSN | Rotate the Neon database password/credential, review database activity, update the Render secret, and validate the application using the new connection string. |
| **Immediate** | Render Production `JWT_SECRET` | Replace with a newly generated high-entropy value. Expect existing JWT sessions to become invalid; require users to authenticate again. |
| **High** | `GNANI_API_KEY`, `GEOAPIFY_API_KEY`, `IGNAV_API_KEY`, `STAYAPI_KEY`, `VISTALINK_API_KEY`, `OLA_MAPS_API_KEY`, `DUFFEL_API_KEY`, `REEFAPI_KEY` | Identify the issuing account for each; revoke/rotate every key that remains valid. Their test/production status was not established by the archive. |
| **High** | `access_token` in `token.json` | Identify the issuing integration from the owner's provider account or local source history, revoke the token and any linked refresh/session token. Do not paste it into chat. |

Do not assume a key is safe because it is free, has a limited free quota, or is in an ignored local file. Free-tier credentials can still grant account/API access, consume quota, expose data or be abused.

## Archive and Git-history scan scope

- The uploaded main ZIP contains approximately 102,319 archive entries and includes large dependency folders, nested ZIPs, ignored local files, backups and a local `.git` directory.
- The scan inspected environment-like files and token filenames without emitting their values. The relevant discovered files are listed above.
- The packaged local Git metadata exposed 489 reachable Git objects during the limited signature scan. No provider-key signature or non-placeholder dotenv credential was detected in the reachable Git blobs. One database-URL-shaped string was found in a production-database test file and appears to be test fixture material; it was not treated as a live credential.
- The archive scan is not a forensic guarantee: unreachable Git objects, binary payloads, arbitrary embedded strings, the live provider account state and cloud logs were not exhaustively certified.
- The Render screenshot showed values masked. Production status and variable names were visible; the values were not extracted from the screenshot. The user-supplied configuration text contained the non-empty values described above.

## New Warik-Labs handling rule

1. Do not copy any values from the old ZIP or conversation into the new repository.
2. Create new, dedicated development credentials only after the selected provider and sandbox contract are approved.
3. Store secrets in a local ignored `.env.local` or a cloud secret manager. Never commit them, never place them in `VITE_*` variables, logs, screenshots, task records or model prompts.
4. Keep old and new environments isolated. Use independent credentials for development, staging and production.
5. Before any integration test, confirm that the credential is test/sandbox-scoped and that the specific test call is explicitly approved.


## Additional archive credential detail

The non-empty backup values were identified by field name only. The following names were present in the archived `backend-backup/.env`:

| Variable | Archive observation | Service / next step |
|---|---|---|
| `GROQ_API_KEY` | Non-empty | Groq; revoke/rotate. |
| `GNANI_API_KEY` | Non-empty | Gnani; revoke/rotate. |
| `HASDATA_API_KEY` | Placeholder-shaped value | HasData; confirm it was never a real credential. |
| `GEOAPIFY_API_KEY` | Non-empty | Geoapify; revoke/rotate. |
| `IGNAV_API_KEY` | Non-empty | Provider identity not independently confirmed from the archive; identify the account, then revoke/rotate. |
| `STAYAPI_KEY` | Non-empty | StayAPI; revoke/rotate. |
| `VISTALINK_API_KEY` | Non-empty | Provider identity/entitlement not independently confirmed; identify the account, then revoke/rotate. |
| `OLA_MAPS_API_KEY` | Non-empty | Ola Maps; revoke/rotate. |
| `DUFFEL_API_KEY` | Non-empty | Duffel; revoke/rotate. |
| `REEFAPI_KEY` | Non-empty | Reef provider; revoke/rotate. |

The backup file also included non-secret model/feature configuration such as `LLM_PROVIDER`, `GROQ_MODEL`, `OLLAMA_MODEL`, `VOICE_ENABLED` and `GNANI_TTS_VOICE`.

The standalone `backend-backup/token.json` had a non-empty `access_token` field. The issuer cannot be proven from the file alone. Treat it as a bearer credential until its issuer has been identified and it has been revoked.

