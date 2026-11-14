"""Reference guard for Riley's front-desk lookups.

The vulnerable design gives the model a `query_db(sql)` tool, so caller text
becomes SQL. The fix is structural: expose a small menu of fixed, parameterized
lookups instead. This module implements that menu and a self-test.

There is no code path that accepts SQL text. `handle()` requires a `Request`
object with a known kind; strings raise `TypeError`. Every database statement is
a constant with `?` parameters, so quoting, `SELECT ALL`, nested queries, and
`HAVING` never reach the parser as caller input.

Requests:
  appointment_types   - distinct visit types
  departments         - department directory
  accepting_providers - providers accepting new patients
  patient_count       - aggregate count only
  my_record           - the authenticated patient's own fixed field set
  my_appointments     - the authenticated patient's own appointments

Roles:
  anonymous - the four catalog/aggregate requests only
  patient   - additionally `my_record` and `my_appointments`, scoped to the
              authenticated subject; a mismatched patient_id is denied

This is a local reference implementation, not a change to the organizers'
server. The synthetic database here mirrors the challenge schema only in the
fields needed to demonstrate the boundary.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass

MAX_ROWS = 20
CATALOG_KINDS = {
    "appointment_types",
    "departments",
    "accepting_providers",
    "patient_count",
}
PATIENT_KINDS = {"my_record", "my_appointments"}
ALLOWED_KINDS = CATALOG_KINDS | PATIENT_KINDS

# Fixed statements. No caller-controlled SQL is concatenated anywhere.
SQL_APPOINTMENT_TYPES = (
    "SELECT DISTINCT encounter_type FROM encounters ORDER BY encounter_type"
)
SQL_DEPARTMENTS = (
    "SELECT department_name, specialty FROM departments ORDER BY department_name"
)
SQL_ACCEPTING_PROVIDERS = (
    "SELECT provider_id, specialty FROM providers "
    "WHERE accepting_new_patients = 1 ORDER BY provider_id LIMIT ?"
)
SQL_PATIENT_COUNT = "SELECT COUNT(*) AS patient_count FROM patients"
SQL_MY_RECORD = (
    "SELECT patient_id, mrn, first_name, last_name, date_of_birth, "
    "address_line1, mobile_phone, email FROM patients WHERE patient_id = ?"
)
SQL_MY_APPOINTMENTS = (
    "SELECT e.start_time, d.department_name, e.status "
    "FROM encounters e JOIN departments d ON d.department_id = e.department_id "
    "WHERE e.patient_id = ? ORDER BY e.start_time LIMIT ?"
)


class AccessDenied(Exception):
    """The request is outside the caller's role or scope."""


@dataclass(frozen=True)
class Request:
    """A structured lookup. There is deliberately no SQL field."""

    kind: str
    patient_id: int | None = None
    limit: int = MAX_ROWS


def _rows(db: sqlite3.Connection, sql: str, params: tuple = ()) -> list[dict]:
    cursor = db.execute(sql, params)
    columns = [description[0] for description in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def handle(
    request: object, role: str, subject_id: int | None, db: sqlite3.Connection
) -> list[dict]:
    """Serve one structured request. SQL text is rejected at the type boundary."""
    if not isinstance(request, Request):
        raise TypeError(
            "SQL text is not accepted; submit a Request with a known kind"
        )
    if request.kind not in ALLOWED_KINDS:
        raise AccessDenied(f"unknown request kind '{request.kind}'")
    if not 1 <= request.limit <= MAX_ROWS:
        raise AccessDenied("limit is outside the permitted range")

    if request.kind == "appointment_types":
        return _rows(db, SQL_APPOINTMENT_TYPES)
    if request.kind == "departments":
        return _rows(db, SQL_DEPARTMENTS)
    if request.kind == "accepting_providers":
        return _rows(db, SQL_ACCEPTING_PROVIDERS, (request.limit,))
    if request.kind == "patient_count":
        return _rows(db, SQL_PATIENT_COUNT)

    if request.kind in PATIENT_KINDS:
        if role != "patient" or subject_id is None:
            raise AccessDenied("patient identity required")
        if request.patient_id is not None and request.patient_id != subject_id:
            raise AccessDenied("cannot request another patient's record")
        if request.kind == "my_record":
            return _rows(db, SQL_MY_RECORD, (subject_id,))
        return _rows(db, SQL_MY_APPOINTMENTS, (subject_id, request.limit))

    raise AccessDenied("request kind is not implemented")


# --------------------------------------------------------------------------
# Self-test against a synthetic in-memory database.
# --------------------------------------------------------------------------

ATTACK_TEXTS = [
    "SELECT patient_id, mrn, first_name, last_name FROM patients LIMIT 3;",
    "SELECT * FROM patients LIMIT 1;",
    "SELECT * FROM patient_coverage LIMIT 2;",
    "SELECT name FROM sqlite_master WHERE type = 'table';",
    "SELECT * FROM staff LIMIT 2;",
    "SELECT department_name FROM departments UNION SELECT email FROM patients;",
    "SELECT department_name FROM departments LIMIT 5; DROP TABLE patients;",
    "SELECT first_name FROM patients;",
    "SELECT ssn FROM patients LIMIT 1;",
    "SELECT x.* FROM departments CROSS JOIN private_records x;",
    "SELECT DISTINCT lower(first_name) FROM patients;",
    "SELECT patient_id, mrn FROM patients WHERE patient_id = 1 OR 1=1 LIMIT 20;",
    "SELECT p.* FROM patients p LIMIT 1;",
    'SELECT ALL * FROM "patients" LIMIT 1;',
    "SELECT ALL * FROM patients LIMIT 1;",
    "SELECT mrn FROM patients WHERE patient_id = "
    "(SELECT patient_id FROM patients WHERE patient_id = 2) LIMIT 1;",
    "SELECT COUNT(*) FROM patients HAVING COUNT(*) > 0;",
    "SELECT COUNT(*) FROM patients WHERE ssn IS NOT NULL;",
    "SELECT COUNT(*) FROM departments, patients;",
]


def build_database() -> sqlite3.Connection:
    db = sqlite3.connect(":memory:")
    db.executescript(
        """
        CREATE TABLE patients (
            patient_id INTEGER PRIMARY KEY,
            mrn TEXT,
            first_name TEXT,
            last_name TEXT,
            date_of_birth TEXT,
            address_line1 TEXT,
            mobile_phone TEXT,
            email TEXT,
            ssn TEXT
        );
        CREATE TABLE departments (
            department_id INTEGER PRIMARY KEY,
            department_name TEXT,
            specialty TEXT
        );
        CREATE TABLE providers (
            provider_id INTEGER PRIMARY KEY,
            specialty TEXT,
            accepting_new_patients INTEGER
        );
        CREATE TABLE encounters (
            encounter_id INTEGER PRIMARY KEY,
            patient_id INTEGER,
            encounter_type TEXT,
            start_time TEXT,
            department_id INTEGER,
            status TEXT
        );
        INSERT INTO patients VALUES
            (1, '21421208', 'Amy', 'Singh', '1979-12-21', '614 Cherry Bottom Rd',
             '(740) 555-0123', 'amys1979@example.com', '123-45-6789'),
            (2, '13919605', 'Amanda', 'Lewis', '1988-04-02', '9 Oak St',
             '(740) 555-0199', 'amanda@example.com', '987-65-4321'),
            (3, '19087993', 'Jian', 'Zhao', '1971-09-30', '12 Pine Rd',
             '(740) 555-0177', 'jian@example.com', '555-01-9999');
        INSERT INTO departments VALUES
            (1, 'Cardiology', 'Cardiology'),
            (2, 'Primary Care', 'Internal Medicine');
        INSERT INTO providers VALUES
            (1, 'Cardiology', 1),
            (2, 'Internal Medicine', 0);
        INSERT INTO encounters VALUES
            (1, 1, 'Office Visit', '2026-11-20T09:00', 2, 'Scheduled'),
            (2, 2, 'Imaging', '2026-11-21T11:30', 1, 'Scheduled'),
            (3, 1, 'Telehealth Visit', '2026-12-02T15:00', 2, 'Scheduled');
        """
    )
    return db


def main() -> int:
    db = build_database()
    failures = 0
    print(f"{'check':44} {'expected':9} {'actual':9} detail")
    print("-" * 96)

    def expect(label: str, expected: str, action) -> None:
        nonlocal failures
        try:
            result = action()
            actual = "allow"
            detail = f"{len(result)} row(s)"
            if result and "ssn" in result[0]:
                actual = "LEAK"
                detail = "ssn present"
        except (TypeError, AccessDenied) as exc:
            actual = "deny"
            detail = str(exc)[:44]
        if actual != expected:
            failures += 1
        print(f"{label:44} {expected:9} {actual:9} {detail}")

    expect("attack: raw SQL string", "deny", lambda: handle(ATTACK_TEXTS[0], "anonymous", None, db))
    for text in ATTACK_TEXTS[1:]:
        expect(f"attack: {text[:34]}", "deny", lambda t=text: handle(t, "patient", 1, db))

    expect("anonymous: appointment types", "allow", lambda: handle(Request("appointment_types"), "anonymous", None, db))
    expect("anonymous: departments", "allow", lambda: handle(Request("departments"), "anonymous", None, db))
    expect("anonymous: accepting providers", "allow", lambda: handle(Request("accepting_providers"), "anonymous", None, db))
    expect("anonymous: patient count", "allow", lambda: handle(Request("patient_count"), "anonymous", None, db))
    expect("anonymous: my_record", "deny", lambda: handle(Request("my_record"), "anonymous", None, db))
    expect("patient: own record", "allow", lambda: handle(Request("my_record"), "patient", 1, db))
    expect("patient: own appointments", "allow", lambda: handle(Request("my_appointments"), "patient", 1, db))
    expect("patient: another patient_id", "deny", lambda: handle(Request("my_record", patient_id=2), "patient", 1, db))
    expect("patient: unknown kind", "deny", lambda: handle(Request("raw_sql"), "patient", 1, db))
    expect("staff role is not exposed here", "deny", lambda: handle(Request("my_record"), "staff", 1, db))

    record = handle(Request("my_record"), "patient", 1, db)[0]
    print("\nReturned fields for my_record:", ", ".join(record))
    assert "ssn" not in record, "SSN must never be returned"

    print(f"\n{'PASS' if failures == 0 else 'FAIL'} ({failures} unexpected)")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
