# Query guard reference implementation

Local reference implementation for F-13. It replaces the free-form
`query_db(sql)` tool with a fixed menu of parameterized lookups. SQL text is not
accepted anywhere in the interface.

```bash
python3 mitigations/query-guard/query_guard.py
```

Expected result: 19 SQL attack strings rejected at the type boundary, 6
legitimate requests served, 4 policy denials, `my_record` returning no SSN, and
`PASS (0 unexpected)`. Captured output: [evaluation.txt](evaluation.txt).

Scope: synthetic in-memory SQLite database, six request kinds, two roles
(`anonymous`, `patient`). It is a demonstration of the boundary, not a deployed
change to the organizers' server, and not a full front-desk application.

The design and the bypass history of the earlier SQL-string validator are
documented in [../user-supplied-sql.md](../user-supplied-sql.md).
