# Python — Topic Map

Reference for [cs-course-designer](../SKILL.md), Step 1. Covers syntax through OOP, error handling, common libraries, and testing/debugging.

**State the Python version.** Default to current stable Python 3.x unless the request names one. Version matters for: f-strings (3.6+), dataclasses (3.7+), the walrus operator (3.8+), dict ordering guarantees (3.7+), `match` statements (3.10+), and built-in generic types like `list[int]` (3.9+). Writing 3.12 examples for a cohort on 3.8 wastes everyone's time.

For language-agnostic fundamentals and data structures, see [computer-science](computer-science.md) — when a course covers both, teach each concept once, where it is first needed.

---

## Topic coverage

| Unit | Topics | Depends on |
| --- | --- | --- |
| 1. Setup & tooling | Interpreter vs. script; REPL; virtual environments; `pip`; editor setup; running from the terminal | — |
| 2. Values & types | `int`, `float`, `str`, `bool`, `None`; dynamic typing; `type()`; conversion; integer vs. float division | 1 |
| 3. Operators & expressions | Arithmetic, comparison, logical; precedence; truthiness of empty values; chained comparison | 2 |
| 4. Control flow | `if`/`elif`/`else`; `while`; `for` over iterables; `range`; `break`/`continue`/`else` on loops | 3 |
| 5. Strings | Immutability; indexing and slicing; methods; f-strings; `split`/`join`; encoding awareness | 2 |
| 6. Lists & tuples | Creation, indexing, slicing, mutation; list methods; tuple immutability and unpacking; nesting | 4 |
| 7. Dicts & sets | Key–value access; `get` vs. `[]`; iteration; set operations; hashability; choosing by access pattern | 6 |
| 8. Comprehensions | List/dict/set comprehensions; conditional comprehensions; when a loop is clearer | 6, 7 |
| 9. Functions | `def`, parameters, defaults, `*args`/`**kwargs`; return values; scope and `global`/`nonlocal`; docstrings | 4 |
| 10. Modules & packages | `import` forms; the standard library; `if __name__ == "__main__"`; project layout | 9 |
| 11. Files & data formats | `open` and context managers; text vs. binary; `csv`, `json`; `pathlib` | 5, 10 |
| 12. Errors & exceptions | Reading a traceback; `try`/`except`/`else`/`finally`; catching specific exceptions; `raise`; custom exceptions; EAFP vs. LBYL | 9 |
| 13. Iterators & generators | The iterator protocol; `yield`; laziness; `enumerate`/`zip`/`sorted` with `key` | 8 |
| 14. OOP | `class`, `__init__`, `self`; instance vs. class attributes; methods; `__repr__`/`__str__`; inheritance; composition; `@property`; dataclasses | 9 |
| 15. Testing | `assert`; `unittest` or `pytest`; arrange–act–assert; edge cases; fixtures; test-first practice | 9, 12 |
| 16. Debugging | Tracebacks; `print` vs. `logging`; `pdb`/IDE debugger; bisection; minimal reproduction | 12 |
| 17. Idioms & style | PEP 8; naming; truthiness idioms; unpacking; `with`; type hints; avoiding mutable defaults | 14 |
| 18. Common libraries (as scoped) | `datetime`, `collections`, `itertools`, `re`, `requests`; and per audience: `pandas`/`numpy`, `flask`/`fastapi` | 10 |

---

## One reasonable sequencing

**12-week intro course:** 1–3 (wk 1) → 4 (wk 2) → 5 (wk 3) → 6 (wk 4) → 7 (wk 5) → *checkpoint* → 9 (wk 6) → 12 + 16 (wk 7) → 10–11 (wk 8) → 8 + 13 (wk 9) → 14 (wk 10–11) → 15 + project (wk 12)

**Hard dependency edges:**

```
types → operators → control flow → functions
lists → dicts → comprehensions
functions → scope → exceptions → debugging
functions → classes            (classes before functions is incoherent)
exceptions → testing edge cases
```

**Sequencing decisions worth making explicitly:**

- **Comprehensions early or late.** Early risks students using them as magic incantations without understanding the loop underneath. Teaching the loop first, then the comprehension as a compression of it, is more durable.
- **OOP depth.** An intro course usually needs classes as *records with behavior*; inheritance hierarchies and metaclasses are a different course. Say which you're doing.
- **Type hints.** Increasingly expected in professional contexts and cheap to introduce at the function unit. For high-school audiences they are often noise. Decide by audience.
- **Testing early or late.** Late is traditional and usually means it doesn't stick. Introducing `assert` at the functions unit and a framework later works well.

---

## Common misconceptions

### Types and values
- **`/` performs integer division** (a Python 2 holdover, and an intuition from other languages). `/` is float division; `//` is floor division.
- **`input()` returns a number.** It always returns a string; the missing `int()` is the classic first-week defect.
- **Float equality works.** `0.1 + 0.2 == 0.3` is `False`. Worth showing once, early, memorably.
- **`is` and `==` are the same.** They coincide for small integers and interned strings, which is exactly what makes the misconception survive — it works until it doesn't.
- **`None` is falsy therefore `None` equals `False`.**

### Mutability and aliasing
- **`b = a` copies the list.** It binds a second name to the same object. The most persistent misconception in the language.
- **Passing a list to a function copies it.** Mutations inside are visible to the caller. Students describe Python as "pass by value" or "pass by reference"; neither is right, and the useful framing is that the *reference* is passed by value.
- **Slicing a nested list deep-copies it.** `a[:]` is shallow; inner lists are still shared.
- **Mutable default arguments are re-created per call.** `def f(x, acc=[])` shares one list across all calls. Excellent Analyze-level item: the code looks obviously correct.
- **Modifying a list while iterating over it works.** Elements get skipped; the symptom appears elsewhere.

### Functions and scope
- **`print` and `return` are the same.** The deepest damage in the whole unit — students who conflate them cannot compose functions, and every later topic suffers.
- **Assigning to a name inside a function modifies the global.** It creates a local, and reading it before assignment raises `UnboundLocalError` — an error message that reads as nonsense without the scope model.
- **A function with no `return` returns nothing.** It returns `None`, which then propagates into confusing downstream errors.
- **Argument order doesn't matter** because keyword arguments exist.

### Dicts, sets, strings
- **`d[k]` on a missing key returns `None`.** It raises `KeyError`; `d.get(k)` returns `None`.
- **Dicts are unordered.** True before 3.7, guaranteed insertion-ordered since. Version-dependent — state it.
- **Sets preserve order.** They do not.
- **String methods mutate the string.** `s.upper()` returns a new string; `s.upper()` alone as a statement does nothing.
- **`+=` on a string in a loop is efficient.** Quadratic; `"".join(parts)` is the idiom.

### Exceptions
- **`except:` bare is a good safety net.** It swallows `KeyboardInterrupt` and `SystemExit`, and hides real defects.
- **Exceptions are for all errors.** No distinction between a recoverable condition and a bug that should crash loudly.
- **`try` blocks are expensive**, so avoid them — the EAFP idiom is idiomatic Python and cheap on the success path.
- **`finally` runs only on success**, or only on failure.
- **Catching an exception fixes the problem.** Catching and passing is how a defect becomes untraceable.

### Comprehensions and iteration
- **A comprehension is always better than a loop.** Nested triple comprehensions are strictly worse than the loop.
- **A generator can be iterated twice.** It is exhausted after the first pass — and the second pass silently yields nothing, which reads as a data bug.
- **`range(1, 5)` includes 5.**
- **`enumerate` returns just the index.**

### OOP
- **`self` is a keyword** the caller passes explicitly.
- **Class attributes are per-instance.** A mutable class attribute is shared across all instances — the same shape of bug as the mutable default.
- **`__init__` is a constructor** that returns the object.
- **Inheritance is the tool for code reuse.** Composition is usually the better answer; teaching inheritance first tends to produce deep, brittle hierarchies.
- **A leading underscore enforces privacy.** It is a convention.

### Testing and debugging
- **Tests are written after the code works.** Then they only cover the happy path the author already checked.
- **A passing test means correct code.** No sense of coverage or of untested edge cases.
- **Tracebacks are read top-down.** The last frame is usually the interesting one; the top is where it started.
- **Debugging is adding prints until it works.** Not a bisection strategy, and not a hypothesis test.

---

## Where formative checks pay most

- After **functions** — a `print` vs. `return` composition item.
- After **lists** — an aliasing prediction item.
- After **scope** — an `UnboundLocalError` diagnosis item.
- After **exceptions** — which of these should be caught, and which should crash.

---

## Related

- [computer-science](computer-science.md) — language-agnostic fundamentals and data structures
- [clo-writing](clo-writing.md) · [assessment-design](assessment-design.md)
