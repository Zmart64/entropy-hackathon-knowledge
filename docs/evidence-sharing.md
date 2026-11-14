# Sharing full synthetic-data snapshots

Recommendation from the 14 November review: preserve **full observed synthetic outputs** for team inspection,
with provenance, in a restricted evidence bundle. Keep the KB as the searchable map plus selected redacted cases.
This review has not uploaded raw logs, unredacted dumps or credentials.

A "dump" must say whether it is complete relative to a queried page, a known table count, or just a model reply.
Do not name a 13-row result a 182-row dump, decode uncertain output into unquestioned truth, or combine conflicting
values from different runs into a single canonical database.

## Proposed bundle contents

| File / object | Required content |
| --- | --- |
| manifest.json | bundle ID, capture time/timezone, environment (live Riley / replica), source commit, contributor, source hash, reviewed sharing status |
| cases.jsonl | exact defender model/provider, turn + conversation IDs, ordered prompts, actual returned calls, rendered reply, fresh/reset dependency; no auth metadata |
| observations.jsonl | dataset, field, row ID, raw/encoded/masked state, decoded candidate, source turn, validation status, corroborating/conflicting turns |
| coverage.json | requested row window, observed unique IDs, field completeness, population evidence, gaps, known duplicates; separate by model |
| README.md | how to inspect, decoding/reconstruction steps, limitations, conflicts, and links back to KB findings |

Before publishing a bundle, inspect its **contents**, not just filenames: exclude real API keys, auth headers,
`.env`, provider auth/config files, unrelated personal material and hidden credentials in nested transcripts.
Synthetic challenge values can be retained only in the intended restricted destination; redact the pitch examples.
A checksum supports provenance, not truth. Keep original observations immutable and attach corrected interpretations.

## Inventory already shared in this review

- [Reviewed coverage map](extraction-goals.md): what exists versus what is missing, by model.
- [41 selected cases](../results/2026-11-14-swarm-extraction/review-evidence.json): sanitized, full IDs, exact prompts for selected examples; not full transcripts.
- [Andrii replica aggregates](../results/2026-11-14-swarm-extraction/andrii-replica-audit.json): recomputed metrics and hashes; no payload text.
- Local full source: `entropy-hackathon/explore/logs/probes.jsonl`, worker notes under `Research/hackathon/`,
  explorer `67172717…/target/trace.jsonl`. These remain local and are **not certified ready to upload**.

Upload destination, access policy and a credential-reviewed bundle are still needed before sharing the full snapshots.
No extra database extraction is necessary merely to package the evidence we already have.
