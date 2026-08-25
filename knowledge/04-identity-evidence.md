# Identity, sources and evidence

## Stable IDs

Format:

```text
PREFIX-NNNNNN
```

Vanliga prefixes:

- MOT
- STR
- BUS
- APP
- TEC
- PHY
- IMP
- CMP
- REL
- SRC
- REF
- ISS
- EV
- CHG

`type` är auktoritativt.
Prefix uttrycker familj/partition och får inte användas för att inferera typ när `type` säger annat.

## Matchning

Prioritet:

1. exakt ID,
2. alias,
3. exakt namn + kompatibel typ,
4. normaliserat namn,
5. extern ID,
6. semantisk likhet.

Osäker match -> issue, inte automatisk merge.

## Evidence

Evidence-status:

- user_confirmed
- document_confirmed
- imported
- inferred
- mixed
- unknown

Assertion kinds:

- explicit
- user_statement
- imported
- derived
- inferred
- contradicting

Derived/inferred kräver `reason`.

## Source och reference

Source beskriver källan.
Reference beskriver exakt position i källan.

Använd `reference_refs` när exakt lokalisering finns.
Använd `source_refs` när bara övergripande källa finns.

Fabricera aldrig referenser.
