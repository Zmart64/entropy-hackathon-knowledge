# Speaker notes: Green Mosaic

Talk estimate 125 s (budget 180 s, limit 180 s) at 140 words/min; video slides count the video length.
Beat boundaries: hook ends 0:12; demo ends 0:55; killchain ends 1:25; evidence ends 1:51; rounds ends 2:36; close ends 3:00.

## 1. hook (12 s budget, ~12 s estimate, 28 words)

Every answer passed the hospital's data filter. Every patient's record still left, read from the
database, returned as tables. The filter checks answers; the breach is the conversation.

## 2. demo (43 s budget, ~18 s estimate, 41 words)

One real session on the range, sped up. Riley answers every question. Green, green, green: the
filter approves each turn. Now the verifier. Red: the rebuilt record matches the ground truth.
Same session with the fix on: the turn is held.

## 3. killchain (30 s budget, ~29 s estimate, 67 words)

How does it get out? Riley runs the SQL we write, verbatim: thirty out of thirty fresh chats.
The filter behaves like a pattern redactor: a social-security shape and a fixed token list. Ask
for the rows as a table and they pass. The answer itself is the exfiltration channel: no tool to
send, the record is just there. Credentials Riley refuses, and a dedicated oracle too.

## 4. evidence (26 s budget, ~20 s estimate, 47 words)

Same harness on two open models. Both leak real records while the filter stays green: sixteen
percent of attack messages on the small model, ten on the large one. The smaller one trends
higher, but the intervals overlap. Claude Haiku and Sonnet are pending the Level-3 unlock.

## 5. rounds (45 s budget, ~26 s estimate, 60 words)

Against ground truth, all thirty-two leaking conversations are blocked; Llama Guard lets twenty-nine
of thirty-two out; the price is twenty-three percent of hard normal questions. Value matching does the
work, the simplest layer; the session budget catches one more; decoding and the oracle rule are
untested here. Layer two is a teammate's query guard: no free SQL. No model call.

## 6. close (24 s budget, ~21 s estimate, 49 words)

Green Mosaic. Every tile is green; the picture is the breach. The product is an output DLP with
memory, a gateway in front of any assistant, policy from the data classification you already
keep. One harness, one ledger, every finding re-verified. Check the conversation, not the answer.
Thank you.

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
