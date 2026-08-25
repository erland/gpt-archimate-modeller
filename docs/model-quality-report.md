# Model quality report – steg 35

## Syfte

Steg 35 ger en dynamisk rapport över den aktuella modellens kvalitet.

Rapporten använder **exakt samma** `quality/profile.yaml` och `run_quality()` som den befintliga quality-checkern.
Det finns därför bara en definition av quality score och quality findings.

## Skillnad mot model-quality-worklist

Två separata koncept finns:

### Dynamisk rapport

```text
reports/dynamic/model-quality-report.yaml
scripts/model_quality_report.py
```

Beräknas varje gång från modellen.

### Lagrad arbetslista

```text
reports/standard/model-quality-worklist.yaml
```

Visar explicita quality issues/observations som redan lagrats i projektet.

En dynamisk finding blir inte automatiskt ett issue.

## Innehåll

Rapporten visar:

- quality score,
- errors/warnings/info,
- antal findings,
- antal objekt med findings,
- findings per regel,
- full åtgärdslista,
- rekommendation,
- relaterade objekt.

## Score

Score är diagnostisk.

Den är en funktion av:

- aktiverade quality-regler,
- deras severity,
- deductions i `quality/profile.yaml`.

Den ska inte beskrivas som en absolut EA-mognadsnivå.

## Output

```bash
python scripts/model_quality_report.py project --format markdown
python scripts/model_quality_report.py project --format csv
python scripts/model_quality_report.py project --format json
python scripts/model_quality_report.py project --format yaml
```

## Governance

Om ett finding behöver följas över tid:

1. granska finding,
2. skapa explicit observation eller issue via change workflow,
3. tilldela owner/prioritet vid behov,
4. lös modellproblemet,
5. kör den dynamiska rapporten igen.

## Designprincip

Quality findings är beräknade observationer, inte persistenta modellfakta.
