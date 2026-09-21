# Step 47 – Backward compatibility and migration

## Scope

Step 47 proves that the format-0.2 target introduced in Step 46 can coexist with existing
format-0.1 projects and provides an explicit deterministic upgrade path.

## Compatibility policy

| Project format | Read | Write/update | Migration |
|---|---|---|---|
| 0.1 | yes | only after explicit migration | MIG-000002 → 0.2 |
| 0.2 | yes | yes | none |
| future > 0.2 | inspection only | no | unavailable |

No automatic downgrade is supported.

## MIG-000002

Migration changes format metadata and support structures only.

### Existing impact-theme registry

If `files.impact_themes` already exists, the path is retained. The file's
`format_version` becomes `0.2`, while the complete `impact_themes` array is preserved.

This covers the real pilot pattern where the controlled registry already existed in a 0.1 project.

### Missing impact-theme registry

If no registry exists, migration adds:

```yaml
files:
  impact_themes: extensions/impact-themes.yaml
```

with:

```yaml
format_version: '0.2'
impact_themes: []
```

An empty registry is support structure, not fabricated EA content.

### Derived artifacts

`PACKAGE-MANIFEST.yaml` and `MODEL-INDEX.json` are removed from the migrated workspace
because their checksums/index content refer to pre-migration files. Repack regenerates current
derived artifacts and the resulting ZIP must pass the package validator.

## Regression coverage

Automated test `T-WF-002` creates a temporary 0.1 project with an existing controlled
`privacy` theme and verifies:

1. compatibility reports `migration_available`,
2. plan resolves to exactly `MIG-000002`,
3. preview reaches 0.2 without modifying the source,
4. impact-theme path/content are preserved,
5. apply records `MIG-000002` in migration history,
6. subsequent compatibility reports `current`,
7. derived stale manifest is absent,
8. repack produces a valid ZIP.

Step 48 may therefore treat 0.2 as the final v1.0 project-format target.
