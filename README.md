# Entropy Hackathon — Shared Knowledge

Private knowledge base for our five-person team. Everyone runs the [organizers’ starter repo](https://github.com/natalienma/break-the-model-starter) in their own local checkout. Use this repository to share what we learn and the evidence behind it.

## Where things go

| Location | Contents |
| --- | --- |
| [docs/extraction-goals.md](docs/extraction-goals.md) | **Start here** — what we are trying to extract: ranked targets, routes, status |
| [docs/secrets-map.md](docs/secrets-map.md) | Where the "keys and secrets" live and how each is protected |
| [docs/](docs/README.md) | Research notes, challenge criteria, sources, and prior work |
| [docs/findings.md](docs/findings.md) | Confirmed findings and links to evidence |
| [experiments/](experiments/README.md) | Hypotheses, prompt sequences, and reproduction write-ups |
| [results/](results/README.md) | Selected responses, measurements, and submission turn IDs |
| [mitigations/](mitigations/README.md) | Proposed defenses, explanations, and evaluation results |
| [presentation/](presentation/README.md) | Slides, demo materials, and speaker notes |

## Contributing

You can edit Markdown files directly on GitHub using the pencil button, or clone this knowledge base separately from your starter checkout:

```bash
git clone https://github.com/Zmart64/entropy-hackathon-knowledge.git
cd entropy-hackathon-knowledge
```

No Python environment or API key is needed for this repository.

Pull the latest changes before editing locally. For larger changes, use a short-lived branch and open a pull request into `main`.

Keep each experiment’s write-up and evidence linked. Include author(s), date, model, exact prompts, conversation reset behavior, results, and `turn_id`s. Record unsuccessful experiments too, so teammates can avoid repeating them. Clearly distinguish hypotheses from verified findings.

Keep runnable scripts and implementations in your local starter or a separate code repository; link to a shared code revision when one is available. Only share selected evidence here. Keep API keys, authentication headers, raw local logs, and unrelated personal data out of this repository.

## Challenge references

- [Rules and judging criteria](docs/challenge.md)
- [Organizer starter and setup instructions](https://github.com/natalienma/break-the-model-starter)
- [Live event page](https://entropy-live.vercel.app/)
- [Submission form](https://docs.google.com/forms/d/e/1FAIpQLSfq1xrhvZgDDo03YHm7XJ7m_LdsdiJWapttVGzgOMBS-vSu5A/viewform?usp=header)

**Pitch and review entry point:** [pitch overview](presentation/pitch-overview.md) · [coverage by model](docs/extraction-goals.md) · [Andrii’s additional findings](docs/andrii-findings.md) · [full evidence-sharing proposal](docs/evidence-sharing.md).
