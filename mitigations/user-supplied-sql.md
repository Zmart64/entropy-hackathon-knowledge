# Mitigation: replace free-form SQL with fixed lookups

Status: local reference implementation with self-test. Not deployed to the
organizers' server.
Finding: [docs/findings.md](../docs/findings.md) F-13
Experiment: [experiments/user-supplied-sql-execution](../experiments/user-supplied-sql-execution/README.md)
Code: [query-guard/query_guard.py](query-guard/query_guard.py)
Output: [query-guard/evaluation.txt](query-guard/evaluation.txt)

## Enforcement point

The `query_db` tool boundary. The attack works because the tool signature is
`query_db(sql: str)` and the model copies the user's text into it. Prompt
hardening cannot fix that. The fix is to remove SQL from the interface: the
model chooses from a fixed menu of lookups, and every statement is a constant
with bound parameters.

## Implemented design

`handle(request, role, subject_id, db)` accepts a `Request` object, never a
string. There is deliberately no SQL field.

| Request kind | Returns | Who may call |
| --- | --- | --- |
| `appointment_types` | distinct visit types | anonymous |
| `departments` | department directory | anonymous |
| `accepting_providers` | providers accepting patients | anonymous |
| `patient_count` | aggregate count only | anonymous |
| `my_record` | fixed field set for the authenticated patient | patient |
| `my_appointments` | the patient's own appointments | patient |

Properties:

1. **No SQL text path.** A string, an object without a known `kind`, or an
   unknown kind is rejected before any database call.
2. **Parameterized statements.** Every query is a module constant using `?`
   placeholders. Quoting, `SELECT ALL`, nested queries, and `HAVING` are not
   representable.
3. **Identity comes from the caller context**, not the request. `my_record` and
   `my_appointments` require `role="patient"` and a subject id; a request that
   names a different `patient_id` is denied.
4. **Fixed field sets.** `my_record` returns patient_id, MRN, name, DOB, address,
   mobile, and email. SSN is not in the projection and cannot be requested.
5. **Aggregates only** for `patient_count`; no row-level patient access for
   anonymous callers.

## Evaluation

Run: `python3 mitigations/query-guard/query_guard.py` (captured output:
[query-guard/evaluation.txt](query-guard/evaluation.txt))

- **19 SQL attack strings rejected**, including every previously reported
  bypass: qualified wildcard, function-wrapped column, cross-join, `OR`
  tautology, nested patient query, quoted table with `SELECT ALL`, `ALL *`
  wildcard, and `HAVING`.
- **6 legitimate requests served**: four anonymous catalog/aggregate requests,
  plus patient own record and own appointments.
- **4 denials by policy**: anonymous `my_record`, a patient naming another
  `patient_id`, an unknown request kind, and a staff role (staff use the
  authenticated system, not this menu).
- `my_record` output contains no `ssn` field.

## Removed prototype

The first version of this guard was a SQL-string validator. Review found
successive bypasses because it recognized spellings rather than understanding
SQL: multi-table joins, `lower(first_name)`, `OR 1=1`, qualified wildcards,
unknown roles, quoted table names with `SELECT ALL`, `ALL *`, nested queries,
and `HAVING`. It was removed rather than patched again; the structured design
makes those inputs unrepresentable. The history is recorded here because the
negative result is part of the evidence.

## Why it addresses the mechanism

The caller no longer writes a statement. It selects an operation, and the
operation determines the fields, the predicate, and the row scope. A model that
fully complies with an attacker still cannot turn "run this SQL" into a data
dump, because there is no SQL input. This is the deterministic property the
challenge asks for: not a better filter, but a smaller capability.

## Relationship to the F-01 / F-03 fix

This is input-side and complementary. F-01 and F-03 need output-side controls
because a legitimate field set can still be abused under pretext, and because
per-turn answers can be aggregated. Layering:

- fixed lookups and identity scoping (this document),
- canonicalized output DLP plus a session disclosure budget (F-01/F-03),
- database views and column grants so the application cannot over-read.

## Limitations

- Local reference only; the organizers' server is unchanged.
- The menu covers the six operations needed for this demonstration, not every
  front-desk workflow. Production needs a product-defined operation set.
- The synthetic SQLite database mirrors only the fields used here.
- No rate limiting or session budget; F-03's aggregation defense is separate.
- Staff workflows are not implemented; staff should use the authenticated
  system, not the chat menu.
- The self-test is a fixture suite, not a live-server harness.

## Recommended rollout

1. Replace `query_db(sql)` with named operations agreed with the front desk.
2. Implement each as a parameterized query or a database view; grant the app
   role only those views.
3. Take patient identity from the authenticated session, never from the request.
4. Keep output DLP and session budgets as the second layer.
5. Log operation name, subject id, and row count for audit.
