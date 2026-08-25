# Semantiska kvalitetskontroller – steg 11

## Syfte

En modell kan vara tekniskt giltig men ändå vara ofullständig eller svag som arkitekturmodell. Steg 11 lägger därför kvalitetskontroller ovanpå den tekniska valideringen.

## Kategorier

- completeness
- connectivity
- evidence
- ownership
- duplication
- modeling balance
- traceability

## Kontroller i version 0.1

### Q-CONN-001 – Isolerat element
Element utan relationer flaggas.

### Q-CAP-001 – Capability utan realisering/stöd
Capability bör ha minst en inkommande `Realization`, `Serving`, `Assignment` eller, som svag fallback, `Association`.

### Q-OWNER-001 – Saknad owner
Följande typer bör normalt ha owner:
- ApplicationComponent
- Node
- SystemSoftware
- TechnologyService
- BusinessProcess
- Capability

### Q-EVID-001 – Saknad evidence
Element utan evidence assertions flaggas.

### Q-EVID-002 – Låg confidence
`low` och `unknown` flaggas som info.

### Q-SRC-001 – Källhänvisning utan exakt reference
Evidence mot ett dokument/webb/presentation/spreadsheet/repository utan `reference_refs` flaggas som info.

### Q-DUP-001 – Stark dubblettkandidat
Samma normaliserade namn inom samma ArchiMate-typ eller delat alias flaggas. Ingen automatisk merge görs.

### Q-BAL-001 – Capabilities utan realiserande lager
Capabilities men inga Application/Technology-element ger warning.

### Q-BAL-002 – Teknik utan verksamhetskoppling
Application/Technology men inga Business/Strategy-element ger warning.

### Q-REL-001 – Relation utan evidence
Relationer utan evidence flaggas särskilt.

## Quality score

Startvärde 100.

Avdrag enligt standardprofil:
- error: 10
- warning: 3
- info: 0.5

Score är diagnostisk, inte ett absolut mognadsmått.

## Körning

Teknisk validering:

```bash
python scripts/validate.py <projekt>
```

Semantisk kvalitet:

```bash
python scripts/quality_check.py <projekt>
```

Samlad kontroll:

```bash
python scripts/check_project.py <projekt>
```

## Designprincip

Kvalitetskontroller ska vara förklarbara, peka på konkreta objekt och aldrig automatiskt ändra semantik.
