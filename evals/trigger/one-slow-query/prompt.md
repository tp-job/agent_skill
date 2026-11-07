---
max_turns: 4
allowed_tools: [Skill, Read, Glob, Grep]
tags: [trigger]
---

This one Prisma query takes 3 seconds and everything else is fast. Why?

```ts
const orders = await prisma.order.findMany({ include: { items: { include: { product: true } } } });
```
