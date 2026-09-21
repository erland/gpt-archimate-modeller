# ArchiMate YAML EA GPT — Release Candidate 5

Version: **1.0.0-rc.5**  
Package version: **0.44.3**

## Runtime migration since RC.4

RC.5 completes the separate GPT Byggaren 1.4 runtime migration without advancing the
original product plan beyond Step 44.

Four runtime distributions are now built from explicit canonical contracts:

- Chat ZIP — equivalent
- Custom GPT — equivalent_with_platform_constraints
- Claude Projects — reduced parity with explicit limitations
- OpenCode — equivalent with typed ArchiMate custom tools

The migration adds platform-neutral runtime contracts, a canonical typed tool contract,
registry-driven builds, runtime-aware hygiene, instruction adherence, five-dimensional
runtime parity, and four-runtime CI/release packaging.

## Product-plan status

The development plan remains **44 / 48**. Step 45 — Real EA pilot — is still not complete.

## Verification

RC.5 is accepted only after the RC.5 commit has green CI and green Build GPT distributions.
