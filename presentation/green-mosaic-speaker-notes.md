# Speaker notes: Green Mosaic

Talk estimate 164 s (budget 180 s, limit 180 s) at 140 words/min; video slides count the video length.
Beat boundaries: hook ends 0:12; demo ends 0:55; killchain ends 1:25; evidence ends 1:51; rounds ends 2:36; close ends 3:00.

## 1. hook (12 s budget, ~14 s estimate, 33 words)

Every answer passed the hospital's data filter. One structured answer carries a whole table of
records past a filter that checks one answer at a time. Hundreds of patients, read from the database.

## 2. demo (43 s budget, ~43 s estimate, 41 words)

One real session on the range, sped up. Riley answers every question. Green, green, green: the
filter approves each turn. Now the verifier. Red: the rebuilt record matches the ground truth.
Same session with the fix on: the turn is held.

## 3. killchain (30 s budget, ~29 s estimate, 67 words)

How does it get out? Riley runs the SQL we write, verbatim: thirty out of thirty fresh chats.
The filter behaves like a pattern redactor: a social-security shape and a fixed token list. Ask
for the rows as a table and they pass. The answer itself is the exfiltration channel: no tool to
send, the record is just there. Credentials Riley refuses, and a dedicated oracle too.

## 4. evidence (26 s budget, ~19 s estimate, 44 words)

The sixty-five percent headline breaks into the two models, per conversation: the small model
leaks a real record in eighty-nine percent of conversations, the large one in fifty-nine. The
smaller, more helpful model leaks more. Claude Haiku and Sonnet are pending the organizer token.

## 5. rounds (45 s budget, ~31 s estimate, 72 words)

You need both controls. The query scope is primary: on the live range, Level 3's scope alone blocked
all twenty-six patient queries; our reference query guard is fixture-tested. The output DLP is the
defence in depth for where scope is absent or must allow a read: it blocks every one of the
thirty-two leaking conversations by matching the values the agent read, at twenty-three percent of
hard benign questions. No model call.

## 6. close (24 s budget, ~28 s estimate, 66 words)

Green Mosaic: every answer is a green tile, and one tile can carry a whole table. Two controls
close it: scope the query, and an output check that matches the records the agent read. The product
is an output DLP with memory, a gateway in front of any assistant. One harness, one ledger, every
finding re-verified. Check the answer against what the agent read. Thank you.

## 7. A1 (appendix, ~0 s estimate, 0 words)

(no notes)

## 8. A2 (appendix, ~0 s estimate, 0 words)

(no notes)

## 9. A3 (appendix, ~0 s estimate, 0 words)

(no notes)

## 10. A4 (appendix, ~0 s estimate, 0 words)

(no notes)

## 11. A5 (appendix, ~0 s estimate, 0 words)

(no notes)

## 12. A6 (appendix, ~0 s estimate, 0 words)

(no notes)
