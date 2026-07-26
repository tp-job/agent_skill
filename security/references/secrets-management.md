# Secrets Manager Integration Patterns

Deep reference for [security](../SKILL.md). Read this when the task involves storing, injecting, or auditing secrets — not when it is about OAuth2 flow design (see [oauth2-deep](oauth2-deep.md)) or agent trust boundaries (see [agent-threat-model](agent-threat-model.md)).

---

## The one rule

A secret must never exist in a place that is version-controlled, logged, or readable by a process that does not need it. Every pattern below is a way of honouring that rule under a different set of constraints.

Ranked from worst to best:

| Storage | Verdict | Why |
| --- | --- | --- |
| Hardcoded in source | Never | Leaks on every clone, fork, and screen-share. Rotation means a code deploy. |
| `.env` committed to git | Never | Same as above, plus it looks safe, which is worse. |
| `.env` gitignored, on developer machines | Local dev only | No audit trail, no rotation, drifts between machines. |
| CI/CD platform secret store | Acceptable for deploy-time | Scoped to pipelines; usually no dynamic rotation. |
| Cloud secrets manager + runtime fetch | Preferred | Central audit, versioning, rotation hooks, IAM-scoped. |
| Short-lived identity (OIDC / workload identity) | Best | There is no long-lived secret to steal. |

---

## Pattern 1 — Runtime fetch from a secrets manager

The application holds an *identity*, not a *secret*. It authenticates to the secrets manager using that identity and fetches credentials at boot or on demand.

```
┌──────────┐   IAM role / workload identity   ┌──────────────────┐
│  Service │ ───────────────────────────────► │ Secrets Manager  │
│          │ ◄─────────────────────────────── │ (AWS SM, Vault,  │
└──────────┘   secret value + version          │  GCP SM, Azure KV)│
                                               └──────────────────┘
```

**Use when** the workload runs in a cloud environment that can issue it an identity (ECS task role, GKE workload identity, Azure managed identity, Kubernetes service account).

**Implementation notes**

- Fetch at startup, cache in memory, never write to disk.
- Set a TTL on the cache (5–15 min is typical) so a rotation propagates without a restart.
- Handle fetch failure by failing closed — a service that boots without its credentials and serves errors is safer than one that falls back to a stale default.
- Request the secret by name plus stage (`prod/payments/stripe-key`), not by version, unless you are pinning deliberately.

```python
# Cache with TTL so rotations propagate without a redeploy.
import time
import boto3

_cache: dict[str, tuple[str, float]] = {}
_TTL = 600
_client = boto3.client("secretsmanager")


def get_secret(name: str) -> str:
    hit = _cache.get(name)
    if hit and time.monotonic() - hit[1] < _TTL:
        return hit[0]
    # Fail closed: let the exception propagate rather than returning a stale
    # or empty credential.
    value = _client.get_secret_value(SecretId=name)["SecretString"]
    _cache[name] = (value, time.monotonic())
    return value
```

---

## Pattern 2 — Injection at deploy time

The orchestrator resolves secrets and injects them as environment variables or mounted files. The application knows nothing about a secrets manager.

**Use when** you cannot change application code, or the runtime has no identity mechanism.

**Trade-offs**

- Simple, works everywhere, no SDK dependency.
- Rotation requires a restart or redeploy.
- Environment variables leak more readily than in-memory values: they appear in `/proc/<pid>/environ`, in crash dumps, in `docker inspect`, and in many APM agents' process metadata.
- Prefer a mounted file over an environment variable when the platform supports it (Kubernetes `secret` volume, Docker secrets). Files can be permission-scoped to a single uid; environment variables cannot.

---

## Pattern 3 — Dynamic / short-lived credentials

The secrets manager mints a credential on request with a short lease (minutes to hours), and the application renews it.

**Use when** the downstream system supports it — databases (Vault database secrets engine), cloud APIs (STS `AssumeRole`), or internal services that accept short-lived tokens.

This is the strongest pattern because a leaked credential expires on its own. Combine with [key rotation](key-rotation.md) for the credentials that cannot be made short-lived.

---

## Pattern 4 — Workload identity federation (no secret at all)

CI runners and cloud workloads exchange a platform-signed OIDC token for a cloud credential. Nothing long-lived is ever stored.

```yaml
# GitHub Actions → AWS with no stored access key
permissions:
  id-token: write
  contents: read
steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::111122223333:role/deploy
      aws-region: us-east-1
```

Prefer this over storing a cloud access key in CI secrets whenever the provider supports it. It removes an entire class of rotation and leak problems.

---

## Scoping: least privilege for secrets

Grant read access per-secret, not per-prefix, unless the prefix is genuinely a single trust domain.

```json
{
  "Effect": "Allow",
  "Action": "secretsmanager:GetSecretValue",
  "Resource": "arn:aws:secretsmanager:us-east-1:111122223333:secret:prod/payments/stripe-key-*"
}
```

Checklist per secret:

- [ ] Which principals can **read** it? (should be one service role)
- [ ] Which principals can **write/rotate** it? (should be a rotation function or a break-glass human role, not the service)
- [ ] Which principals can **delete** it? (should be nobody in prod without approval)
- [ ] Is read access logged to an audit trail the security team can query?

Separating read from write matters: a compromised service can then exfiltrate a credential but cannot silently replace it with one the attacker controls.

---

## Preventing leaks before they land

Layer these — none is sufficient alone.

1. **Pre-commit hook** — `gitleaks protect --staged` or `detect-secrets-hook`. Catches the mistake at the cheapest moment.
2. **CI scan on every PR** — `gitleaks detect`, `trufflehog`. Catches what the hook missed or what someone bypassed with `--no-verify`.
3. **Provider-side push protection** — GitHub secret scanning push protection blocks known credential formats at the remote.
4. **`.gitignore` discipline** — `.env`, `.env.*`, `*.pem`, `*.key`, `credentials.json`. Commit a `.env.example` with keys and empty values so the shape is documented without the values.
5. **Log redaction** — a logging filter that masks anything matching known token patterns, plus a rule never to log whole request headers or config objects.

---

## When a secret leaks

Order matters. Rotating before you understand the blast radius can lock you out mid-incident.

1. **Contain** — revoke the credential at the provider. Do not wait for a clean rotation; a revoked credential that breaks your service is better than a live one in an attacker's hands.
2. **Assess** — check provider access logs for use from unexpected IPs, regions, or user agents, from the moment of first exposure.
3. **Rotate** — issue a replacement following [key-rotation](key-rotation.md).
4. **Purge** — remove from git history (`git filter-repo`), but treat the credential as permanently compromised regardless: it was cloned, cached, and indexed.
5. **Prevent** — add the pattern to the pre-commit and CI scanners so this specific shape cannot recur.

> Purging history is hygiene, not remediation. Rotation is remediation.

---

## Anti-patterns

| Anti-pattern | Why it fails |
| --- | --- |
| Encrypting secrets in the repo with a key that is also in the repo | Moves the problem one file over. |
| One shared "app secret" across all environments | A staging leak becomes a production breach. |
| Secrets in container image layers (`ENV`, `COPY .env`) | Baked into a distributable artifact forever. |
| Passing secrets as CLI arguments | Visible in `ps`, in shell history, in process monitoring. |
| Logging config objects at startup "for debugging" | The single most common accidental disclosure. |
| Long-lived personal access tokens as service credentials | Tied to a human who will eventually leave; audit trail attributes machine actions to a person. |

---

## Related

- [oauth2-deep](oauth2-deep.md) — token flows, PKCE, and what to do instead of a static key
- [key-rotation](key-rotation.md) — rotation automation and compromise response
- [agent-threat-model](agent-threat-model.md) — what changes when the consumer is an autonomous agent
