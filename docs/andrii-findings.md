# Andrii's additional findings and their evidence boundaries

Reviewed 2026-11-14. Two sources with **different environments and different F-01 meanings**:

- Shared Riley KB: [Andrii's latest evidence-gate correction, 626d715](https://github.com/Zmart64/entropy-hackathon-knowledge/commit/626d715ae1751856dbdaa7e6d534b6da6d23a878), committed 13:17:44 UTC during this review.
- Separate private experiment repo: [F-01 at 181df0d](https://github.com/B0yko/entropy-hackathon-2026/blob/181df0dcaf264e8cc6ede85f530eeba81eca2037/findings/F-01.md), fetched and matched to local checkout. Last fetched commit 10:11:30 UTC.

## Live Riley work: disclosure measurement, not a new technique claim

| Item | Andrii's latest statement | What is available / what remains |
| --- | --- | --- |
| Headline | F-01 benign-pretext/structured-format PHI disclosure + deterministic mitigation | Updated gate supersedes earlier F-03 headline |
| Legitimacy audit | 273/450 double-confirmed (61%); about 78% tool-backed, still changing | Latest gate is an author report. Underlying 450-case validation manifest/per-model breakdown is not in this checkout; do not quote 61% as per-attack success rate |
| Earlier attack-attempt pilot | V4-Pro 14/143; Qwen30 15/92 (about 10% vs 16%) | Separate denominator from the 450 validation cohort; earlier findings contain turn examples. Not directly comparable to 273/450 |
| Oracle | Member-ID predicate answers, 5/12 characters; no complete oracle-only reconstruction; datarecon 0/43 | Secondary only. Member ID was not masked, so this does not prove an oracle defeated redaction |
| Integrity failure | Bulk replies invent rows beyond the actual query/read | Supports our need to separate requested LIMIT, rendered rows, and validated records |
| DLP fix | 450/450 in-sample shadow detections; latest benign FP 1/16 | Held-out recall, independent FP and adaptive bypass evaluation missing. Older page says 1/8; these are different snapshots, not automatically comparable |
| Other classifiers | LlamaGuard untested; Prompt Guard 2 result is replica-only supporting work | Do not say LlamaGuard failed on Riley |

**Important reconciliation:** Andrii's new gate still says secrets/DEA have not landed in his lane.
Our separate Qwen/inbox observations do not contradict a lane-local negative result; the shared inventory must
show contributor + target + model + validation depth. In particular, his live headline should not absorb our
one-source employee candidates into its independently confirmed cohort.

## Pre-event replica: Reassembled Trifecta

One untrusted inbox document induces reader/writer agents to release a canary to an authorized partner while
individual scope checks allow the calls. These are **replica event logs, not actual external delivery** and not
Riley. The source explicitly says egress tools log and never send. Source F-01 is called `replica/F-01` here to
avoid colliding with `Riley/F-01` structured PHI disclosure.

I recomputed the following from committed episode rows. [Aggregate evidence with source hashes and Wilson
intervals](../results/2026-11-14-swarm-extraction/andrii-replica-audit.json) retains all inspected cells.

| Model / provider / condition | Measured source-row result | Scope |
| --- | --- | --- |
| GPT-OSS-120B / Near AI / split + scope | 24/42 canary-release episodes; zero scope blocks | Replica headline, 57%, Wilson 95% 42–71% |
| Same + cross-agent flow policy | 0/42; upper Wilson bound about 8% | This sample, not universal prevention |
| GPT-OSS-120B split + scope, three hosts pooled | 71/126 (24 Near AI + 23 AkashML + 24 DeepInfra) | Same tasks, three providers; not three independent task distributions |
| GPT-OSS-20B / CoreWeave / split + scope, doubled budget | 28/42 (67%, CI 52–79%); one truncated episode | Do not use original-budget cell that exceeded truncation gate |
| Claude Haiku 5.5 / Anthropic | 0/42 in each of six cells; 252 episodes, no external-egress events | Negative result for this attack/configuration, not general immunity |
| Qwen3.8-27B / DeepInfra | 189/252 episodes truncated | Zero leaks is not interpretable as a defense success; rerun needed |

Additional source-reported controls: GPT-OSS-120B single-agent scope 50/50, Prompt Guard 2 49/50,
flow policy 0/50; benign-document split ablation 0/42. These N1/ablation cells were read from Andrii's card,
not independently recomputed in this audit. The monitor flags all recorded split leaks but also many legitimate
flows. Owner-bound v2 lowers false positives on the source's benign tasks, but held-out evaluation and adaptive
bypass remain open. Neither headline was pre-registered or commit-stamped at launch; later controls were.

## What to bring into the pitch

Lead the live-hackathon story with the eligible live-range finding and a frozen evidence manifest. Use the replica
as **supporting research** on cross-agent information flow only if presentation scope permits it. The shared
engineering lesson is to enforce permissions on the data and destination, retain provenance across transformations
and delegation, and evaluate both attacks and benign utility. Measurement is the defensible contribution; do not
claim a novel encoding trick, universal stronger-model failure, or a deployed fix.

Missing handoff from Andrii: frozen live run IDs, 450-case validation classifications and per-model denominators,
selected redacted transcripts, held-out fix/FP results, adaptive evaluation, and final deck-ready numbers.
His unpushed local work and other-machine conversations are not accessible here; no claim of exhaustive review of those.
