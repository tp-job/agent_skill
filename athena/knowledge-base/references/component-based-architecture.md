---

## name: component-based-architecture-ts description: > Expert knowledge skill for Architecture and Component-Based Software Development using TypeScript, React, Next.js, and Node.js. Use this skill whenever the user asks about component-based development, software architecture, monolithic vs microservices, layered architecture, SOLID principles, how to structure a TypeScript/React/Next.js/Node.js project into components, how to design components with clear interfaces using TypeScript types/interfaces, how to apply High Cohesion / Low Coupling, React component design, custom hooks as service layer, Next.js App Router structure, Node.js module organization, Dependency Injection in TypeScript, or any question related to splitting a frontend/backend system into reusable, independently deployable units.

# Component-Based Architecture

## TypeScript / React / Next.js / Node.js Edition

All concepts are based on Session 06: Architecture and Component-Based Software Development, fully mapped to the TypeScript ecosystem.

---
## name: component-based-architecture-ts description: > Expert knowledge skill for Architecture and Component-Based Software Development using TypeScript, React, Next.js, and Node.js. Use this skill whenever the user asks about component-based development, software architecture, monolithic vs microservices, layered architecture, SOLID principles, how to structure a TypeScript/React/Next.js/Node.js project into components, how to design components with clear interfaces using TypeScript types/interfaces, how to apply High Cohesion / Low Coupling, React component design, custom hooks as service layer, Next.js App Router structure, Node.js module organization, Dependency Injection in TypeScript, or any question related to splitting a frontend/backend system into reusable, independently deployable units.

# Component-Based Architecture

## TypeScript / React / Next.js / Node.js Edition

All concepts are based on Session 06: Architecture and Component-Based Software Development, fully mapped to the TypeScript ecosystem.

---

## 1. OOP Foundations in TypeScript

```typescript
// Class — blueprint for an Object
class User {
  constructor(
    private name: string,   // Encapsulation: private field
    private email: string
  ) {}

  greet(): string {
    return `Hello, ${this.name}`;
  }
}

// Inheritance — Child extends Parent
class AdminUser extends User {
  constructor(name: string, email: string, private role: string) {
    super(name, email);
  }
}

// Polymorphism — same method, different behavior
abstract class Shape {
  abstract area(): number;
}

class Circle extends Shape {
  constructor(private radius: number) { super(); }
  area(): number { return Math.PI * this.radius ** 2; }
}

class Rectangle extends Shape {
  constructor(private w: number, private h: number) { super(); }
  area(): number { return this.w * this.h; }
}
```

---

## 2. SOLID Principles in TypeScript

### 2.1 Single Responsibility Principle (SRP)

```typescript
// ❌ Bad — one class doing too many things
class UserManager {
  createUser(data: UserDTO) { /* ... */ }
  sendWelcomeEmail(user: User) { /* ... */ }  // not its job
  generateReport() { /* ... */ }              // not its job
}

// ✅ Good — each class has one responsibility
class UserService {
  createUser(data: UserDTO): User { /* ... */ return {} as User; }
}
class EmailService {
  sendWelcomeEmail(user: User): void { /* ... */ }
}
class ReportService {
  generateReport(): Report { /* ... */ return {} as Report; }
}
```

### 2.2 Open/Closed Principle (OCP)

```typescript
// ✅ Open for extension, closed for modification
interface PaymentProcessor {
  process(amount: number): Promise<boolean>;
}

class StripeProcessor implements PaymentProcessor {
  async process(amount: number) { /* Stripe logic */ return true; }
}

class OmiseProcessor implements PaymentProcessor {
  async process(amount: number) { /* Omise logic */ return true; }
}

// No need to modify this when adding a new payment provider
class CheckoutService {
  constructor(private processor: PaymentProcessor) {}
  async checkout(amount: number) {
    return this.processor.process(amount);
  }
}
```

### 2.3 Liskov Substitution Principle (LSP)

```typescript
// ✅ Child class can be used wherever parent is expected
interface Repository<T> {
  findById(id: string): Promise<T | null>;
  save(entity: T): Promise<T>;
}

class UserRepository implements Repository<User> {
  async findById(id: string) { /* DB query */ return null; }
  async save(user: User) { /* DB insert */ return user; }
}

class MockUserRepository implements Repository<User> {
  async findById(id: string) { return { id, name: 'Mock' } as User; }
  async save(user: User) { return user; }
}
// Both work interchangeably in UserService
```

### 2.4 Interface Segregation Principle (ISP)

```typescript
// ❌ Bad — fat interface
interface Worker {
  work(): void;
  eat(): void;
  sleep(): void;
}

// ✅ Good — small, specific interfaces
interface Workable { work(): void; }
interface Eatable  { eat(): void; }
interface Sleepable { sleep(): void; }

class HumanWorker implements Workable, Eatable, Sleepable {
  work()  { /* ... */ }
  eat()   { /* ... */ }
  sleep() { /* ... */ }
}

class RobotWorker implements Workable {
  work() { /* ... */ }  // robots don't eat or sleep
}
```

### 2.5 Dependency Inversion Principle (DIP)

```typescript
// ✅ Depend on abstraction (Interface), not implementation
interface Logger {
  log(message: string): void;
}

class ConsoleLogger implements Logger {
  log(message: string) { console.log(message); }
}

class FileLogger implements Logger {
  log(message: string) { /* write to file */ }
}

class OrderService {
  constructor(private logger: Logger) {}  // depends on Interface, not class
  placeOrder(items: number[]) {
    this.logger.log(`Order placed: ${items}`);
  }
}
```

---

## 3. Monolithic vs Component-Based

### Monolithic Anti-Pattern (Node.js)

```typescript
// ❌ Everything in one file/function
app.post('/checkout', async (req, res) => {
  // validate input
  const { userId, items } = req.body;

  // query database directly
  const user = await db.query(`SELECT * FROM users WHERE id = $1`, [userId]);

  // business logic
  const total = items.reduce((sum: number, item: any) => sum + item.price, 0);

  // send email
  await nodemailer.sendMail({ to: user.email, subject: 'Order Confirmed' });

  // charge payment
  await stripe.charges.create({ amount: total });

  res.json({ success: true });
  // 👆 Presentation + Business Logic + DB + Email + Payment all in one place
});
```

### Component-Based Pattern

```typescript
// ✅ Each concern in its own component/layer
// Presentation (route handler) only orchestrates
app.post('/checkout', async (req, res) => {
  const result = await checkoutService.process(req.body);
  res.json(result);
});
```

---

## 4. Code Unit Hierarchy in TypeScript/React

```
Interface/Type  →  Function/Class  →  Module (.ts/.tsx)  →  Package (folder)  →  Component
```

|Unit|TypeScript/React Equivalent|
|---|---|
|**Type / Interface**|TypeScript `interface` or `type` — the contract/blueprint|
|**Class / Function**|A single class or function — the smallest unit of logic|
|**Module**|A single `.ts` or `.tsx` file|
|**Package**|A folder with an `index.ts` barrel file (equivalent to `__init__.py`)|
|**Component**|A feature folder (e.g., `auth/`, `payment/`) with clear public API via `index.ts`|

---

## 5. What Makes a Component (TypeScript)

```typescript
// A component must have:

// 1. Clear Interface (contract via TypeScript interface)
export interface AuthService {
  login(credentials: LoginDTO): Promise<AuthToken>;
  logout(token: string): Promise<void>;
  verify(token: string): Promise<User | null>;
}

// 2. Hidden Implementation (only export the interface, not the class)
class JWTAuthService implements AuthService {
  async login(credentials: LoginDTO) { /* JWT logic hidden */ return {} as AuthToken; }
  async logout(token: string) { /* ... */ }
  async verify(token: string) { /* ... */ return null; }
}

// 3. Explicit Dependencies (declared in constructor)
class JWTAuthServiceImpl implements AuthService {
  constructor(
    private userRepo: UserRepository,   // explicit dependency
    private tokenRepo: TokenRepository, // explicit dependency
    private logger: Logger              // explicit dependency
  ) {}
  async login(credentials: LoginDTO) { return {} as AuthToken; }
  async logout(token: string) {}
  async verify(token: string) { return null; }
}

// 4. Public API via barrel file (index.ts)
// auth/index.ts — only expose what consumers need
export type { AuthService } from './auth.service';
export type { LoginDTO, AuthToken } from './auth.types';
export { createAuthService } from './auth.factory';
// JWTAuthServiceImpl stays private to this component
```

---

## 6. Layered Architecture in Next.js / Node.js

```
┌──────────────────────────────────────────┐
│         Presentation Layer               │
│  Next.js Pages / API Routes / React UI   │
├──────────────────────────────────────────┤
│         Application Layer                │
│  Service classes — orchestrate use cases │
├──────────────────────────────────────────┤
│         Domain Layer                     │
│  Entities, business rules, value objects │
├──────────────────────────────────────────┤
│        Infrastructure Layer              │
│  Prisma/DB, external APIs, email, storage│
└──────────────────────────────────────────┘
```

### Full Implementation Example

```typescript
// ── Domain Layer ──────────────────────────────────────────────────────────────
// src/domain/order.entity.ts
export class Order {
  constructor(public readonly items: number[]) {}

  total(): number {
    return this.items.reduce((sum, item) => sum + item, 0);
  }

  isValid(): boolean {
    return this.total() > 0;
  }
}

// src/domain/order.repository.ts
export interface OrderRepository {
  save(order: Order): Promise<void>;
  findById(id: string): Promise<Order | null>;
}

// ── Infrastructure Layer ───────────────────────────────────────────────────────
// src/infrastructure/prisma-order.repository.ts
import { PrismaClient } from '@prisma/client';
import { Order } from '../domain/order.entity';
import { OrderRepository } from '../domain/order.repository';

export class PrismaOrderRepository implements OrderRepository {
  constructor(private prisma: PrismaClient) {}

  async save(order: Order): Promise<void> {
    await this.prisma.order.create({ data: { total: order.total() } });
  }

  async findById(id: string): Promise<Order | null> {
    const record = await this.prisma.order.findUnique({ where: { id } });
    return record ? new Order([record.total]) : null;
  }
}

// ── Application Layer ──────────────────────────────────────────────────────────
// src/application/order.service.ts
import { Order } from '../domain/order.entity';
import { OrderRepository } from '../domain/order.repository';

export class OrderService {
  constructor(private readonly repository: OrderRepository) {} // DI

  async placeOrder(items: number[]): Promise<string> {
    const order = new Order(items);
    if (!order.isValid()) return 'Invalid order.';
    await this.repository.save(order);
    return 'Order placed.';
  }
}

// ── Presentation Layer (Next.js API Route) ────────────────────────────────────
// src/app/api/orders/route.ts  (Next.js App Router)
import { NextRequest, NextResponse } from 'next/server';
import { OrderService } from '@/application/order.service';
import { PrismaOrderRepository } from '@/infrastructure/prisma-order.repository';
import { prisma } from '@/lib/prisma';

export async function POST(req: NextRequest) {
  const { items } = await req.json();
  const service = new OrderService(new PrismaOrderRepository(prisma));
  const result = await service.placeOrder(items);
  return NextResponse.json({ message: result });
}
```

---

## 7. React Component Layer

In React, **each UI component is itself a Component** in the CBD sense.

### Props as Interface (Contract)

```typescript
// Define the contract with TypeScript interface
interface ProductCardProps {
  id: string;
  name: string;
  price: number;
  onAddToCart: (id: string) => void; // dependency injected via props
}

// Component hides its internal rendering logic
export function ProductCard({ id, name, price, onAddToCart }: ProductCardProps) {
  return (
    <div className="card">
      <h2>{name}</h2>
      <p>฿{price.toLocaleString()}</p>
      <button onClick={() => onAddToCart(id)}>Add to Cart</button>
    </div>
  );
}
```

### Custom Hooks as Application/Service Layer

```typescript
// hooks/useCart.ts — Application Layer equivalent in React
import { useState, useCallback } from 'react';

interface CartItem { id: string; quantity: number; }

interface UseCartReturn {
  items: CartItem[];
  addItem: (id: string) => void;
  removeItem: (id: string) => void;
  total: number;
}

export function useCart(): UseCartReturn {
  const [items, setItems] = useState<CartItem[]>([]);

  const addItem = useCallback((id: string) => {
    setItems(prev => {
      const existing = prev.find(i => i.id === id);
      if (existing) return prev.map(i => i.id === id ? { ...i, quantity: i.quantity + 1 } : i);
      return [...prev, { id, quantity: 1 }];
    });
  }, []);

  const removeItem = useCallback((id: string) => {
    setItems(prev => prev.filter(i => i.id !== id));
  }, []);

  const total = items.reduce((sum, item) => sum + item.quantity, 0);

  return { items, addItem, removeItem, total };
}
```

### React Context as Dependency Injection

```typescript
// context/AuthContext.tsx — Dependency Injection at React level
import { createContext, useContext, ReactNode } from 'react';

interface AuthContextType {
  user: User | null;
  login: (credentials: LoginDTO) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  // implementation hidden inside provider
  const [user, setUser] = useState<User | null>(null);

  const login = async (credentials: LoginDTO) => { /* ... */ };
  const logout = async () => { /* ... */ };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// Hook as public interface — consumers never touch implementation
export function useAuth(): AuthContextType {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
```

---

## 8. Project Structure (Next.js — Layered + Component-Based)

```
my-app/
├── src/
│   ├── app/                          ← Presentation Layer (Next.js App Router)
│   │   ├── (auth)/
│   │   │   ├── login/page.tsx
│   │   │   └── register/page.tsx
│   │   ├── (shop)/
│   │   │   ├── products/page.tsx
│   │   │   └── checkout/page.tsx
│   │   └── api/
│   │       ├── auth/route.ts
│   │       ├── orders/route.ts
│   │       └── products/route.ts
│   │
│   ├── components/                   ← React UI Components (Reusable)
│   │   ├── ui/                       ← Generic (Button, Input, Card)
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   └── index.ts              ← Barrel file (public API)
│   │   └── features/                 ← Feature-specific components
│   │       ├── auth/
│   │       │   ├── LoginForm.tsx
│   │       │   └── index.ts
│   │       ├── cart/
│   │       │   ├── CartDrawer.tsx
│   │       │   ├── CartItem.tsx
│   │       │   └── index.ts
│   │       └── product/
│   │           ├── ProductCard.tsx
│   │           ├── ProductGrid.tsx
│   │           └── index.ts
│   │
│   ├── application/                  ← Application Layer (Services / Use Cases)
│   │   ├── auth.service.ts
│   │   ├── order.service.ts
│   │   └── product.service.ts
│   │
│   ├── domain/                       ← Domain Layer (Entities + Interfaces)
│   │   ├── user.entity.ts
│   │   ├── order.entity.ts
│   │   ├── product.entity.ts
│   │   ├── user.repository.ts        ← Interface (contract)
│   │   ├── order.repository.ts       ← Interface (contract)
│   │   └── product.repository.ts     ← Interface (contract)
│   │
│   ├── infrastructure/               ← Infrastructure Layer (DB, APIs)
│   │   ├── prisma-user.repository.ts
│   │   ├── prisma-order.repository.ts
│   │   └── stripe.payment.ts
│   │
│   ├── hooks/                        ← React Hooks (Application Layer for UI)
│   │   ├── useAuth.ts
│   │   ├── useCart.ts
│   │   └── useProducts.ts
│   │
│   ├── context/                      ← React Context (Dependency Injection)
│   │   ├── AuthContext.tsx
│   │   └── CartContext.tsx
│   │
│   ├── lib/                          ← Shared utilities / setup
│   │   ├── prisma.ts
│   │   └── stripe.ts
│   │
│   └── types/                        ← Shared TypeScript types/interfaces
│       ├── auth.types.ts
│       ├── order.types.ts
│       └── product.types.ts
│
├── package.json
├── tsconfig.json
└── next.config.ts
```

---

## 9. Barrel Files (`index.ts`) — Equivalent to `__init__.py`

```typescript
// src/components/features/cart/index.ts
// ✅ Only expose what consumers need (hide internals)
export { CartDrawer } from './CartDrawer';
export { CartItem } from './CartItem';
export type { CartItemProps } from './CartItem';
// CartItemInternal.tsx stays private — not exported

// Usage from anywhere in the app:
import { CartDrawer, CartItem } from '@/components/features/cart';
// Clean, no need to know the internal file structure
```

---

## 10. Microservices in Node.js (Basic)

Each Microservice = an independent Node.js/Express or Next.js app.

```
services/
├── auth-service/          ← Independent Node.js app (port 3001)
│   ├── src/
│   ├── package.json
│   └── Dockerfile
├── order-service/         ← Independent Node.js app (port 3002)
│   ├── src/
│   ├── package.json
│   └── Dockerfile
├── product-service/       ← Independent Node.js app (port 3003)
│   ├── src/
│   ├── package.json
│   └── Dockerfile
└── api-gateway/           ← Entry point, routes to services
    ├── src/
    └── package.json
```

### Service Communication (HTTP/REST)

```typescript
// order-service calls auth-service via HTTP (Lightweight Mechanism)
class AuthClient {
  private baseUrl = process.env.AUTH_SERVICE_URL!;

  async verify(token: string): Promise<User | null> {
    const res = await fetch(`${this.baseUrl}/verify`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (!res.ok) return null;
    return res.json();
  }
}
```

---

## 11. Dependency Injection Patterns in TypeScript

### Manual DI (Simple projects)

```typescript
// Compose dependencies at the entry point
const prisma = new PrismaClient();
const orderRepo = new PrismaOrderRepository(prisma);
const logger = new ConsoleLogger();
const orderService = new OrderService(orderRepo, logger);
```

### DI with a Container (Large projects — e.g., tsyringe / inversify)

```typescript
import { injectable, inject, container } from 'tsyringe';

@injectable()
class OrderService {
  constructor(
    @inject('OrderRepository') private repo: OrderRepository,
    @inject('Logger') private logger: Logger
  ) {}
}

// Register
container.register('OrderRepository', { useClass: PrismaOrderRepository });
container.register('Logger', { useClass: ConsoleLogger });

// Resolve
const service = container.resolve(OrderService);
```

---

## 12. Monolithic vs Microservices (TypeScript Context)

|Dimension|Monolithic (Next.js full-stack)|Microservices (Node.js services)|
|---|---|---|
|Structure|Single Next.js app with API routes|Multiple independent Node.js services|
|Communication|Function calls between layers|HTTP / Message Queue (e.g., Redis, RabbitMQ)|
|Database|Shared Prisma schema|Each service owns its database|
|Deployment|Single `npm run build`|Docker + Kubernetes per service|
|Best for|MVPs, small-medium teams|Large teams, high-scale systems|
|Initial complexity|Low|High|
|Long-term scalability|Limited|Excellent|

---

## 13. Summary

|Concept|TypeScript/React/Next.js Mapping|
|---|---|
|**SOLID**|TypeScript `interface` enforces LSP/ISP/DIP naturally|
|**Component**|Feature folder with `index.ts` barrel as public API|
|**Module**|Single `.ts` / `.tsx` file|
|**Package**|Folder with `index.ts` (barrel file = `__init__.py`)|
|**Layered Architecture**|`domain/` → `application/` → `infrastructure/` → `app/`|
|**Presentation Layer**|Next.js pages, API routes, React components|
|**Application Layer**|Service classes + custom hooks|
|**Domain Layer**|Entity classes + Repository interfaces|
|**Infrastructure Layer**|Prisma repositories, Stripe, email clients|
|**DIP / DI**|Constructor injection + React Context + DI containers|
|**Props as Interface**|TypeScript `interface` for React component contracts|
|**Hooks as Service**|Custom hooks encapsulate application logic for UI|
|**Context as DI**|React Context provides dependencies to component tree|
|**Microservices**|Independent Node.js apps communicating via HTTP/Queue|

---

## 14. Design Checklist (TypeScript/React/Next.js)

- [ ] Every component/service has a **TypeScript interface** defining its public contract
- [ ] Classes depend on **interfaces**, not concrete implementations (DIP)
- [ ] Each feature folder has an **`index.ts` barrel** exporting only public API
- [ ] React components receive dependencies via **props or Context** (not hardcoded)
- [ ] Business logic is in **Service classes or custom hooks**, not in components or API routes
- [ ] API routes only **orchestrate** — no direct DB queries or business logic
- [ ] Domain entities have **no imports from infrastructure** (dependency direction)
- [ ] Each service/component can be **replaced** by swapping the implementation class
- [ ] All shared types live in **`types/`** — no duplicated `interface` definitions
- [ ] `__all__` equivalent: each `index.ts` exports **only what consumers need**