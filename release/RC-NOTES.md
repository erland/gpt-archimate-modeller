# ArchiMate YAML EA GPT — Release Candidate 4

Version: **1.0.0-rc.4**  
Package version: **0.44.2**

## Maintenance fix since RC.3

A real-use failure exposed a stale call in `scripts/query.py`: the CLI imported `load_model` but still invoked the old `assemble()` path.

RC.4 fixes the CLI to use `load_model()` and adds a subprocess regression that executes the actual query command.

No canonical model-format change was introduced. The development plan remains at Step 44; the real EA pilot is still Step 45.
