# Key Rotation Automation

Deep reference for [security](../SKILL.md). Read this when designing rotation for API keys, service credentials, or signing keys — including emergency rotation after a compromise.

Companion to [secrets-management](secrets-management.md), which covers where secrets live. This covers how they change.

---

## Why rotation is hard (and how to make it easy)

Rotation fails in practice for one reason: **there is a moment when the old key is dead and the new key is not yet everywhere.** Every technique below exists to eliminate that moment.

The solution is always the same shape — **overlap**. Two keys are valid at once, and the cutover is a sequence of independent, reversible steps rather than a single switch.

```
        ┌──── key A valid ────┐
                    ┌──────── key B valid ────────┐
                    ▲         ▲                   ▲
                    │         │                   │
                 issue B   consumers            revoke A
                           migrated
```

---

## The four-phase rotation

Never collapse these. Each phase is independently verifiable and independently revertible.

### Phase 1 — Issue

Create the new credential. Both old and new are now valid.

- The new key gets its own identity in the provider — not an overwrite of the old one. You cannot roll back an overwrite.
- Tag it with a creation timestamp and the rotation reason (`scheduled` / `compromise` / `personnel-change`).
- Verify the new key actually works against the target system *before* touching any consumer.

### Phase 2 — Distribute

Write the new value to the secrets manager as a new version. Consumers pick it up.

- If consumers fetch at runtime with a TTL cache (see [secrets-management](secrets-management.md) Pattern 1), this is automatic — wait one TTL.
- If consumers read from environment variables, this phase requires a rolling restart. Plan for it.
- **Do not proceed until you can prove every consumer has the new value.** Metrics beat assumptions.

### Phase 3 — Verify

Confirm traffic has actually moved before you break anything.

This is the phase teams skip, and it is the one that prevents outages. You need per-key usage telemetry:

- Provider-side: most API providers expose "last used" per key. Poll it.
- Application-side: emit a metric tagged with a key identifier (never the key itself — use a fingerprint like the last 4 characters or a SHA-256 prefix).

**Gate:** old-key usage has been zero for at least one full traffic cycle — including nightly batch jobs, weekly reports, and anything else that does not run continuously. A 24-hour observation window catches daily cron; a 7-day window catches weekly.

### Phase 4 — Revoke

Delete the old credential at the provider.

- Revoke, don't just "stop using." An unrevoked old key is an unmonitored live credential.
- Keep the audit record of when it was revoked and by what process.
- If revocation causes an incident, the fix is to re-issue *a new key* and restart the cycle — not to un-revoke.

---

## Automating it

```python
"""Scheduled rotation driver. Each phase is a separate, resumable step."""
import hashlib
import logging
import time

log = logging.getLogger(__name__)

OBSERVATION_WINDOW_S = 24 * 3600
POLL_INTERVAL_S = 300


def fingerprint(key: str) -> str:
    """Safe identifier for logs and metrics — never log the key itself."""
    return hashlib.sha256(key.encode()).hexdigest()[:12]


def rotate(secret_name: str, provider, store) -> None:
    old = store.get_current(secret_name)

    # Phase 1 — issue, and prove the new credential works before anything
    # depends on it.
    new = provider.create_key(reason="scheduled")
    if not provider.healthcheck(new):
        provider.revoke(new)
        raise RuntimeError(f"new key {fingerprint(new.value)} failed healthcheck")

    # Phase 2 — distribute. Consumers with a TTL cache pick this up on their
    # next refresh; env-var consumers need the rolling restart triggered here.
    store.put_new_version(secret_name, new.value)
    log.info("issued %s, superseding %s", fingerprint(new.value), fingerprint(old.value))

    # Phase 3 — verify. Wait for old-key usage to go quiet for a full traffic
    # cycle, so weekly and nightly jobs are accounted for.
    deadline = time.monotonic() + OBSERVATION_WINDOW_S
    while time.monotonic() < deadline:
        if provider.last_used(old) is not None and provider.usage_since(old, POLL_INTERVAL_S) > 0:
            # Still in use — restart the quiet period.
            deadline = time.monotonic() + OBSERVATION_WINDOW_S
        time.sleep(POLL_INTERVAL_S)

    # Phase 4 — revoke only after a clean observation window.
    provider.revoke(old)
    log.info("revoked %s", fingerprint(old.value))
```

Run it on a schedule, and alert — loudly — if a rotation stalls in Phase 3. A stalled rotation means a consumer you did not know about is still holding the old key. That is useful information, not a failure.

---

## Rotation cadence

Cadence is a function of blast radius and detection capability, not a number someone picked.

| Credential | Suggested cadence | Rationale |
| --- | --- | --- |
| Short-lived tokens (STS, Vault leases) | Minutes to hours | Automatic; no human process |
| Service-to-service API keys | 90 days | Balances churn against exposure window |
| Database credentials | 30–90 days | High blast radius; automate via dynamic secrets |
| Signing keys (JWT, webhooks) | 6–12 months, overlapping | Consumers cache public keys; needs long overlap |
| Third-party provider keys | Per provider policy, min. annually | Often the constraint is their API |
| Anything after personnel change | Immediately | Access, not time, is the trigger |

Rotating more often than you can do reliably is worse than rotating less often. A quarterly rotation that always completes beats a monthly one that half-completes and leaves orphaned keys.

---

## Signing keys are a special case

For JWTs and webhook signatures, consumers cache your public key. Rotation must publish the new key *well before* you sign with it.

1. Add the new key to the JWKS endpoint with a new `kid`. Do not sign with it yet.
2. Wait longer than the maximum consumer cache TTL (advertise this, e.g. 24h via `Cache-Control`).
3. Start signing with the new `kid`. Verifiers pick the right key from `kid` in the header.
4. Keep the old key in JWKS until every token signed with it has expired.
5. Remove the old key.

Always include `kid` in the header from day one. Retrofitting key identifiers into a live system is far harder than rotating.

---

## Emergency rotation (compromise)

The scheduled process optimizes for zero downtime. The emergency process optimizes for closing the window. **Accept the outage.**

```
1. REVOKE the compromised key immediately.       ← do this first, not last
2. Issue a replacement.
3. Push to the secrets store; force consumer refresh (restart, don't wait for TTL).
4. Audit provider logs for the full exposure window — from first possible
   exposure, not from discovery.
5. Rotate anything the compromised key could have reached (lateral blast radius).
6. Post-incident: why was it exposed, and which control should have caught it?
```

Step 5 is the one that gets missed. If the leaked key could read a secrets manager, every secret it could read is now also compromised and must be rotated too.

---

## Design for rotation up front

The cheapest rotation is one the system was built for. When designing any credential-consuming component:

- [ ] Can the system hold **two valid credentials simultaneously**? If not, every rotation is an outage.
- [ ] Is there a **key identifier** (`kid`, key name, fingerprint) in every use, so you can attribute traffic per key?
- [ ] Can a consumer **refresh without a restart**?
- [ ] Is there **per-key usage telemetry** to gate Phase 4?
- [ ] Is rotation **scripted and scheduled**, not a runbook someone performs by hand?
- [ ] Does the credential **fail closed** on refresh failure?

A "no" to the first question is an architecture bug, and it is worth fixing before the first rotation, not during it.

---

## Related

- [secrets-management](secrets-management.md) — where secrets live and how they are injected
- [oauth2-deep](oauth2-deep.md) — short-lived tokens that reduce the need for rotation
- [agent-threat-model](agent-threat-model.md) — rotation when the credential holder is an autonomous agent
