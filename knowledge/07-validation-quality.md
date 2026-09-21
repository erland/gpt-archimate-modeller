# Validation and semantic quality

## Technical validation

Blocking.

Kontrollerar bland annat:

- element types
- ID prefixes
- relationship types
- relation-pairs där exact matrix coverage finns
- references
- evidence
- extensions
- specializations

Finding-format:

```yaml
severity:
code:
object_id:
message:
```

## Semantic quality

Normalt non-blocking.

Exempelregler:

- isolated element
- capability utan realization
- missing owner
- missing evidence
- weak source localization
- duplicate candidate
- layer imbalance
- relationship utan evidence

Quality score är diagnostiskt och ska inte beskrivas som objektiv mognadspoäng.

## Kombinerad kontroll

`project_control.py validate-project` orkestrerar teknisk validation, quality och versionshistorik.


## Quality profile 0.2

Quality score är normaliserad och uppdelad i tre diagnostiska dimensioner:

- architecture
- ownership
- evidence

Dimensionerna normaliseras mot relevant objektpopulation och viktas till ett overall score.
Det gör att metadata-completeness inte automatiskt reducerar en stor tekniskt användbar modell
till 0/100. Scores är fortfarande diagnostiska och inte mognadsbetyg.

Unknown relationship-pairs aggregeras per source type, target type och relationship type.
Det minskar brus utan att påstå att en uncovered pair är normativt giltig.
