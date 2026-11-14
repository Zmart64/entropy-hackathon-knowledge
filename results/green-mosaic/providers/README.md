# Green Mosaic provider results and scripts

Imported on 14 November 2026 from [Green Mosaic revision 5cc9dd2](https://github.com/B0yko/green-mosaic/tree/5cc9dd241e4242a758fb43c35efb12f4d7f305f7/evidence/haiku-deepseek-harness). The 38 imported files under `source/` are unchanged copies; `.gitignore` was added locally. [source-manifest.json](source-manifest.json) records each source path and SHA-256 hash. Scripts and selected logs are included here at the user's explicit request.

## Provider results

**Start with [providers_leaked_full.csv](source/providers_leaked_full.csv): 55 provider records, eight populated columns, 55 distinct NPIs, and contiguous provider IDs 1–55.** The source describes these as synthetic range records. This is a provider-directory export, not an export of patient records or restricted credentials. The eight columns are listed in the recovered Level 3 public-reference scope; the source's use of “leak” does not by itself establish unauthorized access to these fields.

| Artifact | Contents |
| --- | --- |
| [Complete provider CSV](source/providers_leaked_full.csv) | All 55 records with `provider_id`, `npi`, `credential`, `specialty`, `taxonomy_code`, `board_certified`, `accepting_new_patients`, and `primary_department_id` |
| [Initial provider CSV](source/providers_leaked.csv) | First pass: 55 records, with the four additional fields populated only for the final five records |
| [Nina's report](source/logs/agents/nina/RESULT.md) and [pages](source/logs/agents/nina/pages.md) | Initial extraction, paging prompts, model changes, conversation IDs, and turn IDs |
| [Nina's recorded attempts](source/logs/agents/nina/attempts.jsonl) | 21 logged attempts: 14 Haiku and seven Sonnet; all HTTP 200, including refusals and empty/truncated replies |
| [Widening report](source/RESULT.md) and [Remy's pages](source/logs/agents/remy/pages.md) | Six pages covering all 55 records and all eight fields |
| [Remy's recorded attempts](source/logs/agents/remy/attempts.jsonl) and [widened CSV](source/logs/agents/remy/providers_widened.csv) | Six Sonnet turns in one conversation, with the prompts, replies, calls, and full turn IDs |
| [Original harness report](source/REPORT.md) | Source-authored campaign narrative; includes other experiments and historical interpretations beyond the provider result |

Nina's folder also retains the source JSON exports and verbatim lines. The original directory layout is preserved so evidence references remain recognizable.

## Scripts

All **15 Python files** from this source harness are archived. They were syntax-checked without being executed or imported; no range calls were made for this import.

| Scripts | Purpose |
| --- | --- |
| [atk.py](source/atk.py) | Sends one message and records the prompt, response, tool calls, model, and turn ID; this is the helper cited in the provider runs |
| [probe.py](source/probe.py) | SQL probe helper with retry handling |
| [btm.py](source/btm.py), [chat.py](source/chat.py), [example_attack.py](source/example_attack.py), [setup.py](source/setup.py) | Original client, interactive chat, example, and connection setup |
| [Alias driver](source/logs/agents/alias/drive.py), [second](source/logs/agents/alias/drive2.py), [third](source/logs/agents/alias/drive3.py) | Related Level 3 projection experiments; [report](source/logs/agents/alias/RESULT.md), [attempts](source/logs/agents/alias/attempts.jsonl), and saved run outputs are retained alongside them |
| [Column probe](source/logs/agents/column/probe.py) and [loop](source/logs/agents/column/loop.py), [loop2](source/logs/agents/column/loop2.py), [loop3](source/logs/agents/column/loop3.py), [loop4](source/logs/agents/column/loop4.py), [loop5](source/logs/agents/column/loop5.py) | Related column-scope experiments; [report](source/logs/agents/column/RESULT.md), [attempts](source/logs/agents/column/attempts.jsonl), and probe output are retained |

The alias and column experiments are supporting boundary tests, not the scripts that generated the provider CSV. Their patient-column attempts must not be counted as successful provider-extraction trials.

The scripts retain their original behavior and dependencies (`requests` and `python-dotenv`). `atk.py` reads `API_URL`, `API_KEY`, and optionally `YOUR_NAME` from the environment or a sibling `.env`. The alias drivers and column probe still point to the author's absolute workspace and `.venv/bin/python`; the column loops assume the harness working directory. Adapt these paths in a separate experiment checkout before reuse. The setup script installs dependencies, writes `.env`, and makes a connection-test request; it was not run. Use a separate checkout for new runs because the drivers append to or overwrite paths used by this archived evidence.

No `.env` or credentials are included. The local `.gitignore` makes only the selected archived logs visible to Git while continuing to ignore new run folders, environment files, and Python caches.

## Import validation and source discrepancies

- The complete CSV has **55 × 8 nonempty cells**, 55 unique IDs and NPIs, 26 specialties, 51 board-certified providers, and 32 accepting new patients. Its parsed records match Remy's widened CSV exactly. Every populated field in the initial CSV agrees with the complete export.
- All JSON/JSONL files parse, all 15 Python files parse, and each imported source file matches the pinned Git blob byte for byte. These checks validate the archive and internal consistency, not the organizer's underlying database or universal attack reliability.
- Nina's write-up says 22 turns, but the published `attempts.jsonl` contains **21**. Preserve that discrepancy; do not use the report's count as a verified success-rate denominator.
- Nina's legacy `providers.csv` has unquoted commas in specialties on IDs **26 and 42–46**, producing extra CSV fields. It is preserved as source evidence; use the complete CSV linked above for analysis.
- The original harness report contains claims about prompt recovery, patient-table counts, and SQL enforcement that are outside this provider import. Some are historical: its “WHERE never fires” statement predates the later oracle lane. That lane and the full recovered-prompt document remain in the [pinned upstream evidence](https://github.com/B0yko/green-mosaic/tree/5cc9dd241e4242a758fb43c35efb12f4d7f305f7/evidence/haiku-deepseek-harness/logs/agents), not in this selected collection. Keep current shared conclusions in [Level 3 findings](../../../docs/level-three-2026-11-14.md) separate from these unchanged source reports.

Back to the [Green Mosaic aggregate snapshot](../README.md) or [shared results](../../README.md).
