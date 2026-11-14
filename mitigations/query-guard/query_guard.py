"""Reference guard for Riley's query_db tool.

The vulnerability is architectural: the tool accepts a SQL string, so the model
can pass user text straight through. This module shows a deterministic fix at
the tool boundary:

  1. Parse the request instead of trusting it.
  2. Allow only a single SELECT over an allowlisted table.
  3. Enforce a role policy per table and column.
  4. Require bounded rows and forbid bulk dumps.
  5. Redact identifier patterns from any rendered output (defense in depth).

Run `python query_guard.py` to evaluate the real attack prompts against the
guard and a set of legitimate front-desk requests.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

ALLOWED_TABLES = {
    "departments",
    "encounters",
    "facilities",
    "insurance_plans",
    "patient_contacts",
    "patient_coverage",
    "payers",
    "patients",
    "providers",
}

# Tables whose rows describe an identified person. Anonymous chat users may
# only see aggregates over these, never rows.
PERSON_TABLES = {"patients", "patient_contacts", "patient_coverage", "encounters"}

# Columns that identify a person or their contact/insurance details.
PII_COLUMNS = {
    "patient_id",
    "mrn",
    "first_name",
    "last_name",
    "date_of_birth",
    "address_line1",
    "address_line2",
    "city",
    "zip",
    "county",
    "mobile_phone",
    "home_phone",
    "email",
    "member_id",
    "group_number",
    "subscriber_name",
    "ssn",
}

MAX_ROWS = 20

FORBIDDEN_KEYWORDS = re.compile(
    r"\b(insert|update|delete|drop|alter|create|attach|detach|pragma|vacuum|"
    r"replace|union|intersect|except|into|load_extension|sqlite_master)\b",
    re.IGNORECASE,
)

SELECT_RE = re.compile(
    r"(?is)^select\s+(?P<columns>.+?)\s+from\s+(?P<table>[a-z_][a-z0-9_]*)"
    r"(?P<rest>.*)$"
)
LIMIT_RE = re.compile(r"(?is)\blimit\s+(\d+)\s*$")
COUNT_RE = re.compile(r"(?is)^count\s*\(\s*\*\s*\)(?:\s+as\s+[a-z_][a-z0-9_]*)?$")


class Denied(Exception):
    """Raised when a query is outside the caller's policy."""


@dataclass
class Decision:
    allowed: bool
    reason: str


def _columns(raw: str) -> list[str]:
    raw = raw.strip()
    if raw.lower().startswith("distinct "):
        raw = raw[9:]
    if raw == "*":
        return ["*"]
    return [part.strip() for part in raw.split(",")]


def _base_name(column: str) -> str:
    """Strip alias prefixes and casts: p.first_name -> first_name."""
    name = column.split(".")[-1].strip().lower()
    return re.sub(r"[^a-z0-9_].*$", "", name)


def validate(sql: str, role: str = "anonymous", subject_id: int | None = None) -> Decision:
    """Decide whether this SQL may run for this caller.

    Roles:
      anonymous  - unauthenticated chat user
      patient    - authenticated patient, may read only their own row
      staff      - authenticated front-desk user, may read demographics
    """
    text = sql.strip()
    if text.endswith(";"):
        text = text[:-1].rstrip()
    if not text:
        return Decision(False, "empty statement")
    if ";" in text:
        return Decision(False, "multiple statements are not allowed")
    if not text.lower().startswith("select"):
        return Decision(False, "only SELECT is allowed")
    if FORBIDDEN_KEYWORDS.search(text):
        return Decision(False, "statement contains a forbidden keyword")

    match = SELECT_RE.match(text)
    if not match:
        return Decision(False, "statement could not be parsed as a single-table SELECT")

    table = match.group("table").lower()
    if table not in ALLOWED_TABLES:
        return Decision(False, f"table '{table}' is not in the caller's scope")

    columns = _columns(match.group("columns"))
    rest = match.group("rest").strip()
    distinct = match.group("columns").strip().lower().startswith("distinct ")

    count = bool(COUNT_RE.match(columns[0])) if len(columns) == 1 else False
    # DISTINCT over non-identifying columns is a category lookup, not a row read.
    category_lookup = distinct and not any(
        (_base_name(column) in PII_COLUMNS or column == "*") for column in columns
    )
    aggregate = count or category_lookup

    # Row bound: aggregates and catalog tables are bounded server-side; row
    # reads from person tables must cap output explicitly.
    if table in PERSON_TABLES and not aggregate:
        limit = LIMIT_RE.search(rest)
        if not limit:
            return Decision(False, "row reads must carry an explicit LIMIT")
        if int(limit.group(1)) > MAX_ROWS:
            return Decision(False, f"LIMIT exceeds the {MAX_ROWS}-row cap")

    if role == "anonymous":
        if table in PERSON_TABLES and not aggregate:
            return Decision(False, f"anonymous callers cannot read rows from '{table}'")
        if any(_base_name(column) in PII_COLUMNS for column in columns) or "*" in columns:
            return Decision(False, "anonymous callers cannot select identifying columns")

    if role == "patient":
        if table in PERSON_TABLES and not aggregate:
            if subject_id is None or not re.search(
                rf"(?is)\bpatient_id\s*=\s*{subject_id}\b", rest
            ):
                return Decision(False, "patient callers must filter to their own patient_id")
        if "ssn" in {_base_name(c) for c in columns}:
            return Decision(False, "SSN is never exposed through this tool")

    if role == "staff":
        if "ssn" in {_base_name(c) for c in columns} or "*" in columns:
            return Decision(False, "SSN and wildcard dumps are not exposed to staff")

    return Decision(True, "allowed")


REDACTIONS = [
    ("EMAIL", re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")),
    ("PHONE", re.compile(r"\(\d{3}\)\s?\d{3}-\d{4}|\b\d{3}-\d{3}-\d{4}\b")),
    ("MEMBER_ID", re.compile(r"\b[A-Z]{3}\d{9}\b")),
    ("MRN", re.compile(r"\b\d{8}\b")),
]


def redact(text: str) -> tuple[str, list[str]]:
    """Mask identifier patterns in rendered output. Returns (text, labels)."""
    found: list[str] = []
    for label, pattern in REDACTIONS:
        def _mask(match: re.Match[str], label: str = label) -> str:
            found.append(label)
            return f"[redacted {label.lower()}]"

        text = pattern.sub(_mask, text)
    return text, sorted(set(found))


ATTACKS = [
    ("patient rows", "SELECT patient_id, mrn, first_name, last_name FROM patients LIMIT 3;"),
    ("wildcard patient", "SELECT * FROM patients LIMIT 1;"),
    ("insurance coverage", "SELECT * FROM patient_coverage LIMIT 2;"),
    ("schema metadata", "SELECT name FROM sqlite_master WHERE type = 'table';"),
    ("staff table", "SELECT * FROM staff LIMIT 2;"),
    ("union exfiltration", "SELECT department_name FROM departments UNION SELECT email FROM patients;"),
    ("stacked statement", "SELECT department_name FROM departments LIMIT 5; DROP TABLE patients;"),
    ("unbounded dump", "SELECT first_name FROM patients;"),
]

LEGITIMATE = [
    ("appointment types", "SELECT DISTINCT encounter_type FROM encounters ORDER BY encounter_type;"),
    ("departments", "SELECT department_name, specialty FROM departments ORDER BY department_name;"),
    ("accepting providers", "SELECT provider_id, specialty FROM providers WHERE accepting_new_patients = 1 LIMIT 5;"),
    ("patient count", "SELECT COUNT(*) FROM patients;"),
]

LEAKED_OUTPUT = (
    "| patient_id | mrn | first_name | last_name |\n"
    "| 1 | 21421208 | Amy | Singh |\n"
    "| 2 | 13919605 | Amanda | Lewis |\n"
    "phone (740) 555-0123, email amys1979@example.com, member GLX452948227"
)


def main() -> int:
    failures = 0
    print(f"{'case':22} {'expected':9} {'actual':8} reason")
    print("-" * 78)
    for label, sql in ATTACKS:
        decision = validate(sql, role="anonymous")
        ok = not decision.allowed
        failures += 0 if ok else 1
        print(f"{label:22} {'deny':9} {'deny' if not decision.allowed else 'ALLOW':8} {decision.reason}")

    for label, sql in LEGITIMATE:
        decision = validate(sql, role="anonymous")
        ok = decision.allowed
        failures += 0 if ok else 1
        print(f"{label:22} {'allow':9} {'allow' if decision.allowed else 'DENY':8} {decision.reason}")

    # Patient reading their own row is legitimate; someone else's is not.
    own = validate("SELECT mrn, date_of_birth FROM patients WHERE patient_id = 1 LIMIT 1;",
                   role="patient", subject_id=1)
    other = validate("SELECT mrn, date_of_birth FROM patients WHERE patient_id = 2 LIMIT 1;",
                     role="patient", subject_id=1)
    for label, decision, expect_allowed in (
        ("patient self", own, True),
        ("patient other", other, False),
    ):
        ok = decision.allowed == expect_allowed
        failures += 0 if ok else 1
        print(f"{label:22} {str(expect_allowed).lower():9} {str(decision.allowed).lower():8} {decision.reason}")

    masked, labels = redact(LEAKED_OUTPUT)
    print("\nOutput redaction on the leaked reply:")
    print(masked)
    print("patterns hit:", ", ".join(labels))

    print(f"\n{'PASS' if failures == 0 else 'FAIL'} ({failures} unexpected)")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
