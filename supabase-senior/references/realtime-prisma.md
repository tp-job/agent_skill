# Supabase Realtime + Prisma Coexistence

Running Realtime subscriptions alongside Prisma writes without fighting over the schema.

## 8. SUPABASE REALTIME + PRISMA COEXISTENCE

Realtime subscriptions use the anon key + RLS. Prisma mutations trigger those events.
This is safe — Prisma writes hit Postgres, Supabase Realtime listens to the WAL.

```ts
// Client: subscribe with user-scoped filter
const channel = supabase
  .channel('user-updates')
  .on(
    'postgres_changes',
    {
      event: '*',
      schema: 'public',
      table: 'notifications',
      filter: `user_id=eq.${userId}`,  // Always filter by user — never subscribe to whole table
    },
    (payload) => handleUpdate(payload)
  )
  .subscribe()
```

> **RLS on Realtime**: As of 2024+, Supabase enforces RLS on Realtime subscriptions.
> Ensure the `authenticated` role has SELECT policy on any table being subscribed to.
