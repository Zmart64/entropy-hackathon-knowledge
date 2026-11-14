# Mitigations

Document proposed fixes and their evaluations here, linked to the corresponding experiment and finding. Keep implementations in a separate code checkout or repository and link to a shared revision when available.

Describe the enforcement point, the rule implemented in code, and why it addresses the observed mechanism. Compare verified attack success before and after the fix, and check that representative legitimate requests still work.

Label local demonstrations clearly. A local wrapper or simulated backend is not a deployed change to the organizers' server.

## Proposals

- [Chat endpoint hardening](chat-endpoint-hardening.md): response filtering, identity, tool permissions, validation, secrets, budgets, and regression criteria. Not deployed or evaluated after a patch.
- [User-supplied SQL](user-supplied-sql.md): SQL validator (in-repo, runnable) plus the proposed structured-query interface; blocks 8/8 attack queries, allows 4/4 legitimate ones. Not deployed.
