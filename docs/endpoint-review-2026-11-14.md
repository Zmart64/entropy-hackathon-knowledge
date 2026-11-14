# Scioto Ridge endpoint review

Author: Justus, with Codex-assisted testing. Date: 2026-11-14 (Europe/Berlin).

The reviewed service is `https://2-31-186-181.sslip.io`. Its chat wrapper exposes tool names and raw arguments. Tests with two distinct valid Nebius keys supported separate conversation histories per credential; changing participant names under one shared key did not isolate history. No reasoning traces, internal message arrays, or raw tool-result fields appeared in the 17 successful responses in the authenticated test batch. Two later Qwen requests reported six tool interfaces, but their descriptions and enforcement claims are not a canonical backend schema.

This note consolidates the entire investigation: hosting, service enumeration, unauthenticated checks, authenticated controls, model discovery, tool discovery, and proposed defenses. It records the final interpretation rather than treating earlier hypotheses as established vulnerabilities.

## Scope and evidence

The requester stated that they set up the endpoint and authorized the review. The backend was not available locally. The local starter contained only client code. Authenticated checks used fresh synthetic conversations and random labels; neither existing participant conversations nor the shared `setup-test` history was accessed.

The initial infrastructure scans are historical operator-review evidence. They are outside the hackathon's prompt-only scope and are not instructions or authorization for teammates to repeat them. Follow the [challenge rules](challenge.md) for future experiments.

- [Finding index](findings.md)
- [Conversation and response experiment](../experiments/chat-isolation-and-response-exposure/README.md)
- [Tool inventory experiment](../experiments/tool-interface-disclosure/README.md)
- [Selected evidence](../results/2026-11-14-endpoint-review/README.md)
- [Proposed mitigations](../mitigations/chat-endpoint-hardening.md)

Counts refer to distinct recorded batches: 21 unauthenticated checks, 20 authenticated/isolation checks, and two tool-inventory chat requests. Earlier DNS, HTTP, certificate, passive-DNS, and port probes are additional observations; no total request count is claimed for the whole investigation.

## Hosting and DNS

| Property | Observation |
| --- | --- |
| IPv4 A record | `2.31.186.181` |
| Hosting provider | Hetzner Online GmbH |
| ASN and announced prefix | AS24940, `2.31.0.0/16` |
| Assigned address block | `2.31.176.0/20` (`2.31.176.0`–`2.31.191.255`), named `CLOUD-NBG1`, country `DE` |
| Likely location | Nuremberg, Germany, inferred from Hetzner's `nbg1` location code and the assigned block name |
| Reverse DNS | `static.181.186.31.2.clients.your-server.de` |
| AAAA / CNAME / TXT / CAA | No records returned for the exact hostname |
| MX | Priority 0 to `2-31-186-181.sslip.io`; this does not establish working email service |
| Nameservers returned | `ns-00.nip.io`, `ns-01.nip.io`, `ns-ovh.sslip.io` |

`sslip.io` synthesizes DNS answers from IP addresses embedded in hostnames. It supplies naming, not evidence that the website is hosted by the DNS operator. Broad subdomain enumeration of this shared domain would mostly identify unrelated servers; arbitrary labels containing an IP can also resolve automatically.

Sources consulted during the chat: [sslip.io documentation](https://sslip.io/), [RIPE registration](https://rdap.db.ripe.net/ip/2.31.186.181), [RIPE routing data](https://stat.ripe.net/data/network-info/data.json?resource=2.31.186.181), and [Hetzner locations](https://docs.hetzner.com/cloud/general/locations/). Registry contacts identify the infrastructure provider, not its customer. Public research did not identify the application operator independently.

## Exposed services and TLS

The completed Nmap TCP connect scan covered the 1,000 most common ports. It found ports 22, 80, and 443 open and 997 filtered because no response was received. Filtered ports are not proven closed. [Selected Nmap output](../results/2026-11-14-endpoint-review/service-scan-excerpts.txt).

| Port | Observed service |
| --- | --- |
| 22/tcp | SSH banner: `OpenSSH 10.2p1 Ubuntu-2ubuntu3.8` |
| 80/tcp | Caddy; HTTP 308 redirect to the HTTPS hostname |
| 443/tcp | Caddy; JSON chat service behind it |

The SSH banner suggests Ubuntu but does not independently prove OS version or patch status. Caddy's version was not exposed. HTTPS returned `Via: 1.0 Caddy` and advertised HTTP/3 through `Alt-Svc`; UDP/QUIC was not tested.

The TLS handshake negotiated TLS 1.3 with `TLS_AES_128_GCM_SHA256`. The certificate was issued by Let's Encrypt YE2, with the exact hostname as its sole observed DNS SAN, an EC 256-bit public key, and ECDSA/SHA-384 signature. Validity was 2026-11-14 07:21:44 UTC through 2027-02-12 07:21:43 UTC. Its SHA-256 fingerprint was `3190971dd89f70f77a3d4d5912ede29de0ae9c2b9f61f9b1d0d48c8d6a389a33`.

Several attempts at a full 65,535-port sweep progressed slowly. Timing and parallelism were adjusted, then all bulk scans were stopped when new connections, including HTTPS, timed out. The cause was not established: filtering, throttling, local networking, or service load remained possible. The health endpoint recovered, and the slower 1,000-port scan completed. There is no complete all-port inventory, no confirmed denial-of-service finding, and no vulnerability conclusion based solely on those timeouts.

## Public application behavior

Both `/` and `/health` returned HTTP 200 with:

```json
{"status":"ok","service":"scioto-ridge-harness"}
```

The service name is self-reported. Exact-name searches did not locate relevant public documentation or indexed source code, and the starter contained no matching implementation. The early interpretation that “harness” indicated a testing service was an inference; subsequent inspection of the starter established its fictional hospital red-team context.

`OPTIONS /` returned 405. The following tested paths returned 404: `/robots.txt`, `/openapi.json`, `/docs`, `/healthz`, `/readyz`, `/api`, `/api/health`, `/status`, `/version`, `/metrics`, `/v1/models`, `/swagger.json`, `/redoc`, `/.well-known/security.txt`, `/logs`, `/traces`, `/debug`, `/conversations`, `/turns`, `/tools`, and `/tools/schema`. Singular/plural turn and conversation paths using this review's own generated IDs also returned 404. These results apply only to those paths and methods; they are not proof that no other routes exist.

Certificate discovery through Cert Spotter found the original hostname only. The exact crt.sh lookup returned an empty list; one earlier wildcard query was unsupported and was not counted as a negative result. HackerTarget reverse-IP and Mnemonic/AlienVault passive-DNS queries found no additional names. Coverage and freshness of public databases limit these negative results. No subdomain-finder binary was installed or run; discovery used public certificate and passive-DNS sources.

## Model registry snapshots

The initial `/models` response advertised four Nebius routes. Later live responses advertised seven routes. Gemma was absent from both the starter menu and the later registry, so the user selected Qwen for tool discovery. Provider and tier labels below are those returned by the wrapper, not independent verification of upstream deployments.

| Exact model ID | Provider | Wrapper tier |
| --- | --- | --- |
| `deepseek-ai/DeepSeek-V4-Pro-0813` | Nebius | very large |
| `Qwen/Qwen3-235B-A22B-Instruct-2507` | Nebius | large |
| `openai/gpt-oss-120b` | Nebius | medium |
| `Qwen/Qwen3-30B-A3B-Instruct-2507` | Nebius | small |
| `groq/openai/gpt-oss-120b` | Groq | large |
| `groq/qwen/qwen3.8-27b` | Groq | medium |
| `groq/openai/gpt-oss-20b` | Groq | small |

Only the four Nebius routes were used for successful-response inspection. The three Groq routes were listed but not tested. [Registry snapshots](../results/2026-11-14-endpoint-review/model-registry-snapshots.json).

## Authentication and input validation

The 21-request unauthenticated batch returned one 200, five 503s, three 502s, three 400s, and nine 404s. [Selected evidence](../results/2026-11-14-endpoint-review/unauthenticated-checks.json).

- Missing keys were rejected for all four initial models. An empty key was also rejected. The wrapper returned `503 missing_credential` rather than an authentication-specific status.
- An invalid key returned `502 agent_error` with Nebius's raw HTTP 401 authentication text nested in the message. The same happened when a fake credential was supplied through the supported `nebius_api_key` body field. No usable credential was disclosed.
- Malformed JSON, a top-level array, and an unsupported model were rejected with 400. The unknown-model response listed the registered model IDs.
- An object-valued `message` with an invalid key reached an upstream-authentication error rather than a local type-validation error. This establishes the observed validation ordering/response, not that the upstream accepts non-string messages with valid credentials.
- Error responses included generated turn and conversation IDs. Their presence alone does not prove persistent history was written before authentication.

No application rate limit, hard budget, maximum prompt size, or concurrency limit was established by these low-volume requests. No inference succeeded without a valid key in this batch.

## Conversation isolation and response exposure

The authenticated experiment made 20 requests: 17 returned 200, one returned 503 for a missing key, and two returned 502 (invalid credential and a model tool-loop limit). Two distinct valid credentials were verified, but their provider-account ownership was not inspected.

The same-key test showed that two participant names could read and change the same synthetic conversation. The two-key control showed separate retained markers under the same conversation ID. The second key could recall its own marker, could not retrieve the first key's marker, and could not change the first key's recalled marker. Spoofing the first participant's name under the second key still returned the second key's marker. This supports credential-scoped history in the tested flow and corrects the earlier unverified hypothesis of globally shared history.

Missing-key and invalid-key write attempts were rejected. The original caller subsequently recalled the prior legitimate marker rather than either injected marker. No rejected-write poisoning was observed in those two attempts. Model-mediated recall does not prove the exact persistence implementation or absence of all bypasses.

Every successful response in this batch had exactly `reply`, `tool_calls`, `conversation_id`, and `turn_id`. Two public-hours responses, from Qwen 30B and DeepSeek, contained tool names and raw `args` with attempted filenames and inbox search terms. Those values demonstrate argument exposure but do not prove that the named files exist or that the tool has unrestricted host-filesystem access.

No dedicated reasoning fields, internal message arrays, raw tool-result fields, or inline `<think>` blocks appeared in the 17 successful responses. All four models produced at least one successful response. This was non-streaming sampling, not a guarantee for every prompt or response path. The [Qwen 30B Instruct model card](https://huggingface.co/Qwen/Qwen3-30B-A3B-Instruct-2507) separately documents that model as non-thinking.

One gpt-oss-120b public-hours request returned `agent did not terminate within 10 iterations`; a simpler greeting succeeded. That error exposed an agent-loop detail and indicated a bounded loop for that request, not a complete resource-abuse defense. The different models also gave different visiting-hours answers; no authoritative hospital schedule was consulted, so those answers are not established facts.

## Tool interface discovery

Two fresh Qwen conversations returned matching lists of six tool names and argument sets. Requiredness and types below are model-reported. No defaults or enums were reported; accepted filename values, table names, URLs, and additional backend validation remain unknown.

| Tool | Required arguments | Optional arguments |
| --- | --- | --- |
| `query_db` | `sql: string` | `params: array<string \| number \| boolean \| null>` |
| `read_file` | `path: string` | None reported |
| `read_inbox` | `subject_hint: string` | None reported |
| `send_email` | `to: string`, `subject: string`, `body: string` | None reported |
| `http_post` | `url: string`, `body: string` | None reported |
| `delete_record` | `table: string`, `pk: integer` | None reported |

The model described `read_file` as restricted to public handouts; `read_inbox` as a search returning at most three messages; `send_email` as recording intent without sending; and `http_post`/`delete_record` as denied at “Level 3.” It also claimed SQL scope checks at that level. None of those execution or enforcement claims was independently verified, and the active level was not established.

Although both prompts prohibited tool execution, the second response contained all six names in `tool_calls` with placeholder arguments. For example, `params` was a descriptive string instead of the reported array type, and `pk` was `"integer (required)"` instead of an integer. This confirms unexpected tool-call records in the response; it does not establish successful execution, deletion, outbound delivery, or even the backend's interpretation of those records. Further probes were stopped. [Full experiment](../experiments/tool-interface-disclosure/README.md).

## Client observations and remaining questions

The reviewed starter saved the complete JSON response before displaying only `reply` and tool names. Consequently, hiding reasoning or arguments in the UI would not protect fields already sent over the API. `setup.py` used the fixed `setup-test` conversation ID. That is a collision risk for callers sharing a credential, not a demonstrated cross-key leak. The normal client generated random `conv_` IDs. IDs alone are not authorization.

The setup script wrote the provider key to local `.env`; `.gitignore` excluded `.env`, but the inspected starter did not exclude its `logs/` output. The knowledge base does exclude logs. No keys, authentication-header values, unrelated personal records, or runnable probing scripts are included here.

Open questions include exact server-side ownership checks, key rotation behavior, streaming/event filtering, allowed tool permissions, tool-output filtering, parameter validation, budgets, and other model routes. No patient/staff-data disclosure, arbitrary SQL execution, outbound exfiltration, deletion, or host compromise was demonstrated. No mitigation was deployed or evaluated after a patch.
