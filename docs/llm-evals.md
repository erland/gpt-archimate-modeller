# LLM evals – steg 38

LLM-evals testar observerbart GPT-beteende mot paketets regler, inte dold chain-of-thought.

12 fall täcker new project, identity, evidence, conflicts, update workflow, query/report separation,
interoperability, architecture states, time/lifecycle, impact, quality och uncertainty/governance.

Katalog: `evals/catalog.yaml`.

Validera:
`python scripts/validate_llm_evals.py`

Gradera ett svar:
`python scripts/grade_llm_eval.py evals/cases/EVAL-002.yaml response.md`

Gradera en katalog:
`python scripts/run_llm_evals.py --responses-dir responses`

Rule-based grading kontrollerar observerbara krav. Semantisk nyans kan kompletteras med manuell/LLM-granskning senare.
Grader-fixtures är testdata för graderaren, inte modellgenererade resultat.
