# Fixtures och referensprojekt – steg 36

Fyra giltiga referensprojekt och tio avsiktligt ogiltiga fixtures utgör stabil testdata
för kommande automatiska tester och LLM-evals.

Reference projects ska passera full teknisk validering.
Invalid fixtures ska bryta en dokumenterad regel och matcha ett förväntat validatorfel.

Canonical katalog: `tests/fixtures/fixture-catalog.yaml`.

Fixture-ID:n och deras semantik är stabila. Testdata är deterministiska och nätverksoberoende.
