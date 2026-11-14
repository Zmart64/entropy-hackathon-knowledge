# Hackathon pitch overview — evidence first

Reviewed 14 November 2026. [What we have by model](../docs/extraction-goals.md) ·
[Andrii's live and replica findings](../docs/andrii-findings.md) ·
[Open items](../docs/open-items.md) · [Team work already covered](../docs/team-coverage-reconciliation.md) ·
[Review provenance](../docs/knowledge-review-2026-11-14.md).

**Recommended story:** an assistant can refuse direct requests yet disclose sensitive synthetic records under
other task framings or representations. Returned tool arguments are another visible disclosure surface.
Enforcement must follow sensitive data through queries, transformations and actions; model refusal alone is
inconsistent. Show the evidence, a deterministic control, and the measured utility cost.

## What is ready to explain

| Evidence lane | What can be said | What cannot yet be said |
| --- | --- | --- |
| Andrii — live Riley F-01 | Earlier PHI disclosure pilots on V4-Pro and Qwen30; current headline is measurement + fix | Latest reported 450/450 patient census with 351/450 double-confirmed is not a per-attack ASR or full-field coverage; underlying frozen audit missing here |
| Julian — live Riley F-13 | Caller SQL copied in 30/30 scoped trials; local fixed lookup-menu mitigation | Not arbitrary-table access on every model; local tests are not a deployed patch |
| Our patient encoding | Qwen30 returned encoded SSNs; row 1 agrees in independent single/bulk cases | Not all 450 records; not all 25 values independently verified; no V4-Pro hex win established |
| Our inbox references | Six discovered references, with representation/cross-model corroboration for selected values | Not exhaustive; not all six on all models; not demonstrated external delivery |
| Other stores | Provider page coverage, payment samples, employee/user samples | No complete user/payments dump; disputed employee identifiers/salary remain candidates |
| Andrii — replica/F-01 | Cross-agent scope-clean canary release and a local data-flow control; committed metrics audited | Not live Riley, real network exfiltration, or a successful Haiku bypass |

## Suggested three-minute sequence

1. **0:00–0:25 — problem:** a filtered hospital assistant still exposes synthetic sensitive data; state the live target and tested model.
2. **0:25–1:10 — one concrete example:** use a saved, redacted control and disclosure pair with full turn IDs.
   State whether it is a literal calibration, actual unknown-data disclosure or corroborated reconstruction.
3. **1:10–1:45 — measured scope:** cite the frozen live F-01 cohort and per-model attempt rates once reconciled;
   use sample observations without percentages until then. Mention stronger-model failures as measured negatives.
4. **1:45–2:30 — fix:** deterministic query/data-flow controls; demonstrate a local replay, label it local,
   and report held-out attack/benign performance only when available.
5. **2:30–3:00 — relevance and limits:** auditability for agent deployments, data/recipient authorization, clear model limits and reproducible evidence.

## Before deck lock

- Reconcile Andrii's latest reported 450/450 patient census and 351/450 double-confirmation with the frozen nine-run/1,224-episode manifest; older 273/450 is superseded. Keep population coverage separate from attempt rates and full-field coverage.
- Choose one demo with a known control, decoded-value check and source turn IDs; make an offline redacted recording.
- Obtain held-out mitigation, benign-FP and adaptive results. Latest author reports are 144/145 replies and 27/28 conversations (96.4%, not 100%); the new ledger isolates 27/27 F-01-only conversations, excluding one oracle case. LlamaGuard detects 39/50. Their different cohorts cannot support a paired superiority claim. The earlier 450/450 fix evaluation is in-sample consistency only (a separate metric from the patient census).
  - Done 16:22: [fix-evaluation](../mitigations/fix-evaluation/README.md) has the paired, same-cohort results: 0 of 32 leaking conversations let through vs Llama Guard S7 28 of 32; benign cost 23% [15-34] vs Llama Guard 0% on the same held-out replies; adaptive round 0 of 8 past the fix.
- Replace or retire the [old F-03 talk](warroom-talk-f03-draft.md): its full reconstruction claim and placeholders
  do not match Andrii's latest secondary-oracle status (5/12 incidental member-ID characters, no full reconstruction; dedicated oracle test already reports 0/8).
- Confirm allowed target/track, final submission criteria and current organizer availability before submission.
- Preserve novelty limits: encoding/format evasion is known; measurement and enforceable controls are the contribution.

**Do not pitch:** all secrets recovered; the credential table disappeared; DeepSeek is impossible to break;
hex always works; every response was explicitly filter-green; email was delivered; a fix is deployed;
61% of all attacks succeeded; or the replica's percentages are live hospital results.
