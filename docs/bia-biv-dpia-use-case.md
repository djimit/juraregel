# BIA-BIV-DPIA Use Case — Business Impact Analyse + BIV + DPIA

## User Story

**Als** CIO, security officer of DPO bij een overheidsorganisatie **wil ik** een geïntegreerde Business Impact Analyse (BIA), BIV-classificatie (Beschikbaarheid, Integriteit, Vertrouwelijkheid), risico-analyse én Data Protection Impact Assessment (DPIA) kunnen uitvoeren **zodat** ik voldoe aan BIO2, AVG Art. 35, NEN-ISO 27001 én de verplichtingen van de Autoriteit Persoonsgegevens.

## Wetelijke Basis

| Wet/Standaard | Artikel | Verplichting |
|---|---|---|
| AVG | Art. 35 lid 1 | DPIA verplicht bij hoog risico |
| AVG | Art. 35 lid 3a | DPIA verplicht voor bijzondere categorieën + grootschalige verwerking |
| AVG | Art. 35 lid 7 | DPIA minimum inhoud (beschrijving, beoordeling, maatregelen) |
| AVG | Art. 35 lid 11 | Periodieke herziening DPIA |
| AVG | Art. 36 lid 2 | Voorafgaand overleg AP bij hoog resterend risico |
| AVG | Art. 25 | Privacy by design + by default |
| BIO2 | A.5-6 | Risicoanalyse + business impact analyse |
| BIO2 | A.8 | Classificatie van informatie (BIV) |
| BIO2 | A.10 | Cryptografie voor vertrouwelijkheid |
| BIO2 | A.11 | Beheer van beschikbaarheid |
| BIO2 | A.12 | Beheer van integriteit |
| NEN-ISO/IEC 27001:2017 | A.8.2 | Business impact analysis |
| NEN-ISO 27005 | — | Risicomanagement |
| EU AI Act | Art. 27 | FRIA (Fundamental Rights Impact Assessment) voor AI |

## De 32 Regels — 5 Categorieën

### 1. Business Impact Analyse (5 regels)

| ID | Regel | Prioriteit |
|----|-------|------------|
| BIA-001 | Procesidentificatie verplicht | P3 |
| BIA-002 | Hersteltijd kritiek (≤4u) | P1 |
| BIA-003 | Hersteltijd catastrofaal (≤1u) | P0 |
| BIA-004 | Hersteltijd beperkt (≤24u) | P3 |
| BIA-005 | Hersteltijd te lang voor impactniveau | P2 |

### 2. BIV Classificatie (6 regels)

| ID | Regel | BIV-aspect |
|----|-------|------------|
| BIV-001 | BIV classificatie verplicht | Algemeen |
| BIV-002 | Hoge beschikbaarheid maatregelen | Beschikbaarheid |
| BIV-003 | Hoge integriteit maatregelen | Integriteit |
| BIV-004 | Hoge vertrouwelijkheid maatregelen | Vertrouwelijkheid |
| BIV-005 | BIV mismatch detectie | Consistentie |
| BIV-006 | BIV score berekening | Score |

### 3. Risico-analyse (6 regels)

| ID | Regel | Risico |
|----|-------|--------|
| RIS-001 | Risicoberekening verplicht | Algemeen |
| RIS-002 | Kritiek risico — directe actie | Kritiek |
| RIS-003 | Zeer hoog risico — maatregel | Zeer hoog |
| RIS-004 | Hoog risico — acceptatie | Hoog |
| RIS-005 | Laag risico — acceptabel | Laag |
| RIS-006 | Residuaal risico acceptabel | Residuaal |

### 4. DPIA (12 regels)

| ID | Regel | Artikel |
|----|-------|---------|
| DPI-001 | DPIA verplicht niet uitgevoerd | Art. 35(1) |
| DPI-002 | DPIA uitgevoerd — compliant | Art. 35(1) |
| DPI-003 | Bijzondere categorie — DPIA verplicht | Art. 35(3a) |
| DPI-004 | Grootschalige verwerking — DPIA verplicht | Art. 35(3a) |
| DPI-005 | Beperkingsmaatregelen na DPIA | Art. 35(7d) |
| DPI-006 | DPIA gedeeltelijk — afronden | Art. 35(7) |
| DPI-007 | DPIA herziening | Art. 35(11) |
| DPI-008 | Geen DPIA nodig | Art. 35(1) |
| DPI-009 | Advies toezichthouder | Art. 36(2) |
| DPI-010 | Privacy by design | Art. 25 |
| DPI-011 | DPIA documentatie | Art. 35(7a-f) |
| DPI-012 | DPIA + FRIA voor AI | Art. 27 AI Act |

### 5. Combinatie (3 regels)

| ID | Regel | Scope |
|----|-------|-------|
| COM-001 | Kritiek proces + hoog risico + DPIA | Integraal |
| COM-002 | Acceptabel risico zonder DPIA | Integraal |
| COM-003 | BIV zeer hoog + DPIA verplicht | Integraal |

## API Endpoints

| Endpoint | Functie |
|----------|---------|
| `POST /v1/bia-biv-dpia/calculate` | Compliance check |
| `GET /v1/bia-biv-dpia/standaarden` | Lijst alle 32 regels |
| `GET /v1/health` | Healthcheck |

## DPIA Stappenplan (conform AP-richtlijnen)

1. **Drempeltoets**: Staat de verwerking op de AP-lijst?
2. **Beschrijving**: Beschrijf de verwerking (doel, gegevens, rechtsgrond)
3. **Noodzaak + Proportionaliteit**: Is de verwerking noodzakelijk en evenredig?
4. **Risico-beoordeling**: Beoordel risico's voor rechten en vrijheden
5. **Maatregelen**: Identificeer maatregelen om risico's te mitigeren
6. **Documentatie**: Documenteer alles conform Art. 35(7a-f)
7. **Herziening**: Herzie minimaal jaarlijks of bij wijziging

## Boetebeleid

| Overtreding | Boete |
|-------------|-------|
| Geen DPIA bij verplichting | Tot €10M of 2% wereldwijze omzet (Art. 83(4)) |
| Onvolledige DPIA | Tot €10M of 2% wereldwijze omzet |
| Geen privacy by design | Tot €10M of 2% wereldwijze omzet |

## Voorbeeld: Gemeente met WOZ-systeem

**Situatie**: Gemeente verwerkt WOZ-gegevens (persoonsgegevens + bijzondere categorie: economische situatie). Systeem is kritisch voor heffing.

**BIA**: Impact = kritiek, hersteltijd = 4u → Continuïteitsplan vereist
**BIV**: Beschikbaarheid = zeer_hoog, Integriteit = zeer_hoog, Vertrouwelijkheid = zeer_hoog
**Risico**: Hoog (impact × waarschijnlijkheid) → Management acceptatie vereist
**DPIA**: Verplicht (bijzondere categorie + grootschalig) → Uitvoeren vóór livegang

## NEDERUS Koppeling

| NEDERUS Control | BIA-BIV-DPIA Koppeling |
|---|---|
| NED-01 AI Impact Assessment | BIA-002: Kritisch proces impact |
| NED-04 Transparency | DPI-011: DPIA documentatie |
| NED-05 Incident Response | BIA-003: Catastrofale impact response |
| NED-06 Secure Development | BIV-002/003/004: BIV maatregelen |
| NED-08 AI Liability | DPI-012: DPIA + FRIA voor AI |

## Bronnen

- [Autoriteit Persoonsgegevens — DPIA](https://www.autoriteitpersoonsgegevens.nl/themas/basis-avg/praktisch-avg/data-protection-impact-assessment-dpia)
- [AP — Lijst verplichte DPIA](https://www.autoriteitpersoonsgegevens.nl/documenten/lijst-verplichte-dpia)
- [AVG Art. 35 — EUR-Lex](https://eur-lex.europa.eu/eli/reg/2016/679/art_35)
- [BIO2 — Baseline Informatiebeveiliging Overheid](https://www.digitaleoverheid.nl/overzicht-van-alle-onderwerpen/cybersecurity/bio-en-ensia/baseline-informatiebeveiliging-overheid/)
- [NEN-ISO/IEC 27001:2017](https://www.iso.org/standard/75652.html)
- [NEN-ISO 27005 — Risicomanagement](https://www.iso.org/standard/75652.html)
- [EU AI Act Art. 27 — FRIA](https://eur-lex.europa.eu/eli/reg/2024/1689)
- [EDPB DPIA Guidelines](https://edpb.europa.eu/our-work-tools/our-documents/topic/data-protection-impact-assessment-dpia_nl)
