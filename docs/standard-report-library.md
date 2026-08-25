# Standard report library – steg 30

Sex standardrapporter finns:

1. model-overview
2. application-platform-portfolio
3. capability-realization
4. evidence-review
5. issues-observations
6. model-quality-worklist

Index: `reports/standard-library.yaml`.

Query-format 0.2 kan även läsa `sources`, `references`, `issues` och `observations`
samt filtrera på `status_in` och `priority_in`.

Report-renderaren hanterar nu projicerade dotted keys som `properties.owner` korrekt.

Alla standardrapporter kan renderas till Markdown; tabellsektioner kan exporteras till CSV.
Rapporter är read-only derivat.
