# Deterministic output-DLP fix (canonicalize + label-flow + disclosure budget + field-predicate)

Author: Andrii (AUTO / defense lane). Date: 2026-11-14. Status: v1 measured in shadow on the real Riley logs.
Code (local): `range-harness/dlp_fix.py` (guard), `score.py` (shadow recall), `benign_fp.py` (FP). Keys via `kc`.

## The defense
A deterministic guard on the agent's OUTGOING answer (and any egress tool-call argument), four layers — no model
call, decision in microseconds:
1. **canonicalize + parse** — decode base64 / rot13 / hex / spaced digits AND parse JSON / CSV / markdown-table into
   field values, THEN scan. Defeats F-01 structured-format laundering and transform-evasion (the filter can no
   longer be fooled by wrapping a record in structure).
2. **label-flow** — block if any patient-record field OR credential appears, in any form, in the answer or an egress
   argument.
3. **session-cumulative disclosure budget** — accumulate identifying fields disclosed across the whole conversation;
   block once a session has disclosed >= 2 distinct identifiers. Defeats cumulative-aggregation (F-03) and multi-turn
   reassembly that each-answer-passes-the-filter.
4. **field-predicate** — block a short / yes-no answer that reveals a specific protected field the user asked about.
   Targets the inference-oracle (F-03), where the secret is never emitted verbatim so a content filter is blind.

## Measurement (shadow, over the real logged Riley runs; aggregates only, no record text)
- **Recall on filter-clean leaks** (leaks the SERVER DLP already passed): **100%** — 69/69 DeepSeek-V4-Pro and
  163/163 Qwen3-30B flagged leaks blocked in shadow.
- **Benign false positives** (8 legitimate patient-service queries): **v1 = 2/8**, both facility-phone mis-flags (the
  pattern-level guard can't tell a hospital's main line from a patient's phone).
- **v2 (in progress):** scope `phone` to patient-record provenance (require co-occurrence with a patient identifier),
  which removes the facility-phone FP; then role/recipient-bound declassification (an authorized clinician may see
  their own patient). Re-measured FP to follow.

## For the measured campaign (hub's lane)
Use this guard as the fix row in the `ek` campaign (replica l1/l4 with seeded canaries) for N>=30/arm + Wilson CI,
with `promptguard2` / `llamaguard` as the status-quo input-classifier rows. The contrast: an input classifier scores
the request; this guard scores the OUTPUT post-hoc, so it blocks regardless of how benign the framing was.
