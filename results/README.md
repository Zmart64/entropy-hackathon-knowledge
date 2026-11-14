# Shared results

Store selected experiment evidence here, grouped by experiment name. Raw logs stay in each teammate's separate local starter checkout.

Include the model, prompt sequence, conversation IDs, relevant responses, `turn_id`s, date, and validation method. Keep attempted and successful trial counts explicit. Link each result to its experiment notes.

Review files before sharing: exclude API keys, authentication headers, and unrelated personal data. Preserve the fictional challenge evidence needed to reproduce and verify the result.

## Evidence collections

- [Green Mosaic results snapshot](green-mosaic/README.md): 37 source measurements and a 56-entry findings catalog, pinned to the source revision with duplicate-run mapping and later-correction notes.
- [Green Mosaic provider results and scripts](green-mosaic/providers/README.md): 55 provider records across eight fields, source reports and selected turn logs, and all 15 harness scripts from revision `5cc9dd2`.
- [14 November 2026 endpoint review](2026-11-14-endpoint-review/README.md): curated API cases, model snapshots, tool schemas, and historical service-scan excerpts.
- [14 November 2026 afternoon extraction campaign](2026-11-14-swarm-extraction/README.md): per-store extraction ledger (extracted vs attempted-not-obtained), routes, turn_ids, costs.
- [14 November 2026 credential status audit](2026-11-14-credential-status/README.md): password/credential absence checks, partial extracted-data counts, and a 32-case redacted trace bundle.
- [Haiku L3 scope-gate + FROM-tail relay](2026-11-14-haiku-l3-and-tail-relay/README.md): Haiku 0/96 emissions on any 6th table; V4-Pro tail executes 6/17 and leaks patient-table cardinality, then denies having run it.
- [User-supplied SQL execution](user-supplied-sql-execution.md): 30/30 disclosure, quoted patient and insurance evidence, negative control, log hash.
- [14 November 2026 Claude Haiku L3](2026-11-14-haiku-l3/README.md): allowed-table row rendering (provider NPI, 25-row page, insurance page), the 0/96 scope-gate qualification, selected turns, and the complete target-side traces for the four runs.
- [14 November 2026 measurement, Level 3 and fix evaluation](2026-11-14-measurement-firewall-l3-and-fix-eval.md): existing Green Mosaic run note; see the [snapshot notes](green-mosaic/README.md) for later rescoring and evidence boundaries.
- [Audit pretext and plain-prose leak](audit-pretext-plain-prose-leak/README.md): existing Qwen3-30B reproduction with the submitted turn ID.
