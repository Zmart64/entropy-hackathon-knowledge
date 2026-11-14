# Experiment write-ups

Create a folder per experiment, for example `experiments/short-descriptive-name/`. Share the hypothesis, exact prompt sequence, method, and outcomes here. Run scripts in your separate local starter checkout; link to a shared code revision if one is available.

Use this outline in each experiment's README:

```markdown
# Experiment name

Author(s):
Date:
Status: hypothesis / tested / reproduced / unsuccessful

## Hypothesis
What behavior are we testing, and why might it occur?

## Reproduction
Model, exact prompts in order, conversation reset behavior, and number
of independent trials. Include any code reference and commands to run
in a separate starter checkout. Never include API keys.

## Results
Verified successes / total attempts, validation method, turn IDs,
and links to selected evidence in results/.

## Interpretation
Observed mechanism, alternative explanations, limitations, prior work.

## Mitigation
Proposed fix and link to any implementation or evaluation.
```

Do not treat errors or timeouts as successful attacks. Report them separately. Coordinate longer runs with teammates to avoid duplicating experiments.

## Recorded experiments

- [Conversation isolation and response exposure](chat-isolation-and-response-exposure/README.md)
- [Tool interface disclosure](tool-interface-disclosure/README.md)
- [`http_post` semantics and DLP separator map](http-post-semantics/README.md)
- [`http_post` gate mechanics, persuasion, and execution verdict](http-post-gate/README.md)
- [User-supplied SQL execution](user-supplied-sql-execution/README.md)

- [Afternoon evidence review](afternoon-evidence-review/README.md): offline provenance and coverage checks; selected reproduction cases.
