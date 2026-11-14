# Green Mosaic results snapshot

Imported on 14 November 2026 from [B0yko/green-mosaic, revision 7ed2ded](https://github.com/B0yko/green-mosaic/tree/7ed2ded738e423bdc37cfa704084173f996b8c8e/results).
The source results directory was compared with this knowledge repository at `8a2ce04bdbe2bac85ae2d6da48a9bf1f7212fc06`.

**Previously included in part.** Both run write-ups and much of the narrative and fix-evaluation evidence were already here. The two structured JSON files were missing; they are now copied byte for byte, with their original metadata, evidence references, denominators, and status labels.

## Provider evidence added from the later push

[Provider results and scripts](providers/README.md) archives the 55-record provider export, Nina/Remy evidence, and all 15 Python harness scripts at revision `5cc9dd2`. It has its own source manifest and validation notes. The two aggregate JSON files below retain their original `7ed2ded` snapshot.

## Imported data

| File | Contents |
| --- | --- |
| [results.json](results.json) | 37 measurements covering the Level 2 census, attack rates, Level 3 rescoring, negative results, mitigation comparisons, benign cost, ablations, and controls; also scalar summaries |
| [findings.json](findings.json) | 56 catalog entries across seven classes: 24 source-labelled verified, 18 single-case, nine negative, three withdrawn, one contested, and one pending |

These are **source-reported aggregate results and a historical catalog**, not new experiments or an independent audit of every claim. References and repository-wide statements inside the unchanged JSON refer to the source repository. Finding IDs overlap this knowledge base's IDs; this import does not create 56 new discoveries.

## What was already included

| Source file | Existing evidence / handling |
| --- | --- |
| `runs/2026-11-14-measurement-firewall-l3-and-fix-eval.md` | [Existing result note](../2026-11-14-measurement-firewall-l3-and-fix-eval.md) is byte-identical; no duplicate added. |
| `runs/audit-pretext-plain-prose-leak.md` | [Existing audit-pretext result](../audit-pretext-plain-prose-leak/README.md) records the same prompt, outcome, and full turn ID `5f27a8100fef42b488bd7957172f0284`. The public source only redacts the synthetic name/date of birth and changes links. The existing evidence is retained. |
| `runs/README.md` | Its two run links are represented above and in the [shared results index](../README.md). |
| `verify.py` and `make_findings.py` | Linked below at the imported revision. Runnable tooling stays in the source code repository, following this knowledge base's contribution convention. |

Related evidence already present: [ground-truth snapshot manifest](../../mitigations/fix-evaluation/evidence/gt_snapshot_manifest.json), [fix evaluation and evidence](../../mitigations/fix-evaluation/README.md), [shared findings](../../docs/findings.md), and [Green Mosaic one-pager](../../docs/green-mosaic-one-pager.md).

## Interpretation and later corrections

- **The census, conversations, and messages use different denominators.** The reported 450/450 patient census and 351/450 corroborated records are not a 100% per-attack success rate. The Level 2 conversation result is 28/43, split into 20/34 DeepSeek and 8/9 Qwen conversations.
- **Preserve the Level 3 rescoring.** `l3_first_count` (16/177) is explicitly superseded; public facility phone matches are separated from patient-field matches, and `l3_laneB` remains contested in the imported source. Do not promote historical counts into a current patient-disclosure claim.
- **L3-16 is stale in the imported catalog.** Its claim that restricted columns on other allowed tables are enforced only by the model was refuted by this repository's later 17:00 CET sweep. See the corrected L3-16 and L3-27 in the [17:00 CET findings at commit 8a2ce04](https://github.com/Zmart64/entropy-hackathon-knowledge/blob/8a2ce04bdbe2bac85ae2d6da48a9bf1f7212fc06/docs/level-three-2026-11-14.md), which show guard enforcement on `payers` and `insurance_plans`. That correction was present on the original comparison branch; it is linked to its exact revision because it is not yet in the PR's `main` base. The source JSON is kept unchanged for traceability; its `verified` label does not override that correction. The source catalog also omits later entries such as F-22, L3-26, and L3-27.
- **The oracle counts remain scoped to their source.** The imported dedicated cell is 0/7; its F-03 evidence text separately acknowledges the team's earlier 0/8 report. This import does not reconcile those cohorts or establish oracle-only reconstruction.
- **Mitigation statistics are replay results.** The 0/32 leak-conversations result is in-sample, with an independent ground-truth label. Keep its benign false-positive cost and adaptive-test scope alongside it; no organizer deployment or universal prevention is established.
- **Aggregate provenance is not a raw transcript handoff.** The existing snapshot manifest provides hashes and cohort counts. These two imported files do not supply the complete nine-run/1,224-episode corpus or independently settle every outstanding evidence request.

## Provenance and validation

| Imported file | SHA-256 |
| --- | --- |
| `results.json` | `d472358262586a4f980990ff3b30219bf98fb8cbd9da5a800d3a550f7277c044` |
| `findings.json` | `932270bc285b7ddf6b1c7b6dc24ddd44fb5d84770f63b0e09161bb2d360daff4` |

The reviewed [source verifier](https://github.com/B0yko/green-mosaic/blob/7ed2ded738e423bdc37cfa704084173f996b8c8e/results/verify.py) passed in a checkout of that exact revision: **32 Wilson intervals and three Fisher tests recomputed**, with quoted fractions and intervals in the source README and findings catalog traced to the data. Imported JSON was parsed and compared byte for byte with that checkout. Numerical consistency does not independently validate the underlying observations.

For the source's reproduction workflow, run `python3 results/verify.py` from a checkout of the pinned revision. The [catalog generator](https://github.com/B0yko/green-mosaic/blob/7ed2ded738e423bdc37cfa704084173f996b8c8e/results/make_findings.py) and [rendered source catalog](https://github.com/B0yko/green-mosaic/blob/7ed2ded738e423bdc37cfa704084173f996b8c8e/FINDINGS.md) remain available there.
