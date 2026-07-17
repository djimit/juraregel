# 5 controls die EU AI Act, BIO2 en NIS2 simultaan dekken

**Publicatie-target**: djimit.nl/blog
**Status**: Draft klaar, wacht op publicatie door Dennis

---

Nederlandse overheden staan voor een unieke uitdaging: voldoen aan vier tegelijk
geldende kaders voor AI-gebruik. De EU AI Act, BIO2, NIS2 en NORA — elk met
eigen definities, eigen risicoclassificaties, eigen meldplichten.

Het gevolg? Dezelfde risicoanalyse wordt drie keer geschreven in drie formaten
voor drie verschillende auditors.

## Het probleem: compliance-inflatie

Een gemeente die een AI-systeem inzet voor vergunningverlening moet:

1. Een **Fundamental Rights Impact Assessment** (EU AI Act Art. 27)
2. Een **risicoanalyse** volgens BIO2 (A.5-6)
3. Een **risicobeoordeling** volgens NIS2 (Art. 21)
4. Een **grondslag-toets** volgens NORA

Vier documenten. Vier formaten. Dezelfde kernvraag: *is deze AI veilig en
verantwoord in te zetten?*

## De oplossing: één control, meerdere kaders

Het Canadese [SCITus-framework](https://arxiv.org/abs/2607.15051) (arXiv:2607.15051)
bewijst dat dit anders kan. SCITUS mapped 127 federale en provinciale vereisten
naar 57 unified controls. Het resultaat: één controle die aan meerdere
wetgevingen voldoet.

Vandaag publiceren wij **NEDERUS** (Nederlandse Unified AI Standards) —
dezelfde methodologie, toegepast op de Nederlandse situatie.

## De 5 NEDERUS controls

| # | Control | EU AI Act | BIO2 | NIS2 | NORA |
|---|---------|-----------|------|------|------|
| 1 | AI Impact Assessment | Art. 9, 27 | A.5-6 | Art. 21 | Grondslag-toets |
| 2 | Bias & Fairness Testing | Art. 10 | — | — | Evenredigheid |
| 3 | Human Oversight | Art. 14 | — | — | Proportionaliteit |
| 4 | Transparency | Art. 13, 50 | — | — | Openbaarheid |
| 5 | Incident Response | Art. 72 | C.6-7 | Art. 23 | — |

Elke control is zodanig gedefinieerd dat implementatie ervan automatisch
aantoont dat je aan meerdere kaders voldoet.

## Open, versioned, gratis

NEDERUS is beschikbaar onder CC-BY 4.0 licentie op
[github.com/djimit/nederus-framework](https://github.com/djimit/nederus-framework).

Het framework is versioned (semver), heeft een publieke changelog, en een
validation pipeline die automatisch checkt of de mappings consistent zijn.

## Wat je nu kunt doen

1. **Download** de [mapping-matrix](https://github.com/djimit/nederus-framework/blob/main/mapping-matrix.csv)
2. **Lees** de [crosswalk-documentatie](https://github.com/djimit/nederus-framework/tree/main/crosswalks)
3. **Gebruik** de controls als startpunt voor je volgende compliance-review

Wil je weten hoe NEDITUS specifiek voor jouw organisatie kan worden ingezet?
[Neem contact op](https://djimit.nl/contact) voor een compliance quickscan.

---

*NEDERUS is geïnspireerd door SCITUS (arXiv:2607.15051) van Mohammad Etemad,
met dank voor de methodologische basis.*
