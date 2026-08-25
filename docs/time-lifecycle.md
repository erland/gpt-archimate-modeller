# Time och lifecycle – steg 33

Steg 33 skiljer explicit mellan faktisk giltighet, planerade datum och lifecycle-klassificering.

Temporal metadata på element/relation:
`valid_from`, `valid_to`, `planned_from`, `planned_to`, `retired_on`, `as_of`, `status_source`.

`status_source`: actual, planned, inferred, unknown.

Lifecycle är fortsatt standard extension med `planned`, `active`, `phase_out`, `retired`, `unknown`.
Lifecycle är klassificering, inte datum.

Architecture states får `time_basis: actual | planned | scenario`.
Transitions får planned_start/planned_end och actual_start/actual_end.

Validatorn fångar ogiltiga intervall och varnar för uppenbara lifecycle/tidskonflikter.

Framtida avsikter ska inte uttryckas som redan inträffade fakta.
