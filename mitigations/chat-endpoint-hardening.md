# Chat endpoint hardening proposal

Author: Justus, with Codex-assisted testing. Date: 2026-11-14.
Status: proposed; no server changes or before/after mitigation evaluation performed.

These controls address the [recorded findings](../docs/findings.md). The two-key experiment already supports credential-scoped history; preserve that behavior rather than treating the earlier global-history hypothesis as a confirmed defect.

## Public response serialization

Construct a dedicated public response containing the approved final answer, caller-owned conversation ID, and turn ID. If tool visibility is needed for the client, expose only an allowlisted tool name. Remove `args` unless there is an explicit authorization and product requirement to disclose a particular field. Do not forward full provider/agent objects.

Separate final output from reasoning using the applicable provider/model parser. Exclude internal messages, raw tool results, reasoning channels, and debugging traces from every outward path, including streaming events and error handling. No such fields were observed in this sample, so these are regression requirements. Apply privacy checks to all public fields, not only `reply`. UI hiding does not protect JSON already returned to callers.

Test with harmless canary values in tool arguments, internal reasoning fields, tool results, errors, and stream fragments. Assert that only authorized final content and approved metadata reach the caller. Existing pre-fix evidence confirms raw tool-argument exposure; no post-fix result exists.

## Identity and conversation ownership

Keep distinct credentials for distinct users. For enrollment, revocation, and per-user quotas, issue an application credential independently of the upstream provider key. Derive identity from authenticated server context, never the submitted participant name. A provider key is a bearer secret and is not a durable account identity across rotation.

Bind all history reads, writes, exports, and resets to the authenticated owner. Generate fresh conversation IDs and replace the fixed `setup-test` value with a unique ID; random IDs complement ownership checks rather than replacing them. Ensure failed authentication cannot create or append user history.

Regression tests should cover two separate credentials with the same conversation ID, participant-name spoofing, failed writes, concurrent turns, key rotation, and legitimate owner continuation. The current two-key controls passed; shared-key participant isolation did not exist and should not be advertised.

## Tool execution permissions

Enforce tool eligibility and argument types before dispatch. For example, a deletion primary key declared as an integer must not accept `"integer (required)"`, and SQL parameters declared as an array must not accept explanatory prose. Documentation-only requests should use a server-side path that cannot dispatch tools.

Keep the challenge dataset synthetic and isolated from the host and real operational data. Use constrained database identities, parameterized queries and table/operation allowlists, a restricted public-file root, and explicit inbox permissions. Remove general external HTTP or destructive tools unless the application needs them and an independently enforced policy permits them. Validate outbound destinations if network access is required. Do not infer permission from the model's “Level 3” claims or from a system-prompt instruction.

## Authentication errors and secret handling

Reject missing/invalid application credentials before expensive agent work. Return stable application error codes; use appropriate 401/403 responses for application authentication/authorization rather than forwarding provider errors as 502/503. Keep diagnostic details in access-controlled server logs. The observed errors disclosed upstream authentication text and a tool-loop limit, not a credential or stack trace.

Explicitly redact both the `X-Nebius-Key` header and the accepted `nebius_api_key` body field at every logging layer. Never place credentials in model input. Prefer header-only credentials if body transport is unnecessary. Keep local `.env` private and exclude complete local response logs from Git. Preserve research retention requirements through intentional, access-controlled storage rather than indiscriminate logging.

## Resource controls

Apply per-user and aggregate request, token, cost, concurrency, input-size, history-size, and execution-time budgets. Bound tool iterations, retries, queue depth, stored conversations, and log volume. Authenticate before allocating expensive work. Add budget cutoffs, anomaly alerts, and cancellation propagation.

For a small pilot, 10 requests/minute/user, two concurrent requests/user, a 16 KiB request-body limit, and a 2,000-output-token cap are illustrative starting values, not measured capacity recommendations. Tune them against actual legitimate workloads. The observed ten-iteration error proves only that a bound was reached on one request. Nebius's dynamic rate limits are not a substitute for application budget enforcement.

## Infrastructure

Restrict SSH to administrators through a VPN or source-IP allowlist, use key-based access, and patch host packages. Bind the backend privately behind the intended reverse proxy and firewall unused ports. A custom hostname or hidden health banner is not authentication. If a gateway is introduced, prevent direct-origin access from bypassing its controls.

The earlier scan covered 1,000 TCP ports and did not inspect the server from inside. No infrastructure configuration change or vulnerability-specific patch recommendation is justified solely by the observed banners.

## Evaluation required

Before claiming a fix, rerun authorized synthetic chat controls in an isolated environment, inspect complete JSON and supported streams, check appropriate failures before tool dispatch, and verify representative legitimate conversations still work. Report attack successes/attempts and legitimate-request outcomes before and after each actual patch. Follow [challenge scope](../docs/challenge.md); do not repeat infrastructure scans as part of the prompt-only competition.

Sources: [OWASP object-level authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/), [resource consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/), [sensitive information disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/), [excessive agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/), and [Nebius rate-limit behavior](https://docs.tokenfactory.nebius.com/ai-models-inference/rate-limits.md).
