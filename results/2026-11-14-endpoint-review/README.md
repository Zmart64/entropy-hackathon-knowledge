# Selected endpoint review evidence

Author: Justus, with Codex-assisted testing. Date: 2026-11-14.

These files are curated evidence for the [review](../../docs/endpoint-review-2026-11-14.md), [conversation experiment](../../experiments/chat-isolation-and-response-exposure/README.md), and [tool-interface experiment](../../experiments/tool-interface-disclosure/README.md). No API keys, authentication-header values, unrelated personal data, or runnable test scripts are included. Synthetic labels and turn IDs are retained for verification. No challenge submission was made.

| File | Provenance and contents |
| --- | --- |
| [chat-cases.json](chat-cases.json) | Selected request/response fields from all 20 authenticated/control requests; exact prompts, IDs, outputs, and outcomes. Credential labels A/B are represented as `valid`/`second`, never secret values. |
| [unauthenticated-checks.json](unauthenticated-checks.json) | 21 unauthenticated checks; statuses and relevant response bodies, with request headers omitted. These observations predate successful authenticated testing. |
| [http-route-checks.json](http-route-checks.json) | Earlier standard web-route checks plus three schema-route probes. Root/health and some initial 404 checks were recorded only in the chat and are summarized in the review. |
| [service-scan-excerpts.txt](service-scan-excerpts.txt) | Selected output from the completed common-port and three-port service scans. Local paths and invocation commands omitted. No complete all-port scan is claimed. |
| [model-registry-snapshots.json](model-registry-snapshots.json) | Initial four-model response extracted from saved evidence; later seven-model response transcribed from the tool result in the chat. These are historical snapshots, not current availability guarantees. |
| [tool-inventory-cases.json](tool-inventory-cases.json) | Two exact Qwen schema requests and responses, including unexpected tool-call records in the second response. |
| [tool-inventory.json](tool-inventory.json) | Parsed model-reported tool schemas with corroboration and uncertainty annotations. Not a backend schema export. |

The 20-request authenticated batch yielded 17 HTTP 200s, one 503, and two 502s. The 21-request unauthenticated batch yielded one 200, five 503s, three 502s, three 400s, and nine 404s. The two later inventory requests both returned 200. These batches exclude additional DNS, HTTP, certificate, passive-DNS, and scan activity.

Failures, empty lookups, and model-reported restrictions are preserved as such. All observed filenames and public-hours answers are model outputs, not verification of real file existence or correct hospital schedules. The full original logs remain local; only selected fields needed to support findings are shared.
