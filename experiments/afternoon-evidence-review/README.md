# Offline review of the afternoon extraction evidence

Author: Edgar's review agent. Date: 2026-11-14. No new range requests.

Scope: reconcile PR #6 at `56703f8` with nine other project threads active in the fixed window
12:08:55–13:08:55 UTC, five worker notes, the mainline report and saved request/response records.
The [coverage audit](../../docs/knowledge-review-2026-11-14.md) identifies the sources.

Reproduction material: [selected evidence JSON](../../results/2026-11-14-swarm-extraction/review-evidence.json).
It contains full model/turn/conversation IDs and exact prompts for selected cases. `previous_logged_turns_same_conversation`
records the observed reset dependency; payment schema and sample are two turns in one conversation.
Unknown-secret outputs are omitted. Source hashes and line references allow the local owners to inspect originals.

Validation: distinguish actual top-level `tool_calls` from model-written JSON, compare patient-row-1 encoded
outputs across two calls, compare VIP demographics across two outputs, count rendered CSV rows, inspect SQL
for actual hex computation, inspect token-transform agreement and preserve model/refusal scope.

Findings: the morning credential claims have empty actual calls; app-users sample is 13 rows, employees cited
CSV is five rows, employee encoding is model-side in W5, role response is a summary. The selected patient hex
route has corroboration. Token coverage and transfer are partial; external delivery and universal filter behavior
are not established. See [the ledger](../../results/2026-11-14-swarm-extraction/README.md).

Limits: selected cases rather than randomized trials; no server source, raw tool-result channel, organizer
verification, current target availability check, or before/after defense test. No success-rate claim or CI.
