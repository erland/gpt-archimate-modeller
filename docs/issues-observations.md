# Issues och observations – steg 29

Issues beskriver problem, konflikter och öppna frågor som kräver beslut eller åtgärd.
Observations beskriver iakttagelser som ska bevaras men ännu inte är modellfakta eller nödvändigtvis issue.

## IDs
- ISS-NNNNNN
- OBS-NNNNNN
- RES-NNNNNN

## Issue status
open, in_review, resolved, ignored.

## Observation status
noted, reviewed, promoted, dismissed.

## Prioritet
critical, high, medium, low.

## Länkar
`object_refs`, `source_refs`, `reference_refs`, `owner`, `due`.

Resolved issue kräver resolutionmetadata.
Ignored issue kräver ignore_reason.
Dismissed observation kräver dismiss_reason.
Promoted observation måste länka till promoted_to_issue.

## Canonical fil
`issues/issues.yaml`:

```yaml
issues: []
observations: []
```

Observation kan promotas explicit till issue.
Quality/conflict-fynd får föreslås men skrivs inte automatiskt in utan change workflow.

Issues/observations är workflowobjekt, inte ArchiMate-fakta.
