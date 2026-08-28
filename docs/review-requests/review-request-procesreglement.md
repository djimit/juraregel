# Review Request — Procesreglement Rules

## Use case: `procesreglement`

**Domein:** Civiele dagvaardingszaken — procesreglementregels voor digitale indiening

**JREM versie:** 2026.1
**Aantal regels:** 20
**Aantal tests:** 1 quarantaine-invariant
**API poort:** 8491

---

## Wat wordt gereviewd?

Deze use case vertaalt de volgende bronnen naar testbare, auditeerbare regels in het JuraRegel JREM formaat:

- Landelijk procesreglement civiele dagvaardingszaken, juli 2025-juni 2026
- Landelijk procesreglement civiele dagvaardingszaken, tweede versie vanaf 1 juli 2026
- Reglement inzake toegang tot en gebruik van systeem DT Rechtspraak

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

De use case bevat 16 testscenario's die de regels valideren. De jurist kan deze scenario's gebruiken om randgevallen en uitzonderingen te identificeren die mogelijk ontbreken.

## Uitkomst van review

Per regel kan de jurist aangeven:

- ✅ **Accordeer** — regel is juridisch correct
- ⚠️ **Accordeer met opmerking** — regel is grotendeels correct, met aanvulling
- ❌ **Afkeur** — regel bevat een juridische fout of is incompleet

## Status

- **Huidige status:** Quarantaine; alle uitkomsten zijn fail-closed en vereisen handmatige controle
- **Doel:** Eerst reconstructie per bronversie, daarna pas onafhankelijke review en eventuele pilot
- **Na review:** Resultaten worden vastgelegd in `docs/review-results/procesreglement.md`

---

*Deze review request is gegenereerd door JuraRegel. Zie [README.md](../../README.md) voor het volledige platform overzicht.*
