# Mitigations

Document proposed fixes and their evaluations here, linked to the corresponding experiment and finding. Keep implementations in a separate code checkout or repository and link to a shared revision when available.

Describe the enforcement point, the rule implemented in code, and why it addresses the observed mechanism. Compare verified attack success before and after the fix, and check that representative legitimate requests still work.

Label local demonstrations clearly. A local wrapper or simulated backend is not a deployed change to the organizers' server.

## Proposals

- [Chat endpoint hardening](chat-endpoint-hardening.md): response filtering, identity, tool permissions, validation, secrets, budgets, and regression criteria. Not deployed or evaluated after a patch.
- [User-supplied SQL](user-supplied-sql.md): fixed lookup menu (in-repo, runnable) replacing free-form SQL; 19 attack strings rejected at the type boundary, 6 legitimate requests served. Not deployed.

- [Deterministic DLP fix](deterministic-dlp-fix.md): design of the provenance-anchored output DLP. Local shadow evaluation, not deployed.
- [Independent fix evaluation](fix-evaluation/README.md): 0 of 32 leaking conversations let through on any record field (Llama Guard S7: 29 of 32; Prompt Guard 2: 32 of 32); hard benign answers blocked 23% [15-34] vs Llama Guard 0% on the same 77 held-out replies; adaptive round 0 of 8 past the fix. Same-cohort, per-conversation, held-out benign sets frozen before the run. Oracle channel not measured; Claude held-out test pending.
