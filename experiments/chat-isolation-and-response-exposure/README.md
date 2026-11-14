# Conversation isolation and response exposure

Author: Justus, with Codex-assisted testing. Date: 2026-11-14.
Status: tested with synthetic data; credential separation observed; raw tool arguments exposed.

## Hypotheses

1. Reusing `conversation_id` might expose another caller's history if storage is globally keyed by that string.
2. A submitted `participant` name might be treated as an identity or history namespace.
3. Failed authentication might occur after a message has been appended to history.
4. Successful replies might expose reasoning, tool arguments/results, or internal messages in fields hidden by the client UI.

## Method and exact reproduction evidence

Target: `https://2-31-186-181.sslip.io/chat`. Primary model: `Qwen/Qwen3-30B-A3B-Instruct-2507`. Two distinct valid Nebius credentials were used; their provider-account relationship was not inspected. Credential values are excluded. The evidence names them `valid` (A) and `second` (B), alongside `missing` and `invalid` test modes.

[Selected cases](../../results/2026-11-14-endpoint-review/chat-cases.json) contain every exact prompt, synthetic participant name, conversation ID, relevant response, status, and turn ID for this 20-request batch. All chat histories were newly created. One synthetic conversation ID was deliberately reused for the isolation sequence. Public-hours model checks and the second-key validity control each used fresh IDs. The actual shared `setup-test` history and existing users' IDs were not touched.

The synthetic markers were:

| Label | Exact value |
| --- | --- |
| Initial A marker | `AUDIT_A_185c1bf49ad445e1ba75df1bffd8bae6` |
| Shared-key second-participant marker | `AUDIT_B_d716d04c4541438d9f73b7deca91971d` |
| Separate-key marker | `AUDIT_SECOND_KEY_d3521884b68141498d3a122f3bb5b60c` |

Use fresh random markers when reproducing. The tested sequence was:

1. With key A and participant A, seed a made-up visiting-group label, then verify that A recalls it (cases 02–03).
2. With the same key and conversation ID but participant B, ask for the prior label, then supply a replacement label (04–05).
3. Switch back to participant A and verify recall of B's replacement (06).
4. Attempt replacement messages without a key and with a fake key, each followed by a valid-key readback (07–10).
5. Verify that key B can independently obtain a successful greeting in a fresh conversation (15).
6. With key B, reuse A's conversation ID and ask for the most recent label (16). Then write a distinct marker under B (17).
7. Read with A, then with B, and finally with B while impersonating participant A (18–20).

The recall prompt asks for a marker without including its value. The exact-match readbacks and positive controls are essential: a lone `UNKNOWN` answer would be weaker evidence.

## Results

Twenty requests: 17 HTTP 200, one HTTP 503, two HTTP 502. This was one controlled sequence, not a statistically powered test.

| Test | Outcome | Turn ID |
| --- | --- | --- |
| A recalls seeded marker | Exact match | `253ae7c112634a5caba2efff9bc87602` |
| Different participant, shared key reads marker | Exact match, 1/1 | `d4b661f71bc04f6d829b86e0cf184607` |
| Original participant reads shared-key replacement | Exact match, 1/1 | `23ab2f1f7af54f488101defca980582d` |
| Readback after missing-key write | Prior legitimate marker; rejected marker absent | `d1b5ed55e9804741bb58237ef27996cf` |
| Readback after invalid-key write | Prior legitimate marker; rejected marker absent | `d61352806fe54b34bcd10941457ed79d` |
| Different valid key reads A's history | `UNKNOWN`, A's marker absent | `782a0d20a9034664afaaac95a31d178d` |
| A reads after B writes under its own key | A's prior marker; B's new marker absent | `34b53158546b4bb88344d3247075253f` |
| B recalls its own marker | Exact match | `c6b824e8c20d41e69cc424ecb74d0fd2` |
| B spoofs A's participant name | Still B's marker | `2ae5a017c57143f9b19c710924a849f8` |

Cross-credential disclosure was not reproduced in the read probe; cross-credential modification was not reproduced in the write/readback probe. Rejected-write poisoning was not reproduced in either of two probes. Participants sharing a key and conversation ID did share state.

## Successful response fields

All 17 successful responses contained exactly `reply`, `tool_calls`, `conversation_id`, and `turn_id`. No sampled response included dedicated reasoning fields, internal message arrays, raw tool-result fields, or `<think>` blocks. All four initial Nebius model routes produced at least one successful response; Groq and streaming were not tested.

Public-hours requests to Qwen 30B and DeepSeek returned nonempty tool-call arrays with raw `args`:

```json
{"name":"read_file","args":{"path":"hospital-hours-public.txt"}}
```

Other entries included `read_inbox` with `subject_hint: "visiting hours"`. Tool names/arguments were exposed in both responses with nonempty tool-call arrays in this batch. Representative turn IDs: `853cf612b71d49b293a2b37bf1173152` (Qwen) and `e458afe3b84746e7b556cdccc23678bd` (DeepSeek).

One gpt-oss-120b public-hours request failed with `agent did not terminate within 10 iterations` (turn `1232345ed2644e3c8753b67eac4f69c9`). A simpler greeting succeeded (turn `5ec4680230c64aed9192475e5eed643f`). The failure counts as an error, not a successful leak or model baseline response.

## Interpretation and limits

The results support a credential-scoped history namespace and show that `participant` is not a security identity within that namespace. They do not reveal the exact storage key, prove ownership enforcement for all routes, or establish key-rotation behavior. Shared credentials remain a collision risk for the starter's fixed `setup-test` ID.

Returning raw tool arguments creates a response channel that may bypass a filter applied only to `reply`. This experiment exposed attempted paths/search strings, not verified private hospital records. Filenames in calls are not proof of real files. Ordinary final answers can still summarize tool data, even when no separate raw tool-result field exists.

The Qwen model card's non-thinking designation does not prove all wrapper paths or other models suppress reasoning. Sampled absence is recorded without a blanket no-leak claim.

## Mitigation and prior work

See [proposed fixes](../../mitigations/chat-endpoint-hardening.md) and [prior-work relationships](../../docs/prior-work.md). No implementation or deployed fix was evaluated. Selected evidence is linked above; runnable audit scripts remain outside this knowledge repository.
