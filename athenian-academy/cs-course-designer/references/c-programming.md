# C Programming — Topic Map

Reference for [cs-course-designer](../SKILL.md), Step 1. Covers pointers, memory management, structs, and low-level concepts.

**State the standard.** Default to **C11/C17** unless the request names another. It matters for: variable declarations in `for` loops (C99+), `//` comments (C99+), variable-length arrays (C99, optional since C11), `_Static_assert` and `<stdalign.h>` (C11), and `gets` (removed in C11). Also state the compiler and flags — students should be compiling with `-Wall -Wextra` from day one, because the warnings *are* the curriculum.

For language-agnostic fundamentals, see [computer-science](computer-science.md).

---

## Topic coverage

| Unit | Topics | Depends on |
| --- | --- | --- |
| 1. Toolchain | Source → preprocess → compile → assemble → link; `gcc`/`clang` invocation; `-Wall -Wextra -g`; `make` basics; reading compiler errors | — |
| 2. Program structure | `main` and its return; `#include`; statements and blocks; `printf` basics | 1 |
| 3. Types & variables | `int`, `char`, `float`, `double`; `signed`/`unsigned`; `short`/`long`; `sizeof`; implementation-defined sizes; integer overflow; implicit conversion | 2 |
| 4. Operators | Arithmetic, relational, logical, bitwise; precedence and associativity; compound assignment; increment/decrement; **sequence points** | 3 |
| 5. Control flow | `if`/`else`, `switch` (and fallthrough), `while`, `do-while`, `for`, `break`/`continue`, `goto` (and why not) | 4 |
| 6. Functions | Declaration vs. definition; prototypes and headers; pass-by-value; return types; recursion; `static` linkage | 5 |
| 7. The memory model | Address space layout: text, data, BSS, heap, stack; automatic vs. static vs. dynamic storage duration; lifetime and scope as distinct ideas | 6 |
| 8. Pointers | Address-of and dereference; pointer types and why they differ; `NULL`; pointers as parameters (output params); pointer to pointer | 7 |
| 9. Arrays | Declaration, indexing, no bounds checking; array–pointer relationship and decay; arrays as parameters; multidimensional arrays and layout | 8 |
| 10. Pointer arithmetic | Scaling by element size; pointer comparison; iterating with pointers; one-past-the-end | 9 |
| 11. Strings | `char` arrays and the NUL terminator; string literals and their immutability; `<string.h>`; `strlen` vs. `sizeof`; safe vs. unsafe functions | 9 |
| 12. Dynamic memory | `malloc`/`calloc`/`realloc`/`free`; checking for allocation failure; ownership; leaks, double free, use-after-free, dangling pointers | 10 |
| 13. Structs & unions | Definition, member access, `->`; nesting; passing and returning; `typedef`; padding and alignment; unions; enums | 8 |
| 14. Data structures in C | Linked lists, stacks, queues, trees built from structs and pointers; the malloc/free discipline for each | 12, 13 |
| 15. File I/O | `FILE*`, `fopen`/`fclose`, text vs. binary, `fread`/`fwrite`, `fgets`, error checking, EOF | 11 |
| 16. Preprocessor | `#define` object- and function-like macros; macro pitfalls; `#include` guards; conditional compilation | 6 |
| 17. Multi-file programs | Headers vs. sources; `extern`; `static` for internal linkage; the one-definition rule; `make` | 16, 6 |
| 18. Debugging & tooling | `gdb`; Valgrind or ASan/UBSan; interpreting a segfault; reading a core dump; the discipline of fixing warnings | 12, 1 |
| 19. Undefined behavior | What UB means; common instances; why "it worked on my machine" proves nothing | 12, 10 |

---

## One reasonable sequencing

**14-week course:** 1–2 (wk 1) → 3–4 (wk 2) → 5 (wk 3) → 6 (wk 4) → 7 (wk 5) → *checkpoint: the memory model must be solid* → 8 (wk 6–7) → 9–10 (wk 8) → 11 (wk 9) → 12 + 18 (wk 10–11) → 13 (wk 12) → 14 (wk 13) → 15–17 + project (wk 14)

**Hard dependency edges — the least forgiving of any subject in this skill:**

```
types & sizeof → memory model → pointers → pointer arithmetic → arrays/strings
pointers → dynamic memory → data structures
functions & pass-by-value → output parameters (which require pointers)
dynamic memory → debugging tools (Valgrind is meaningless before malloc)
```

**The memory model gate.** More than in any other language, students who do not have a concrete mental model of addresses and storage before pointers are introduced will not recover — every subsequent topic compounds the deficit, and by the linked-lists unit they are copying code they cannot reason about. Spend the extra session on unit 7, and use a formative check to gate it explicitly.

**Sequencing decisions worth making explicitly:**

- **Arrays before or after pointers.** Arrays-first is intuitive but sets up the "arrays are pointers" misconception. Pointers-first is harder initially but makes decay comprehensible rather than magical.
- **Strings early or with arrays.** C strings are just arrays with a convention; teaching them before the array/pointer relationship makes the convention seem arbitrary.
- **Tooling from day one, or later.** Introducing `-Wall -Wextra` and a sanitizer at week 1 costs one session and prevents a semester of undiagnosed memory errors. Strongly prefer day one.

---

## Common misconceptions

### Types and arithmetic
- **`int` is 32 bits.** Sizes are implementation-defined; only minimum ranges are guaranteed.
- **`char` is signed** (or unsigned) — it is implementation-defined, and this bites on comparisons.
- **Integer overflow wraps.** Signed overflow is *undefined behavior*, not wraparound. Unsigned wraps; signed does not.
- **`5 / 2` is `2.5`.** Integer division truncates; students expect their calculator.
- **Implicit conversions are harmless.** Integer promotion and the usual arithmetic conversions produce surprising signed/unsigned comparison results.
- **`sizeof` is a function.** It is an operator, evaluated at compile time.

### Pointers
- **A pointer is a special kind of integer.** Encourages arithmetic that ignores type scaling.
- **`*` means the same thing in a declaration and in an expression.** In `int *p` it declares; in `*p = 5` it dereferences. Genuinely confusing and worth naming explicitly.
- **An uninitialized pointer is NULL.** It holds garbage. Dereferencing it may crash — or, worse, may not.
- **`p = NULL` frees the memory.** It leaks it.
- **Passing a pointer copies what it points to.** The pointer is copied; the target is shared. This is precisely why output parameters work.
- **To modify a caller's pointer you pass the pointer.** You need a pointer-to-pointer. The classic broken `void alloc_it(int *p)` that leaks and changes nothing.

### Arrays and pointer arithmetic
- **Arrays and pointers are the same thing.** They are not: an array *decays* to a pointer in most expressions, but `sizeof` and `&` behave differently. This half-truth is repeated in many textbooks and causes real defects.
- **`sizeof(arr)` inside a function gives the array size.** The parameter is a pointer; it gives the pointer size. Silent, and produces wrong loop bounds.
- **`p + 1` advances one byte.** It advances one element.
- **Reading past the end returns an error.** There is no bounds checking; it returns whatever is there, and the program continues plausibly.
- **Indexing off the end "usually works."** It sometimes appears to, which is the entire problem — and the reason `-fsanitize=address` belongs in the course.

### Strings
- **`strlen` and `sizeof` are interchangeable.** `strlen` counts to the NUL; `sizeof` includes it (for arrays) or gives the pointer size.
- **A `char` array is a string.** Only if NUL-terminated. Forgetting the terminator is a top-three defect.
- **Allocating `strlen(s)` bytes for a copy.** Off by one, every time — the NUL needs room.
- **String literals are modifiable.** `char *s = "hi"; s[0] = 'H';` is undefined behavior; `char s[] = "hi"` is fine. A precise and testable distinction.
- **`strcpy`/`gets` are fine for coursework.** `gets` was removed in C11. Teach the bounded alternatives from the start rather than as a later "security" addendum.

### Dynamic memory
- **`malloc` initializes memory.** It does not; `calloc` does.
- **`malloc` cannot fail**, so the return value needs no check.
- **`free` sets the pointer to NULL.** It does not — the pointer is now dangling, and using it is undefined behavior.
- **Freeing twice is harmless.**
- **Memory is freed when the pointer goes out of scope.** Confusing automatic storage with heap allocation.
- **A leak doesn't matter because the program exits.** True for a short program, catastrophic for anything long-running — and the habit is what is being taught.
- **`realloc` always returns the same pointer**, so `p = realloc(p, n)` is safe — it leaks the original on failure.

### Structs
- **`.` and `->` are interchangeable.** `->` is for a pointer to struct.
- **`sizeof(struct)` equals the sum of its members.** Padding and alignment change it; member order changes it too.
- **Assigning a struct deep-copies it.** It is a shallow member-wise copy; pointer members are shared.
- **Comparing structs with `==` works.** It does not compile; comparison must be member-wise.

### Undefined behavior
- **UB means "the result is unpredictable but the rest of the program is fine."** The compiler may assume UB never happens and optimize accordingly, changing unrelated code.
- **"It works on my machine" means it is correct.** The most important thing to dislodge in the entire course.
- **A program that runs without crashing has no memory errors.** Valgrind or ASan output is the evidence; the absence of a crash is not.

---

## Where formative checks pay most

- After the **memory model**, before pointers — a stack-vs-heap-vs-static placement item. Gate on this.
- After **pointers** — a swap-via-pointer implementation.
- After **array decay** — predict `sizeof` inside vs. outside a function.
- After **malloc/free** — identify which of leak / double free / use-after-free a snippet exhibits.

Every code item should state the standard and be compiled with `-Wall -Wextra` — if the item's warnings reveal the answer, that is a feature.

---

## Related

- [computer-science](computer-science.md) — language-agnostic fundamentals and data structures
- [clo-writing](clo-writing.md) · [assessment-design](assessment-design.md)
