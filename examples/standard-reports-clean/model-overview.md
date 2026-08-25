# Modellöversikt

Sammanfattande inventering av modellens element och relationer.

## Element per typ

Totalt: **3**

| Grupp | Antal |
|---|---:|
| ApplicationComponent | 1 |
| Capability | 1 |
| Node | 1 |

## Element

| ID | Typ | Namn | Specialisering |
| --- | --- | --- | --- |
| `STR-000001` | Capability | Ärendehantering | — |
| `APP-000001` | ApplicationComponent | Ärendehanteringssystem | BusinessApplication |
| `TEC-000001` | Node | Containerplattform | Platform |

## Relationer

| ID | Typ | Källa | Mål | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- |
| `REL-000001` | Realization | `APP-000001` | `STR-000001` | inferred | medium |
