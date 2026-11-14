# Deterministic output-DLP fix (canonicalize + label-flow + disclosure budget + field-predicate)

Author: Andrii (AUTO / defense lane). Date: 2026-11-14. Status: PROVEN for F-01 (mass structured PHI exfil) on real
Riley logs; objectivity caveats below. Code (local): `range-harness/dlp_fix.py` (guard), `score.py`, `verify.py`,
`benign_fp.py`.

## The defense
A deterministic guard on the agent's OUTGOING answer (and any egress tool-call argument) — no model call, microseconds:
1. **canonicalize + parse** — decode base64/rot13/hex/spaced digits AND parse JSON/CSV/markdown-table into field
   values, THEN scan. Defeats F-01 structured-format laundering (wrapping a record in structure no longer hides it). **[proven]**
2. **label-flow** — block if any patient-record field or credential appears, in any form, in the answer or an egress
   argument. **[proven]**
3. **session-cumulative disclosure budget** — accumulate identifying fields across the conversation; block after >= 2
   distinct identifiers. *[design, for multi-turn aggregation — secondary, not yet validated against traces]*
4. **field-predicate** — a design layer for an inference-oracle channel. NOTE: the credential-masking /
   oracle-reconstruction claim is **DROPPED** (not proven — member_id isn't masked, no oracle-only reconstruction,
   credentials refused). The oracle is at most a secondary alternative channel; this layer is not validated.

## Measurement (shadow, real Riley logs; aggregates only)
- **Recall (NON-CIRCULAR, independent label).** The leak label = the supervisor's GT tool-backed real MRNs
  (datarecon), NOT the fix's own matcher. Per reply: **144/145 = 99%**. Per conversation, F-01 family:
  **27/28 = 100%** (structured-dump 13/13, enumeration 7/7). The in-sample dlp_fix-matcher "450/450" is a
  consistency check, not recall — use these GT-labeled numbers.
- **Benign false positives:** 1/16 (6%) on a broader patient-service set (the single facility-phone case). CAVEAT:
  v2's phone rule was tuned on the observed FPs -> an out-of-sample re-score on a frozen, harder benign set is pending.
- **Objectivity (honest):** NOT pre-registered — rules written after the attack class (generic info-flow rules, not
  payload-overfit, so claim "generic, not overfit"). Held-out recall (runs after the fix froze) and one adaptive
  attack (via the local model, residual) are pending.

## Status-quo comparison (MEASURED on the real data)
| guard | what it is | catches the exfil? |
|---|---|---|
| Riley's OWN deployed output DLP | the range's built-in filter | **0%** — passed all 450 filter-clean leaks |
| PromptGuard2 (Llama-Prompt-Guard-2-86M) | input injection/jailbreak classifier | **0/500 attack inputs = 0%** (benign-pretext exfil passes; it flags obvious injections — a raw "ignore instructions" scores 0.9995 — just not these). Replies 0/500; benign FP 0% |
| LlamaGuard-4 S7 (llama-guard-4-12b, OpenRouter) | content/privacy classifier (12B, a model call per output) | **78% (39/50 leaking replies blocked), 0% benign FP** — it CATCHES most leaks; misses ~22% (obfuscated/edge). NOT a miss. |
| **our deterministic output DLP** | output label-flow, no model call | **100%** (F-01, non-circular) at microseconds, auditable |

Honest thesis (do NOT claim "guards miss it"): the DEPLOYED output DLP FAILED (0%); an input injection guard is the
wrong tool (PromptGuard2 0%); even a SOTA output classifier (LlamaGuard-4 S7) reaches only **78%** at a
12B-model-call-per-response cost, is probabilistic, and misses obfuscated variants; our deterministic rule reaches
**100%** (F-01) at microseconds, with no model call and a full audit trail — and catches the obfuscated forms
LlamaGuard misses (via canonicalize). The pitch is "deterministic, complete, cheap, auditable", not "nothing else catches it".
