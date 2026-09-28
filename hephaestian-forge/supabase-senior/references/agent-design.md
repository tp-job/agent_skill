# Agent Design — Supabase-Backed AI Agents

Auth boundaries for agents, the Edge Function agent pattern, and multi-step agent workflows with Prisma.

## 7. AGENT DESIGN — SUPABASE-BACKED AI AGENTS

### Agent Auth Architecture

```
Agent Layer
    │
    ├── User-context agents  → use anon key + JWT forwarding → RLS enforced
    │                           (chatbots, copilots acting on behalf of a user)
    │
    └── System agents        → use service_role            → RLS bypassed
                                (data processing, cron, background jobs)
```

### Edge Function Agent Pattern

```ts
// supabase/functions/agent-handler/index.ts
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

Deno.serve(async (req) => {
  // 1. Verify user JWT (anon client respects RLS)
  const userClient = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_ANON_KEY')!,
    { global: { headers: { Authorization: req.headers.get('Authorization')! } } }
  )
  const { data: { user }, error } = await userClient.auth.getUser()
  if (error || !user) return new Response('Unauthorized', { status: 401 })

  // 2. Use service_role for privileged operations AFTER auth check
  const adminClient = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  )

  // 3. Scope all admin operations explicitly to user
  const { data } = await adminClient
    .from('agent_logs')
    .insert({ user_id: user.id, action: 'run', timestamp: new Date() })

  return new Response(JSON.stringify({ ok: true }), {
    headers: { 'Content-Type': 'application/json' },
  })
})
```

### Multi-Step Agent Workflow with Prisma

```ts
// Long workflow with transaction safety
async function runAgentWorkflow(userId: string, payload: AgentPayload) {
  return await prisma.$transaction(async (tx) => {
    // Step 1: Reserve the job (atomic)
    const job = await tx.agentJob.update({
      where: { id: payload.jobId, status: 'pending' },
      data: { status: 'running', startedAt: new Date() },
    })

    try {
      // Step 2: Execute agent steps
      const result = await executeSteps(job.steps)

      // Step 3: Commit result
      await tx.agentJob.update({
        where: { id: job.id },
        data: { status: 'completed', result, completedAt: new Date() },
      })

      return result
    } catch (err) {
      // Step 4: Rollback on failure — transaction auto-rolls back
      // but log the error for observability
      await tx.agentJob.update({
        where: { id: job.id },
        data: { status: 'failed', error: String(err) },
      })
      throw err
    }
  })
}
```
