# Query guard reference implementation

Sanitized copy of the validator evaluated for F-13. Standalone; Python standard
library only; no network, credentials, or challenge data.

```bash
python3 mitigations/query-guard/query_guard.py
```

Expected result: eight attack queries denied, four legitimate catalog/aggregate
requests allowed, patient-self allowed / patient-other denied, identifier
redaction demo, and a final `PASS (0 unexpected)`. Captured output:
[evaluation.txt](evaluation.txt).

Scope: this is a **validator for SQL strings**, not a replacement tool interface.
It shows the policy that could be enforced in front of `query_db`; it does not
remove SQL from the interface, and it is not deployed on the organizers' server.
The fixture lists (`ATTACKS`, `LEGITIMATE`) are the exact cases reported in the
mitigation document; this is a self-test, not a live-server harness.
