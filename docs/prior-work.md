# Prior work

Record relevant literature as it is reviewed. No novelty claims have been established yet.

| Source | Mechanism | Relationship to our experiment | Specific difference | Reviewed by / date |
| --- | --- | --- | --- | --- |

Use primary sources where possible. Record search terms and scope when assessing novelty; not finding a paper does not prove that no prior work exists.

## Sources reviewed for the endpoint investigation

Reviewed by Justus with Codex on 2026-11-14. These sources establish existing risk categories and relevant product behavior, not novelty or proof of a vulnerability in this service.

| Source | Relationship to the observed findings | Specific limit |
| --- | --- | --- |
| [OWASP API1 object-level authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/) | Motivated ownership checks when a caller supplies conversation_id. | The two-key experiment supported isolation; a cross-key authorization flaw was not reproduced. |
| [OWASP API4 resource consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/) | Supports request, token, concurrency, storage, and budget controls. | No application stress test or cost-amplification exploit was performed. |
| [OWASP LLM02 sensitive information disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/) | Raw tool arguments and verbose errors are outward information channels. | Only attempted paths/search terms and diagnostic details were demonstrated; no private hospital records. |
| [OWASP LLM06 excessive agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) | A documentation request returned tool-call records despite asking for no execution. | Successful tool execution and side effects were not established. |
| [Qwen 30B Instruct model card](https://huggingface.co/Qwen/Qwen3-30B-A3B-Instruct-2507) | Documents the selected model as non-thinking. | Does not prove wrapper behavior, all prompts, or other models are free of trace exposure. |
| [Nebius rate limits](https://docs.tokenfactory.nebius.com/ai-models-inference/rate-limits.md) | Describes dynamic provider rate limits; application budget enforcement remains necessary. | No account-specific limits were measured. |

Exact-name searches for `scioto-ridge-harness`, variants containing `scioto-ridge`, and the endpoint hostname/IP did not locate relevant public implementation documentation. This was service identification, not a comprehensive literature review or evidence of originality. Tavily was unavailable due to a usage limit; public web sources and direct registry requests were used instead.
