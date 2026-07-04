# JuraRegel — Use Cases Beyond de Rechtspraak

## De Grotere Markt

JuraRegel is niet alleen voor de Rechtspraak. Het is voor **elke overheidsorganisatie die met regels werkt**. De pseudonimiseringsrichtlijn engine en griffierecht API bewijzen het concept. De volgende use cases bewijzen de schaal.

---

## UC-10: BIO2 — Baseline Informatiebeveiliging Overheid

### Wat is BIO2?

De BIO (Baseline Informatiebeveiliging Overheid) is het **normenkader voor informatiebeveiliging binnen alle overheidsentiteiten**. Gebaseerd op NEN-EN-ISO/IEC 27001/27002, aangevuld met specifieke overheidseisen.

- **167 maatregelen** in 4 categorieën (organisatorisch, mensgericht, fysiek, technologisch)
- **Bron**: [MinBZK GitHub](https://github.com/MinBZK/Baseline-Informatiebeveiliging-Overheid) + [bio-overheid.nl](https://www.bio-overheid.nl/category/producten/bio)
- **Versie**: BIO2 v1.2 (definitief), v1.3 (werkversie op GitHub)
- **Doelgroep**: ALLE overheidsentiteiten (honderden organisaties)
- **Compliance**: ENSIA (Elektronische Normering Systeem Informatiebeveiliging Ambtenaren)
- **Toezicht**: CIP (Centrum voor Informatiebeveiliging en Privacybescherming)

### Waarom BIO2 perfect is voor JuraRegel

| Criterium | BIO2 | JuraRegel fit |
|---|---|---|
| Regelhardheid | Hoog — maatregelen zijn verplicht | ✅ L1/L2 |
| Testbaarheid | Hoog — "is maatregel X geïmplementeerd?" is binair | ✅ Deterministisch |
| Brontraceerbaarheid | Hoog — elke maatregel verwijst naar ISO 27002 clause | ✅ sourceRef naar ISO |
| Versieerbaarheid | Hoog — v1.0 → v1.1 → v1.2 → v1.3 | ✅ JREM versioning |
| Businesswaarde | Zeer hoog — alle overheidsorganisaties | ✅ Massale schaal |
| Discretionaire ruimte | Laag — maatregelen zijn verplicht, niet discretionair | ✅ L1 |
| API-service potentieel | Hoog — "check BIO compliance" API | ✅ Rule API |
| PoC-risico | Laag — maatregelen staan al op GitHub in Markdown | ✅ Data beschikbaar |

### JuraRegel architectuur voor BIO2

```
BIO2 GitHub (MinBZK) — 167 maatregelen in Markdown
  ↓ Rule Extraction Sprint (parse Markdown → RegelSpraak)
RegelSpraak CNL — 167 regels met ISO 27002 verwijzingen
  ↓ Vertaling naar JREM
JREM exports — bio2-maatregelen-v1.2.json
  ↓ CI/CD gates
14 gates: brontraceability (ISO ref), coverage (alle 167), versie-check
  ↓ Rule API
POST /v1/bio2/check-maatregel
  Input: { maatregelId: "5.01.01", organisatie: "gemeente-X", implementatie: "ja", evidence: "beleid-document.pdf" }
  Output: { compliant: true, maatregel: "Informatiebeveiligingsbeleid opgesteld", isoRef: "ISO 27002 5.1.1", categorie: "organisatorisch" }
  ↓ Audit trail
ENSIA compliance report — per organisatie, per maatregel, per versie
```

### ENSIA integratie

ENSIA is het systeem waarmee overheidsorganisaties hun BIO-compliance rapporteren. JuraRegel kan de **rule engine** achter ENSIA worden:

1. Organisatie voert in: "maatregel 5.01.01 is geïmplementeerd, evidence = beleidsdocument"
2. JuraRegel checkt: "is dit voldoende voor BIO2 v1.2 maatregel 5.01.01?"
3. JuraRegel retourneert: "compliant ja/nee + ontbrekende elementen + ISO referentie"
4. Audit trail wordt opgeslagen voor ENSIA rapportage

### BIO2 maatregelen structuur

| Categorie | Aantal maatregelen | Voorbeeld |
|---|---|---|
| 5: Organisatorisch | ~60 | 5.01.01: Informatiebeveiligingsbeleid opgesteld |
| 6: Mensgericht | ~15 | 5.04.01: Scholing cyberbeveiligingsrisico's |
| 7: Fysiek | ~25 | Beveiliging van fysieke toegang |
| 8: Technologisch | ~67 | Encryptie, access control, logging |

Elke maatregel:
- Uniek nummer (5.01.01) → eerste 3 cijfers = ISO 27002 referentie
- Beschrijving (wat moet er gedaan worden)
- Verwijzing naar ISO 27002 beheersmaatregel
- Versie (BIO2 v1.0 → v1.1 → v1.2 → v1.3)

### RegelSpraak voorbeeld voor BIO2

```
regel BIO2-5.01.01 "Informatiebeveiligingsbeleid opgesteld":
  als maatregelId is "5.01.01"
  en implementatie is "ja"
  en evidence bevat "beleid" en "bestuur" en "vastgesteld"
  dan is compliant ja
  en is isoRef "ISO 27002 5.1.1"
  en is categorie "organisatorisch".

regel BIO2-5.01.01-NIET "Informatiebeveiligingsbeleid niet opgesteld":
  als maatregelId is "5.01.01"
  en implementatie is "nee"
  dan is compliant nee
  en is handmatige controle vereist
  met als reden "Maatregel 5.01.01 niet geïmplementeerd — beleid ontbreekt."
```

---

## UC-11: AVG/GDPR Compliance Checks

### Wat?
AVG (Algemene Verordening Gegevensbescherming) = GDPR in Nederland. Verplicht privacy by design, DPIA, data minimisation, recht op inzage.

### JuraRegel toepassing
- "Is voor deze verwerking een DPIA vereist?" → deterministisch op basis van criteria
- "Is bewaartermijn correct?" → regel met wettelijke termijn
- "Is data minimisation toegepast?" → check op veldniveau
- Bron: AVG artikelen, Uitvoeringsregeling AVG

### Regelhardheid: Hoog (L1/L2)

---

## UC-12: NIS2 — Network and Information Security

### Wat?
EU-richtlijn voor cybersecurity van essentiële en belangrijke entiteiten. Verplicht meldingen, risicobeheer, governance.

### JuraRegel toepassing
- "Valt deze organisatie onder NIS2?" → classificatie op basis van sector en grootte
- "Zijn de NIS2 meldingsverplichtingen geïmplementeerd?" → compliance check
- Bron: NIS2 richtlijn, Uitvoeringswet NIS2

### Regelhardheid: Hoog (L1/L2)

---

## UC-13: Belastingdienst — Belastingregels

### Wat?
Inkomstenbelasting, BTW, vennootschapsbelasting, heffingen, vrijstellingen.

### JuraRegel toepassing
- "Welk btw-tarief geldt voor dit product?" → deterministisch
- "Komt deze persoon in aanmerking voor heffingskorting?" → inkomensafhankelijk
- "Wat is de bewaartermijn voor deze belastingaanslag?" → wettelijk
- Bron: Wet inkomstenbelasting, Wet op de omzetbelasting

### Regelhardheid: Hoog (L1/L2)

---

## UC-14: UWV — Uitkeringsregels

### Wat?
Werkloosheidswet (WW), WIA, Wajong, AOW, kinderbijslag. Inkomensgrenzen, wachttijden, premies.

### JuraRegel toepassing
- "Heeft deze persoon recht op WW?" → voorwaarden check
- "Wat is de WW-uitkering hoogte?" → berekening op basis van verdiensten
- "Is de wachttijd correct berekend?" → termijnberekening
- Bron: Werkloosheidswet, WIA, Wajong

### Regelhardheid: Hoog (L1/L2)

---

## UC-15: IND — Verblijfsregels

### Wat?
Verblijfsvergunningen, naturalisatie, asiel. Inkomenseisen, integratieverplichtingen.

### JuraRegel toepassing
- "Komt deze aanvrager in aanmerking voor een verblijfsvergunning?" → voorwaarden check
- "Is aan het inkomenseis voldaan?" → drempelbedrag check
- Bron: Vreemdelingenwet 2000, Regeling uitvoering Vreemdelingenwet

### Regelhardheid: Hoog (L1/L2)

---

## UC-16: Gemeenten — Wmo en Participatiewet

### Wat?
Wmo-zorg, participatieuitkering, schuldhulpverlening, parkeervergunningen.

### JuraRegel toepassing
- "Komt deze burger in aanmerking voor Wmo-zorg?" → voorwaarden check
- "Wat is de hoogte van de participatieuitkering?" → berekening
- "Is een parkeervergunning vereist?" → gebiedscheck
- Bron: Wmo 2015, Participatiewet

### Regelhardheid: Hoog (L1/L2)

---

## Use Case Portfolio — Buiten de Rechtspraak

| # | Use Case | Domein | Regelhardheid | Schaal | Bron beschikbaar |
|---|---|---|---|---|---|
| UC-10 | **BIO2** | Informatiebeveiliging | Hoog | Alle overheidsentiteiten | ✅ GitHub (MinBZK) |
| UC-11 | AVG/GDPR compliance | Privacy | Hoog | Alle organisaties | ✅ Wetten.overheid.nl |
| UC-12 | NIS2 | Cybersecurity | Hoog | Essentiële entiteiten | ✅ EU-richtlijn |
| UC-13 | Belastingregels | Fiscaal | Hoog | Alle burgers/bedrijven | ✅ Wetten.overheid.nl |
| UC-14 | UWV uitkeringsregels | Sociale zekerheid | Hoog | alle werknemers | ✅ Wetten.overheid.nl |
| UC-15 | IND verblijfsregels | Immigratie | Hoog | Alle migranten | ✅ Wetten.overheid.nl |
| UC-16 | Gemeenten Wmo/Participatie | Sociaal domein | Hoog | Alle gemeenten | ✅ Wetten.overheid.nl |

---

## Strategische Positionering

### JuraRegel als Cross-Government Platform

```
                    JuraRegel Platform
                   /    |    |    \    \
                  /     |    |     \    \
          Rechtspraak  BIO2  AVG  Belasting  UWV  IND  Gemeenten
          (pilot)     (volgende)
```

De Rechtspraak is de pilot. BIO2 is de volgende use case die de schaal bewijst: niet één domein, maar **alle overheidsentiteiten**.

### De BIO2 pitch

> "De BIO2 heeft 167 beveiligingsmaatregelen, gebaseerd op ISO 27002, die elke overheidsorganisatie moet implementeren. JuraRegel vertaalt deze maatregelen naar testbare, auditeerbare regels met een Rule API: 'is maatregel 5.01.01 geïmplementeerd?' Met ENSIA integratie voor compliance reporting. Niet handmatig checken — automatisch valideren."

### Waarom BIO2 de beste volgende use case is

1. **Data staat al op GitHub** — MinBZK repo met 167 maatregelen in Markdown
2. **Massale schaal** — alle overheidsentiteiten, niet één domein
3. **ISO gekoppeld** — elke maatregel heeft een ISO 27002 referentie (brontraceerbaarheid)
4. **Versiebeheer** — BIO2 v1.0 → v1.2 → v1.3 (JREM versioning)
5. **Compliance reporting** — ENSIA als bestaand systeem dat JuraRegel kan aanjagen
6. **NIS2 overlap** — BIO2 topics bevatten NIS2 (cybersecurity richtlijn)
7. **CIP ondersteuning** — CIP beheert de BIO en kan JuraRegel adopteren
8. **Rule Maturity Model** — BIO2 maatregelen zijn L1 (deterministisch, verplicht)

### Verbinding met bestaand werk

| Bestaand | BIO2 connectie |
|---|---|
| Pseudonimiseringsrichtlijn engine | Beide implementeren een richtlijn als code |
| JREM open standaard | BIO2 maatregelen → JREM exports met ISO refs |
| CI/CD gates | Brontraceability → ISO 27002 reference per maatregel |
| Rule API factory | `create_app("bio2", jrem_path, 8494)` |
| Rule Maturity Model | BIO2 = L1 (deterministisch, geen discretionaire ruimte) |
| Whitepaper | "From PDFs to APIs" → "From Markdown to APIs" (BIO2 staat op GitHub) |

### De volgende Rule Extraction Sprint voor BIO2

1. **Dag 1**: Parse MinBZK GitHub Markdown → extract 167 maatregelen met structuur
2. **Dag 2**: Begrippenmodel — maatregelId, categorie, isoRef, compliant, evidence
3. **Dag 3-4**: Beslistabellen — per maatregel: voorwaarden → compliant ja/nee
4. **Dag 5**: JREM export met 167 regels, ISO refs, scenario's
5. **Dag 6-7**: Jurist-acceptatie — CIP beoordeelt of regels conform BIO2 v1.2
