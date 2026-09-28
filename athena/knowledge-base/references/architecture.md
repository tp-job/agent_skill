---

## name: component-based-architecture description: > Expert knowledge skill for Architecture and Component-Based Software Development (CBD). Use this skill whenever the user asks about component-based development, software architecture, monolithic vs microservices, layered architecture, SOLID principles, Python modules/packages, how to structure a Python project into components, how to design components with clear interfaces, how to apply High Cohesion / Low Coupling, or any question related to splitting a system into reusable, independently deployable units. Also trigger when the user mentions Class, Module, Package, Component hierarchy in Python, Dependency Injection, or Interface-based communication.

# Component-Based Architecture & Software Development

This skill contains complete, authoritative knowledge from Session 06 covering: OOP foundations → SOLID principles → Monolithic systems → Component-Based Development → Layered Architecture → Microservices → Python Modules & Packages.

---

Expert knowledge skill for Architecture and Component-Based Software Development (CBD). Use this skill whenever the user asks about component-based development, software architecture, monolithic vs microservices, layered architecture, SOLID principles, Python modules/packages, how to structure a Python project into components, how to design components with clear interfaces, how to apply High Cohesion / Low Coupling, or any question related to splitting a system into reusable, independently deployable units. Also trigger when the user mentions Class, Module, Package, Component hierarchy in Python, Dependency Injection, or Interface-based communication.

# Component-Based Architecture & Software Development

This skill contains complete, authoritative knowledge from Session 06 covering: OOP foundations → SOLID principles → Monolithic systems → Component-Based Development → Layered Architecture → Microservices → Python Modules & Packages.

---

## 1. OOP Foundations (Prerequisites)

|Concept|Summary|
|---|---|
|**Class**|Blueprint / template for creating Objects|
|**Object**|Instance of a Class|
|**Encapsulation**|Bundling data + behavior; hiding internal details|
|**Inheritance**|Child class inherits attributes & methods from parent|
|**Polymorphism**|Same interface, different behavior depending on the object|

---

## 2. SOLID Principles

### 2.1 Single Responsibility Principle (SRP)

- A class should have **one reason to change** — one responsibility only.

### 2.2 Open/Closed Principle (OCP)

- **Open for extension, closed for modification.**
- Add new behavior by extending, not by changing existing code.

### 2.3 Liskov Substitution Principle (LSP)

- A **child class must be substitutable** for its parent class without breaking the system.

### 2.4 Interface Segregation Principle (ISP)

- Prefer **small, specific interfaces** over large, general ones.
- A class should not be forced to implement methods it doesn't need.

### 2.5 Dependency Inversion Principle (DIP)

- **Depend on abstractions (Interfaces), not on concrete implementations.**
- High-level modules should not depend on low-level modules; both should depend on abstractions.

---

## 3. Monolithic Architecture

### Definition

A system design where **everything is bundled into a single structure or program**.

### Characteristics

- All parts are tightly coupled
- Small changes can impact the entire system
- Difficult to maintain, test, and scale
- Deployment is slow and risky
- Large teams struggle to work in parallel

### Example (Python — Monolithic Anti-Pattern)

```python
def main():
    user_input = input("Enter your name: ")
    print(f"Hello, {user_input}!")
    # connect to database
    # process data
    # display result
    # everything in one function

main()
```

---

## 4. Component-Based Development (CBD)

### Definition

An approach to building software from **reusable, independently deployable, modular units (components)**.

### Benefits of CBD

|Benefit|Description|
|---|---|
|**Reusability**|Components can be reused across multiple projects (e.g., User Auth, Payment Gateway)|
|**Independent Deployment**|Each component can be deployed, updated, and tested independently → reduces risk & downtime|
|**Modularity**|System is split into small, well-bounded units (SRP at a large scale)|
|**Reduced Complexity**|Large problems broken into smaller, manageable sub-problems|
|**Team Collaboration**|Different teams can work on different components simultaneously|
|**Flexibility**|Replace or upgrade one component without affecting others|

---

## 5. Code Unit Hierarchy (Small → Large)

```
Class  →  Module  →  Package  →  Component
```

|Unit|Definition|
|---|---|
|**Class**|Blueprint for an Object; the smallest unit in OOP|
|**Module**|A single Python file (`.py`) that can contain Classes, Functions, and Variables|
|**Package**|A folder containing multiple Modules + an `__init__.py` file|
|**Component**|A larger unit (may contain many Classes, Modules, Packages) with a clear Interface, reusable and independently deployable|

---

## 6. What Makes a Component?

A Component **must**:

1. **Have a clear Interface**

    - Defines what it can do
    - Specifies what data it accepts/returns (API contract)
2. **Hide its Implementation**

    - External consumers do not need to know internal logic
3. **Declare its Dependencies explicitly**

    - States which other components it depends on

### Replaceability

A component is **replaceable** — you can swap it out for another component with the same interface/contract without breaking the overall system.

---

## 7. Component Design Principles

### 7.1 Defining Component Boundaries

Determine boundaries by considering:

- **Business Capabilities** — What the organization does (e.g., Order Management, Payment, Customer Management)
- **Rate of Change** — How frequently is this code modified? (e.g., Promotions display, Tax calculation) — high change frequency → separate component
- **Team Ownership** — Which team develops, tests, and deploys this component?

### 7.2 Design Target

```
High Cohesion WITHIN a component
Low Coupling BETWEEN components
```

### 7.3 Managing Dependencies Between Components

|Strategy|Description|
|---|---|
|**Dependency Direction**|Higher-level components depend on lower-level ones; never reverse|
|**Interface-based Communication**|Components communicate through pre-defined Interfaces without knowing internal implementation (similar to OCP)|
|**Dependency Injection**|Dependencies are passed in from outside rather than created internally|

---

## 8. Layered Architecture

### Overview

Layered Architecture provides **clear separation of responsibilities** and is the foundation for Component Design.

### The 4 Layers

```
┌─────────────────────────────┐
│      Presentation Layer     │  ← User Interface (UI)
├─────────────────────────────┤
│      Application Layer      │  ← Business Logic Orchestration
├─────────────────────────────┤
│        Domain Layer         │  ← Core Business Entities & Rules
├─────────────────────────────┤
│    Infrastructure Layer     │  ← Database, External APIs, File System
└─────────────────────────────┘
```

### Layer Responsibilities

#### Presentation Layer (UI)

- Entry point for user interaction
- Collects input, displays output

#### Application Layer (Business Logic)

- Receives commands from Presentation Layer
- Calls Domain Layer and Infrastructure Layer in order
- **Must NOT** contain direct Business Logic (delegate to Domain Layer)
- **Must NOT** access databases directly (call through Infrastructure Layer interface)

#### Domain Layer (Core Business Entities)

- Central layer managing core entities, behaviors, and business rules
- Reflects the real-world understanding of the business domain

#### Infrastructure Layer (Database / External Services)

- Manages database connections
- Integrates with external APIs
- Manages file systems and other external resources

> **Key rule:** Each Layer is a Component with a specific responsibility that communicates with other layers through Interfaces.

### Python Implementation Example

```python
# ── Domain Layer ──────────────────────────────────────────────────────────────
# Responsibility: Core business logic and entities
class Order:
    def __init__(self, items):
        self.items = items

    def total(self):
        return sum(self.items)

    def is_valid(self):
        return self.total() > 0

# ── Infrastructure Layer ──────────────────────────────────────────────────────
# Responsibility: Connect to external systems (database, APIs, files)
class InMemoryOrderRepository:
    def save(self, order: Order):
        print(f"[Infrastructure] Order saved with total: {order.total()}")

# ── Application Layer ──────────────────────────────────────────────────────────
# Responsibility: Orchestrate between Domain and Infrastructure
class OrderService:
    def __init__(self, repository):
        self.repository = repository  # Dependency Injection

    def place_order(self, items):
        order = Order(items)
        if order.is_valid():
            self.repository.save(order)
            return "Order placed."
        return "Invalid order."

# ── Presentation Layer ─────────────────────────────────────────────────────────
# Responsibility: Interface with the user
def main():
    print("[Presentation] Placing order...")
    items = [100, 200, 300]  # mock user input
    service = OrderService(InMemoryOrderRepository())
    result = service.place_order(items)
    print(f"[Presentation] Result: {result}")

if __name__ == "__main__":
    main()
```

---

## 9. Microservices Architecture

### Definition

An architectural style where an application is developed as a **suite of small, independently running services**.

### Key Characteristics

- Each service is a self-contained Component
- Each Microservice has its **own database** (or carefully shared)
- Services communicate via **Lightweight Mechanisms**: HTTP/REST API, Message Queues

### Advantages of Microservices

|Advantage|Description|
|---|---|
|**Scalability**|Scale each service independently|
|**Technology Diversity**|Each service can use different tech stacks|
|**Resilience**|If one service fails, others keep running|
|**Independent Deployment**|Deploy each service separately|
|**Easier to Understand/Maintain**|Small codebase per service|

### Considerations / Trade-offs

|Consideration|Description|
|---|---|
|**Management Complexity**|Must manage many services, communication, monitoring|
|**Communication Overhead**|Network overhead between services|
|**Distributed Transactions**|Cross-service transactions are difficult|
|**Best suited for**|Large projects, large teams requiring high flexibility|

---

## 10. Monolithic vs Microservices — Comparison

|Dimension|Monolithic|Microservices|
|---|---|---|
|Structure|Single large application|Many small independent services|
|Coupling|All parts bundled together|Services communicate via APIs|
|Initial Setup|Easy to start|Complex to set up initially|
|Scaling|Difficult as it grows|Flexible and scales well long-term|
|Maintenance|Hard at scale|Easier per service|
|Deployment|Full re-deploy required|Independent per service|

---

## 11. Python Modules

### Definition

A Python **Module** is a single `.py` file containing Python code (Functions, Classes, Variables).

### Purpose

- Organizes code into logical sections
- Enables reuse across files

### Import Patterns

```python
import my_module                          # import entire module
from my_module import my_function         # import specific item
from my_module import *                   # NOT recommended — pollutes namespace
```

---

## 12. Python Packages

### Definition

A **Package** is a folder containing multiple Modules and a special file `__init__.py`.

### Purpose

- Groups related Modules together
- Creates a hierarchical (nested) structure

### Example Project Structure

```
my_project/
├── main.py
└── my_package/
    ├── __init__.py
    ├── module_a.py
    └── sub_package/
        ├── __init__.py
        └── module_b.py
```

### Import Patterns

```python
import my_package.module_a
from my_package.sub_package import module_b
```

---

## 13. The `__init__.py` File

|Context|Behavior|
|---|---|
|**Python 2 & Python ≤ 3.2**|Required to mark a folder as a Python Package|
|**Python 3.3+**|Optional (namespace packages supported), but still commonly used|

### Common Uses in Python 3.3+

- Define what gets exported when `from package import *` is called (via `__all__`)
- Run Package-level initialization code
- Re-export Sub-modules to simplify import paths for consumers

---

## 14. Modules/Packages and CBD

Python Modules and Packages are the **foundational tools for building Components** at the code level:

- Each Package can be treated as a **sub-Component** with a specific responsibility
- Enables structured organization of large projects
- `__init__.py` acts as the **public interface** of a Package/Component

---

## 15. Summary

|Concept|Key Takeaway|
|---|---|
|**CBD**|Build software from reusable, independently deployable, modular components|
|**Component**|Independent unit with clear Interface, hidden Implementation, and explicit Dependencies|
|**SOLID**|Design principles ensuring maintainable, extensible OOP code|
|**Layered Architecture**|4-layer structure (Presentation → Application → Domain → Infrastructure) providing clear separation of concerns|
|**Microservices**|Each service = independent Component; communicates via API/Message Queue|
|**Python Module**|Single `.py` file; basic unit of code organization|
|**Python Package**|Folder of Modules + `__init__.py`; represents a Component in code|

---

## 16. Design Checklist

Use this checklist when designing a Component-Based system:

- [ ] Does each component have a **single, clear responsibility**? (SRP / High Cohesion)
- [ ] Are components communicating through **Interfaces**, not concrete implementations? (DIP / OCP)
- [ ] Is the **dependency direction** correct (high-level → low-level)?
- [ ] Can each component be **deployed independently**?
- [ ] Can each component be **replaced** without breaking others?
- [ ] Are **dependencies declared explicitly** (Dependency Injection)?
- [ ] Is there **Low Coupling** between components and **High Cohesion** within each component?
- [ ] Does each Python Package have an appropriate `__init__.py` defining its public API?