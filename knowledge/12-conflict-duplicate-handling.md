# Conflict and duplicate handling

Konflikter ska klassificeras explicit:

- possible_duplicate
- identity_conflict
- type_conflict
- property_conflict
- evidence_conflict
- relationship_conflict

Tillåtna resolution actions:

- merge
- keep_separate
- prefer_existing
- prefer_incoming
- defer
- reject_incoming

GPT får automatiskt detektera, klassificera och föreslå.
GPT får inte automatiskt mergea, delete:a, retype:a eller kasta evidence.

`defer` kräver issue.
`merge` kräver canonical_id och ska materialiseras via explicit change workflow.
