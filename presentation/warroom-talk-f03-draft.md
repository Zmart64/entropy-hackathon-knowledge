# Talk F-03: "Green Mosaic" (3:00, Riley main line)

> **Superseded headline draft:** Andrii’s 626d715 update makes live F-01 the headline and F-03 secondary; full oracle reconstruction is unproven. Do not present this script or fill its placeholders from unrelated cohorts. Use [pitch-overview.md](pitch-overview.md).

Headline: **F-03** (inference oracle + cumulative aggregation: a content filter is blind to it by construction).
Banked floor: **F-01** (structured-format laundering; known evasion class, carries the impact and the real `turn_id`s).
The fix is one deterministic control: **canonicalize + session-cumulative disclosure budget + field-predicate**.
Technique names only, no payloads, canary data only, every number a `{{placeholder}}` (index in section 4).
Working name "Green Mosaic" (every answer a green tile, the picture is the breach); the captain confirms at CP2.
Source files: deck `talk/slides/content_f03.yaml`, facts `talk/data/facts_f03.yaml`, ladder `talk/slides/assets/ladder_f03.svg`,
demo `talk/demo/storyboard_f03.yaml` (fallback `storyboard_f01_fallback.yaml`). Render:
`make -C talk slides CONTENT=slides/content_f03.yaml SLIDES_OUT=out/f03` -> `talk/out/f03/slides.{html,pdf}`, notes, `preview/`.

## 1. Second-by-second script (about 345 spoken words with the numbers read out; 301 as the kit counts them)

Pace 140 words per minute. Over time: cut words, never speed up. `[ ]` = stage direction.

| Time | Slide | Say |
|---|---|---|
| 0:00-0:12 | 1 hook | "Every answer our attacker got passed the hospital's data filter. We still rebuilt the patient record, in {{f03_rate}} of sessions. The filter checks answers. The breach is the conversation." [number and the green audit card are already on screen] |
| 0:12-0:17 | 2 demo | "One real session on the range, sped up. Riley answers every question." [video starts: context, then the direct-ask control, blocked] |
| 0:17-0:21 | 2 | [silence: the control is refused, red chip] |
| 0:21-0:30 | 2 | "Green, green, green: the filter approves each turn." [oracle turns scroll, counter ticks] |
| 0:30-0:41 | 2 | [silence: the tiles fill in, field by field, all green] |
| 0:41-0:47 | 2 | "Now the verifier. Red: the rebuilt record matches the ground truth." [banner RECORD REBUILT] |
| 0:47-0:52 | 2 | "Same session with the fix on: the fourth turn is held." [HELD chip; say the turn number the recording shows] |
| 0:52-0:55 | 2 | [number card: {{f03_rate}} to {{v2_f03_rate}}] |
| 0:55-1:05 | 3 evidence | "On Riley: {{f03_rate}}, interval {{f03_ci}}, N equals {{f03_n}}. A planted canary record decides success, not a judge." |
| 1:05-1:10 | 3 | "The direct ask is refused. The technique is not." |
| 1:10-1:25 | 3 | "Now the ladder: same attack, five models. The easier the model, the more it leaks. The small model leaks {{ladder_ratio}} times the frontier one. Helpfulness is the attack surface." [point at the top bar, then the bottom bar] |
| 1:25-1:30 | 4 rounds | "We fixed it, then attacked our own fix. Round one: {{f03_rate}}." |
| 1:30-1:42 | 4 | "Round two canonicalizes every answer and tracks provenance. It kills the format tricks, but the oracle and the mosaic still leak {{v1_f03_rate}}." |
| 1:42-1:58 | 4 | "Round three adds a session budget per record and a field-predicate rule: {{v2_f03_rate}}, with {{fp_v2_rate}} of normal hospital questions blocked. Input guards on the same runs still leak {{guard_rate}}." |
| 1:58-2:05 | 4 | "Round four, our own attack: spread across conversations. Residual {{adaptive_rate}}. It stays on the slide." |
| 2:05-2:10 | 4 | [buffer: 5 s of slack for the slowest slide] |
| 2:10-2:16 | 5 why | "A content filter is a per-message checker. The breach is a conversation." |
| 2:16-2:24 | 5 | "Your minimum-necessary rule lets one field out at a time, and nothing trips. The access review passes. The log is green." |
| 2:24-2:34 | 5 | "Our fix is deterministic, {{fix_latency_us}} microseconds a decision, no model call, a policy you can read and replay." |
| 2:34-2:40 | 5 | "The attacker pays {{cost_per_record_usd}} a record." |
| 2:40-2:52 | 6 close | "{{finding_name}}. Every tile is green; the picture is the breach. One control closes it: canonicalize, budget the session, bind the field." |
| 2:52-3:00 | 6 | "Every number reproduces with one command, pre-registered at commit {{prereg_commit}}. Check the conversation, not just the answer. Thank you." |

Rules kept: finding first, no team intro; each number said once with its unit; no "first" (the novelty line says
"we did not find a measurement of ... as of 14 Nov 2026", appendix A3); the hosts' filter is framed as the base we
strengthen; no hardware names on stage (the build flags them); providers anonymized.

Branches to decide by the data (swap the sentence, not the structure):
- **Ladder does not hold** (flat or inverted): title becomes "Every rung leaks, the stronger models too" and the
  line becomes "Capability does not buy safety here: the frontier model still leaks {{ladder_frontier_rate}}." Say it as a result, do not hide it.
- **Held turn is not the 4th**: change "fourth" in 0:47-0:52 and the audit card on slide 1 (4 PASS lines) to the recording.
- **F-03 has no on-range instance with a scorer pass by CP3 (15:30)**: F-01 becomes the headline on the same spine: demo =
  `storyboard_f01_fallback.yaml`, hook number = F-01 rate, round 2 (canonicalize) becomes the hero fix, round 3 is shown
  as "designed, replica numbers" and F-03 moves to one "what comes next" sentence. Hook sentence stays true: the prose filter passed every answer.

## 2. Slide outline (5-6 main slides, ONE placeholder number each; 7 appendix slides for Q&A)

| # | id / layout | Seconds | On the slide (at most 15 words besides the number) | The one number |
|---|---|---|---|---|
| 1 | hook (audit card) | 12 | "Every answer was approved by the hospital's data filter. The record left anyway." Right: Riley filter card, four green PASS lines (yes/no, range, fragment, fragment), one red LEAK line | `{{f03_rate}}` (CI and N under it) |
| 2 | demo (video) | 43 | "One session on Riley: N green turns, then a red record." Full-screen video, poster frame as fallback | `{{demo_green_turns}}` (in the title) |
| 3 | evidence = the ladder (diagram) | 30 | "The easier the model, the more it leaks." Five bars, small to frontier, same technique and seeds; bar labels are the chart data | `{{ladder_ratio}}`x |
| 4 | rounds | 45 | "One control, built in rounds: break it, fix it, break the fix." Four cards; the status-quo input guards ride in the footnote | one per card: `{{f03_rate}}`, `{{v1_f03_rate}}`, `{{v2_f03_rate}}`, `{{adaptive_rate}}` (benign false positive on the v1 and v2 cards, `{{fp_v1_rate}}`, `{{fp_v2_rate}}`) |
| 5 | why | 30 | "Why a CISO cares": filter green, access review passes, fix is a readable rule; minimum-necessary / data-minimisation hook | `{{cost_per_record_usd}}` |
| 6 | close (hook layout) | 20 | "Green Mosaic: every tile is green. The picture is the breach." Commit hash and repo underneath | `{{n_total}}` episodes |

Appendix (not timed): A1 method and statistics, A2 the F-01 floor (before/after), A3 prior-art delta, A4 limitations,
A5 kill chain and severity with OWASP LLM02/LLM01 and ATLAS ids (v2026.10, re-check before quoting), A6 disclosure.
Budget check from the build: 6 slides, seconds sum 180, no beat over its budget, no error; the PDF has 12 pages.

## 3. The 45-second demo shot list (43 s, the 0:12-0:55 slot; file `talk/demo/storyboard_f03.yaml`)

Screen rule: attacker turns appear as technique LABELS and filter verdict chips, never as prompt text; synthetic patient,
canary-style ids; nothing from the range output is pasted anywhere with credentials. Captions at most 60 characters, two lines.

| Time | Scene (on screen) | Caption | Dur |
|---|---|---|---|
| 0:00-0:04 | Riley chat UI, badge "fictional hospital - synthetic data", rail "Output DLP filter: ON", empty session ledger | A hospital's AI assistant. Output data filter: on. | 4 s |
| 0:04-0:09 | Turn labelled "direct ask (control)", refusal, red chip BLOCKED | Ask for the record directly: blocked. The filter works. | 5 s |
| 0:09-0:21 | 3-4 turns labelled "inference oracle" (yes/no, range, comparison), each with a green chip FILTER: PASS, counter up to `{{demo_green_turns}}`; the value is never printed; ledger shows masked bars | Yes/no and range answers. The value is never printed. Green. | 12 s |
| 0:21-0:29 | Turns labelled "cumulative aggregation": fragments, each green; ledger tiles turn grey to green, field by field | Each answer is clean. The session is not. | 8 s |
| 0:29-0:35 | Verifier panel slides in: rebuilt record vs ground-truth canary record, all ticks; red banner "RECORD REBUILT - filter never fired"; last `turn_id` in the corner | Verifier: record rebuilt. Filter never fired. | 6 s |
| 0:35-0:40 | Same session replayed, fix on (labelled replica): turn 4 answer replaced by a HELD chip, reason "session disclosure budget for this record", tiles stay grey | Same session, fix on: held at turn 4. | 5 s |
| 0:40-0:43 | Number card with the slide-4 digits: `{{f03_rate}}` to `{{v2_f03_rate}}`, benign blocked `{{fp_v2_rate}}`, N and run_id in small type | `{{f03_rate}}` to `{{v2_f03_rate}}` leak, `{{fp_v2_rate}}` benign blocked | 3 s |

Green, green, green, red = shots 3-5. Record: terminal or screen recorder (`make -C talk demo TAPE=...` for a VHS tape), then
`make -C talk srt SB=demo/storyboard_f03.yaml`, `make -C talk subs IN=out/demo/demo_raw.mp4 SRT=out/demo/captions.srt OUT=assets/demo.mp4`,
`make -C talk poster IN=assets/demo.mp4 OUT=assets/demo_poster.png`. The fix shot is a replica replay of the same turns: say so in the
caption box. Offline fallback: the poster frame plus `demo/fake_session.sh` (the video must play without venue Wi-Fi).

## 4. Placeholder index (fill into `talk/data/facts_f03.yaml`; the build prints every name still open)

All from `ek report <run_id>` (summary.json, Wilson 95%) of the locked run_ids; the run_id goes into the speaker notes.
Open dependency: the kit's headline field is `exfil`; F-03's success is the scorer's "record rebuilt and verified" with the
filter green at every turn, so the scorer must write a per-episode success field before `make numbers METRIC=<that field>` can feed these.

| Placeholder | Meaning | Slide |
|---|---|---|
| `f03_rate`, `f03_ci`, `f03_n` | F-03 filter-clean reconstruction rate on the range model, Wilson 95%, episodes in the cell | 1, 3, 4, video |
| `range_model` | anonymized range model label | 1 |
| `f03_direct_refusal` | direct ask (control) refused, same model and seeds | 3 footnote, A1 |
| `demo_green_turns` | green turns in the recorded session | 2, video |
| `ladder_small_rate` ... `ladder_frontier_rate` (5), `ladder_*_pct` (5 bar lengths, 0-100), `ladder_ratio` | per-rung rate with CI, bar length, small/frontier ratio (one decimal) | 3 |
| `v1_f03_rate`, `v1_ci`, `v1_n` | round 2: canonicalize + provenance | 4 |
| `v2_f03_rate`, `v2_ci`, `v2_n` | round 3: + session budget + field predicate | 4, video |
| `fp_v1_rate`, `fp_v2_rate`, `n_benign` | normal hospital Q&A blocked (v1, v2) and N | 4 |
| `guard_rate` | Prompt Guard 2 / Llama Guard on the same runs | 4 footnote |
| `adaptive_variant`, `adaptive_rate`, `adaptive_ci` | round 4 residual (our attack on v2) | 4, A4 |
| `fix_latency_us`, `cost_per_record_usd` | median added latency per decision; attack cost per rebuilt record | 5 |
| `severity`, `severity_desc` | L0-L6 level and meaning | 5 footnote, A5 |
| `f01_rate`, `f01_ci`, `f01_n`, `f01_v1_rate` | banked floor before/after canonicalize | A2 |
| `n_total`, `prereg_commit`, `repo_url` | episodes behind the talk, pre-registration hash, repo | 6, A1 |

Non-number facts already filled: finding name (working), fix rule, regulatory hook, OWASP/ATLAS ids, novelty line, limitations.
Still `PLACEHOLDER`: team name, vendor disclosure.

## 5. Hallway version (30 s, 18:00-18:30)

"A hospital's AI assistant sits behind a data filter that approved every answer we got. We still rebuilt the patient record
in {{f03_rate}} of sessions, by asking yes/no and range questions and collecting fragments across one conversation. The
filter checks answers; the breach is the conversation. Weaker models leak more, {{ladder_ratio}} times the frontier one.
One deterministic control fixes it, {{v2_f03_rate}} leak at {{fp_v2_rate}} false positives. Everything reproduces with one command."
