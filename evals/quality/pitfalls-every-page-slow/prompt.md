---
max_turns: 14
allowed_tools: [Skill, Read, Glob, Grep]
tags: [quality]
---

Every page in our app takes 2-6 seconds to load. Backend is Fastify + Prisma on Supabase; the database is in Tokyo, we connect through the transaction pooler on port 6543 with pgbouncer=true, read-only queries are wrapped in prisma.$transaction([...]), and the class dashboard makes one request per student. Make it faster.
