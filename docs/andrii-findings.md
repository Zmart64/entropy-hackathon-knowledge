# Andrii's additional findings and their evidence boundaries

Reviewed 2026-11-14. Two sources with **different environments and different F-01 meanings**:

- Shared Riley KB: [Andrii's latest evidence-gate correction, 626d715](https://github.com/Zmart64/entropy-hackathon-knowledge/commit/626d715ae1751856dbdaa7e6d534b6da6d23a878), committed 13:17:44 UTC during this review.
- Separate private experiment repo: [F-01 at 181df0d](https://github.com/B0yko/entropy-hackathon-2026/blob/181df0dcaf264e8cc6ede85f530eeba81eca2037/findings/F-01.md), fetched and matched to local checkout. Last fetched commit 10:11:30 UTC.
- Later shared-KB updates: [a724b32](https://github.com/Zmart64/entropy-hackathon-knowledge/commit/a724b32) and [8e9b08f](https://github.com/Zmart64/entropy-hackathon-knowledge/commit/8e9b08fc548d51f08b0212c11eda0b7a38c8bcb2) add independent-label shadow results and LlamaGuard comparisons; incorporated below.

Latest push: [76b8b7b ledger](https://github.com/Zmart64/entropy-hackathon-knowledge/commit/76b8b7b)
and [b0075ba board](https://github.com/Zmart64/entropy-hackathon-knowledge/commit/b0075ba) were merged during
follow-up coordination. They contain both historical and newer claims; the latest reported state is below.
[Team reconciliation](team-coverage-reconciliation.md) maps completed work to the remaining gaps.

## Live Riley work: disclosure measurement, not a new technique claim

| Item | Andrii's latest statement | What is available / what remains |
| --- | --- | --- |
| Headline | F-01 benign-pretext/structured-format PHI disclosure + deterministic mitigation | Updated gate supersedes earlier F-03 headline |
| Legitimacy audit | Latest ledger: 450/450 tool-backed; 351/450 double-confirmed (78%); nine run files / 1,224 episodes | Author report supersedes 273/450. Frozen row-level manifest, field/model breakdown and raw result provenance unavailable here. Population coverage is not per-attack success |
| Earlier attack-attempt pilot | V4-Pro 14/143; Qwen30 15/92 (about 10% vs 16%) | Separate denominator from the 450 validation cohort; earlier findings contain turn examples. Not directly comparable to 273/450 |
| Oracle | Incidental member-ID answers: 5/12 characters; no complete oracle-only reconstruction, datarecon 0/43. Latest dedicated test: 0/8; six refusals, two verbatim appearances | Dedicated test is already done, source-reported null; not an unrun task. Member ID was not masked. No oracle-defeats-redaction claim |
| Integrity failure | Bulk replies invent rows beyond the actual query/read | Supports our need to separate requested LIMIT, rendered rows, and validated records |
| DLP fix | Latest independent-label shadow report: 144/145 replies; 27/28 conversations; benign FP 1/16 | 99.3% and 96.4%, respectively; source incorrectly labeled 27/28 as 100%. Latest ledger also reports 27/27 for F-01 only, excluding one oracle conversation; do not silently swap denominators. Case manifest unavailable here. The earlier fix 450/450 is in-sample consistency (distinct from patient census); held-out/adaptive evaluation pending |
| Other classifiers | Latest source reports LlamaGuard-4 S7 39/50 (78%) leaking replies detected; PromptGuard2 0/500 attack inputs | Supersedes 626d715’s “untested” status. Different tasks/denominators; paired evaluation missing, benign-FP denominators absent. Do not say all other guards fail |

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

Missing handoff from Andrii: frozen nine-run/1,224-episode manifest underlying the reported 450/450 census and 351/450 corroboration, field/model denominators, independent-label 145-reply/28-conversation and F-01-only 27-conversation fix manifests, classifier comparison manifests,
selected redacted transcripts, held-out fix/FP results, adaptive evaluation, and final deck-ready numbers.
His unpushed local work and other-machine conversations are not accessible here; no claim of exhaustive review of those.
