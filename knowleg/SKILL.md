---
name: knowledge-base
description: Software engineering knowledge base covering architecture patterns, component-based design, security fundamentals, software design principles, and use case + microservices design. Use this skill when answering questions about software architecture, design patterns, system design, security best practices, or use case modeling. Triggers on tasks involving architecture decisions, component design, security review, software design review, or microservices planning. Also trigger for: "architecture patterns", "component design", "software design", "system design", "security patterns", "use case diagram", "microservices design", "3-tier architecture", "design principles", or any request for software engineering reference knowledge.
license: MIT
metadata:
  author: nevinas06 (enhanced by Claude)
  version: "1.0.0"
  source: Software Engineering Knowledge Base (compiled 2026)
---

# Software Engineering Knowledge Base

A curated knowledge base covering five core software engineering domains. Use as a reference when making architecture decisions, designing systems, reviewing security posture, or modeling use cases.

## When to Apply

Reference this knowledge base when:
- Making architecture or system design decisions
- Designing component hierarchies and boundaries
- Reviewing or improving security posture
- Studying or applying software design principles (SOLID, DRY, Clean Architecture)
- Modeling systems with use case diagrams, microservices, or 3-tier patterns
- Onboarding to a new codebase or system

## Knowledge Domains

| Domain | File | Topics Covered |
|--------|------|---------------|
| Architecture | `architecture.md` | System architecture patterns, trade-offs, scalability |
| Component-Based Architecture | `component-based-architecture.md` | Component design, composition, atomic design |
| Security | `security.md` | Security fundamentals, threat modeling, secure defaults |
| Software Design 2024 | `software-design-2024.md` | Modern design principles, Clean Architecture, DDD |
| Use Cases + Microservices + 3-Tier | `usecase-microservices-3tier.md` | Use case modeling, Microservices patterns, 3-tier design |

## Quick Reference

### 1. Architecture Patterns
- Monolith vs Microservices — when to choose each
- Event-driven architecture — pub/sub, CQRS, event sourcing
- Layered architecture — presentation, business, data layers
- Hexagonal (Ports & Adapters) — decoupling core from infrastructure
- Key trade-offs: scalability, maintainability, operational complexity

### 2. Component-Based Architecture
- Atomic Design: Atom → Molecule → Organism → Template → Page
- Single Responsibility per component
- Composition over inheritance
- Props-down, events-up communication pattern
- Component API contracts and prop types

### 3. Security Fundamentals
- Authentication vs Authorization — identity vs permission
- Principle of Least Privilege — grant minimum required access
- Defense in Depth — multiple security layers
- Input validation at every boundary
- Secrets management — never in source code

### 4. Software Design Principles (2024)
- **SOLID** — Single Responsibility, Open/Closed, Liskov, Interface Segregation, Dependency Inversion
- **DRY** — Don't Repeat Yourself; but don't abstract prematurely (Rule of Three)
- **YAGNI** — You Aren't Gonna Need It; build what's needed now
- **Clean Architecture** — dependencies point inward; domain at the center
- **Domain-Driven Design** — model software around business domain language

### 5. Use Cases + Microservices + 3-Tier
- Use Case Diagram: Actor → System Boundary → Use Case (ellipse)
- Use case naming: Verb + Noun (e.g. "Register Account", "Place Order")
- 3-Tier: Presentation → Business Logic → Data Access
- Microservices: one service per bounded context
- API Gateway pattern — single entry point, routing, auth, rate limiting
- Service decomposition: by business capability, not by technical layer

## How to Use

1. Identify the domain matching the current question or task
2. Open the corresponding reference file for detailed patterns
3. Apply the relevant principles to the design or code under review

```
architecture.md              — System and service architecture
component-based-architecture.md — UI and component design
security.md                  — Security review and design
software-design-2024.md      — Design principles and patterns
usecase-microservices-3tier.md — System modeling and architecture
```

## Reference Files

| File | Read When |
|------|-----------|
| `architecture.md` | System design, architectural decisions |
| `component-based-architecture.md` | Component design, atomic design, composition |
| `security.md` | Security review, threat modeling |
| `software-design-2024.md` | Design principles, Clean Architecture, DDD |
| `usecase-microservices-3tier.md` | Use case modeling, Microservices, 3-tier |
