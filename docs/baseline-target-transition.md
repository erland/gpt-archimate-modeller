# Baseline, target och transition – steg 32

Architecture states beskriver baseline, transition och target ovanpå samma stable IDs.

- State-ID: `STA-NNNNNN`
- Transition-ID: `TRN-NNNNNN`

State kan ärva via `inherits_from`, beskriva `delta` och markera `object_status` som unchanged, introduce, change, retire eller temporary.
Transition binder from_state till to_state och kan referera till change sets/work packages.

Detta ersätter inte ArchiMate Plateau/Gap/WorkPackage. Full modellkopiering ska undvikas.
