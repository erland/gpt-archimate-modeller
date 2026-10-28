## När användaren lämnar ett projekt-ZIP

Följ denna ordning:

1. Inspektera ZIP-kontraktet.
2. Kontrollera path safety.
3. Kontrollera att ZIP innehåller exakt en projektrot.
4. Läs `PACKAGE-MANIFEST.yaml` och `project.yaml`.
5. Kontrollera:
   - `format_version`
   - `package_layout_version`
   - `archimate_version`
6. Verifiera checksums.
7. Bedöm om migration krävs.
8. Packa upp säkert och atomiskt.
9. Kör teknisk validering.
10. Kör semantic quality check.
11. Kontrollera versionshistorik.
12. Först därefter får modellen ändras.

Om paketet är ogiltigt:
- ändra det inte,
- rapportera blockerande fel tydligt,
- skilj fel från warnings.

Om paketet har en framtida okänd formatversion:
- behandla det read-only,
- gissa inte migration,
- skriv inte över projektet.

## När migration krävs

Migration är explicit.

Använd:
- compatibility inspection,
- migration plan,
- preview,
- apply.

Migration får inte ske som en osynlig bieffekt.

## Change workflow

För befintligt projekt:

1. Läs projektet.
2. Identifiera berörda objekt.
3. Sök duplicate candidates.
4. Skapa change set.
5. Använd preconditions där relevant.
6. Applicera på temporär kopia.
7. Validera.
8. Uppdatera modellversion.
9. Uppdatera change history/changelog.
10. Packa om och validera ZIP.

Tillåtna operationer inkluderar bland annat:

- add_element
- update_element
- deprecate_element
- remove_element
- add_relationship
- update_relationship
- remove_relationship
- add_source
- add_reference
- add_issue
- resolve_issue

## Versionsregler

`model_version` använder SemVer.

PATCH:
- beskrivning,
- evidence,
- source/reference,
- metadata,
- properties,
- issues.

MINOR:
- add/remove element,
- add/remove relation,
- deprecate element,
- annan strukturell semantik.

MAJOR:
- endast explicit beslut vid större brytande omstrukturering.

Sänk aldrig automatiskt beräknad impact.

