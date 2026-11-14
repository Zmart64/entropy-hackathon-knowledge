# Knowledge-base and PR review — 14 November 2026

Review scope: nine other project threads with activity in **12:08:55–13:08:55 UTC** (13:08:55–14:08:55 CET),
PR [#6](https://github.com/Zmart64/entropy-hackathon-knowledge/pull/6) at `56703f8`, local worker reports and source
records. Follow-up expanded the review to Andrii's additional findings, including live-KB commit `626d715`
and his separate repo at `181df0d`. The sidechat branches contain inherited material; they are not independent trials.

## Outcome

The layer/method/open-item structure is useful, but the original PR overstated confidence, completeness and
cross-model generality. Corrections now have selected source evidence. The [pitch overview](../presentation/pitch-overview.md)
and [model/coverage map](extraction-goals.md) are the entry points. No new range probes or raw-dump uploads.

## Thread coverage

| Thread | Contribution preserved | Where it is represented |
| --- | --- | --- |
| `71ceea6d-3db5-45d4-b77d-3ac572de5555` | Five-worker coordination, user requirement for model scope and no impossibility claims, PR integration | Coverage, model matrix, reviewed PR |
| `056455de-3c3f-42e5-99fd-582e68d285fe` | Mainline authority frame, patient/VIP/employee/payment/RBAC outputs; attacker wiring | Results; discarded overclaims logged below |
| `agent-f916a082675ec881cd52264d2fa672c1` | W1 credential absence replies, patient predicates and SQL hex | F-09/F-14/F-18; open credentials |
| `agent-cee4b03724f5c986fa750ffff9649ef5` | W2 payment schema/sample, provider pages, RBAC negatives | Ledger, model map |
| `agent-e1d12d0b2806fe5497b604eb3acf1289` | W3 refs, anchor/decoy errors, recovery bodies, apparent-filename correction | Per-ref ledger and remaining census |
| `agent-bf92f50324c1e268ab85c0d43be0089f` | W4 research, eight literal-calibration probes, later clarification that it recovered no redacted secret | Methods, calibration/unknown-data distinction |
| `agent-53a7d3e5e5d3ee0ecb2b57c881aa479a` | W5 employee candidates, args shape grid, model differences | Boundary matrix, employee conflict and channel evidence |
| `3bba8edb-d340-40fb-8606-b0608dc148a2` | W4 sidechat copy of research and adaptive ideas | Provenance only; not double-counted |
| `463825ff-1d5c-4f19-82d8-ba615f6ecba1` | Recon sidechat: levels, tools, system/config/inbox map | Historical target map with current corrections |

Andrii's work has no matching local Synara thread; inspected sources are the two Git repositories. His unpushed
work and other-machine conversations are outside this audit. Endpoint/receiver/SQL mitigation work by teammates
is retained through the existing merged KB pages and linked from the pitch overview.

## Standards review

1. **Counts exceeded evidence.** 182 users were called a dump despite a sampled reply. Direct inspection now
   finds only IDs 1–13 in the cited LIMIT-15 response. Repository results guidance requires explicit observed counts.
2. **Local-only evidence was not a usable team handoff.** Added 37 sanitized case entries with full identifiers,
   selected exact prompts, source hashes and reset/context metadata. Cases with omitted prompts are clearly partial.
3. **Exploratory observations weakened the evidence gate.** Removed n≥2/n≥3 substitutes and universal server-property
   claims; quantitative/generalization claims still need the team's gate and campaign-specific denominators.

Three standards findings; worst: claims lacked the required independently inspectable evidence. No code-smell findings.

## Spec review

1. **Credential “flicker” was unsupported.** Actual morning calls are empty; apparent envelopes are in model text.
   Credential-store existence/change stays unresolved. This matters to the instruction to know what is actually obtained.
2. **Completeness and verification were inflated.** Employee cited CSV has five rows; W5's SQL contains no hex;
   salaries disagree; a checksum is not truth validation. User/role coverage, provider counts and inbox census now differ explicitly.
3. **Model failures were generalized to server properties.** Rules now separate value class, channel, model and
   uncertainty. Base64 SSN can pass while token attempts fail; three-value failures coexist with successful triples.
4. **The shared handoff was incomplete.** Added inspected cases, methods, open items and Andrii's live/replica digest.
   Research-only families remain labeled unrun; no “impossible on DeepSeek” conclusion.

Four spec findings; worst: unresolved/model-narrated evidence was presented as verified extraction. No material scope creep.

## Additional source corrections and retained research

- Six discovered refs are not six of every ref in the inbox. One value lacks the asserted prefix-hyphen format.
- Returned email args disclose information to the caller; `.invalid` recipients give no delivery evidence.
- A 25-row SQL-hex output cross-checks row 1 with a separate call; remaining values retain their verification gap.
- Mainline recon claimed contacts unavailable while later samples contain them; preserve case/frame differences.
- Worker request counts are estimates, not a deduplicated campaign ledger. About 284 by final reports differs from PR's 235.
- W4's 20 ranked primitives and adaptive ladder cover authority/config impersonation, tool-argument carriers,
  staging, TAP-style refinement, Unicode/encoding combinations, split/cumulative reconstruction and decoy controls.
  Only its eight calibration probes were run by W4; other workers independently tested some routes. Full templates
  remain in local `Research/hackathon/w4-unmask-primitives.md`; do not report the entire research list as tested.
- Attacker plumbing: explorer run `67172717…` completed; worker/KB-worker runs were reported cancelled. Successful
  plumbing is not a measured attack success rate. No credentials or host-specific configuration are copied here.
- The latest Andrii update supersedes his old F-03 headline; live validation, attack-attempt pilot and replica metrics
  have different denominators/environments. Replica aggregate counts were independently recomputed from 1,470 rows.

## Verification and limits

Inspected saved Synara messages, five worker notes, mainline report, 728-record probe snapshot and explorer target
trace. The trace records real calls elsewhere (16 of 52 replies), while all inspected morning credential claims
have empty actual calls. Selected JSON parses, IDs resolve against source records, row counts and patient-row-1
agreement were computed offline. Six replica metric files were aggregated with per-cell error/truncation and Wilson intervals.

No server source/raw DB result channel, fresh range retest, independent organizer ground truth, held-out mitigation
experiment or complete data census. Full source logs remain local; the [sharing proposal](evidence-sharing.md)
explains how to package synthetic snapshots without credentials. The audit is not a completed hackathon submission.
