# Changelog

## 0.44.2 – 2026-08-25

### Fixed
- `scripts/query.py` CLI no longer calls stale `assemble()` after the Step 40 model-loader migration.
- Query CLI now uses `load_model()` and therefore shares model-index validation/fallback behavior with reports, views, impact and quality operations.

### Tests
- Added `QUERY-011`.
- Added automated subprocess regression `T-QRV-002` that executes the real query CLI and validates its JSON result.

### Release
- Maintenance RC updated to `1.0.0-rc.4`.
- Development plan remains at Step 44; no Step 45 pilot claim is made.

## 0.44.1 – 2026-08-25

### Maintenance
- Release candidate updated to 1.0.0-rc.3 without advancing the development plan.
- Removed Python cache files and generated E2E result artifacts from source package.
- Added `.gitignore` to prevent cache/build artifacts from returning.
- Added reproducible Custom GPT and Chat distribution builders/validators.
- Added GitHub Actions CI, distribution build and tag-driven release workflows.
- Release events now attach exactly two GPT distribution ZIPs.

## 0.44.0 – 2026-08-25

### Added
- End-to-end GPT/project workflow test 0.1.
- Nine E2E scenarios and persisted E2E evidence.
- Release candidate 1.0.0-rc.2.

### Fixed
- `new_project.create_zip()` now validates the actual output ZIP after `pack()` returns a structured result.
- Safe unpack/update now supports canonical flat-root ZIPs as well as legacy single-root ZIPs.
- Unpacked workspace uses stable project-id directory naming.

### Validated
- 9/9 E2E scenarios pass.
- 12/12 observable LLM behavior evals pass.
- Duplicate/stale writes are blocked without output ZIP.
- Final ZIP manifest and model index validate.

### Clarified
- E2E validates the deterministic toolchain and observable LLM contract; it does not claim execution inside a separate hosted Custom GPT session.

## 0.43.0 – 2026-08-25

### Added
- First release candidate: 1.0.0-rc.1.
- RC policy and freeze rules.
- RC checklist.
- RC notes.
- RC manifest with hashes for key canonical/runtime contracts.

### Changed
- Package version updated to 0.43.0.
- Plan status updated to 43/48.
- Canonical format/runtime contracts enter candidate freeze.

### Not yet complete
- End-to-end GPT runtime validation remains Step 44.
- Real EA pilot remains Step 45.

## 0.42.0 – 2026-08-25

### Added
- Developer documentation 0.1.
- Architecture and module-boundary documentation.
- Schema/format evolution guidance.
- Change/migration/versioning guidance.
- Testing/fixture strategy.
- Interoperability, performance/packaging and release compatibility guidance.
- Machine-readable developer documentation catalog.
- Developer-documentation validator.
- Developer help Knowledge routing.

### Changed
- Root README now links directly to developer documentation.
- Project version updated to 0.42.0.
- Plan status updated to 42/48.

## 0.41.0 – 2026-08-25

### Added
- User documentation 0.1.
- User documentation index and quickstart.
- Guides for project ZIP workflow, modeling, evidence, conflicts, analysis/exports, change architecture, quality/impact and troubleshooting.
- Machine-readable user documentation catalog.
- User-documentation validator.
- User help Knowledge routing.

### Changed
- Root README replaced with a current user-facing entry point instead of cumulative early-step development notes.
- Project version updated to 0.41.0.
- Plan status updated to 41/48.

## 0.40.0 – 2026-08-25

### Added
- Derived model index 0.1.
- MODEL-INDEX.json with source fingerprint and assembled logical model.
- Index-aware model loader with YAML fallback.
- Pack-time index rebuild.
- Read-path index integration for reports/views/query/impact/quality.
- Large-model benchmark and index regression tests.

### Changed
- Model index is explicitly non-canonical and rebuildable.
- Project version updated to 0.40.0.
- Plan status updated to 40/48.

## 0.39.0 – 2026-08-25

### Added
- ZIP robustness profile 0.1.
- Deterministic pack including required empty directories.
- Duplicate/case-collision/traversal/symlink/size/compression guards.
- Manifest v0.2 and large synthetic fixture generator.

### Changed
- Safe extraction validates ZIP first.
- Package 0.39.0; plan 39/48.

## 0.38.0 – 2026-08-25

### Added
- LLM eval suite 0.1 with 12 behavior cases.
- Eval schema/catalog/profile, offline grader and runner.
- Grader regression fixtures and Knowledge guidance.

### Changed
- Package 0.38.0; plan 38/48.

## 0.37.0 – 2026-08-25

### Added
- Automated test suite 0.1.
- Eight offline suites, JSON/YAML/text output and CI exit codes.
- Test-run JSON schema and shell wrapper.

### Changed
- Package 0.37.0; plan 37/48.

## 0.36.0 – 2026-08-25

### Added
- Fixture/reference-project library 0.1.
- Four valid reference projects and ten invalid fixtures.
- Canonical fixture catalog and validators.

### Changed
- Package 0.36.0; plan 36/48.

## 0.35.0 – 2026-08-25

### Added
- Dynamic model quality report 0.1.
- Markdown, CSV, JSON and YAML quality report outputs.
- Findings per rule/severity and object worklist.
- Dynamic report descriptor/library.
- Quality report validator.
- Model quality report Knowledge guidance.

### Changed
- Dynamic quality reporting explicitly reuses the existing quality checker and profile.
- Dynamic findings remain separate from persisted quality issues/observations.
- Project version updated to 0.35.0.
- Plan status updated to 35/48.

## 0.34.0 – 2026-08-25

### Added
- Impact analysis engine 0.1.
- Directed incoming/outgoing/both traversal.
- Direct/indirect impact classification.
- Relationship-path traceability.
- Evidence-based path certainty.
- Change-set and architecture-state-delta seeding.
- YAML, JSON and Markdown output.
- Impact analysis Knowledge guidance.

### Changed
- Project version updated to 0.34.0.
- Plan status updated to 34/48.

## 0.33.0 – 2026-08-25

### Added
- Time/lifecycle model 0.1.
- Temporal metadata on elements/relationships.
- State time_basis and transition planned/actual dates.
- Temporal validator integrated into unified validation.
- Lifecycle query/report and Knowledge guidance.

### Changed
- Query filters include lifecycle_in and temporal_status_source_in.
- Package 0.33.0; plan 33/48.

## 0.32.0 – 2026-08-25

### Added
- Architecture states 0.1 with baseline/transition/target, STA/TRN IDs, inheritance/delta, resolver and ZIP-contract integration.

### Changed
- New-project and counters integrate architecture states.
- Package 0.32.0; plan 32/48.

## 0.31.0 – 2026-08-25

### Added
- Standard view library 0.1 with six views.
- Standard view validator and reference draw.io/Mermaid exports.
- Supporting standard-view queries and Knowledge guidance.

### Fixed
- Packaged assembler accepts observations in issues/issues.yaml as intended by Step 29/30.

### Changed
- Package 0.31.0; plan 31/48.

## 0.30.0 – 2026-08-25

### Added
- Standard report library 0.1 with six reports.
- Query support for sources/references/issues/observations and status/priority filters.
- Standard library validator and rendered examples.

### Fixed
- Projected dotted fields render correctly in reports/previews.

### Changed
- Query format 0.2; package 0.30.0; plan 30/48.

## 0.29.0 – 2026-08-25

### Added
- Issues/observations model 0.2.
- OBS IDs, lifecycle, validator and promotion helper.
- Knowledge guidance.

### Changed
- Canonical issue file, assembler, new-project and import integration updated.
- OBS/RES counters added.

## 0.28.0 – 2026-08-25

### Added
- Conflict/duplicate policy 0.1.
- Conflict classification.
- Duplicate/conflict detector.
- Resolution JSON Schema.
- RES stable identifiers.
- Safe resolution translator.
- Explicit keep-separate/defer/prefer/merge semantics.
- Conflict/duplicate Knowledge guidance.

### Changed
- Project version updated to 0.28.0.
- Plan status updated to 28/48.

## 0.27.0 – 2026-08-25

### Added
- Update-project workflow 0.1.
- End-to-end ZIP-to-ZIP update orchestrator.
- Compatibility/migration gate.
- Optimistic locking.
- Duplicate candidate gate.
- Canonical dry-run and apply integration.
- Post-validation/quality reporting.
- Final ZIP validation.
- Update-project Knowledge and example change set.

### Changed
- Project version updated to 0.27.0.
- Plan status updated to 27/48.

## 0.26.0 – 2026-08-25

### Added
- New-project workflow 0.1.
- New-project schema and examples.
- Template-based project generator.
- Empty-project initialization.
- Strict evidence-valid seed support.
- Initial histories and ID counters.
- Direct validated ZIP creation.
- New-project Knowledge guidance.

### Changed
- New-project generation reuses canonical project template and preserves normal validation rules.
- Project version updated to 0.26.0.
- Plan status updated to 26/48.

## 0.25.0 – 2026-08-25

### Added
- GPT Knowledge structure 0.1.
- Nine thematic core knowledge files.
- Machine-readable knowledge index.
- Intent-to-knowledge routing.
- Explicit machine-readable authority mapping.
- Knowledge validator.
- Knowledge architecture documentation.

### Changed
- Project version updated to 0.25.0.
- Plan status updated to 25/48.

## 0.24.0 – 2026-08-25

### Added
- Full GPT system instruction 0.1.
- Compact Custom GPT instruction.
- Machine-readable runtime policy.
- GPT instruction validation.
- Explicit runtime behavior for ZIP validation, migration, ArchiMate modeling, evidence, change workflow, reports/views and final packaging.

### Changed
- Project version updated to 0.24.0.
- Plan status updated to 24/48.

## 0.23.0 – 2026-08-25

### Added
- Migration framework 0.1.
- Machine-readable migration registry.
- Compatibility inspection, plan and preview.
- Atomic migration apply.
- Separate migrations/history.yaml.
- Legacy 0.0 → 0.1 reference migration.
- Future-version write protection.

### Changed
- Legacy migration fixture now represents a semantically complete older project.
- Migration creates later mandatory support structures before validation.
- Project version updated to 0.23.0.
- Plan status updated to 23/48.

## 0.22.0 – 2026-08-25

### Added
- Project control 0.1.
- Unified project_control.py CLI.
- Safe explicit ZIP extraction.
- Atomic verified unpack.
- Atomic validated pack.
- Project inspection/status summary.
- Combined project validation orchestration.
- ZIP roundtrip command.
- Workspace marker `.project-control.yaml`.

### Changed
- Package manifest and packer ignore workspace marker.
- Project version updated to 0.22.0.
- Plan status updated to 22/48.

## 0.21.0 – 2026-08-25

### Added
- Project ZIP contract 0.1.
- Machine-readable contract.
- Required canonical files/directories.
- Version compatibility rules.
- PACKAGE-MANIFEST.yaml with SHA-256.
- Manifest generator, ZIP validator and project packer.
- Path traversal/symlink checks.
- Explicit ZIP entries for required empty directories.
- Controlled errors for malformed project.yaml.

### Changed
- Example/template split projects include PACKAGE-MANIFEST.yaml.
- Project version updated to 0.21.0.
- Plan status updated to 21/48.

## 0.20.0 – 2026-08-25

### Added
- Model Exchange import evaluation.
- Model Exchange import profile 0.1.
- Import preview.
- Staging project creation.
- Element/relationship/property mapping.
- Specialization and evidence summary restoration.
- Unsupported/lossy content reporting.
- Export/import core graph round-trip tests.

### Changed
- Direct merge from Model Exchange into an existing EA project is explicitly deferred.
- Project version updated to 0.20.0.
- Plan status updated to 20/48.

## 0.19.0 – 2026-08-25

### Added
- ArchiMate Model Exchange export 0.1.
- ArchiMate 3.1 exchange schema metadata for ArchiMate 3.2 semantic models.
- Element and relationship XML export.
- PropertyDefinitions and property instances.
- Specialization/aliases/evidence summary preservation as properties.
- Structural Model Exchange validator.
- Export profile metadata.
- Generated Model Exchange example.

### Changed
- Project version updated to 0.19.0.
- Plan status updated to 19/48.

## 0.18.0 – 2026-08-25

### Added
- Diagram export 0.1.
- draw.io / diagrams.net XML export.
- Mermaid flowchart export.
- Deterministic simple layout.
- Stable element/relationship IDs in draw.io output.
- View grouping as Mermaid subgraphs.
- Rendered example diagrams.

### Changed
- Project version updated to 0.18.0.
- Plan status updated to 18/48.

## 0.17.0 – 2026-08-25

### Added
- View format 0.1.
- View JSON Schema.
- View validator.
- Neutral view compiler.
- Layout hints and grouping.
- Node and edge display configuration.
- Capability-realization and architecture-overview example views.
- Queries supporting view compilation.

### Changed
- Project version updated to 0.17.0.
- Plan status updated to 17/48.

## 0.16.0 – 2026-08-25

### Added
- Report engine 0.1.
- Markdown rendering.
- CSV export per table section.
- Table/list/summary renderers.
- Grouped Markdown rendering.
- Markdown escaping and simple formatting.
- Deterministic rendering tests.
- Application list example report.

### Changed
- Project version updated to 0.16.0.
- Plan status updated to 16/48.

## 0.15.0 – 2026-08-25

### Added
- Report format 0.1.
- Report JSON Schema.
- Report validator.
- Report preview pipeline.
- Table, list and summary render definitions.
- Columns and formatting metadata.
- Grouping and presentation sorting.
- Standard application/platform/summary reports.

### Changed
- Project version updated to 0.15.0.
- Plan status updated to 15/48.

## 0.14.0 – 2026-08-25

### Added
- Query format 0.1.
- Query JSON Schema.
- Query validator and execution engine.
- Element/relationship filters.
- Property/evidence filters.
- Graph traversal.
- Projection, sorting, limits.
- Count and group-by aggregation.
- Standard example queries.

### Changed
- Project version updated to 0.14.0.
- Plan status updated to 14/48.

## 0.13.0 – 2026-08-25

### Added
- Versioning policy 0.1.
- SemVer model-version rules.
- Change impact classification.
- changes/index.yaml and versioning/history.yaml.
- Duplicate change-set guard.
- Version-history validator.

### Fixed
- Explicit add operations now update ID counters transactionally before validation.

### Changed
- apply_changes.py uses shared versioning policy.
- Applied changes record impact and resulting model version.
- Project version updated to 0.13.0.
- Plan status updated to 13/48.

## 0.12.0 – 2026-08-25

### Added
- Change workflow 0.1.
- Change-set JSON Schema.
- Transactional change application engine.
- Preconditions.
- Expected model version guard.
- Dry-run.
- Stable change-set IDs `CHG-NNNNNN`.
- Change history directory.
- Initial model-version bump logic.
- Duplicate check before add_element.
- Safety rules for destructive changes.
- Example change set.

### Changed
- Project version updated to 0.12.0.
- Plan status updated to 12/48.

## 0.11.0 – 2026-08-25

### Added
- Semantic quality profile 0.1.
- Quality checker.
- Combined technical + semantic project checker.
- Quality score 0–100.
- Connectivity, capability support, ownership, evidence, traceability, duplicate and balance checks.
- Technically valid but semantically weak test fixture.

### Changed
- Reference project completed with owner information for Capability and Platform.
- Project version updated to 0.11.0.
- Plan status updated to 11/48.

## 0.10.0 – 2026-08-25

### Added
- Unified validator `scripts/validate.py`.
- Validation profile 0.1.
- ArchiMate element/relationship type validation.
- Portable relationship-pair profile with pinned third-party cross-check metadata.
- Normal and strict relationship coverage modes.
- Structured error/warning codes.
- JSON validation report.
- Invalid ArchiMate relationship fixture.

### Fixed
- Reference model: `ApplicationComponent --Serving--> Capability` corrected to `Realization`.

### Changed
- Project version updated to 0.10.0.
- Plan status updated to 10/48.

## 0.9.0 – 2026-08-25

### Added
- Specialization model 0.2.
- Base type och parent specialization.
- Inheritance cycle validation.
- Governance/deprecation.
- Standard specialization profile.
- Example BusinessApplication och Platform.
- Specialization validator.

### Changed
- Referensprojekt uppdaterat med specializations.
- Projektversion uppdaterad till 0.9.0.
- Planstatus uppdaterad till 9/48.

## 0.8.0 – 2026-08-25

### Added

- Extension model 0.2.
- Deklarativ extensionprofil.
- Applies-to-regler per object kind och ArchiMate-typ.
- Value-type validering.
- Enum/list/reference-stöd.
- Evidence-required-regler.
- Governance metadata och deprecation.
- Strict/permissive extension validation.
- Standard extensions: lifecycle, owner, criticality, information_classification, strategic_fit, technical_debt.
- Negativa testfall för ogiltigt enumvärde och okänd property.

### Changed

- Referensprojektets extensions migrerade till nya modellen.
- Exempelapplikation kompletterad med criticality + evidence.
- Projektversion uppdaterad till 0.8.0.
- Planstatus uppdaterad till 8/48.

## 0.7.0 – 2026-08-25

### Added

- Source/reference model 0.2.
- Separata reference-objekt med `REF-NNNNNN`.
- Strukturerade locator-typer.
- Source origin för file, url, conversation och external system.
- Source quality metadata.
- Authors, publisher och owner.
- Published/retrieved/effective/expires dates.
- Optional content fingerprint.
- Evidence stöd för `reference_refs`.
- Source/reference-validator.
- REF-counter i identity-strategin.

### Changed

- Split-exempelprojekt kompletterat med references.yaml.
- Monolitiskt exempelprojekt uppdaterat med references.
- Package manifest och schemas uppdaterade.
- Projektversion uppdaterad till 0.7.0.
- Planstatus uppdaterad till 7/48.

## 0.6.0 – 2026-08-25

### Added

- Evidence model 0.2.
- Evidence assertions med stabila `EV-NNNNNN`-ID:n.
- Separata assertion kinds: explicit, user_statement, imported, derived, inferred och contradicting.
- `supports` för spårning av vilken modelldata evidensen gäller.
- `reason` för härledd/infererad information.
- `mixed` evidence-status.
- Evidence-specifik validator.
- EV-counter i identity-strategin.
- Negativt testfall för inferens utan reason.

### Changed

- Exempelprojekt migrerat till assertions-baserad evidence.
- Monolitiskt referensprojekt migrerat till samma evidence-format.
- Package assembler och project validator uppdaterade för nested evidence.
- Projektversion uppdaterad till 0.6.0.
- Planstatus uppdaterad till 6/48.

## 0.5.0 – 2026-08-25

### Added

- Identity strategy 0.1.
- Stabilt `PREFIX-NNNNNN`-format.
- Typfamiljsprefix för element.
- Separata prefix för relationer, sources och issues.
- ID-counters i projektpaketet.
- ID-allokeringsscript.
- Namnnormalisering.
- Initial dubblettkandidatdetektering.
- Validering av ID-format, prefix och counter consistency.
- Designregler för alias, external IDs och merge.

### Changed

- Exempelprojekt migrerat till den nya ID-strategin.
- Monolitiskt referensprojekt migrerat till nya ID:n.
- Projektversion uppdaterad till 0.5.0.
- Planstatus uppdaterad till 5/48.

## 0.4.0 – 2026-08-25

### Added

- Package layout 0.1.
- Hybrid filindelning för EA-projekt.
- Manifest-schema för uppdelade projektpaket.
- Standardpartitioner per ArchiMate-domän/lager.
- Uppdelat referensprojekt.
- Uppdelad projektmall.
- Assembler från fysisk paketering till logisk modell.
- Package validator med path-säkerhet och global referensintegritet.
- Dokumentation av skalbarhets- och shardingprinciper.

### Changed

- Projektversion uppdaterad till 0.4.0.
- Planstatus uppdaterad till 4/48.
- Uppdelad projektstruktur är nu rekommenderad standard framför monolitisk projektfil.

## 0.3.0 – 2026-08-25

### Added

- EA-projektformat 0.1.
- JSON Schema för projektformatet.
- Modellstruktur för element och relationer.
- Projektmetadata med separat format- och modellversion.
- Evidence-struktur.
- Source-struktur.
- Extensions-definitioner.
- Specialization-definitioner.
- Issues-struktur.
- Minimal referensmodell.
- Projektmall.
- Initial projektvalidator med referensintegritetskontroller.

### Changed

- Projektversion uppdaterad till 0.3.0.
- Planstatus uppdaterad till 3/48.

## 0.2.0 – 2026-08-25

### Added

- Maskinläsbar ArchiMate 3.2-metaprofil.
- 60 elementtyper klassificerade per domän, lager och aspekt.
- 11 relationstyper med kategori och relevanta attribut.
- Relationship connector-modell med AND/OR-varianter.
- Lager- och aspektregister.
- Top-level concept model.
- Semantiska kandidatregler för relationer.
- Metamodel index och källregister.
- Konsistensvalidator för metamodelldefinitionerna.
- Dokumentation av gränsen mellan steg 2 och exakt Appendix B-validering i steg 10.

### Changed

- Projektversion uppdaterad till 0.2.0.
- Planstatus uppdaterad till 2/48.
- ArchiMate 3.2 fastställd som första metamodelprofil.

## 0.1.0 – 2026-08-25

### Added

- Initial project structure.
- Project vision.
- Version 1 use cases.
- Version 1 scope and explicit non-goals.
- ZIP-first, repository-agnostic architecture principle.
- Separation between GPT package and EA project package.
- Initial decision to keep model, query, report and view as separate concepts.

### Planned

- Step 2: machine-readable ArchiMate metamodel inventory.
