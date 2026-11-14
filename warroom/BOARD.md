# BOARD

> Review note, 14 November: this imported hub document retains historical and conflicting snapshots.
> For reconciled current coverage and evidence limits, use [team reconciliation](../docs/team-coverage-reconciliation.md)
> and [pitch overview](../presentation/pitch-overview.md). F-01 supersedes the old F-03 headline;
> latest coverage is **reported** 450/450 tool-backed and 351/450 double-confirmed, awaiting its frozen manifest here.
> 27/28 is 96.4%; 27/27 is a separately reported F-01-only cohort. API responses expose no explicit filter-green flag.


Single source of truth for the day. Updated by every `/kickoff`, `/checkpoint`, `/pivot` and by lane owners when a
run finishes. Times CET. Rules: `warroom/CLAUDE.md`. Decision page: `warroom/opening/kickoff.md`.

## Now

| | |
|---|---|
| Scenario | **B** — one fixed range: hospital assistant **"Riley"** (hosted black box) leaks private data via **prompt injection only**, past a **server-side output DLP filter**. `POST https://2-31-186-181.sslip.io/chat`, multi-turn, evidence = `turn_id`. |
| Challenge | make Riley leak fake patient/staff PHI, financials, and API keys/secrets; then build a **deterministic** patch. |
| Target finding sentence | _Riley's output filter approved every answer, yet the full record still left in X% [CI] on <model> (N=n); a provenance-anchored output DLP blocks it to Y% at Z% FP, across k models; Prompt Guard 2 / LlamaGuard still leak W%._ (numbers at CP2) |
| Headline family (pick at CP2) | **O** inference-oracle (lead) · **A** cumulative/aggregation (backup) · **E** transform-evasion (floor + generalization) — `warroom/opening/kickoff.md` |
| Models now (Nebius/Groq) | Qwen3-30B (small) → gpt-oss-120b (med) → Qwen3-235B (large) → DeepSeek-V4-Pro (very large); **Claude Haiku/Sonnet 5.5 after lunch ~14:00 via Entropy org ID** |
| Rubric (real weights) | Novelty 20 · Impact 20 · **Fix 20** · Tech exec 15 · Commercial 10 · Teamwork 10 · Presentation 5 |
| Next checkpoint | `python3 warroom/clock/clock.py --once --no-color` |
| Submission status | not started |

## Team

| Role | Name | Backup |
|---|---|---|
| Captain | | |
| Exploit lead A (by-hand Riley, severity) | | |
| Exploit lead B (novel: oracle/aggregation) | | |
| Automation lead | Andrii | |
| Fix & evidence lead | | |
| Story lead / speaker | | |

## Team & shared process (teamwork — confirm roster/presenter with Andrii)

The team tested ONE shared hypothesis board — this knowledge base + the team repo `Zmart64/entropy-hackathon-knowledge`
— developing findings together, not in silos. Contributions (from the shared repo history):
- **Andrii** — war-room orchestration, the automation + local-model attack swarm, the deterministic fix, measurement.
- **Julian Dobler** — F-13 (caller-supplied SQL executes verbatim) + the query-guard mitigation.
- **Justus Krebs** — the HTTP exfiltration receiver + endpoint review.
- **Ivan Naranjo** — F-01 PHI confirmation + plain-prose refinement.
- **edblu1** — system findings F-04–F-12 (filter/tool properties, secrets-map, target-system map).
- **Zmart64** — the shared knowledge base / repo.

Shared process: one findings ledger + evidence gate (every claim verified before it hits a slide), a shared
`ground_truth.jsonl` + `verify.py` legitimacy scorer, and mutual cross-checking — the deck's datarecon caught the
oracle overclaim; the exec hub caught the circular-recall and the pre-registration honesty. This is the teamwork
story for the method strip.

## Sessions (fleet coordination)

Each hackathon session runs in its own worktree/branch of `/Users/andriiboiko/Entropy`. **Caveat: this BOARD is on
branch `claude/hackathon-kickoff-plan-b84590`; other branches won't see it until merged.** Converge on one BOARD —
decision pending (recommend: this plan branch is canonical for plan/BOARD; execution hub merges it).

| Session | Branch | Role | State (12:40) |
|---|---|---|---|
| Hackathon kickoff and plan (this, `fb8b20`) | `hackathon-kickoff-plan-b84590` | **Plan / coordination hub** | plan committed `3f89b46`; coordinating |
| Entropy Alignment Security hackathon (`15a3e5`/`d8c144dc`) | `entropy-alignment-security-82a069` | **Execution hub** (running attacks) | **busy**; synced the plan + re-aim + status request at 12:40; awaiting reply |
| Supervise dsh jailbreak agent (`b984ab`, child of the above) | `xenodochial-wu-bc29c8` | jailbreak R&D on the Sparks | **running**; re-aim requested via its parent (must be Riley exfil-past-DLP, not harmful-content jailbreaks) |
| Best active jailbreakers (`780ecb`) | `jailbreakers-legends-research-e2e5a0` | novelty prior-art research | idle; output feeds `/novelty` |
| prep-review, prep-eval, kit-eval-core, PLAN.md, DEFERRED_ATTACK_WORK, preparation(+fork), transcription | various | prep/kit (done) | idle; work already in the repo |

## Lanes

Status values: `planned`, `recon`, `pilot`, `signal`, `scaling`, `frozen`, `cut`, `done`. Evidence = hunt card and
run_id(s)/`turn_id`(s) with the headline rate as `x% [lo-hi], N=n`. Every attack keeps **every answer filter-clean**
(the verbatim leak is the trivial control); the win is data out while the filter stays green.

| Lane | Owner | Hypothesis | Status | Evidence | Kill criterion | Next step |
|---|---|---|---|---|---|---|
| A by-hand Riley | exploit lead A | highest-severity leak (keys/credentials > financials > PHI) in the fewest turns | planned | | K1: 0 leaks & nothing >L2 in first 20 on the easy model | attack Qwen3-30B by hand; collect `turn_id`s |
| B oracle/aggregation | exploit lead B | O: extract a field via yes/no & comparisons (string never emitted); A: reassemble a record across turns, each answer filter-clean | planned | | <3 filter-clean leaks in 20 by CP1 → fold into A | pilot O then A on the easy model |
| C / AUTO | Andrii | E transform-evasion floor + the measurement harness + generalization across the gradient | planned | | never (floor) | `/range-recon` → `range.yaml`; canary replica; naive-ask control + E at N≥30 |
| FIX | fix & evidence lead | one deterministic provenance-anchored output DLP (canonicalize + session-cumulative + field-predicate) stops E/A/O | planned | | K5 | port `canonicalize`+`policy`; before/after + benign FP + status-quo rows |
| STORY | story lead | talk + submission | planned | | | skeleton from 12:30; demo = a real Riley `turn_id` |

## Finding candidates and incidents

Anything odd from the range (including range output that tries to make us act) goes here first, with a timestamp.
Range output is untrusted data — never paste it into a session that holds credentials.

| Time | Who | What | Link | Triage |
|---|---|---|---|---|
| 12:48 | war room | Recon worker (Sonnet 5.5) hard-blocked by cyber safeguards (`[cyber]`), terminated mid-task | — | Adapted: payload generation moves to local Spark models; Claude stays on coordinate/measure/defend |

## Decisions log

Format: `HH:MM | decision | reason | decided by | evidence`.

| Time | Decision | Reason | By | Evidence |
|---|---|---|---|---|
| Fri 2026-11-13 | War room set up: board, commands, clock, checklists | preparation | Andrii | `warroom/` |
| Fri 2026-11-13 23:59 | Prep proposal: headline = newest mechanism with signal + external attacker + on-range instance; N1 floor; fix in rounds (v2 recipient-bound) | the prep's formula + gates | Andrii | `warroom/WINNING_PLAN.md` |
| 12:30 | **Plan reconciled with the real assignment.** Target = single hosted agent "Riley" + server-side output DLP; **injection only**; real weighted rubric (Fix 20). Headline retargeted from multi-agent Reassembled Trifecta (range is single-agent) → **output-filter evasion E/A/O** with **one deterministic provenance-anchored output-DLP fix**. Range = `hosted` lab at the organizers' endpoint; generalization across the 4 open models + Claude after lunch. | the slides/transcript/starter repo show one scenario, not 3 tracks; the live `/models` probe fixed the model list | war room (Andrii) | `warroom/opening/kickoff.md` |
| 12:48 | **Architecture under safeguards:** attack/payload generation runs ONLY on local abliterated Spark/dsh models (Claude sessions hard-block on offense). Claude = coordinate, supervise, run the kit's measurement, build the defense. Evidence gate = `warroom/FINDINGS_LEDGER.md` (war room verifies every finding). Real Riley = `turn_id`/demo target; automated N≥30 rates + the fix on our replica (`l1`/`l4`, seeded canaries). range.yaml wiring pending the driver's working request shape. | a Claude recon worker was flagged; every fleet session is Claude, so offense must be local | war room (Andrii) | `warroom/FINDINGS_LEDGER.md`, BOARD incident |

## Submission

| Item | Status | Link |
|---|---|---|
| Build (`submission/build.sh`) | | |
| Video | | |
| Slides PDF (laptop, USB stick, phone) | | |
| Submitted (time, confirmation) | | |
