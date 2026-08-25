# Första diagram-/visualiseringsexport – steg 18

## Syfte

Steg 18 gör `view_result` exporterbart till konkreta diagramformat.

Primärt format:

- **draw.io / diagrams.net XML**

Sekundärt format:

- **Mermaid flowchart**

Båda bygger på samma kompilerade view-resultat och ändrar inte modellen.

## Flöde

```text
model
  ↓
query
  ↓
view
  ↓
compile_view.py
  ↓
view_result
  ↓
export_diagram.py
  ├─ draw.io XML
  └─ Mermaid
```

## Varför draw.io först?

draw.io är:

- redigerbart,
- XML-baserat,
- möjligt att versionshantera,
- lätt att öppna i diagrams.net,
- användbart som grund för Confluence-/Gliffy-nära arbetsflöden.

Exporten använder i version 0.1 generiska ArchiMate-inspirerade boxar. Den försöker inte återskapa hela ArchiMate-notationen grafiskt ännu.

## Layout

Version 0.1 implementerar deterministisk enkel layout.

### layered + left_to_right

Grupper/type placeras i kolumner från vänster till höger.

### layered + top_to_bottom

Grupper/type placeras i rader uppifrån och ned.

### grid/auto

Noder placeras i ett deterministiskt rutnät.

### manual

Manuell layout kräver i framtida version node-koordinater i view-formatet. I version 0.1 faller `manual` tillbaka till grid.

## Grupper

View-grupper påverkar layoutordning och kan representeras som enkla visuella swimlane-liknande containers i draw.io.

I version 0.1 hålls implementationen medvetet enkel:

- noder får gruppnamn som metadata/label,
- fysisk container-layout införs inte ännu.

## Node labels

Primär label:

```yaml
nodes:
  label:
    primary: name
```

Sekundära fält läggs under namnet:

```text
Ärendehanteringssystem
ApplicationComponent
BusinessApplication
```

Valda properties visas därefter:

```text
owner: Applikationsteam
lifecycle: active
```

## Edges

Relationer exporteras med:

- relationstyp,
- valfritt namn,
- valfri confidence.

Exempel:

```text
Realization
confidence: medium
```

## draw.io XML

CLI:

```bash
python scripts/export_diagram.py   examples/ea-project-split   views/capability-realization.yaml   --format drawio   --output exports/capability-realization.drawio
```

Filen kan öppnas direkt i diagrams.net/draw.io.

## Mermaid

```bash
python scripts/export_diagram.py   examples/ea-project-split   views/capability-realization.yaml   --format mermaid   --output exports/capability-realization.mmd
```

Version 0.1 använder:

```text
flowchart LR
```

eller motsvarande riktning från view.layout.

## Determinism

Samma model + query + view ska ge:

- samma node-ID:n,
- samma edge-ID:n,
- samma ordning,
- samma koordinater,
- samma exporterade XML/Mermaid-text.

## Begränsningar i 0.1

- inga fullständiga ArchiMate-symboler,
- ingen automatisk avancerad edge routing,
- inga manuella koordinater,
- inga nested containers,
- ingen SVG/PNG-rendering utan extern renderare.

Det viktiga i steg 18 är att view-formatet nu faktiskt kan bli en redigerbar visuell artefakt.
