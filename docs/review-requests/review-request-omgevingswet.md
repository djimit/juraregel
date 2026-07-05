# Review Request — Omgevingswet Activiteitenbesluit Rule Service

## Use case: `omgevingswet`

**Domein:** Omgevingswet — bepaling vergunningplichtig, meldingplichtig of vrij bij activiteiten in de leefomgeving

**JREM versie:** 2025.1
**Aantal regels:** 20
**Aantal tests:** 19
**API poort:** 8515

---

## Wat wordt gereviewd?

Deze use case vertaalt de volgende bronnen naar testbare, auditeerbare regels in het JuraRegel JREM formaat:

- Omgevingswet (Stb. 2021, 413)
- Besluit activiteiten leefomgeving (Bal)
- Activiteitenbesluit milieubeheer

## Review criteria

De jurist wordt gevraagd per regel te beoordelen:

1. **Broninterpretatie** — Is de juridische bron juist geïnterpreteerd in de regel?
2. **Regeltekst** — Is de RegelSpraak/CNL tekst juridisch correct en volledig?
3. **Voorwaarden** — Zijn de voorwaarden compleet en juist geordend?
4. **Uitkomst** — Is het rechtsgevolg juist weergegeven?
5. **Uitzonderingen** — Ontbreken er uitzonderingen die in de PoC moeten worden meegenomen?
6. **Geldigheid** — Zijn validFrom/validUntil juist en conform de bron?
7. **Bronverwijzing** — Is elke regel herleidbaar naar de juiste wetsbepaling of richtlijn?

## Testscenario's

De use case bevat 19 testscenario's die de regels valideren. De jurist kan deze scenario's gebruiken om randgevallen en uitzonderingen te identificeren die mogelijk ontbreken.

## Uitkomst van review

Per regel kan de jurist aangeven:

- ✅ **Accordeer** — regel is juridisch correct
- ⚠️ **Accordeer met opmerking** — regel is grotendeels correct, met aanvulling
- ❌ **Afkeur** — regel bevat een juridische fout of is incompleet

## Status

- **Huidige accordering:** Self-approved door D. Landman (niet onafhankelijk)
- **Doel:** Onafhankelijke jurist-review voordat deze use case in productie wordt genomen
- **Na review:** Resultaten worden vastgelegd in `docs/review-results/omgevingswet.md`

---

*Deze review request is gegenereerd door JuraRegel. Zie [README.md](../../README.md) voor het volledige platform overzicht.*
