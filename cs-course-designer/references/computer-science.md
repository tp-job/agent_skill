# General Computer Science — Topic Map

Reference for [cs-course-designer](../SKILL.md), Step 1. Covers CS1/CS2 fundamentals, algorithms, and data structures.

The sequencing below is **a** defensible order, not **the** order. Institutions reasonably disagree — objects-first vs. objects-later, spiral vs. linear. If the user's request implies a different philosophy or a specific textbook order, follow that instead.

---

## Topic coverage

### CS1 — Programming fundamentals

| Unit | Topics | Depends on |
| --- | --- | --- |
| 1. Computation & values | What a program is; variables, types, assignment; expressions and operator precedence; input/output | — |
| 2. Selection | Boolean expressions, comparison, logical operators; `if`/`else`/chained conditions; truthiness | 1 |
| 3. Iteration | Definite loops (`for`), indefinite loops (`while`); accumulator pattern; loop boundaries; nesting | 2 |
| 4. Functions | Definition and call; parameters and arguments; return values; scope and lifetime; the call stack | 3 |
| 5. Collections | Sequences/lists (index, slice, iterate); dictionaries/maps; sets; choosing by access pattern | 3 |
| 6. Strings & text | Immutability, indexing, common operations, formatting, parsing | 5 |
| 7. Files & I/O | Reading and writing; the resource lifecycle; simple formats (CSV, lines) | 5 |
| 8. Errors & debugging | Reading tracebacks; syntax vs. runtime vs. logic errors; systematic bisection; print/logging/debugger | 4 |
| 9. Recursion | Base case and recursive case; the stack during recursion; recursion vs. iteration | 4 |
| 10. Program design | Decomposition; naming; single responsibility; when to extract a function | 4 |

### CS2 — Data structures & algorithms

| Unit | Topics | Depends on |
| --- | --- | --- |
| 11. Complexity | Growth rates; Big-O; counting operations; best/average/worst case; space vs. time | CS1 3, 9 |
| 12. Arrays & dynamic arrays | Contiguous memory; O(1) index, O(n) insert; amortized growth | 11 |
| 13. Linked structures | Singly/doubly linked lists; node-and-pointer thinking; trade-offs vs. arrays | 12 |
| 14. Stacks & queues | LIFO/FIFO; array vs. linked implementations; applications (call stack, BFS, undo) | 13 |
| 15. Searching | Linear vs. binary search; the sorted precondition; O(log n) intuition | 11 |
| 16. Sorting | Selection/insertion/bubble (as teaching devices); merge sort; quicksort; stability; when the library sort is right | 11, 15 |
| 17. Trees | Terminology; binary trees; BST insert/search/delete; traversals; balance and its absence | 13, 9 |
| 18. Hash tables | Hashing, buckets, collisions, load factor; why average O(1) and worst O(n) | 12 |
| 19. Graphs | Representations (adjacency list/matrix); BFS and DFS; shortest path intuition | 14, 17 |
| 20. Algorithm strategies | Brute force, divide and conquer, greedy, dynamic programming (intro) | 16, 11 |
| 21. OOP (if in scope) | Classes and objects; encapsulation; inheritance and composition; polymorphism | CS1 10 |

---

## One reasonable sequencing

**CS1 (14 weeks):** 1–2 (wk 1–2) → 3 (wk 3–4) → 4 (wk 5–6) → *checkpoint* → 5 (wk 7–8) → 6–7 (wk 9) → 8 (wk 10, woven throughout) → 9 (wk 11–12) → 10 + project (wk 13–14)

**CS2 (14 weeks):** 11 (wk 1) → 12–13 (wk 2–3) → 14 (wk 4) → *checkpoint* → 15–16 (wk 5–7) → 17 (wk 8–9) → 18 (wk 10) → 19 (wk 11–12) → 20 (wk 13) → project (wk 14)

**Hard dependency edges** — violating these reliably produces a stuck cohort:

```
variables → conditions → loops → functions → recursion
functions → scope → the call stack → recursion
loops → collections → iteration over collections
arrays → linked lists → trees → graphs
complexity → any discussion of "which is better"
```

**Sequencing decisions worth making explicitly:**

- **Objects-first vs. objects-later.** Objects-first front-loads abstraction and suits students who will go on to large systems; objects-later gets students writing working code faster. Neither is wrong; pick and state it.
- **Recursion early or late.** Early (right after functions) makes it feel natural; late risks students cementing iterative-only thinking. But early recursion requires the call stack to be solid first.
- **Debugging as a unit or woven in.** Woven in is more realistic; a dedicated unit ensures it actually gets taught. Doing neither is the common failure.

---

## Common misconceptions

These are what students predictably get wrong. Anticipating them live is what separates a lesson plan from a slide deck — and each makes an excellent MCQ distractor or debugging item.

### Variables and assignment
- **Assignment reads as algebra.** `x = x + 1` is read as an equation to be solved rather than an instruction executed in order. Students conclude it is impossible.
- **A variable holds an expression, not a value.** After `b = a`, students expect `b` to change when `a` changes. Reinforced by spreadsheet experience.
- **Type is a property of the name.** Expecting a variable that once held an integer to reject a string.

### Conditionals
- `if x == 1 or 2` — reads naturally in English, is always true in most languages. Extremely persistent.
- **Chained conditions are independent.** Believing every `elif` branch is tested, rather than the first match winning.
- **Confusing `=` with `==`.** Less common with modern error messages but still present in C-family languages.

### Loops
- **Off-by-one.** `range(1, n)` vs. `range(n)`; `<` vs. `<=`. The single most common defect in student code.
- **The loop variable persists meaningfully after the loop.** Or conversely, surprise that it does.
- **Modifying a collection while iterating over it.** Produces skipped elements; the symptom looks like a logic error elsewhere.
- **Nested loop counting.** Believing an inner loop runs its full range once total rather than once per outer iteration.

### Functions
- **Parameters and arguments are the same thing** — confusion about which name is visible where.
- **A function without an explicit `return` returns nothing useful** — students write the computation, forget to return it, then use the `None`.
- **`print` and `return` are the same.** The deepest and most damaging function misconception: students who conflate them cannot compose functions at all.
- **Scope leakage.** Expecting a local variable to be visible outside, or expecting a global assignment inside a function to work without declaration.

### Collections
- **Aliasing vs. copying.** Two names bound to one list; mutating through one and being surprised by the other. Persists well past CS1.
- **Index vs. element** in a loop — using the index where the element was meant.
- **Dictionaries are ordered / unordered** — assumptions vary by language and version. State the version.

### Recursion
- **No base case, or an unreachable one.** The recursive case is written first and the base case bolted on.
- **Believing the recursive call "goes and comes back" without state.** Not seeing that each frame has its own locals.
- **Expecting the function to somehow know its own results** — mistrust of the recursive call, leading students to try to "help" it with globals.
- **Confusing what happens before the recursive call with what happens after.** The root of every reversed-output bug.

### Complexity
- **Big-O measures runtime in seconds.** Expecting an O(n log n) algorithm to always beat O(n²) on any input, including n=5.
- **Counting lines instead of operations** — treating a loop body as O(1) regardless of what it calls.
- **Dropping the wrong term**, or keeping constants: "O(2n)".
- **Best case is the useful case.** Reaching for best-case complexity when comparing algorithms.

### Data structures
- **Linked lists are faster than arrays.** Repeated as a rule without the "for insertion at a known position" qualifier — and without cache-locality reality.
- **Binary search works on any list.** Forgetting the sorted precondition.
- **Hash tables are always O(1).** Not connecting the average case to load factor and collision handling.
- **A BST stays balanced by itself.** Not seeing that sorted insertion produces a linked list with extra steps.
- **Traversal orders are interchangeable.** Not connecting in-order to the sorted property of a BST.

---

## Where formative checks pay most

- After **functions**, before recursion — check `print` vs. `return` explicitly.
- After **loops**, before collections — a trace item with a boundary condition.
- After **complexity**, before any sorting comparison — ask them to justify, not recall.
- After **pointers/references** in whatever form the language has them — before linked structures.

---

## Related

- [clo-writing](clo-writing.md) · [assessment-design](assessment-design.md)
- [python](python.md) · [c-programming](c-programming.md) — language-specific detail
