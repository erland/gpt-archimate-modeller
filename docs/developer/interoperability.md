# Interoperabilitet och export

## ArchiMate Model Exchange

Export är en derivatfunktion från canonical YAML.

Import går via staging.

Direkt merge/overwrite från XML till canonical modell är förbjudet.

## Importprincip

```text
XML
→ parse
→ staging representation
→ validate
→ identity/conflict resolution
→ explicit change set
→ canonical YAML
```

## Förlustfrihet

Full round-trip-förlustfrihet är inte garanterad.

Canonical YAML innehåller metadata som inte alltid finns i Model Exchange, exempelvis:

- provenance/evidence,
- change history,
- query/report/view definitions,
- vissa organisationsegna extensions.

## Diagram

draw.io/Mermaid är visualiseringar, inte canonical modeller.

Stable IDs bör bevaras där formatet tillåter.

## Exportregel

En export får aldrig vara enda platsen där ny arkitekturfakta skapas.
