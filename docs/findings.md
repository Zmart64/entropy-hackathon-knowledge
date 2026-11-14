# Confirmed findings

Author: Justus, with Codex-assisted testing. Date: 2026-11-14.

The [Scioto Ridge review](endpoint-review-2026-11-14.md) records the endpoint investigation and its evidence. The results below concern API behavior and synthetic conversation state. No private patient/staff-data leak or novelty claim has been established.

| ID | Finding | Evidence and limits |
| --- | --- | --- |
| F01 | Raw tool names and arguments are returned to the caller. | Two public-hours responses contained `tool_calls[].args` with filenames/search terms. Arguments may expose data outside a filtered final reply, but no private record was demonstrated. [Experiment](../experiments/chat-isolation-and-response-exposure/README.md). |
| F02 | Participant names do not isolate history within a shared key. | One same-key/different-name read retrieved the prior marker; one write became visible to the original participant. No separate identity is established by the submitted name. [Experiment](../experiments/chat-isolation-and-response-exposure/README.md). |
| F03 | Provider and agent error details are returned. | Invalid credentials exposed upstream authentication text; one gpt-oss request exposed a ten-iteration agent limit. No API key or stack trace was observed. [Unauthenticated evidence](../results/2026-11-14-endpoint-review/unauthenticated-checks.json) and [chat evidence](../results/2026-11-14-endpoint-review/chat-cases.json). |
| F04 | The model disclosed six tool interfaces in two fresh chats. | Names and argument sets matched across replies and response tool-call entries. Types, requiredness, descriptions, and completeness remain model-reported. [Experiment](../experiments/tool-interface-disclosure/README.md). |
| F05 | A documentation-only request produced tool-call records. | One of two inventory requests returned entries for all six tools despite an explicit no-execution instruction. Placeholder/type-invalid arguments and absent results prevent a claim of successful execution. [Evidence](../results/2026-11-14-endpoint-review/tool-inventory-cases.json). |
| F06 | A non-string message did not receive local type rejection. | One object-valued `message` with a fake key produced the upstream authentication error. This shows the observed validation response; valid-key acceptance or coercion of that input is unverified. [Evidence](../results/2026-11-14-endpoint-review/unauthenticated-checks.json). |

## Negative results and observed protections

- **Separate valid keys retained separate history in the tested flow.** Key B failed to retrieve A's marker, B's write did not affect A's recalled marker, and B recalled its own marker even while spoofing A's participant name. One two-key experiment with positive controls; exact implementation remains unknown.
- **Missing/fake-key history poisoning was not reproduced:** zero injected-marker recalls in two readback checks. The prior valid marker remained visible.
- **No reasoning traces, internal message arrays, or raw tool-result fields were observed** in 17 successful non-streaming responses across four models. This does not cover all prompts, streaming, or the subsequently listed Groq routes.
- **All four initial model routes rejected missing keys.** Malformed JSON, top-level arrays, and an unsupported model were rejected. Tested log/trace/schema routes returned 404.
- **No additional public hostnames were discovered** in the certificate/passive-DNS sources queried. This is not an exhaustive domain inventory.

## Important corrections

The shared `setup-test` ID originally raised a hypothesis of globally shared conversation state. The later two-key controls did not reproduce that hypothesis. The demonstrated collision risk is within a shared credential. Similarly, early concern about thinking-trace exposure was not confirmed; raw tool-argument exposure was confirmed instead.

Infrastructure metadata and the incomplete all-port scan are recorded in the [review](endpoint-review-2026-11-14.md). Three ports were open among 1,000 tested; this is not proof that only three ports are exposed. Temporary timeouts are not a confirmed denial-of-service vulnerability.

## Follow-up and mitigations

Prioritize a server-side response allowlist, argument redaction, deterministic identity/ownership checks, strict validation, sanitized errors, and resource controls. See the [mitigation proposal](../mitigations/chat-endpoint-hardening.md). No fix has been deployed, and no before/after evaluation has been performed.

Relevant existing categories include OWASP object-level authorization, resource consumption, sensitive information disclosure, and excessive agency. [Prior-work notes](prior-work.md) describe the relationship; no originality or challenge-submission success is claimed.
