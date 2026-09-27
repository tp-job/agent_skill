# Threat Response Playbook

What to do, in order, on a compromised key or suspicious OAuth2 token activity.

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
