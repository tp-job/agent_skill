# Fuzzing

Fuzzing feeds generated input — random, mutated, or shaped by a schema — and watches for crashes, hangs, and broken invariants. Design techniques find the edge cases you can think of; fuzzing finds the ones you cannot.

It runs **inside** two levels, never as a step of its own: a fuzzer needs a target and a harness, which do not exist before the design step.

| Where | Kind | Target | Tool |
| --- | --- | --- | --- |
| Unit | property-based / coverage-guided | pure functions that parse, decode, transform, serialise | fast-check, Hypothesis, jqwik, `go test -fuzz`, cargo-fuzz, Atheris, Jazzer |
| System | schema-driven API fuzz | every endpoint in the OpenAPI or GraphQL schema | Schemathesis, RESTler |

## When it pays

| Fuzz | Skip or keep light |
| --- | --- |
| parsers, decoders, file formats | UI layout |
| anything taking untrusted input | pure CRUD with schema validation already fuzzed at the API |
| serialise/deserialise round trips | business rules better covered by a decision table |
| public APIs | code with no input surface |

## Write an invariant, not an example

A fuzz test asserts something true for **every** input.

| Invariant | Example |
| --- | --- |
| Never crashes | `parse(anyString)` returns a value or a typed error, never throws |
| Round trip | `decode(encode(x)) == x` |
| Idempotent | `normalise(normalise(x)) == normalise(x)` |
| Oracle | `fastSort(xs)` equals `referenceSort(xs)` |
| Bounds | `0 <= discount(order) <= order.total` |

```ts
// fast-check 4, Vitest
import fc from "fast-check";
test("price never negative, never above total", () => {
  fc.assert(fc.property(orderArb, (order) => {
    const d = discount(order);
    return d >= 0 && d <= order.total;
  }));
});
```

```python
# Hypothesis, pytest
from hypothesis import given, strategies as st
@given(st.binary())
def test_decode_never_crashes(data):
    try:
        decode(data)
    except DecodeError:
        pass  # typed error is allowed; anything else fails
```

```bash
# Schemathesis 3.x against a running API
schemathesis run http://localhost:8000/openapi.json --checks all --hypothesis-max-examples 500
```

## Time box and stop rule

| Context | Budget per target |
| --- | --- |
| Every CI run | property tests at default example count (100–500); coverage-guided 1–10 min |
| Before release | 1 h per high-risk target |
| Nightly | as long as the budget allows, corpus kept between runs |

Stop when the boxed time passes with no new crash and no new coverage. Report the number of executions and the time, not "fuzzed thoroughly".

## Corpus and regression

- Keep the corpus in the repository (or an artifact store) so each run starts where the last stopped.
- Every crash input is minimised (the fuzzer's shrink step), saved, and copied into a named unit test. That test runs on every commit, forever.
- A crash that reveals a missing rule combination also becomes a decision-table column.

## Do not

- Fuzz with no assertion but "no exception" when an invariant exists — you will miss wrong answers.
- Point an API fuzzer at production or at shared staging data. Use a disposable environment.
- Let a fuzz job run unbounded in CI; it will be disabled within a week.
