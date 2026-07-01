# PERN/MERN Full-Stack Debug Deep Dive — L8/L9/L10

## L8: Express API — Common Failure Patterns

### Middleware Order (most common mistake)
```javascript
// ❌ WRONG — validation before body parsing
app.use('/api', validateBody, express.json(), handler);

// ✅ CORRECT
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use('/api', validateBody, handler);
```

### Unhandled Async Errors (Node < 18 doesn't catch these automatically)
```javascript
// ❌ Crashes the server silently
router.get('/users', async (req, res) => {
  const users = await User.find(); // throws but no try/catch
  res.json(users);
});

// ✅ 
router.get('/users', async (req, res, next) => {
  try {
    const users = await User.find();
    res.json(users);
  } catch (err) {
    next(err); // passes to error handler middleware
  }
});

// Or use a wrapper:
const asyncHandler = fn => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next);
```

### CORS Debug Sequence
```
1. Check OPTIONS preflight: DevTools → Network → filter OPTIONS
2. Response headers must have:
   Access-Control-Allow-Origin: http://localhost:3000 (exact, not *)
   Access-Control-Allow-Credentials: true (if using cookies)
   Access-Control-Allow-Headers: Content-Type, Authorization
3. If * with credentials → browser blocks (CORS spec)
4. Check credentials: 'include' on fetch/axios client side
```

---

## L9: Database Deep Dive

### PostgreSQL (PERN) — Connection Pool Exhaustion
```javascript
// Symptom: requests hang, timeout after 30s
// Cause: queries not releasing connections

// Debug: check active connections
SELECT count(*) FROM pg_stat_activity WHERE state = 'active';
SELECT count(*) FROM pg_stat_activity WHERE state = 'idle';

// Fix: ensure pool.query() used (auto-releases) not manual client.connect()
// If using manual: always client.release() in finally block
const client = await pool.connect();
try {
  await client.query('...');
} finally {
  client.release(); // ← critical
}
```

### MongoDB (MERN) — Index Missing Diagnosis
```javascript
// Step 1: get execution stats
db.collection.find({ email: 'x@x.com' }).explain('executionStats')

// Red flags in output:
// executionStats.totalDocsExamined >> totalDocsReturned  → no index
// executionStats.executionTimeMillis > 100ms → slow
// winningPlan.stage === "COLLSCAN" → full collection scan

// Fix:
db.collection.createIndex({ email: 1 }, { unique: true });
// Or in Mongoose schema:
email: { type: String, index: true, unique: true }
```

### N+1 Query Pattern (both stacks)
```javascript
// ❌ N+1: 1 query for posts + N queries for authors
const posts = await Post.find();
for (const post of posts) {
  post.author = await User.findById(post.authorId); // N queries
}

// ✅ PostgreSQL: JOIN
SELECT p.*, u.name FROM posts p JOIN users u ON p.author_id = u.id;

// ✅ MongoDB: $lookup or .populate()
Post.find().populate('authorId', 'name email');
```

---

## L10: Auth Debug Patterns

### JWT Token Expiry Race
```javascript
// Symptom: user gets 401 mid-session, has to re-login
// Cause: access token expires, refresh not handled

// Fix: Axios interceptor pattern
axios.interceptors.response.use(
  res => res,
  async err => {
    const original = err.config;
    if (err.response?.status === 401 && !original._retry) {
      original._retry = true;
      try {
        const { data } = await axios.post('/api/auth/refresh');
        original.headers.Authorization = `Bearer ${data.token}`;
        return axios(original);
      } catch {
        // Refresh failed → logout
        window.location.href = '/login';
      }
    }
    return Promise.reject(err);
  }
);
```

### Role-Based Access Debug
```javascript
// Symptom: admin endpoint returns 403 for admin user
// Debug: decode JWT and check role claim
const decoded = jwt.decode(token); // no verify, just decode
console.log(decoded.role); // is it 'admin'?

// Common mistake: role not included when signing token
const token = jwt.sign(
  { id: user._id }, // ❌ missing role
  secret
);

// Fix:
const token = jwt.sign(
  { id: user._id, role: user.role }, // ✅
  secret,
  { expiresIn: '15m' }
);
```

### CSRF with JWT (common misconception)
```
JWT in Authorization header → no CSRF risk (JS-readable, same-origin only)
JWT in HttpOnly cookie → CSRF risk → add CSRF token or SameSite=Strict
```