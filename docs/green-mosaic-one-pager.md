# Green Mosaic

**Team Team TBD** · Entropy Alignment Security Hackathon, Berlin, 14 Nov 2026 · Track: Open

## Finding

A hospital assistant's output filter checks one answer at a time, so an ordinary conversation walks the patient table out while every answer stays clean; yes/no questions even read fields the filter never sees. On Riley on the organizers' range the server-side output filter refuses a direct request for records but
behaves like a pattern redactor (an SSN shape, a fixed token list). Two routes walk records past it, each answer
approved: the agent runs the **caller's SQL verbatim** (30/30 fresh chats [89-100]), and a record
returned as **JSON, CSV or a table** passes intact — no encoding trick.

**Impact.** A census: all **450 / 450** patients' records read through a real database call, every answer
filter-clean; **351 / 450 (78%)** reproduced across two or more independent
replies. Per conversation the attack succeeds in **65% [50-78]** (N=43, Wilson 95%). No tool sends
the record out — the reply itself is the channel. Severity L5: regulated patient data disclosed at the scale of the whole table.

**Novelty.** Even Llama Guard-4's privacy classifier lets 28 of 32 leaking conversations out: a single benign-pretext structured answer carries a whole table of records past a filter that checks one answer at a time. We did not find this measured against a deployed healthcare assistant's output DLP as of 14 Nov 2026; our contribution is that measurement plus a deterministic provenance value-matching fix, with its measured false-positive cost.

**Honest nulls.** A dedicated inference-oracle cell, reported in full, is refused (0 of 7); no L6 credential landed
(the credential columns are refused). We report both.

## Evidence

Real-record leak per conversation, same harness (the 65% headline by model): Qwen3-30B
89% [57-98] (N=9), DeepSeek-V4-Pro 59% [42-74]
(N=34); Claude pending the organizer token. A record counts only when its value came from a real
`query_db` read and was confirmed against ground truth; invented records (a separate data-integrity failure) are
excluded.

## Fix

Two deterministic layers: a fixed menu of lookups instead of free SQL, and an output check that blocks any identifier-grade value the agent read via query_db from reaching the reply in any parsed form, with a session disclosure budget and a field-predicate rule as defense in depth. No model call. **Layer 1, provenance output DLP:** against an independent ground-truth label it lets
**0% [0-11]** of 32 leak-conversations through, at **23% [15-34] hard held-out (9% [4-17] everyday)** benign queries
blocked. **Layer 2, query guard:** 19/19 SQL attack strings rejected, 6/6 legitimate
served, so the oracle has nothing to ask with. Full-field, identical sets, in-sample (per leaking conversation): ours lets 0/32 through [0-11]; Llama Guard-4 S7 28/32 (88% [72-95], public numbers excluded); Prompt Guard 2 32/32 (Fisher p=6e-14). Benign price on the same 77 hard replies: ours 23% [15-34], Llama Guard 0% [0-5]; 387 us vs 525 ms. A trade-off — for patient records the leak is the expensive error, so we default to the complete rule; FPs are v3. Guard rows our re-run.

## Why it matters

Per-message filters are what regulated assistants deploy today; every answer here passes them.
Minimum-necessary (HIPAA) and data minimisation (GDPR Art. 5(1)(c)) are about the total disclosed, not per message. Today every log line says allowed; the fix writes one signed decision record per answer, revokes a conversation that passes the per-record budget, and leaves the policy to the assistant's security owner (from the data classification they already keep). Session DLP: a gateway in front of assistants. Buyer: their security owner. Policy from your data classification; no model call.

## Limitations and reproduce

One fictional hospital assistant, black-box over HTTP. Model ladder: two open models; Claude pending the organizer token. Fix measured against independent ground-truth labels, not deployed on the organizers' server; benign false positives on a hard held-out set are 23% [15-34] (9% [4-17] on everyday questions): a real cost we show, not bury. Repo https://github.com/B0yko/green-mosaic; finding cards carry the `turn_id`s; frozen snapshot
gt-20261114T143309:5c298f83ebaf (Level 2, 9 runs, 1,224 episodes, span 12:26-14:18). Attacker and judge models and full statistics: methodology.md.
Shared with the organizers with this submission; the hospital, the range and every record are synthetic.
