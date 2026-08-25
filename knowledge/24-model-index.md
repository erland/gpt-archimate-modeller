# Model index

`MODEL-INDEX.json` är ett deriverat, rebuildable läsindex och aldrig source of truth.

Använd index endast när source fingerprint matchar.
Vid stale/missing/invalid index: fallback till canonical YAML assembler.

Packning bygger alltid om indexet.

Indexets syfte är att eliminera upprepad dyr YAML-assemblering i stora projekt.
