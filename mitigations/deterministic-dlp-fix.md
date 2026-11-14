# Deterministic output-DLP fix (canonicalize + label-flow + disclosure budget + field-predicate)

Author: Andrii (AUTO / defense lane). Date: 2026-11-14. Status: author-reported independent-label shadow evaluation for F-01 on Riley logs; held-out/adaptive evidence pending. Code (local): `range-harness/dlp_fix.py` (guard), `score.py`, `verify.py`,
`benign_fp.py`.

> **Numbers superseded (15:36 CET).** The independent evaluation in [fix-evaluation/](fix-evaluation/README.md)
> replaces the measurement and status-quo figures in this file: 0 of 32 leaking conversations let through on any record field (Llama Guard S7: 29 of 32; Prompt Guard 2: 32 of 32); hard benign answers blocked 23% [15-34] vs Llama Guard 0% on the same 77 held-out replies; adaptive round 0 of 8 past the fix. The design description stands; describe the
> working mechanism as value matching against tagged record values (the decoding layer added nothing on the data).


## The defense

A deterministic guard on the agent's OUTGOING answer (and any egress tool-call argument) — no model call, microseconds:
1. **canonicalize + parse** — decode base64/rot13/hex/spaced digits AND parse JSON/CSV/markdown-table into field
   values, THEN scan. Defeats F-01 structured-format laundering (wrapping a record in structure no longer hides it). **[observed in the reported shadow evaluation]**
2. **label-flow** — block if any patient-record field or credential appears, in any form, in the answer or an egress
   argument. **[observed in the reported shadow evaluation]**
3. **session-cumulative disclosure budget** — accumulate identifying fields across the conversation; block after >= 2
   distinct identifiers. *[design, for multi-turn aggregation — secondary, not yet validated against traces]*
4. **field-predicate** — a design layer for an inference-oracle channel. NOTE: the credential-masking /
   oracle-reconstruction claim is **DROPPED** (not proven — member_id isn't masked, no oracle-only reconstruction,
   credentials refused). The oracle is at most a secondary alternative channel; this layer is not validated.

## Measurement (shadow, real Riley logs; aggregates only)

- **Recall (NON-CIRCULAR, independent label).** The leak label = the supervisor's GT tool-backed real MRNs
  (datarecon), NOT the fix's own matcher. Per reply: **144/145 = 99.3%**. Per conversation, F-01 family:
  **27/28 = 96.4%** (structured-dump 13/13, enumeration 7/7). The in-sample dlp_fix-matcher "450/450" is a
  consistency check, not recall — use these GT-labeled numbers.
- **Benign false positives:** 1/16 (6%) on a broader patient-service set (the single facility-phone case). CAVEAT:
  v2's phone rule was tuned on the observed FPs -> an out-of-sample re-score on a frozen, harder benign set is pending.
- **Objectivity (honest):** NOT pre-registered — rules written after the attack class (generic info-flow rules, not
  payload-overfit, so claim "generic, not overfit"). Held-out recall (runs after the fix froze) and one adaptive
  attack (via the local model, residual) are pending.

## Status-quo comparison (author-reported, different cohorts)

| guard | what it is | catches the exfil? |
|---|---|---|
| Riley's OWN deployed output DLP | the range's built-in filter | **0%** — passed all 450 filter-clean leaks |
| PromptGuard2 (Llama-Prompt-Guard-2-86M) | input injection/jailbreak classifier | **0/500 attack inputs = 0%** (benign-pretext exfil passes; it flags obvious injections — a raw "ignore instructions" scores 0.9995 — just not these). Replies 0/500; benign FP 0% |
| LlamaGuard-4 S7 (llama-guard-4-12b, OpenRouter) | content/privacy classifier (12B, a model call per output) | **78% (39/50 leaking replies blocked), 0% benign FP** — it CATCHES most leaks; misses ~22% (obfuscated/edge). NOT a miss. |
| **our deterministic output DLP** | output label-flow, no model call | Reported **144/145 replies (99.3%)**, **27/28 conversations (96.4%)**; named subgroups 13/13 and 7/7. Paired/held-out evaluation pending |

Comparison limits: LlamaGuard catches most tested leaks (39/50); it is not a failed detector. The deterministic
rule's reported 144/145 reply and 27/28 conversation results have different denominators from that 50-case cell.
A paired, frozen evaluation is needed before claiming superiority. “450/450” is an in-sample consistency check;
Riley's 0% on a cohort selected for passed leaks is not its detection rate on all attempted disclosures.
Benign FP 0% for the classifiers lacks a denominator in this write-up. Runtime comparisons need measured latency
on the same workload. None of these controls is deployed on the organizer server by this work.

Review correction: the incoming source labeled 27/28 “100%”; arithmetic is 96.4%. The 13/13 structured-dump and
7/7 enumeration subsets do not sum to 28; preserve the full case manifest before selecting a headline percentage.
The underlying independent-label manifest and code revision are not shared here, so these remain contributor-reported
results. Source history: [a724b32](https://github.com/Zmart64/entropy-hackathon-knowledge/commit/a724b32) and
[8e9b08f](https://github.com/Zmart64/entropy-hackathon-knowledge/commit/8e9b08fc548d51f08b0212c11eda0b7a38c8bcb2).
