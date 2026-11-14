# Scope and egress enforcement — proposed deterministic fixes

Proposed, not deployed (the organizers own the server). Each rule maps to findings in
`docs/findings.md`; evaluation = before/after leak rate on the attack battery plus false-positive
rate on benign front-desk tasks.

| Finding class | Enforcement point | Deterministic rule | Why it closes the observed mechanism |
| --- | --- | --- | --- |
| F-03, F-04, F-11 (SQL scope) | `query_db` harness layer, pre-DB | Parse SQL server-side (AST): table allow-list per level; resolve `alias.*` to the same 26-column projection as `*`; reject disallowed joins (or allow-list join pairs); per-request row budget that `OFFSET` cannot reset | The DB currently executes everything; scope lived only in model choices |
| F-05 (aggregates) | DB view layer | Bucket suppression / k-anonymity on `confidentiality_level` aggregates; strip tier columns from the exposed projection | Counts and per-row tier values disclosed hidden classes |
| F-06 (columns) | data layer | Column pruning per scope at the data layer; add `dea_number` to the filter's scanned classes | Never-reference column returned raw |
| F-07 (egress) | `send_email` tool | Recipient allowlist (patient-on-file or internal domains); outbound DLP for name+DOB/MRN/clinical-text combinations; taint rule: a DB-read result may not reach an external send in the same session without an approval step | Recipient restriction existed only as prompt text |
| F-01, F-08 (output filter) | filter pre-processing | Normalize unicode/whitespace/separators; parse JSON/CSV/table wrappers into fields, then scan; reject transform intents (hex/base64/spelled) at the intent layer | Filter matched exact ASCII shapes of prose only |
| F-09 (blind oracle) | query layer, expression analysis | Reject `length`/predicate/`substr`/comparison expressions on restricted columns; flag oracle-shaped patterns as findings | Lengths and booleans on masked columns evaluated unmasked |
| F-10 (inbox directives) | content tagging + tool gateway | Uniform untrusted-content tagging for ALL tool-sourced text (inbox, files, rows — not rows only); alert on any outbound-tool attempt within N turns of a content read | Injections crossed from content to tool calls |
| F-12 (filter on metadata) | filter audit | Log which protected class matched a redacted tool-returned identifier; expose a rule id in findings | Filter currently redacts silently, even filenames |
| F-14 (non-determinism) | harness layer | Move all guard decisions into deterministic harness rules, logged with rule ids; model layer advisory only | Same input produced different outcomes across turns |

Benign-use spot-check set for every evaluation: visiting-hours ask, insurance coverage check,
appointment reschedule, referral routing, one legitimate `send_email` confirmation to a patient —
all must keep working unchanged.
