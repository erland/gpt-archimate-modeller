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
