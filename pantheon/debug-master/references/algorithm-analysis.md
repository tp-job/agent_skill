# Phase 3 — Algorithm Analysis & Summary

Complexity, correctness audit, the summary block, and optimization recommendation — for slow or subtly wrong algorithms.

## PHASE 3 — Algorithm Analysis & Summary

Run this phase when the user shares a function, class, or module and asks why it's slow, incorrect, or hard to understand.

### 3-A Complexity Analysis

Analyze every loop, recursion, and nested call:

```
COMPLEXITY REPORT TEMPLATE
──────────────────────────
Function: <name>
Lines:    <N>

Time Complexity:
  Best case:    O(?)  ← when / why
  Average case: O(?)
  Worst case:   O(?)  ← when / why (focus here)

Space Complexity:
  O(?)  ← what grows: stack, heap, accumulator?

Dominant term: <the loop/call that drives complexity>
Hidden costs:
  • <e.g., dict lookup inside inner loop looks O(1) but worst-case O(n) with collision>
  • <e.g., string concatenation in loop: O(n²) due to immutability>
  • <e.g., list.index() inside loop: O(n²) total>
```

### 3-B Correctness Audit

Walk through the algorithm with **three canonical inputs**:

|Input Class|Example|Expected Output|Actual Output|Pass?|
|---|---|---|---|---|
|Happy path|normal input|expected|actual|✓/✗|
|Edge: empty / zero|`[]`, `0`, `""`|expected|actual|✓/✗|
|Edge: large / overflow|`10^9`, `sys.maxsize`|expected|actual|✓/✗|

Common algorithm bugs to check:

- **Off-by-one**: loop range `< n` vs `<= n`, index `i` vs `i+1`
- **Integer overflow**: use `//` for floor division, check `sys.maxsize`
- **Float precision**: never use `==` on floats; use `math.isclose()`
- **Mutable defaults**: `def fn(lst=[])` — classic Python footgun
- **Early return / break missing**: loop that should exit doesn't
- **Greedy vs optimal**: greedy choice not globally optimal
- **Base case missing**: recursion without a halt condition

### 3-C Algorithm Summary Block

After analysis, produce this concise block for the user:

```
╔══════════════════════════════════════════════════════════════╗
║  ALGORITHM SUMMARY: <function_name>                          ║
╠══════════════════════════════════════════════════════════════╣
║  Purpose:     <one sentence>                                 ║
║  Approach:    <paradigm: greedy / DP / BFS / divide&conquer> ║
║  Input:       <type, constraints>                            ║
║  Output:      <type>                                         ║
║  Time:        O(?)  — <why>                                  ║
║  Space:       O(?)  — <why>                                  ║
║  Correctness: ✓ / ✗ — <note any known bug>                  ║
║  Optimizable: YES/NO — <what and how>                        ║
╚══════════════════════════════════════════════════════════════╝
```

### 3-D Optimization Recommendation

Only suggest an optimization when it materially changes complexity:

```
Current:  O(n²)  — nested list search
Fix:      O(n)   — replace inner list with set() lookup
Tradeoff: +O(n) space; justified when n > ~1000

Current:  O(n log n)  — sort then binary search, called k times
Fix:      O(n + k)    — precompute sorted index once, reuse
Tradeoff: minimal; always do this if k > 1
```
