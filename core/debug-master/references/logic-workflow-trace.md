# Phase 2 — Logic & Workflow Trace

Entry point, long-workflow decomposition, AI agent/LLM workflow debugging, and branch-logic audits — for wrong output with no crash.

## PHASE 2 — Logic & Workflow Trace

Run this phase for: wrong output, silent failures, incorrect state, off-by-one errors, race conditions, agent loops, broken pipelines, and any "it runs but does the wrong thing" scenario.

### 2-A Locate the Entry Point

Identify where execution begins and trace forward:

```
1. Find main() / __main__ / handler / run() / start()
2. Mark the FIRST observable deviation from expected behavior
3. Everything before that point is TRUSTED; focus after it
```

Ask (or infer from context):

- What is the **first output** the user actually sees?
- At what **step** does it diverge from expectation?
- What **data shape** enters the buggy function?

### 2-B Long Workflow Decomposition

For workflows with 5+ steps, pipelines, DAGs, or agent chains:

```
Step  │ Name             │ Input Shape      │ Output Shape     │ Status
──────┼──────────────────┼──────────────────┼──────────────────┼────────
  1   │ load_data()      │ path: str        │ df: DataFrame    │  ✓ OK
  2   │ preprocess()     │ df: DataFrame    │ df: DataFrame    │  ✓ OK
  3   │ split_chunks()   │ df: DataFrame    │ chunks: list     │  ? UNK
  4   │ embed()          │ chunks: list     │ vectors: ndarray │  ✗ FAIL ← bug here
  5   │ index_store()    │ vectors: ndarray │ index: FAISS     │  – SKIP
```

**Rules for tracing long chains:**

- Add a `print(f"[STEP N] type={type(x)}, shape={getattr(x,'shape',len(x))}")` after each step
- Never assume a step succeeded without logging its output type and size
- For async workflows: log timestamps; a 0ms step likely short-circuited
- For agent loops: log every tool call and its return value

**State mutation audit** (for OOP or stateful pipelines):

```python
# Snapshot state before and after each method call
import copy

state_before = copy.deepcopy(obj.__dict__)
obj.some_method()
state_after = obj.__dict__

diff = {k: (state_before.get(k), state_after.get(k))
        for k in set(state_before) | set(state_after)
        if state_before.get(k) != state_after.get(k)}
print("State mutations:", diff)
```

### 2-C AI Agent / LLM Workflow Debugging

For LangChain, LangGraph, AutoGen, CrewAI, custom agent loops:

```
Agent Debug Checklist:
┌─────────────────────────────────────────────────────────────┐
│ PROMPT LAYER                                                │
│  □ Is the system prompt reaching the model unchanged?      │
│  □ Is context window being exceeded? (count tokens)        │
│  □ Is the model receiving the right tool definitions?      │
│                                                             │
│ TOOL / FUNCTION LAYER                                       │
│  □ Does tool schema match the actual function signature?   │
│  □ Is the tool returning the expected type/format?         │
│  □ Are tool errors being caught and re-fed to the model?   │
│                                                             │
│ STATE / MEMORY LAYER                                        │
│  □ Is conversation history being truncated too early?      │
│  □ Is memory being written/read from the right key/index?  │
│  □ Is shared state thread-safe (for parallel agents)?      │
│                                                             │
│ LOOP / ORCHESTRATION LAYER                                  │
│  □ Is the termination condition ever True?                  │
│  □ Is the router sending to the right node/agent?          │
│  □ Are intermediate steps being logged?                    │
└─────────────────────────────────────────────────────────────┘
```

**Minimal agent trace shim (LangChain):**

```python
from langchain.callbacks.base import BaseCallbackHandler

class DebugCallback(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kw):
        print(f"\n[LLM START] tokens≈{sum(len(p)//4 for p in prompts)}")
        print(f"  Prompt preview: {prompts[0][:200]}...")

    def on_tool_start(self, serialized, input_str, **kw):
        print(f"\n[TOOL] {serialized['name']} ← {input_str[:100]}")

    def on_tool_end(self, output, **kw):
        print(f"[TOOL] → {str(output)[:200]}")

    def on_llm_error(self, error, **kw):
        print(f"[LLM ERROR] {error}")
```

### 2-D Conditional & Branch Logic Audit

For bugs that appear "sometimes" or "only with certain inputs":

```python
# Instrument every branch
def debug_branch(condition_name: str, value: bool, context: dict = None):
    print(f"[BRANCH] {condition_name} = {value}  context={context}")
    return value

# Usage:
if debug_branch("user_is_admin", user.role == "admin", {"user_id": user.id}):
    ...
elif debug_branch("user_is_editor", user.role == "editor"):
    ...
else:
    debug_branch("fallback", True)
```

For SQL / data pipelines — check NULLs, empty sets, type coercion:

```sql
-- Before the query that fails:
SELECT COUNT(*), COUNT(column_name), COUNT(DISTINCT column_name)
FROM   table_name
WHERE  your_filter_condition;
-- If COUNT(*) >> COUNT(column_name): NULLs are causing the bug
```
