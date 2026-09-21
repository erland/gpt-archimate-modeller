# ArchiMate YAML EA GPT 1.0.0

## Overview

Version 1.0.0 completes the original 48-step development plan.

The product provides a ZIP-based Enterprise Architecture workflow using ArchiMate 3.2 as
semantic core and YAML as canonical working format.

## Stable project format

- write target: format 0.2
- readable: format 0.1 and 0.2
- supported upgrade: `MIG-000002` from 0.1 to 0.2
- unknown future formats: read-only
- automatic downgrade: unsupported

Format 0.2 incorporates findings from a real EA pilot, including controlled impact themes,
less noisy relationship coverage diagnostics, normalized quality dimensions, broader capability
realization semantics and bounded query-tool output.

## Runtime distributions

The release publishes four distributions:

- Chat ZIP — equivalent
- Custom GPT — equivalent with platform constraints
- Claude Projects — reduced parity with explicit limitations
- OpenCode — equivalent with typed canonical ArchiMate tools

## Release verification

The tag-driven release pipeline runs:

1. automated regression suite,
2. canonical contract validators,
3. migration/compatibility tests,
4. repository hygiene checks,
5. build of all four runtimes,
6. distribution validation,
7. instruction adherence for all four runtimes,
8. five-dimensional runtime parity,
9. SHA-256 checksum generation,
10. release metadata generation.

The stable release tag is `v1.0.0`.
