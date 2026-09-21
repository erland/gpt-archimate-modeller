# ArchiMate YAML EA GPT — Release Candidate 8

Version: **1.0.0-rc.8**  
Package version: **0.47.0**

## Step 47 – Backward compatibility/migration

RC.8 adds explicit backward compatibility for the format-0.2 target.

- format 0.1 remains readable,
- `MIG-000002` upgrades 0.1 → 0.2,
- existing impact-theme registries and all entries are preserved,
- missing registries are initialized empty,
- stale derived package manifest/model index are invalidated before repack,
- migration history records the format step separately,
- downgrade is not automatic or supported.

Regression coverage verifies preview non-mutation, apply, preservation, idempotence and final
valid ZIP packaging.

## Product-plan status

The development plan is now **47 / 48**. Step 48 — v1.0.0 — is next.
