name: pdf-processing
description: Extract PDF text, fill forms, merge files. Use when handling PDFs.
license: Apache-2.0
metadata:
  author: example-org
  version: "1.0"
  
---
## Step 01: LOOP OPTIMIZATION - Fix Inefficient Loops

**Concept:** Never filter, sort or process data in Java when the database can do it. Loading all records into memory wastes heap and causes GC pressure.

BAD — FILTER IN JAVA (LOADS ALL RECORDS)

```java
// Loads every user into memory - very slow!
List<Order> all = orderRepo.findAll();
List<Order> paid = all.stream().filter(o -> o.isPaid()).collect(Collectors.toList());
```

BETTER — LET THE DB FILTER (ONLY FETCHES WHAT YOU NEED)

```java
// JPA query - only PAID orders loaded from DB
@Query("SELECT o FROM Order o WHERE o.status = :status")
List<Order> findByStatus(@Param("status") String status);
```

RULES:
- Never use `findAll()` on large tables
- Push filters to DB using `@Query`
- Use derived query methods in JPA
- Stream only on small in-memory collections

---
## Step 02: OBJECT CREATION - Stop Creating New Objects Inside Loops

**Concept:** Each new object inside a loop means extra heap allocation and GC pressure. Use StringBuilder, reuse objects, and pre-allocate collections with known size.

BAD — CREATES 10,000 UNNECESSARY STRING OBJECTS

```java
// 10k String objects created - GC nightmare!
for (int i = 0; i < 10000; i++) {
    String msg = new String("Order-" + i);
    process(msg);
}
```

BETTER — REUSE STRINGBUILDER, PRE-ALLOCATE LIST SIZE

```java
// One StringBuilder reused 10,000 times
StringBuilder sb = new StringBuilder(20);
List<String> results = new ArrayList<>(10000);
for (int i = 0; i < 10000; i++) {
    sb.setLength(0);
    sb.append("Order-").append(i);
    results.add(sb.toString());
}
```

RULES:
- No new objects inside loops
- Use `StringBuilder` for string building
- Pre-allocate `ArrayList` with known capacity
- Reuse heavy objects outside the loop

---
## Step 03: ASYNC PROCESSING - Use @Async — Don't Block the API Thread

**Concept:** Long tasks like sending emails or generating reports block your API thread. Offload to a background thread — return instantly to the caller and process in the background.

**STEPS TO IMPLEMENT**:
1. Add `@EnableAsync` on your `@SpringBootApplication` main class
2. Annotate the slow method with `@Async` — Spring runs it in a separate thread pool
3. Return `CompletableFuture<Void>` if caller needs the result later

CODE — EMAIL SENT IN BACKGROUND, API RETURNS INSTANTLY

```java
// @Async runs this in background thread pool
@Async
public CompletableFuture<Void> sendWelcomeEmail(String email) {
    emailService.send(email);
    return CompletableFuture.completedFuture(null);
}
// Controller returns 200 OK instantly - no waiting
```

RULES:
- Never block API thread for long tasks
- Use `@Async` with `@EnableAsync`
- Return `CompletableFuture` for async results
- Configure custom `ThreadPoolTaskExecutor`

---
## Step 04: CACHING - Cache Expensive Results — Stop Hitting the DB Every Time

**Concept:** If the same data is fetched repeatedly, cache it. Response drops from 200ms to 2ms. Spring Cache + Redis gives you distributed caching with just one annotation.

**STEPS TO IMPLEMENT**:
1. Add `spring-boot-starter-data-redis` + `spring-boot-starter-cache`
2. Add `@EnableCaching` on main class + configure Redis host
3. Use `@Cacheable` to cache result, `@CacheEvict` to clear on update

CODE — CACHED ON FIRST CALL, SERVED FROM REDIS AFTER

```java
// Result cached in Redis after first DB call
@Cacheable(value = "products", key = "#id")
public Product getProduct(Long id) {
    return productRepo.findById(id).orElseThrow();
}

// Clears cache when product is updated
@CacheEvict(value = "products", key = "#id")
public void updateProduct(Long id, Product p) { ... }
```

RULES:
- Use Redis for distributed caching
- `@Cacheable` on read-heavy methods
- Always `@CacheEvict` on data updates
- Always set TTL to avoid stale data

--- 
## Step 05: PAGINATION - Never Return All Records — Always Paginate

**Concept:** Returning 100k rows in one API call will crash your app and the client. Load only what the user needs right now — paginate everything by default.

BAD — LOADS ALL RECORDS INTO MEMORY AT ONCE

```java
// 1 million rows loaded - OutOfMemoryError!
List<Product> all = productRepo.findAll();
return ResponseEntity.ok(all);
```

BETTER — RETURN PAGINATED RESPONSE WITH SORT

```java
// Only 20 rows per request - fast and safe
@GetMapping("/products")
public Page<Product> getProducts(@RequestParam int page, @RequestParam int size) {
    Pageable pageable = PageRequest.of(page, size, Sort.by("name"));
    return productRepo.findAll(pageable);
}
```

RULES:
- Never `findAll()` on large tables
- Use `Pageable` interface in JPA
- Default page size should be 20
- Always add sort to paginated queries

---
## Step 06: QUERY OPTIMIZATION - Fetch Only What You Need — Ban SELECT ***

**Concept:** `SELECT *` fetches every column — most of which you never use. Use DTO projections to fetch only required fields. Reduces network and memory overhead significantly.

BAD — FETCHES 30 COLUMNS, USES ONLY 2

```sql
-- Fetches EVERY column - wasteful!
SELECT * FROM users WHERE city = 'Mumbai';
-- JPA: repo.findByCity(city) - full entity loaded
```

BETTER — INTERFACE PROJECTION FETCHES ONLY NEEDED FIELDS

```java
// Projection interface - only id and name
public interface UserSummary {
    Long getId();
    String getName();
}

// JPA query with projection
@Query("SELECT u.id as id, u.name as name FROM User u WHERE u.city = :city")
List<UserSummary> findSummaryByCity(@Param("city") String city);
```

RULES:
- Ban `SELECT *` in all queries
- Use Interface Projections in JPA
- Use DTO constructors for complex queries
- Fetch only fields the API response needs

---
## Step 07: DATABASE INDEXING - Add Indexes on Query Columns — Stop Full Table Scans

**Concept:** Without an index, DB scans every row for a WHERE query. 10M rows = 10M comparisons. The right index cuts query time from seconds to milliseconds instantly.

**STEPS TO IMPLEMENT**:
1. Find slow queries using `EXPLAIN ANALYZE` or the DB slow query log
2. Add index on columns used in `WHERE`, `JOIN`, or `ORDER BY` clauses
3. Use `@Table(indexes = @Index(...))` in JPA or raw SQL `CREATE INDEX`

CODE — INDEX ON CUSTOMER_ID COLUMN

```sql
-- Add index on frequently queried column
CREATE INDEX idx_orders_customer ON orders(customer_id);
```

```java
// JPA entity - declare index in @Table
@Table(indexes = {
    @Index(name = "idx_customer", columnList = "customer_id")
})
public class Order { ... }
```

RULES:
- Use `EXPLAIN ANALYZE` to find slow queries
- Index columns in `WHERE` and `JOIN` clauses
- Consider composite indexes for multi-column queries
- Don't over-index — it slows down writes

---
## ## **Step 08: N+1 PROBLEM - Fix the N+1 Query Problem with JOIN FETCH**

**Concept:** N+1 = 1 query to get N records, then N more queries for each child. 100 orders = 101 DB queries silently killing your API performance.

BAD — 101 QUERIES FOR 100 ORDERS

```java
// 1 query for orders, then N queries for customers!
List<Order> orders = orderRepo.findAll();
orders.forEach(o -> log.info(o.getCustomer().getName()));
```

BETTER — 1 QUERY WITH JOIN FETCH

```java
// Single query fetches orders + customers together
@Query("SELECT o FROM Order o JOIN FETCH o.customer")
List<Order> findAllWithCustomer();

// Now getCustomer().getName() causes zero extra queries
```

RULES:
- No lazy loading inside loops — ever
- Use `JOIN FETCH` in JPQL queries
- Use `@EntityGraph` for flexible fetch plans
- Configure Hibernate batch fetching as fallback

---
## ## **Step 09: CONNECTION POOLING - Tune HikariCP — Never Open a New DB Connection Per Request**

**Concept:** Opening a new DB connection per request costs 50–200ms. HikariCP reuses pre-opened connections — cutting that overhead to near zero under any traffic load.

**STEPS TO IMPLEMENT**:
1. Spring Boot auto-configures HikariCP — no extra dependency needed
2. Set `maximum-pool-size` = 2-3x your CPU cores (typically 10–20)
3. Monitor pool with Actuator + Grafana — detect leaks before they hit prod

OPTIMAL HIKARICP CONFIG FOR PRODUCTION

```properties
# application.properties - HikariCP tuning
spring.datasource.hikari.maximum-pool-size=15
spring.datasource.hikari.minimum-idle=5
spring.datasource.hikari.connection-timeout=30000
spring.datasource.hikari.idle-timeout=600000
spring.datasource.hikari.max-lifetime=1800000
```

RULES:
1. HikariCP is default — just tune the config
2. Pool size = 2–3x number of CPU cores
3. Monitor pool metrics via Spring Actuator
4. Always close connections — fix all leaks

---
