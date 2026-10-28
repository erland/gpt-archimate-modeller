## Query

Query beskriver urval och traversal.

Använd query för:
- elementurval,
- relationsurval,
- property/evidence-filter,
- traversal,
- projection,
- sortering,
- aggregation.

Lägg inte presentationslogik i query om den hör hemma i report.


## Report

Report beskriver presentation av query-resultat.

Använd:
- table,
- list,
- summary,
- sections,
- grouping,
- presentation sorting.

Report ska inte själv leta upp fakta som queryn inte returnerat.


## View

View beskriver visualisering.

Använd:
- node/edge-urval,
- grupper,
- layout-hints,
- labels,
- display properties.

View får inte skapa nya arkitekturfakta.


## Diagram

Views kan exporteras till:
- draw.io/diagrams.net XML,
- Mermaid.

draw.io är primärt redigerbart diagramformat.


## När användaren ber om analys

Använd modellens query-/graph-logik.

Skilj:
- direkt relation,
- transitive dependency,
- inference,
- gap/quality finding.

Presentera stabila IDs när det förbättrar spårbarhet.


## När användaren ber om rapport eller vy

Återanvänd befintliga queries om möjligt.

Skapa ny query endast om urvalslogiken saknas.

Håll:
- query,
- report,
- view

separata.

