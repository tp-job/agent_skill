# Requirements: [Component/Feature Name]
**Date:** [YYYY-MM-DD]  **Mode:** REVERSE | FORWARD | GAP
**Stack layers:** [detected layers]  **DS Version:** [if found]

---

## Component Contract
[STEP 2A output]

## API Contract
[STEP 2B output — omit if L2/L3 not detected]

## DB Contract
[STEP 2C output — omit if L4 not detected]

## Requirements
[STEP 3 output — REQ-L1-001, REQ-L2-001, etc.]

## Non-Functional Requirements
[STEP 4 table]

## Risk Register
[STEP 5 output — only real risks]

## Sign-off Checklist

### Developer
- [ ] All REQ-* implemented and self-tested
- [ ] No TypeScript errors or eslint warnings
- [ ] useEffect cleanup verified (no memory leaks)
- [ ] DS tokens used throughout (no magic numbers)

### Designer (if applicable)
- [ ] Visual output matches Figma/spec
- [ ] DS version compliance confirmed
- [ ] Responsive behavior validated

### QA / Second Developer
- [ ] P0 and P1 acceptance criteria pass
- [ ] API error states tested
- [ ] Auth edge cases tested (if applicable)

---

## Assumptions & Inferences
[All [INFERRED] and [ASSUMED] items consolidated here]
[All [MISSING] items that human must fill in]
