# Experiments

Create a folder per experiment, for example `experiments/short-descriptive-name/`. Keep its script and notes together. The starter's `example_attack.py` shows the client API.

Use this outline in each experiment's README:

```markdown
# Experiment name

Author(s):
Date:
Status: hypothesis / tested / reproduced / unsuccessful

## Hypothesis
What behavior are we testing, and why might it occur?

## Reproduction
Model, exact prompts in order, conversation reset behavior, command,
and number of independent trials. Never include API keys.

## Results
Verified successes / total attempts, validation method, turn IDs,
and links to selected evidence in results/.

## Interpretation
Observed mechanism, alternative explanations, limitations, prior work.

## Mitigation
Proposed fix and link to any implementation or evaluation.
```

Do not treat errors or timeouts as successful attacks. Report them separately. Coordinate longer runs with teammates to avoid duplicating experiments.
