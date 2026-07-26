---
name: security
description: >
  Senior-level security architecture skill covering OAuth2 authorization flows and Leveled API Key design. Activate whenever the user mentions OAuth2, access tokens, authorization flows, API key management, key rotation, key compromise, leveled permissions (read-only / write / admin), resource server security, or agent authentication patterns. Also trigger for: designing secure agent-to-service communication, reviewing API key scoping, auditing key privilege levels, implementing token exchange flows, or any question about "who can access what and how". Use proactively — if the user is building anything that touches auth, keys, or service-to-service security, this skill almost certainly applies.
license: MIT
metadata:
  author: tp-job (enhanced by Claude)
  version: "1.0.0"
  source: OAuth2 / API Key security architecture (compiled 2026)
---

# Security — OAuth2 & Leveled API Key Architecture

You are acting as a **Senior Lead** across four disciplines simultaneously:

- **Prompt Engineering** — crafting precise auth-aware prompts for AI agents
- **Context Engineering** — managing token/key context across agent memory and tool calls
- **Agent Design** — designing secure agent-to-service boundaries with correct privilege levels
- **AI Workflow Architecture** — multi-step pipelines with least-privilege key routing

Always think in two axes:

- **Who is the caller?** (User / App / Agent / Admin)
- **What is the minimum key level needed?** (read-only → write → admin)

---

## 1. OAUTH2 FLOW — ARCHITECTURE REFERENCE

> Source: Auth diagram — OAuth2 with Facebook/Google as Authorization Server

### The Four Actors

|Actor|Role|Trust Level|
|---|---|---|
|**User**|Human initiating access|Untrusted until approved|
|**Mobile App / Client**|Requests on behalf of user|Partially trusted|
|**Authorization Server**|Identity provider (e.g. Google, Facebook)|Fully trusted|
|**Resource Server**|Holds the protected data|Trusts only valid tokens|

### The 7-Step OAuth2 Flow (Canonical)

```
Step 1  Mobile App  ──Authorize Service──►  Authorization Server
        (App registers intent to access resources)

Step 2  Authorization Server  ──Request Permission──►  User
        (Server asks user: "Allow this app?")

Step 3  User  ──Request Approved──►  Authorization Server
        (User grants consent)

Step 4  Authorization Server  ──Permission Granted──►  Mobile App
        (Auth code / grant issued to client)

Step 5  Mobile App  ──Get Access Token──►  Authorization Server
        (Exchange grant for token — PKCE here for public clients)

Step 6  Authorization Server  ──Access Token──►  Mobile App
        (Short-lived JWT or opaque token returned)

Step 7a Mobile App  ──Request Data (with token)──►  Resource Server
Step 7b Resource Server  ──Data──►  Mobile App
        (Resource Server validates token, returns protected data)
```

### Token Types — Know the Difference

|Token|Lifetime|Storage|Use|
|---|---|---|---|
|**Authorization Code**|Single-use, ~10 min|Server memory|Exchange for tokens only|
|**Access Token**|Short (15 min – 1 hr)|In-memory / HttpOnly cookie|API calls|
|**Refresh Token**|Long (days–weeks)|Secure HttpOnly cookie / keychain|Get new access tokens|
|**ID Token (OIDC)**|Short|Client-side|Identity claim only — never send to Resource Server|

### Implementation Checklist — OAuth2

```
✅ Use PKCE for all public clients (mobile, SPA) — no client_secret exposure
✅ Validate token signature + expiry + audience (aud) on Resource Server
✅ Never log access tokens or refresh tokens
✅ Refresh token rotation — invalidate old token on use
✅ Short access token TTL (15–60 min); longer refresh TTL (7–30 days)
✅ Scope tokens minimally — request only the scopes needed
✅ HTTPS everywhere — no token over plain HTTP
✅ Store access tokens in memory (not localStorage) for web clients
✅ Store refresh tokens in HttpOnly, Secure, SameSite=Strict cookies
```

### Anti-Patterns — Catch and Fix

|Anti-Pattern|Risk|Fix|
|---|---|---|
|`token` stored in `localStorage`|XSS steals token permanently|Move to memory / HttpOnly cookie|
|Access token used as long-lived credential|Wide blast radius on leak|Add expiry; implement refresh rotation|
|Missing `aud` validation on Resource Server|Token accepted for wrong service|Always validate `aud` matches this service|
|Skipping PKCE for mobile app|Auth code interception attack|Always add `code_challenge` / `code_verifier`|
|Opaque refresh token stored in JS|XSS pivot to full session takeover|HttpOnly cookie with `SameSite=Strict`|
|Accepting tokens from any issuer|Token forgery|Pin `iss` to expected Authorization Server|

---

## 2. LEVELED API KEYS — ARCHITECTURE REFERENCE

> Source: "Leveled API Keys" diagram — three-tier privilege model

### The Three Tiers

```
🟡 READ-ONLY KEY  — can only read data
                    → data access path only
                    → compromise: data leak (confidentiality risk)

⚪ WRITE KEY      — can read + modify data
                    → data access + modify data path
                    → compromise: data corruption / exfiltration

🟣 ADMIN KEY      — can read + write + deploy updates
                    → data access + modify data + deploy update
                    → compromise: full system takeover
```

### The "Same Key" Blast Radius Problem

The diagram highlights the critical danger of reusing the same API key across services.

```
❌ BAD — Same key across all services:

  App ──(api-key: 1234-4321-5678-8765-98)──► Service 1
  App ──(api-key: 1234-4321-5678-8765-98)──► Service 2
  App ──(api-key: 1234-4321-5678-8765-98)──► Service 3

  If Service 1's key is compromised:
  → Attacker gains access to ALL three services
  → One breach = total breach
```

```
✅ GOOD — Unique scoped key per service per privilege level:

  App ──(read-only-key-svc1)──► Service 1  (data access only)
  App ──(write-key-svc2)    ──► Service 2  (modify data)
  App ──(admin-key-svc3)    ──► Service 3  (deploy update)

  If Service 1's key is compromised:
  → Rotate only that key
  → Services 2 and 3 are unaffected
  → Blast radius = 1 service
```

### Key Naming Convention (Recommended)

```
Format: {service}-{environment}-{privilege}-{version}

Examples:
  payments-prod-read-v1
  analytics-prod-write-v2
  infra-prod-admin-v1
  payments-staging-read-v1
```

### Leveled API Key Design Rules

```
Rule 1 — MINIMUM PRIVILEGE
  Issue the lowest key level that satisfies the use case.
  Never give a write key when read-only is sufficient.
  Never give an admin key to any automated process.

Rule 2 — ONE KEY PER SERVICE BOUNDARY
  Never share a key across two different services.
  Each service gets its own key, even at the same privilege level.

Rule 3 — ROTATE ON SUSPECTED COMPROMISE
  Rotate immediately — do not wait to confirm breach.
  Rotation is cheap. Breach impact is not.

Rule 4 — EXPIRY + ROTATION SCHEDULE
  read-only keys: 90-day rotation
  write keys:     30-day rotation
  admin keys:     14-day rotation OR just-in-time issuance

Rule 5 — AUDIT EVERY KEY USE
  Log: key_id (not key value), timestamp, service_id, action, result
  Alert on: after-hours use, geographic anomaly, unusual volume

Rule 6 — NEVER LOG KEY VALUES
  Log key IDs (a hash or reference), never the raw key string.
  Keys in logs = keys exposed to everyone with log access.
```

### Key Storage Matrix

|Location|Read-Only Key|Write Key|Admin Key|
|---|---|---|---|
|Environment variable (server)|✅ OK|✅ OK|✅ OK (+ extra ACL)|
|`.env` file committed to git|🔴 NEVER|🔴 NEVER|🔴 NEVER|
|Secrets manager (Vault, AWS SM)|✅ Preferred|✅ Required|✅ Required|
|Client-side code / browser|🔴 NEVER|🔴 NEVER|🔴 NEVER|
|CI/CD environment secret|✅ OK|✅ OK|⚠️ Audit access|
|Docker image layer|🔴 NEVER|🔴 NEVER|🔴 NEVER|

---

## 3. AGENT DESIGN — SECURITY ARCHITECTURE

### Agent Key Assignment Model

Map each agent type to its correct key tier:

```
Agent Type              Key Tier         Rationale
──────────────────────────────────────────────────────────────────
Read agent              🟡 read-only     Fetches context only
Summarizer agent        🟡 read-only     Reads data, outputs summary
Writer/creator agent    ⚪ write         Needs to store outputs
Orchestrator agent      ⚪ write         Coordinates sub-agents
Deploy/infra agent      🟣 admin         Touches infrastructure
Human-in-the-loop gate  🟣 admin (JIT)   Admin only on confirmed action
```

### OAuth2 for Agent-to-Service Auth

When agents call external services (not just APIs), use OAuth2 Client Credentials flow:

```
Step 1  Agent  ──POST /token──►  Authorization Server
        Body: { grant_type: "client_credentials", scope: "data:read" }

Step 2  Authorization Server  ──Access Token──►  Agent
        (Short-lived token scoped to requested permissions)

Step 3  Agent  ──GET /resource (Bearer: token)──►  Resource Server

Step 4  Resource Server validates token ──► returns data
```

```typescript
// Agent token acquisition — Client Credentials flow
async function getAgentToken(scope: string): Promise<string> {
  const response = await fetch('https://auth.example.com/oauth/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'client_credentials',
      client_id: process.env.AGENT_CLIENT_ID!,
      client_secret: process.env.AGENT_CLIENT_SECRET!,
      scope,
    }),
  })
  const { access_token, expires_in } = await response.json()
  return access_token
}

// Always scope to minimum required
const token = await getAgentToken('data:read')           // Not 'data:write'
const adminToken = await getAgentToken('deploy:update')  // Only when deploying
```

### Key Injection Pattern for Multi-Agent Systems

```typescript
// Never hardcode keys — inject via context
interface AgentConfig {
  serviceUrl: string
  keyId: string          // Reference ID only — never the key value itself
  keyTier: 'read' | 'write' | 'admin'
}

// Fetch key at runtime from secrets manager
async function resolveKey(keyId: string): Promise<string> {
  // AWS Secrets Manager / HashiCorp Vault / GCP Secret Manager
  return await secretsManager.getSecretValue(keyId)
}

// Agent calls service with just-in-time key resolution
async function agentCallService(config: AgentConfig, path: string) {
  const key = await resolveKey(config.keyId)
  return fetch(`${config.serviceUrl}${path}`, {
    headers: { 'x-api-key': key },
  })
}
```

---

## 4. THREAT RESPONSE PLAYBOOK

### On Key Compromise

```
IMMEDIATE (< 5 min):
  1. Rotate the compromised key in secrets manager
  2. Deploy new key to affected services
  3. Invalidate / blocklist old key if provider supports it
  4. Confirm no new traffic on old key

SHORT-TERM (< 1 hr):
  5. Pull access logs for old key — identify all requests
  6. Scope the breach: which data was accessed/modified
  7. Check for lateral movement: did attacker use write/admin operations?
  8. Notify affected teams

FOLLOW-UP (< 24 hr):
  9. Root cause: how was key exposed? (logs, git, client-side code, etc.)
  10. Remediate exposure vector
  11. Audit all other keys at same tier — were they also exposed?
  12. Review key rotation schedule; tighten if needed
```

### On Suspicious Token Activity (OAuth2)

```
SIGNALS:
  - Token used from new geographic region
  - Token used after expected session end
  - Unusually high request volume for token
  - Token used for scopes not originally requested

RESPONSE:
  1. Revoke access token immediately
  2. Revoke refresh token if suspicious pattern continues
  3. Force re-authentication for user
  4. Review OIDC/OAuth logs for token issuance chain
  5. Check if authorization server supports token introspection — use it
```

---

## 5. SECURITY REVIEW CHECKLIST

Run this before any auth/API-key related code ships:

```
OAUTH2 REVIEW
  □ PKCE implemented for public clients?
  □ Access tokens short-lived (< 1 hr)?
  □ Refresh token rotation enabled?
  □ Token stored in memory / HttpOnly cookie (not localStorage)?
  □ Resource Server validates: signature, expiry, aud, iss?
  □ Scopes minimized to what's actually used?
  □ HTTPS enforced on all token endpoints?

API KEY REVIEW
  □ Each service has its own unique key?
  □ Keys follow minimum-privilege tier (read/write/admin)?
  □ Keys stored in secrets manager (not env files or source code)?
  □ Key rotation schedule defined and automated?
  □ Key usage is logged (by ID, not value)?
  □ Alerts defined for anomalous key usage?
  □ Admin keys use JIT issuance where possible?

AGENT-SPECIFIC REVIEW
  □ Each agent assigned minimum key tier for its task?
  □ Admin operations gated by human-in-the-loop confirmation?
  □ Tokens/keys injected at runtime (not baked into agent config)?
  □ Agent cannot escalate its own privilege level?
  □ Token/key is not passed through prompt context or logged in LLM traces?
```

---

## 6. DECISION MATRIX — WHICH PATTERN TO USE?

|Scenario|Pattern|Key Tier|
|---|---|---|
|User logs in via Google/Facebook|OAuth2 Authorization Code + PKCE|N/A (user token)|
|Mobile app calls your API|OAuth2 PKCE flow|Access token (scoped)|
|Server-to-server internal call|API Key or OAuth2 Client Credentials|read/write/admin|
|Agent reads data to build context|API Key — read-only|🟡 read-only|
|Agent writes results to database|API Key — write|⚪ write|
|Agent deploys a config update|API Key — admin (JIT)|🟣 admin|
|Third-party webhook calls your service|HMAC signature validation|N/A|
|Public API with rate limiting|API Key — read-only|🟡 read-only|
|CI/CD deploys infrastructure|API Key — admin (short TTL)|🟣 admin|

---

## REFERENCES

For deeper dives, load the relevant reference file when needed:

| Topic                                | Reference File                     |
| ------------------------------------ | ---------------------------------- |
| OAuth2 detailed token flow + PKCE    | [oauth2-deep](references/oauth2-deep.md)        |
| Secrets manager integration patterns | [secrets-management](references/secrets-management.md) |
| Key rotation automation scripts      | [key-rotation](references/key-rotation.md) |
| Agent security threat model          | [agent-threat-model](references/agent-threat-model.md) |

---

## RED FLAGS — ALWAYS CALL OUT

```
🔴 API key in any client-side code, browser bundle, or NEXT_PUBLIC_ variable
🔴 Same key used across more than one service
🔴 Admin key in any automated / unattended process without human gate
🔴 Access token stored in localStorage
🔴 No token expiry set
🔴 Missing audience (aud) validation on Resource Server
🔴 Refresh token not rotated on use
🔴 Key values appearing in application logs or LLM traces
🔴 Agent with write/admin key when read-only would suffice
🔴 Authorization Code flow without PKCE for mobile or SPA clients
```