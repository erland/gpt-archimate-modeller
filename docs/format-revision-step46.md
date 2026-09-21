# Step 46 – Format revision after real EA pilot

## Goal

Convert the Step 45 pilot findings into the final pre-1.0 format design. Format changes are
made now so Step 47 can focus on explicit compatibility and migration rather than changing
the target again.

## Target versions

- EA project format: **0.2**
- package layout: **0.1**
- project ZIP contract: **0.2**
- validation profile: **0.2**
- quality profile: **0.2**

Readers continue to accept format 0.1 and 0.2. New-project creation emits 0.2. Automatic
write-upgrade of existing 0.1 projects is deliberately deferred to Step 47.

## Decision 1 – Controlled impact themes

Split-project `project.yaml` may contain:

```yaml
files:
  impact_themes: extensions/impact-themes.yaml
```

The registry file has:

```yaml
format_version: '0.2'
impact_themes:
- id: privacy
  label: Privacy
  description: Controlled semantic impact theme.
```

The registry is optional. When present, any `properties.impact_themes` values used by
elements or relationships must reference known theme ids. Values may remain comma-separated
strings for compatibility with the pilot model; list values are also understood by validation.

This keeps semantic qualification controlled without turning impact themes into ArchiMate
elements or silently inventing direct governance relationships.

## Decision 2 – Relationship coverage warnings

The portable exact pair matrix remains intentionally partial. Unknown type pairs are not
silently accepted.

Instead of one warning per relationship, validation emits one finding per
`source_type + target_type + relationship_type` combination with occurrence count and sample ids.
Strict relationship mode still turns uncovered combinations into errors.

This preserves signal while preventing a large valid portfolio model from producing thousands
of duplicate warnings.

## Decision 3 – Quality dimensions

Quality profile 0.2 separates:

- **architecture** – connectivity, capability support, duplicates and balance,
- **ownership** – owner completeness on recommended object types,
- **evidence** – evidence and precise source-reference completeness.

Each dimension is normalized against a relevant population and the overall diagnostic score is
a weighted combination. Missing metadata can therefore be visible without forcing an otherwise
structurally useful portfolio model to 0/100.

The score remains a diagnostic signal, not an architecture maturity rating.

## Decision 4 – Capability realization

The standard capability-realization query no longer assumes only
`ApplicationComponent --Realization--> Capability`.

It accepts incoming support/realization through:

- Realization
- Serving
- Assignment
- Association

and reports relevant ApplicationComponent, TechnologyService, Node, SystemSoftware and
BusinessProcess elements. This matches real platform/capability models while retaining the
relationship type in the canonical model as the semantic truth.

## Decision 5 – Large query results

The query document format remains 0.2. Runtime/CLI emission changes:

- default maximum emitted rows: 200,
- `--max-rows 0` requests unlimited CLI output,
- result metadata includes `matched_count`, `returned_count` and `truncated`,
- aggregations are computed before the runtime emission cap.

Direct in-process report/query execution remains unbounded unless the query definition itself
contains `limit`.

## Compatibility boundary for Step 47

Step 46 deliberately does not rewrite existing format-0.1 projects. Step 47 must:

1. add an explicit 0.1 → 0.2 migration,
2. preserve projects that do not need impact themes,
3. recognize and preserve an existing `files.impact_themes` pilot file,
4. regenerate manifest/history correctly,
5. prove older reference/pilot ZIPs can be opened or migrated to the 0.2 target.
