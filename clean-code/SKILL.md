---
name: clean-code-javascript
description: >-
  Clean Code principles and best practices for JavaScript. Use this skill when writing, reviewing, or refactoring JavaScript/TypeScript code to improve readability, maintainability, and correctness. Triggers on tasks involving naming conventions, function design, class structure, SOLID principles, error handling, testing patterns, or code formatting. Also trigger for: "clean up my code", "make this readable", "refactor this function", "bad variable names", "code review", "improve code quality", "apply SOLID", "JavaScript best practices", or any request to improve JS/TS code quality.
license: MIT
metadata:
  author: nevinas06 (enhanced by Claude)
  version: "1.0.0"
  source: Clean Code by Robert C. Martin — JS/TS adaptation (compiled 2026)
---

# Clean Code — JavaScript

Adapted from Robert C. Martin's _Clean Code_ for JavaScript and TypeScript. A comprehensive guide covering 11 categories of code quality principles, from variable naming to error handling and testing.

## When to Apply

Reference these guidelines when:
- Writing new JavaScript or TypeScript modules
- Reviewing code for readability or maintainability issues
- Refactoring legacy code to improve structure
- Naming variables, functions, or classes
- Designing class hierarchies and applying SOLID
- Setting up error handling or async patterns

## Principle Categories by Priority

| Priority | Category | Impact |
|----------|---------|--------|
| 1 | Variables — naming and scope | CRITICAL |
| 2 | Functions — size, arguments, side effects | CRITICAL |
| 3 | Objects and Data Structures | HIGH |
| 4 | Classes — structure and cohesion | HIGH |
| 5 | SOLID Principles | HIGH |
| 6 | Error Handling | MEDIUM-HIGH |
| 7 | Testing — coverage and clarity | MEDIUM |
| 8 | Concurrency — async patterns | MEDIUM |
| 9 | Formatting — consistency | MEDIUM |
| 10 | Comments — when to write, when to delete | LOW-MEDIUM |

## Quick Reference

### 1. Variables (CRITICAL)
- Use meaningful, pronounceable variable names — no abbreviations like `yyyymmdstr`
- Same vocabulary for same concept — pick one: `getUserInfo` vs `getClientData` vs `getCustomerRecord`
- Use searchable names — no magic numbers like `86400`
- Avoid mental mapping — `i` OK in short loops, not elsewhere
- Use `const` over `let`; avoid `var`
- Use default arguments instead of short-circuit `||` tricks

### 2. Functions (CRITICAL)
- Functions should do **one thing** only
- Keep functions small — aim for ≤ 20 lines
- No more than 2–3 parameters; group extra params into objects
- Avoid flag (boolean) arguments — split into two functions
- No side effects — a function should do what its name says
- Prefer pure functions; avoid shared mutable state
- Use `Object.assign` or spread for default object params

### 3. Objects and Data Structures (HIGH)
- Use getters/setters for property access — easier to validate, log, and intercept
- Favor composition over inheritance
- Avoid primitive obsession — model domain concepts as objects

### 4. Classes (HIGH)
- Prefer ES6 classes over plain prototype functions
- Use method chaining (return `this`) for fluent APIs
- Small, focused classes — single responsibility per class

### 5. SOLID Principles (HIGH)
- **S** — Single Responsibility: one reason to change per class
- **O** — Open/Closed: open for extension, closed for modification
- **L** — Liskov Substitution: subclasses must honor parent contracts
- **I** — Interface Segregation: small focused interfaces
- **D** — Dependency Inversion: depend on abstractions, not implementations

### 6. Error Handling (MEDIUM-HIGH)
- Always handle Promise rejections — never silent `.catch()` with empty body
- Use `async/await` with `try/catch` over naked Promise chains
- Throw `Error` objects, not plain strings
- Provide context in error messages

### 7. Testing (MEDIUM)
- One concept per test — each test covers a single behavior
- Use F.I.R.S.T: Fast, Independent, Repeatable, Self-validating, Timely
- Readable test names — describe the scenario, not the implementation

### 8. Concurrency (MEDIUM)
- Prefer `async/await` over raw Promise chains for readability
- Use `Promise.all()` for parallel operations
- Avoid mixing callbacks and Promises

### 9. Formatting (MEDIUM)
- Consistent indentation across the whole codebase
- One concept per line — avoid dense one-liners
- Related code belongs together — vertical proximity matters

### 10. Comments (LOW-MEDIUM)
- Good code documents itself — a comment explaining *what* is a red flag
- Comments should explain *why*, not *what*
- Remove commented-out code — use git instead
- No journal comments in source files

## How to Use

Open the reference document for full explanations with BAD vs GOOD code examples:

```
clean-code-javascript.md — Variables section
clean-code-javascript.md — Functions section
clean-code-javascript.md — SOLID section
```

Each section contains:
- Brief principle statement
- Bad code example with explanation
- Good code example with explanation

## Full Reference Document

For the complete guide with all examples: `clean-code-javascript.md`