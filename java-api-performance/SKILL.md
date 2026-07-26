---
name: java-api-performance
description: >-
  Java Spring Boot backend API performance optimization. Use this skill when writing, reviewing, or refactoring Java/Spring Boot code to fix slow APIs, memory issues, or database inefficiencies. Triggers on tasks involving loop optimization, caching, pagination, query tuning, N+1 problems, database indexing, async processing, or connection pooling. Also trigger for: "my API is slow", "fix N+1 query", "add caching", "optimize database", "Spring Boot performance", "HikariCP config", "reduce memory usage", "paginate results", "add @Async", or any Java backend performance request.
license: MIT
metadata:
  author: nevinas06 (enhanced by Claude)
  version: "1.0.0"
  source: Java Spring Boot performance patterns (compiled 2026)
---

# Java Spring Boot — API Performance Optimization

9 concrete patterns to eliminate the most common Java backend performance killers. Each pattern has a BAD vs BETTER example with copy-ready code.

## When to Apply

Reference these patterns when:
- Writing new Spring Boot services or repositories
- Reviewing code for slow API response times
- Fixing memory pressure, GC issues, or OutOfMemoryError
- Optimizing database query patterns
- Implementing caching, async processing, or pagination
- Configuring production-grade connection pooling

## Patterns by Priority

| Priority | Pattern | Impact | ID |
|----------|---------|--------|-----|
| 1 | Loop Optimization — filter in DB, not Java | CRITICAL | `loop-` |
| 2 | Object Creation — stop new objects inside loops | CRITICAL | `object-` |
| 3 | Async Processing — @Async for long tasks | HIGH | `async-` |
| 4 | Caching — @Cacheable with Redis | HIGH | `cache-` |
| 5 | Pagination — never return all records | HIGH | `page-` |
| 6 | Query Optimization — ban SELECT * | MEDIUM | `query-` |
| 7 | Database Indexing — stop full table scans | MEDIUM | `index-` |
| 8 | N+1 Problem — JOIN FETCH instead of lazy load | MEDIUM | `n1-` |
| 9 | Connection Pooling — tune HikariCP | MEDIUM | `pool-` |

## Quick Reference

### 1. Loop Optimization (CRITICAL)
- `loop-db-filter` — Push `WHERE` clauses to JPA `@Query`, never `findAll()` + Java stream filter
- `loop-derived-query` — Use JPA derived query methods (`findByStatus`) for simple filters
- `loop-no-stream-large` — Stream only on small, already-loaded in-memory collections

### 2. Object Creation (CRITICAL)
- `object-stringbuilder` — Reuse `StringBuilder` instead of string concatenation inside loops
- `object-preallocate` — Pre-allocate `ArrayList` with known capacity (`new ArrayList<>(n)`)
- `object-no-new-loop` — Never instantiate heavy objects inside a loop body

### 3. Async Processing (HIGH)
- `async-enable` — Add `@EnableAsync` on main class + `@Async` on slow method
- `async-completable` — Return `CompletableFuture<Void>` for caller-awaitable results
- `async-thread-pool` — Configure custom `ThreadPoolTaskExecutor` for production load

### 4. Caching (HIGH)
- `cache-cacheable` — `@Cacheable(value, key)` on read-heavy methods
- `cache-evict` — Always pair with `@CacheEvict` on data-mutating methods
- `cache-ttl` — Always set Redis TTL to prevent stale data buildup
- `cache-redis` — Use `spring-boot-starter-data-redis` for distributed caching

### 5. Pagination (HIGH)
- `page-pageable` — Accept `Pageable` in repository and return `Page<T>`
- `page-default-size` — Default page size = 20; enforce max via `@PageableDefault`
- `page-sort` — Always include a `Sort` clause on paginated queries

### 6. Query Optimization (MEDIUM)
- `query-no-select-star` — Ban `SELECT *`; use Interface Projections or DTO constructors
- `query-projection` — Fetch only fields the API response actually needs
- `query-dto-constructor` — Use JPQL constructor expressions for complex multi-field DTOs

### 7. Database Indexing (MEDIUM)
- `index-explain-analyze` — Find slow queries with `EXPLAIN ANALYZE` before adding indexes
- `index-where-join` — Index columns used in `WHERE`, `JOIN`, and `ORDER BY`
- `index-jpa-annotation` — Declare indexes via `@Table(indexes = @Index(...))` in JPA entity
- `index-no-over-index` — Don't over-index — every index slows down writes

### 8. N+1 Problem (MEDIUM)
- `n1-join-fetch` — Use `JOIN FETCH` in JPQL to load related entities in one query
- `n1-entity-graph` — Use `@EntityGraph` for flexible fetch strategies without modifying queries
- `n1-no-lazy-loop` — Never access lazy-loaded associations inside a loop

### 9. Connection Pooling (MEDIUM)
- `pool-hikari-size` — Set `maximum-pool-size` = 2–3× CPU cores (typically 10–20)
- `pool-idle-timeout` — Configure `idle-timeout`, `max-lifetime`, `connection-timeout`
- `pool-actuator` — Monitor pool metrics via Spring Actuator + Grafana

## How to Use

Each pattern ID maps to a concrete before/after example in [api](references/api.md):

```
api.md — Step 01: loop-db-filter
api.md — Step 03: async-enable
api.md — Step 04: cache-cacheable
```

Apply the highest-priority patterns first. For new services, implement patterns 1–5 before launch.

## Full Reference Document

For all 9 patterns with complete code examples: [api](references/api.md)
