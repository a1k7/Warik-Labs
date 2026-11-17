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
