# OAuth2 Deep Reference

## Grant Types Comparison

|Grant Type|When to Use|Client Type|
|---|---|---|
|Authorization Code + PKCE|User-facing apps (mobile, SPA)|Public|
|Client Credentials|Server-to-server, agent-to-service|Confidential|
|Device Code|CLI tools, IoT, TV apps|Public|
|Refresh Token|Extending sessions without re-auth|Both|
|❌ Implicit|DEPRECATED — never use|—|
|❌ Password|DEPRECATED — never use|—|

## PKCE Step-by-Step

```typescript
// 1. Generate verifier (before redirect)
const codeVerifier = crypto.randomBytes(32).toString('base64url')

// 2. Hash it → challenge
const codeChallenge = crypto
  .createHash('sha256')
  .update(codeVerifier)
  .digest('base64url')

// 3. Include in authorization URL
const authUrl = new URL('https://auth.example.com/authorize')
authUrl.searchParams.set('code_challenge', codeChallenge)
authUrl.searchParams.set('code_challenge_method', 'S256')

// 4. On callback, exchange code + verifier
const tokenResponse = await fetch('/token', {
  body: new URLSearchParams({
    grant_type: 'authorization_code',
    code: authorizationCode,
    code_verifier: codeVerifier,  // Server recomputes hash to verify
  }),
})
```

## Token Validation on Resource Server

```typescript
import { jwtVerify, createRemoteJWKSet } from 'jose'

const JWKS = createRemoteJWKSet(
  new URL('https://auth.example.com/.well-known/jwks.json')
)

async function validateToken(token: string, expectedAud: string) {
  const { payload } = await jwtVerify(token, JWKS, {
    issuer: 'https://auth.example.com',   // Pin to known issuer
    audience: expectedAud,                 // Must match THIS service
  })

  // Additional checks
  if (Date.now() / 1000 > payload.exp!) throw new Error('Token expired')
  if (!payload.scope?.includes('data:read')) throw new Error('Insufficient scope')

  return payload
}
```