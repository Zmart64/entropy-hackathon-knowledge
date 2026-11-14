# Query guard reference implementation

Sanitized copy of the validator evaluated for F-13. Standalone; Python standard
library only; no network, credentials, or challenge data.

```bash
python3 mitigations/query-guard/query_guard.py
```

Expected result: nineteen attack queries denied, seven legitimate requests
allowed, patient-other denied, identifier redaction demo, and a final
`PASS (0 unexpected)`. Captured output: [evaluation.txt](evaluation.txt).

The suite includes the six bypasses found in review (qualified wildcard,
function-wrapped column, cross-join, `OR` predicate, patient wildcard, unknown
role) plus comma-join and `JOIN`-subquery regressions.

Scope: this is a **validator for SQL strings**, not a replacement tool interface.
It shows the policy that could be enforced in front of `query_db`; it does not
remove SQL from the interface, and it is not deployed on the organizers' server.
The fixture lists (`ATTACKS`, `LEGITIMATE`) are the exact cases reported in the
mitigation document; this is a self-test, not a live-server harness.
