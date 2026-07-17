# NORA Compliance Matrix

## Architectuur Overzicht

```mermaid
graph TD
    NORA[NURA Compliance API :8497]
    
    NORA --> N1[NORA-001: Open standaarden]
    NORA --> N2[NORA-002: Digitaal]
    NORA --> N3[NORA-003: Beveiliging]
    NORA --> N6[NORA-006: Identiteit]
    NORA --> N7[NORA-007: Privacy by design]
    NORA --> N10[NORA-010: API standaardisatie]
    
    N1 --> FS[Forum Standaardisatie :8495]
    N1 --> OS[Overheidsstandaarden :8496]
    N2 --> GR[Griffierecht :8490]
    N2 --> PR[Procesreglement :8491]
    N2 --> CL[Classificatie :8492]
    N3 --> BIO[BIO2 :8494]
    N3 --> PUB[Publicatie/PII :8493]
    N6 --> OS
    N7 --> PUB
    N10 --> OS
```

## Principes → Use Cases Mapping

| NORA Principe | Use Case | Poort | Regels |
|---|---|---|---|
| Open standaarden | Forum Standaardisatie | 8495 | 22 |
| Open standaarden | Overheidsstandaarden | 8496 | 24 |
| Digitaal | Griffierecht | 8490 | 36 |
| Digitaal | Procesreglement | 8491 | 4 |
| Digitaal | Classificatie | 8492 | 3 |
| Beveiliging | BIO2 | 8494 | 162 |
| Beveiliging | Publicatie (PII) | 8493 | 3 |
| Identiteit | Overheidsstandaarden | 8496 | 24 |
| Privacy by design | Publicatie (PII) | 8493 | 3 |
| API standaardisatie | Overheidsstandaarden | 8496 | 24 |
| Event-driven | Overheidsstandaarden | 8496 | 24 |
| Gegevensuitwisseling | Overheidsstandaarden | 8496 | 24 |
| Sovereignty | BIO2 | 8494 | 162 |

## NEDERUS Mapping

NEDERUS (Nederlandse Unified AI Standards) koppelt NORA principes aan EU AI Act,
BIO2 en NIS2. De matrix hieronder toont welke NEDERUS controls dekking bieden
voor elk NORA principe.

| NORA Principe | NEDERUS Control | EU AI Act | BIO2 | NIS2 |
|---|---|---|---|---|
| Grondslag-toets | NED-01 | Art. 9(2), Art. 27 | A.5-6 | Art. 21 |
| Evenredigheid | NED-02 | Art. 10 | — | — |
| Proportionaliteit | NED-03 | Art. 14 | — | — |
| Openbaarheid | NED-04 | Art. 13, Art. 50 | — | — |
| Verantwoordelijkheid | NED-01, NED-03 | Art. 9, Art. 14 | A.5-6 | — |

Zie [NEDERUS repository](https://github.com/djimit/nederus-framework) voor de
volledige mapping-matrix en crosswalk-documentatie.
