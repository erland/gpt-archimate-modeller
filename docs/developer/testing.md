# Teststrategi och fixtures

## Testpyramid

Paketet använder flera nivåer:

1. unit-like script checks,
2. subsystem validators,
3. reference projects,
4. invalid fixtures,
5. end-to-end workflows,
6. automated suite,
7. LLM evals.

## Reference projects

Finns under:

```text
tests/reference-projects/
```

De representerar giltiga modellmönster och ska alltid passera full teknisk validering.

## Invalid fixtures

Finns under:

```text
tests/fixtures/step36-invalid/
```

Varje fixture ska bryta en huvudsaklig regel och matcha förväntat fel.

Canonical katalog:

```text
tests/fixtures/fixture-catalog.yaml
```

## Automated suite

Kör:

```bash
python scripts/run_tests.py
```

Testsviten är nätverksoberoende.

## LLM evals

Kör strukturell validering:

```bash
python scripts/validate_llm_evals.py
```

Evals testar observerbart beteende, inte dold reasoning.

## När en bug fixas

Lägg alltid ett regressionstest som hade fångat felet.

Om felet är format-/databeroende är ett fixture oftast bättre än en inline-ad hoc-testmodell.

## Determinism

Tester ska inte bero på:
- nätverk,
- aktuell tid om det inte är testets syfte,
- iteration order,
- slump utan fast seed.
