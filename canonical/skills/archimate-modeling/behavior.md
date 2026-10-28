## ArchiMate-modellering

Använd standard-ArchiMate-typer som `type`.

Organisationens egna begrepp ska normalt modelleras som:

- specialization, om det är en semantisk underkategori av en ArchiMate-typ,
- extension/property, om det är klassificering, metadata, status eller attribut.

Exempel:

```yaml
type: Node
specialization: Platform
```

är korrekt.

Skapa inte egna ArchiMate `type`-värden för organisationens egna kategorier.

## Elementidentitet

Stable ID är primär identitet.

Matcha befintliga objekt i denna ordning:

1. exakt ID,
2. alias,
3. exakt namn + kompatibel typ,
4. normaliserat namn,
5. extern identifierare,
6. semantisk likhet.

Vid osäkerhet:
- skapa issue,
- mergea inte automatiskt.

ID-format:

```text
PREFIX-NNNNNN
```

ID får aldrig återanvändas.

## Relationer

Validera relationer mot ArchiMate-reglerna i paketet.

Om relation source/target-paret finns i den exakta relation-matrisen:
- följ den strikt.

Om paret ännu saknar exakt täckning:
- använd coarse semantic rules,
- markera osäkerhet,
- fabricera inte normativ säkerhet.

Byt inte source/target på en befintlig relation genom `update_relationship`.
Skapa hellre en ny relation och ta bort den gamla via explicit change set om semantiken förändras.

## Evidence och provenance

Ett påstående ska, när möjligt, ha evidence.

Separera:

- explicit fakta,
- användaruppgift,
- importerad information,
- derived,
- inferred,
- contradicting.

För inferred/derived:
- ange reason.

När exakt källa finns:
- använd `reference_refs`.

När bara övergripande källa finns:
- använd `source_refs`.

Fabricera aldrig:
- källor,
- sidnummer,
- headings,
- assertions.

## Confidence

Confidence uttrycker hur säker modellen är på själva påståendet.

Source quality uttrycker källans kvalitet.

Blanda inte ihop dessa.

## Extensions

Använd endast deklarerade extensions i strikt mode.

Nya organisationsspecifika properties bör först få en declaration.

Använd extension för sådant som:
- lifecycle,
- owner,
- criticality,
- information classification,
- technical debt.

## Specializations

Använd specialization för semantisk underkategori.

Exempel:
- Node → Platform
- ApplicationComponent → BusinessApplication

Specialization ska ha kompatibel `base_type`.

Statusliknande värden ska inte modelleras som specialization.

## Issues

Skapa issue när modellen innehåller exempelvis:

- möjlig duplicate,
- konflikt,
- saknad source,
- invalid relation,
- öppen fråga.

Lös inte osäkerhet genom att hitta på.

## När användaren ger ostrukturerad information

Identifiera kandidater till:
- element,
- relationer,
- properties,
- evidence,
- sources/references,
- issues.

Säg inte att något är ett faktum om det bara är en inference.

Om flera rimliga ArchiMate-tolkningar finns:
- välj inte godtyckligt,
- ge rekommenderad tolkning,
- dokumentera osäkerheten,
- skapa issue vid behov.

