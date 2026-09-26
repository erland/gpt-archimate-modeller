# OpenAI Plugin compatibility assessment – GPT Byggaren 1.5.0

## Beslut

OpenAI Plugin är **inte en aktiv runtime-distribution** för ArchiMate YAML EA GPT 1.5.0.

Compatibility-målet är **reduced / advisory only**.

Pluginen får användas för rådgivande ArchiMate-stöd, förklaringar, modellgranskning och förslag när användaren tillhandahåller tillräckligt underlag, men den får inte presenteras som fullvärdig peer runtime för projektets ZIP-first change/validate/package-flöde.

## Varför full parity inte är möjlig

Projektets canonical runtime contract kräver följande capabilities för full funktion:

1. filesystem read,
2. filesystem write,
3. code execution,
4. structured data,
5. persistent workspace,
6. archive I/O.

Dessutom kräver kärnflödet:

- explicit projectRoot/workspace,
- verklig exekvering av valideringsverktyg,
- kontrollerad canonical mutation via change-set,
- teknisk validering före och efter mutation,
- komplett projekt-ZIP efter ändring,
- faktisk Project ZIP contract-verifiering,
- no-false-PASS.

En skills-first plugin får därför inte anta att dessa capabilities finns bara för att instruktioner eller referensfiler kan paketeras.

## Tillåtet advisory-beteende

En framtida advisory-plugin får:

- förklara ArchiMate-semantik,
- resonera om element, relationer och specializations,
- föreslå change sets,
- analysera användartillhandahållet modellunderlag,
- föreslå queries, reports och views,
- förklara valideringsfel som användaren tillhandahåller.

Den får inte, utan faktisk capability:

- hävda att ett script har körts,
- hävda att teknisk validering har passerat,
- hävda att workspace har muterats,
- hävda att ett komplett projekt-ZIP har skapats,
- hävda att Project ZIP contract har passerat,
- behandla chattminne som projektets auktoritativa state.

## Aktiveringskriterier

OpenAI Plugin får inte flyttas till aktiv peer runtime förrän en konkret implementation kan demonstrera och CI-verifiera:

- filesystem read,
- filesystem write,
- code execution,
- persistent workspace,
- archive I/O,
- deterministisk validation/mutation mot canonical tool-contract.

Fram till dess gäller:

- registry status: `not_active`
- runtime contract status: `not_planned`
- compatibility target: `reduced`
- distribution artifact: ingen
