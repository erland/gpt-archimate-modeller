# Large ZIP robustness – steg 39

Packning är deterministisk: sorterade entries, fast timestamp, normaliserade rättigheter, fast kompression och required empty directories.

ZIP-validatorn blockerar duplicate/case-collision names, traversal, absolute/backslash paths, symlinks, special files,
storleks-/entrygränser, extrem compression ratio och manifest mismatch.

`PACKAGE-MANIFEST.yaml` v0.2 innehåller path, SHA-256 och size och måste exakt motsvara payloadfilerna.

Defaultgränser finns i `package/zip-robustness.yaml`.

Stora syntetiska projekt kan genereras med `scripts/generate_large_fixture.py`.
Steg 40 används endast om mätningarna visar behov av model index.
