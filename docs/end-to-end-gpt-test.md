# End-to-end GPT test – steg 44

## Resultat

Steg 44 verifierar den observerbara GPT-/projektkedjan på release candidate.

Två lager testas:

1. **Deterministisk toolchain E2E** – verkligt nytt projekt, update, safety gates, analys, view-export och slutligt ZIP.
2. **Observerbart LLM-kontrakt** – 12 historiska domänevalfall från steg 38, kompletterade senare med 3 runtime-adherence-evals.

Detta gör inte anspråk på att en separat hosted Custom GPT-session har exekverats.

## 9 E2E-scenarier

1. skapa nytt komplett projekt-ZIP,
2. applicera change set med Capability, ApplicationComponent och Realization,
3. blockera duplicate candidate,
4. blockera stale change set,
5. impact analysis,
6. modellkvalitetsrapport,
7. standardvy till draw.io och Mermaid,
8. slutlig ZIP-validering med manifest/index,
9. de ursprungliga 12/12 observerbara domänevalsen.

## Fel som hittades av E2E

### E2E-DEFECT-001

Efter steg 39 returnerade `pack_project.pack()` ett strukturerat resultatobjekt. `new_project.create_zip()` behandlade fortfarande returvärdet som en ZIP-path vid validering.

**Fix:** validera explicit `output_zip`; behåll pack-resultatet separat.

### E2E-DEFECT-002

Canonical packer skriver projektfiler direkt i ZIP-roten, medan `safe_unpack.py` fortfarande krävde exakt en underkatalog.

**Fix:** acceptera canonical flat-root layout och fortsatt äldre single-root layout; `project_control.unpack_project()` ger stabil katalog baserad på project id.

## Verifierat

- modellversion `0.1.0 → 0.2.0`,
- input-ZIP är oförändrad,
- duplicate/stale operationer producerar inget output-ZIP,
- impact-resultat gör inget kausalt överpåstående,
- quality score presenteras diagnostiskt,
- draw.io/Mermaid export fungerar,
- final ZIP innehåller `MODEL-INDEX.json` och `PACKAGE-MANIFEST.yaml`,
- 9/9 E2E-scenarier passerar,
- de ursprungliga 12/12 domänevalsen passerar; runtime-adherence-evals valideras separat som del av den senare runtime-hardening.

Körning:

```bash
python scripts/run_e2e_gpt_test.py --output-dir /tmp/e2e
```

Steg 45 är real EA pilot.
