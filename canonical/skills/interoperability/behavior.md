## Model Exchange

YAML är source of truth.

ArchiMate Model Exchange används för interoperabilitet.

Export:
- standardelement,
- relationer,
- properties,
- documentation.

Organisationens specialization exporteras som property, inte som egen `xsi:type`.

Import:
- behandlas som kontrollerad staging-import,
- direkt merge in i befintlig modell sker inte automatiskt,
- information som inte går att round-trippa lossless ska markeras.

