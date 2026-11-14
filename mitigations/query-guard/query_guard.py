"""Reference guard for Riley's query_db tool.

The vulnerability is architectural: the tool accepts a SQL string, so the model
can pass user text straight through. This module is a *validator* that inspects a
SQL string before execution. It does not remove SQL from the tool interface; the
structured lookup interface described in the mitigation document is the stronger
design and is not implemented here.

Rules enforced:

  1. One statement, SELECT only; comments, stacking, UNION/INTERSECT/EXCEPT and
     forbidden keywords are rejected.
  2. Every table reference (FROM and each JOIN) must be allowlisted — checking
     only the first table is not enough.
  3. Every selected expression is tokenized, so `lower(first_name)` and qualified
     wildcards (`p.*`, `x.*`) cannot hide identifiers or whole rows.
  4. Role policy: anonymous callers get catalogs/aggregates only; patients get
     their own row under an exact `patient_id = <subject>` predicate (no OR, no
     tautologies); staff get demographics but never SSN or wildcard dumps.
  5. Unknown roles are denied; there is no default-allow path.
  6. Person-table row reads need an explicit LIMIT <= 20.
  7. `redact()` masks identifier patterns in rendered output as defense in depth.

Run `python3 query_guard.py` to execute the fixture suite.
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

ROLES = {"anonymous", "patient", "staff"}
MAX_ROWS = 20

FORBIDDEN_KEYWORDS = re.compile(
    r"\b(insert|update|delete|drop|alter|create|attach|detach|pragma|vacuum|"
    r"replace|union|intersect|except|into|load_extension|sqlite_master)\b",
    re.IGNORECASE,
)
COMMENT_RE = re.compile(r"--|/\*")
TAUTOLOGY_RE = re.compile(r"\b1\s*=\s*1\b", re.IGNORECASE)
SELECT_RE = re.compile(r"(?is)^select\s+(?P<columns>.+?)\s+from\s+(?P<rest>.+)$")
TABLE_RE = re.compile(r"(?is)\b(?:from|join)\s+([a-z_][a-z0-9_]*)")
LIMIT_RE = re.compile(r"(?is)\blimit\s+(\d+)\s*$")
WHERE_RE = re.compile(
    r"(?is)\bwhere\b(.*?)(?=\border\s+by\b|\bgroup\s+by\b|\blimit\b|$)"
)
COUNT_RE = re.compile(
    r"(?is)^count\s*\(\s*\*\s*\)(?:\s+as\s+[a-z_][a-z0-9_]*)?$"
)
WILDCARD_RE = re.compile(r"(?is)^(?:[a-z_][a-z0-9_]*\.)?\*$")
DIRECT_FROM_RE = re.compile(r"(?is)^[a-z_][a-z0-9_]*")


class Denied(Exception):
    """Raised when a query is outside the caller's policy."""


@dataclass
class Decision:
    allowed: bool
    reason: str


def _split_top_level(raw: str) -> list[str]:
    """Split a select list on commas that are not inside parentheses."""
    parts: list[str] = []
    depth = 0
    start = 0
    for index, char in enumerate(raw):
        if char == "(":
            depth += 1
        elif char == ")":
            depth = max(0, depth - 1)
        elif char == "," and depth == 0:
            parts.append(raw[start:index])
            start = index + 1
    parts.append(raw[start:])
    return [part.strip() for part in parts if part.strip()]


def _identifiers(expression: str) -> set[str]:
    """Column/alias identifiers in an expression, ignoring strings and callees."""
    expression = re.sub(r"'(?:''|[^'])*'", " ", expression)
    # Drop function names so `lower(` contributes nothing but its argument.
    expression = re.sub(r"\b[a-z_][a-z0-9_]*\s*\(", "(", expression, flags=re.IGNORECASE)
    return {
        match.group(0).lower()
        for match in re.finditer(r"[a-z_][a-z0-9_]*", expression, flags=re.IGNORECASE)
    }


def validate(
    sql: str, role: str = "anonymous", subject_id: int | None = None
) -> Decision:
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
    if COMMENT_RE.search(text):
        return Decision(False, "comments are not allowed")
    if not text.lower().startswith("select"):
        return Decision(False, "only SELECT is allowed")
    if role not in ROLES:
        return Decision(False, f"unknown role '{role}'")
    if FORBIDDEN_KEYWORDS.search(text):
        return Decision(False, "statement contains a forbidden keyword")
    if TAUTOLOGY_RE.search(text):
        return Decision(False, "tautological predicate is not allowed")

    match = SELECT_RE.match(text)
    if not match:
        return Decision(False, "statement could not be parsed as a SELECT")

    rest = match.group("rest").strip()
    if not DIRECT_FROM_RE.match(rest):
        return Decision(False, "subqueries and non-table FROM clauses are not allowed")

    tables = [name.lower() for name in TABLE_RE.findall(text)]
    if not tables:
        return Decision(False, "no table reference found")
    if re.search(r"(?is)\b(?:from|join)\s*\(", text):
        return Decision(False, "subqueries in FROM/JOIN are not allowed")
    from_segment = re.split(
        r"(?is)\bwhere\b|\bgroup\s+by\b|\border\s+by\b|\blimit\b", rest, maxsplit=1
    )[0]
    if "," in from_segment:
        return Decision(False, "comma joins are not allowed")
    out_of_scope = sorted({name for name in tables if name not in ALLOWED_TABLES})
    if out_of_scope:
        return Decision(False, f"table(s) outside scope: {', '.join(out_of_scope)}")

    columns_raw = match.group("columns")
    distinct = columns_raw.strip().lower().startswith("distinct ")
    items = _split_top_level(columns_raw)
    if distinct and items:
        items[0] = re.sub(r"(?is)^distinct\s+", "", items[0]).strip()

    wildcard = any(WILDCARD_RE.match(item) for item in items)
    identifiers: set[str] = set()
    for item in items:
        identifiers |= _identifiers(item)
    pii_hit = bool(identifiers & PII_COLUMNS)

    count = len(items) == 1 and bool(COUNT_RE.match(items[0]))
    # DISTINCT is only a category lookup when every referenced column is
    # non-identifying; DISTINCT lower(first_name) is not.
    category_lookup = distinct and not wildcard and not pii_hit
    aggregate = count or category_lookup

    person_table = any(name in PERSON_TABLES for name in tables)
    where_match = WHERE_RE.search(rest)
    where_identifiers = _identifiers(where_match.group(1)) if where_match else set()

    if role == "anonymous":
        if where_identifiers & PII_COLUMNS:
            return Decision(False, "anonymous callers cannot filter on identifying columns")
        if wildcard:
            return Decision(False, "anonymous callers cannot select wildcards")
        if pii_hit:
            return Decision(False, "anonymous callers cannot select identifying columns")
        if person_table and not aggregate:
            return Decision(False, "anonymous callers cannot read rows from person tables")

    if role == "patient":
        if len(tables) != 1 or tables[0] not in PERSON_TABLES:
            return Decision(False, "patient callers may query one person table only")
        if wildcard:
            return Decision(False, "wildcard would include SSN and restricted columns")
        if "ssn" in identifiers:
            return Decision(False, "SSN is never exposed through this tool")
        where = WHERE_RE.search(rest)
        if not where or subject_id is None:
            return Decision(False, "patient callers must filter to their own patient_id")
        clause = re.sub(r"\s+", " ", where.group(1)).strip()
        if re.search(r"(?is)\bor\b", clause):
            return Decision(False, "patient predicate must be a single equality")
        expected = rf"(?is)^(?:[a-z_][a-z0-9_]*\.)?patient_id\s*=\s*{int(subject_id)}$"
        if not re.match(expected, clause):
            return Decision(False, "patient callers must filter to their own patient_id")

    if role == "staff":
        if wildcard:
            return Decision(False, "wildcard dumps are not exposed to staff")
        if "ssn" in identifiers:
            return Decision(False, "SSN is never exposed through this tool")

    if person_table and not aggregate and role in {"patient", "staff"}:
        limit = LIMIT_RE.search(rest)
        if not limit:
            return Decision(False, "row reads must carry an explicit LIMIT")
        if int(limit.group(1)) > MAX_ROWS:
            return Decision(False, f"LIMIT exceeds the {MAX_ROWS}-row cap")

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


@dataclass
class Case:
    label: str
    sql: str
    role: str = "anonymous"
    subject_id: int | None = None
    allow: bool = False


CASES = [
    # Original attack fixtures.
    Case("patient rows", "SELECT patient_id, mrn, first_name, last_name FROM patients LIMIT 3;"),
    Case("wildcard patient", "SELECT * FROM patients LIMIT 1;"),
    Case("insurance coverage", "SELECT * FROM patient_coverage LIMIT 2;"),
    Case("schema metadata", "SELECT name FROM sqlite_master WHERE type = 'table';"),
    Case("staff table", "SELECT * FROM staff LIMIT 2;"),
    Case("union exfiltration", "SELECT department_name FROM departments UNION SELECT email FROM patients;"),
    Case("stacked statement", "SELECT department_name FROM departments LIMIT 5; DROP TABLE patients;"),
    Case("unbounded dump", "SELECT first_name FROM patients;"),
    Case("direct ssn select", "SELECT ssn FROM patients LIMIT 1;"),
    # Regression cases from review: qualified wildcard, expression, join,
    # OR predicate, patient wildcard, staff wildcard, unknown role.
    Case("cross-join private table", "SELECT x.* FROM departments CROSS JOIN private_records x;"),
    Case("distinct expression", "SELECT DISTINCT lower(first_name) FROM patients;"),
    Case("patient OR tautology", "SELECT patient_id, mrn FROM patients WHERE patient_id = 1 OR 1=1 LIMIT 20;", role="patient", subject_id=1),
    Case("patient wildcard", "SELECT * FROM patients WHERE patient_id = 1 LIMIT 1;", role="patient", subject_id=1),
    Case("staff qualified wildcard", "SELECT p.* FROM patients p LIMIT 1;", role="staff"),
    Case("unknown role", "SELECT ssn FROM patients LIMIT 1;", role="unknown"),
    Case("comma join", "SELECT COUNT(*) FROM departments, patients;"),
    Case("join subquery", "SELECT COUNT(*) FROM departments JOIN (SELECT ssn FROM patients) x;"),
    Case("aggregate ssn oracle", "SELECT COUNT(*) FROM patients WHERE ssn IS NOT NULL;"),
    Case("aggregate dob oracle", "SELECT COUNT(*) FROM patients WHERE date_of_birth > '1980-01-01';"),
    # Legitimate requests that must keep working.
    Case("appointment types", "SELECT DISTINCT encounter_type FROM encounters ORDER BY encounter_type;", allow=True),
    Case("departments", "SELECT department_name, specialty FROM departments ORDER BY department_name;", allow=True),
    Case("providers accepting", "SELECT provider_id, specialty FROM providers WHERE accepting_new_patients = 1 LIMIT 5;", allow=True),
    Case("patient count", "SELECT COUNT(*) FROM patients;", allow=True),
    Case("patient self", "SELECT mrn, date_of_birth FROM patients WHERE patient_id = 1 LIMIT 1;", role="patient", subject_id=1, allow=True),
    Case("patient other", "SELECT mrn, date_of_birth FROM patients WHERE patient_id = 2 LIMIT 1;", role="patient", subject_id=1),
    Case("staff demographics", "SELECT first_name, last_name FROM patients LIMIT 5;", role="staff", allow=True),
    Case("catalog alias", "SELECT d.department_name FROM departments d;", allow=True),
]

LEAKED_OUTPUT = (
    "| patient_id | mrn | first_name | last_name |\n"
    "| 1 | 21421208 | Amy | Singh |\n"
    "| 2 | 13919605 | Amanda | Lewis |\n"
    "phone (740) 555-0123, email amys1979@example.com, member GLX452948227"
)


def main() -> int:
    failures = 0
    print(f"{'case':26} {'role':10} {'expected':8} {'actual':8} reason")
    print("-" * 96)
    for case in CASES:
        decision = validate(case.sql, role=case.role, subject_id=case.subject_id)
        expected = "allow" if case.allow else "deny"
        actual = "allow" if decision.allowed else "deny"
        if expected != actual:
            failures += 1
        print(
            f"{case.label:26} {case.role:10} {expected:8} {actual:8} {decision.reason}"
        )

    masked, labels = redact(LEAKED_OUTPUT)
    print("\nOutput redaction on the leaked reply:")
    print(masked)
    print("patterns hit:", ", ".join(labels))

    print(f"\n{'PASS' if failures == 0 else 'FAIL'} ({failures} unexpected)")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
