"""Uitgebreide assessment templates — Fase 2: Methodologisch rijk.

Templates gebaseerd op:
- EDPB/CNIL: DPIA ↔ FRIA overlap guidance
- ISO 27005:2022 + CNIL PIA methodology (risicoschaal)
- EU AI Act Art. 10 (data governance) + Art. 14 (human oversight)
- NIST AI 600-1 (Generative AI Profile)
- AVG Art. 5(1)(e) (bewaartermijnen) + Art. 30 (verwerkingsregister)
"""

from datetime import date
from typing import Any


def dpia_fria_overlap_matrix_template(org_naam: str, ai_systeem: str, **kwargs) -> dict:
    """DPIA ↔ FRIA Overlap-Matrix — Dubbel werk voorkomen.

    Gebaseerd op:
    - EDPB guidance: "use DPIA as starting point for FRIA"
    - CNIL: "DPIA et FRIA — comment articuler les deux?"
    - EU AI Act Art. 27(2): deployer mag rekening houden met reeds uitgevoerde DPIA

    Doel:
    1. Identificereen overlappende secties (niet dubbel invullen)
    2. Identificeren FRIA-specifieke secties (alleen in FRIA)
    3. Identificeren DPIA-specifieke secties (alleen in DPIA)
    4. Creer een gezamenlijke workflow
    """
    return {
        "document": "DPIA ↔ FRIA Overlap-Matrix",
        "wettelijke_basis": "AVG Art. 35 + EU AI Act Art. 27(2) + EDPB/CNIL guidance",
        "model_versie": "1.0 (EDPB/CNIL gebaseerd)",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "inleiding": {
                "titel": "Inleiding",
                "content": f"""
AI-systeem: [{ai_systeem}]

Art. 27(2) EU AI Act stelt dat de deployer rekening mag houden met reeds uitgevoerde DPIA's.
Deze matrix helpt om:
- Dubbel werk te voorkomen
- FRIA-specifieke aanvullingen te identificeren
- Een gezamenlijke workflow te creeren
""",
            },
            "matrix": {
                "titel": "Overlap-Matrix",
                "instructie": "Markeer voor elke sectie: DPIA-only, FRIA-only, of Overlap.",
                "content": """
| # | Sectie | DPIA | FRIA | Overlap | Actie |
|---|--------|------|------|---------|-------|
| 1 | Beschrijving verwerking / AI-systeem | ✅ | ✅ | ✅ | Eenmaal invullen, beiden gebruiken |
| 2 | Doel en context | ✅ | ✅ | ✅ | Eenmaal invullen |
| 3 | Betrokkenen / getroffen personen | ✅ | ✅ | ✅ | Eenmaal invullen |
| 4 | Noodzaak en proportionaliteit | ✅ | ✅ | ✅ | Eenmaal invullen |
| 5 | Risico-inschatting privacy | ✅ | ❌ | ❌ | DPIA-only |
| 6 | Maatregelen privacy (encryptie, pseudonimisering) | ✅ | ❌ | ❌ | DPIA-only |
| 7 | AP-overleg (Art. 36) | ✅ | ❌ | ❌ | DPIA-only |
| 8 | Grondrechtenanalyse (10+ rechten) | ❌ | ✅ | ❌ | FRIA-only |
| 9 | Kwetsbare groepen (uitgebreid) | ❌ | ✅ | ❌ | FRIA-only |
| 10 | Menselijke tussenkomst (Art. 14) | ❌ | ✅ | ❌ | FRIA-only |
| 11 | Geografische reikwijdte | ❌ | ✅ | ❌ | FRIA-only |
| 12 | Update triggers (Art. 27(3)) | ❌ | ✅ | ❌ | FRIA-only |
| 13 | Risico-analyse (algemeen) | ✅ | ✅ | ✅ | Gezamenlijk |
| 14 | Maatregelen (algemeen) | ✅ | ✅ | ✅ | Gezamenlijk |
| 15 | Goedkeuring | ✅ | ✅ | ✅ | Gezamenlijk |
""",
            },
            "workflow": {
                "titel": "Gezamenlijke Workflow",
                "content": """
Stap 1: Voer Pre-scan DPIA uit (zie dpia_pre_scan template)
  → GO? Ga naar Stap 2
  → NO-GO? DPIA niet verplicht, maar FRIA mogelijk wel (AI-systeem)

Stap 2: Voer DPIA uit (zie dpia_rijksdienst template)
  → Gezamenlijke secties invullen (rij 1-4, 13-15)
  → DPIA-only secties invullen (rij 5-7)

Stap 3: Voer AI Risicoclassificatie uit (zie ai_risicoclassificatie template)
  → Hoog-risico? FRIA verplicht
  → Niet hoog-risico? FRIA niet verplicht

Stap 4: Voer FRIA uit (zie fria_eu_template)
  → Gebruik DPIA voor overlappende secties
  → Vul FRIA-specifieke secties aan (rij 8-12)

Stap 5: Integreer en valideer
  → Consistentie tussen DPIA en FRIA
  → Goedkeuring door FG + AI-verantwoordelijke
  → Documenteer als geheel
""",
            },
            "praktische_tips": {
                "titel": "Praktische Tips",
                "content": """
1. Begin altijd met DPIA — dit vormt de basis
2. Gebruik dezelfde terminologie in beide documenten
3. Houd versiebeheer bij voor beide documenten
4. Plan gezamenlijke herziening (niet apart)
5. Bewaar beide documenten als één evidence-package
6. Let op: FRIA heeft kortere update-cyclus bij wijzigingen (Art. 27(3))
""",
            },
        },
    }


def kwantitatieve_risico_methodiek_template(
    org_naam: str, verwerking: str, **kwargs
) -> dict:
    """Kwantitatieve Risico-Methodiek — ISO 27005 + CNIL PIA gebaseerd.

    Gebaseerd op:
    - ISO/IEC 27005:2022 — Information security risk management
    - CNIL PIA Methodology (Guide 1) — 4-niveau risicoschaal
    - EDPB WP29 — DPIA risk assessment guidance
    - NIST SP 800-30 — Guide for Conducting Risk Assessments

    Biedt een gestandaardiseerde, reproduceerbare risico-methode
    die vervanging is voor de subjectieve 1-5 schaal in bestaande templates.
    """
    return {
        "document": "Kwantitatieve Risico-Methodiek",
        "wettelijke_basis": "ISO/IEC 27005:2022 + CNIL PIA + EDPB WP29",
        "model_versie": "1.0 (ISO/CNIL/EDPB gebaseerd)",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "inleiding": {
                "titel": "Inleiding",
                "content": f"""
Verwerking: [{verwerking}]

Deze methodiek vervangt subjectieve risicoschalen door een gestandaardiseerde,
reproduceerbare benadering gebaseerd op ISO 27005 en CNIL PIA.

4-niveau risicoschaal (CNIL):
- G1: Verwaarloosbaar (Negligible)
- G2: Beperkt (Limited)
- G3: Significant (Significant)
- G4: Maximaal (Maximal)

Elk niveau heeft gedefinieerde criteria voor zowel impact als waarschijnlijkheid.
""",
            },
            "impact_schaal": {
                "titel": "Impact-Schaal (G1-G4)",
                "content": """
G4 — MAXIMAAL:
- Onomkeerbare schade aan betrokkenen
- Fysiek letsel, financieel verlies >€100.000, discriminatie op grote schaal
- Fundamentele rechten ernstig aangetast
- Massa-expositie (>100.000 betrokkenen)
- Letsel voor levensonderhoud of gezondheid

G3 — SIGNIFICANT:
- Serieuze maar omkeerbare schade
- Financieel verlies €10.000-€100.000
- Discriminatie van individuen of kleine groepen
- Ernstige inbreuk op fundamentele rechten
- Expositie 10.000-100.000 betrokkenen

G2 — BEPERKTT:
- Beperkte maar merkbare schade
- Financieel verlies <€10.000
- Ongemak zonder blijvende gevolgen
- Inbreuk op privacy met beperkte reikwijdte
- Expositie 1.000-10.000 betrokkenen

G1 — VERWAARLOOSBAAR:
- Verwaarloosbare of geen schade
- Geen financieel verlies
- Gemakkelijk te herstellen
- Minimale inbreuk op privacy
- Expositie <1.000 betrokkenen
""",
            },
            "waarschijnlijkheid_schaal": {
                "titel": "Waarschijnlijkheid-Schaal (G1-G4)",
                "content": """
G4 — ZEER WAARSCHIJNLIJK:
- Geschiedenis van incidenten (≥1 per jaar)
- Kwetsbaarheid bekend en exploiteerbaar
- Geen effectieve maatregelen
- Externe dreiging actueel

G3 — WAARSCHIJNLIJK:
- Incidenten in verleden (1 per 3 jaar)
- Kwetsbaarheid bekend maar beperkt exploiteerbaar
- Enkele maatregelen aanwezig
- Dreiging plausibel

G2 — MOGELIJK:
- Geen geschiedenis, maar plausibel
- Kwetsbaarheid theoretisch
- Basismaatregelen aanwezig
- Dreiging mogelijk maar onwaarschijnlijk

G1 — ONWAARSCHIJNLIJK:
- Zeer onwaarschijnlijk gebaseerd op bewijs
- Geen bekende kwetsbaarheden
- Robuuste maatregelen
- Geen indicatie van dreiging
""",
            },
            "risicomatrix": {
                "titel": "Risico-Matrix (4x4)",
                "content": """
         │ G1 Impact │ G2 Impact │ G3 Impact │ G4 Impact
─────────┼───────────┼───────────┼───────────┼──────────
G4 Waar. │ G4 (Oranje)│ G4 (Rood)  │ G4 (Rood)  │ G4 (Rood)
G3 Waar. │ G3 (Geel)  │ G4 (Oranje)│ G4 (Rood)  │ G4 (Rood)
G2 Waar. │ G2 (Groen) │ G3 (Geel)  │ G4 (Oranje)│ G4 (Rood)
G1 Waar. │ G1 (Groen) │ G2 (Groen) │ G3 (Geel)  │ G4 (Oranje)

G1 (Groen)  : Accepteer — routine monitoring
G2 (Groen)  : Accepteer — periodieke review
G3 (Geel)   : Behandel — maatregelen vereist binnen 3 maanden
G4 (Oranje) : Behandel — maatregelen vereist binnen 1 maand
G4 (Rood)   : Stop — onmiddellijke maatregelen, AP-overleg bij hoog risico
""",
            },
            "risico_invulling": {
                "titel": "Risico-Invul-Template",
                "content": """
Risico [nummer]: [beschrijving]

Beschrijving:
[beschrijf het risico in termen van bedreiging × kwetsbaarheid × impact]

Bron/Threat:
[waarom kan dit gebeuren?]

Kwetsbaarheid:
[wat maat het mogelijk?]

Impact beoordeling:
- Type schade: [fysiek / financieel / reputatie / discriminatie / fundamentele rechten]
- Aantal betrokkenen: [___]
- Omvang: [G1/G2/G3/G4]
- Motivatie: [waarom dit niveau?]

Waarschijnlijkheid:
- Geschiedenis: [incidenten in verleden?]
- Exploiteerbaarheid: [makkelijk/moeilijk]
- Maatregelen: [welke zijn er al?]
- Niveau: [G1/G2/G3/G4]
- Motivatie: [waarom dit niveau?]

Risicoscore: [G1-G4] × [G1-G4] = [G1-G4]

Huidige maatregelen:
[beschrijf bestaande maatregelen]

Resicidaal risico na huidige maatregelen: [G1-G4]

Extra maatregelen (indien G3+):
[beschrijf aanvullende maatregelen]

Resicidaal risico na extra maatregelen: [G1-G4]

Acceptabel? [Ja/Nee]
Indien Nee: [verdere maatregelen of stop verwerking]
""",
            },
            "documentatie": {
                "titel": "Documentatie en Herziening",
                "content": """
- Alle risico's gedocumenteerd in risicoregister
- Scores onderbouwd met bewijs
- Herziening: jaarlijks of bij wijziging
- Goedkeuring: FG + management
- Versiebeheer: semver + changelog
""",
            },
        },
    }


def bias_audit_protocol_template(org_naam: str, ai_systeem: str, **kwargs) -> dict:
    """Bias Audit Protocol — EU AI Act Art. 10 + NIST AI 600-1.

    Gebaseerd op:
    - EU AI Act Art. 10(2)(f): training data must be relevant, sufficiently representative,
      and to the best extent possible, free of errors and complete
    - EU AI Act Art. 10(3): examine for possible biases
    - NIST AI 600-1 (Generative AI Profile): bias testing, fairness metrics
    - IEEE 7000-2021: addressing ethical concerns
    - AI Fairness 360 (IBM) / Fairlearn (Microsoft) metrics

    Doel: Kwantificeerbare bias-meting met drempelwaarden en remediation.
    """
    return {
        "document": "Bias Audit Protocol",
        "wettelijke_basis": "EU AI Act Art. 10(2)(f) + Art. 10(3) + NIST AI 600-1",
        "model_versie": "1.0 (EU AI Act + NIST gebaseerd)",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "inleiding": {
                "titel": "Inleiding",
                "content": f"""
AI-systeem: [{ai_systeem}]

Art. 10(3) EU AI Act: trainingsdata moeten worden onderzocht op mogelijke biases.
Dit protocol biedt een reproduceerbare methode voor bias-auditing met:
- Kwantitatieve metrics
- Gedefinieerde drempelwaarden
- Remediation-acties
""",
            },
            "stap_1": {
                "titel": "Stap 1 — Data-Profilering",
                "instructie": "Beschrijf de trainingsdata en identificeer beschermde kenmerken.",
                "content": """
1a. Trainingsdata beschrijving:
- Bron: [beschrijf data-bron]
- Omvang: [aantal records]
- Periode: [tijdsperiode data]
- Type: [gestructureerd / beeld / tekst / etc.]

1b. Beschermde kenmerken (protected attributes):
[ ] Geslacht
[ ] Leeftijd
[ ] Etniciteit / afkomst
[ ] Religie
[ ] Seksuele geaardheid
[ ] Handicap
[ ] Sociaaleconomische status
[ ] Andere: [specificeer]

1c. Distributie-analyse:
Voor elk beschermend kenmerk:
- Categorie: [naam]
- Aantal: [___]
- Percentage: [___%]
- Vergelijking met doelpopulatie: [representatief / ondervertegenwoordigd / oververtegenwoordigd]
- Bewijs: [link naar data-analyse]
""",
            },
            "stap_2": {
                "titel": "Stap 2 — Bias-Metrics",
                "instructie": "Meet bias met kwantitatieve metrics.",
                "content": """
2a. Demographic Parity (statistische pariteit):
- Definitie: P(Ŷ=1|A=a) = P(Ŷ=1|A=b) voor alle groepen a, b
- Gemeten waarde: [___]
- Drempel: verschil < 0.05 (5%)
- Resultaat: [Pass / Fail]

2b. Equalized Odds:
- Definitie: P(Ŷ=1|Y=y,A=a) = P(Ŷ=1|Y=y,A=b) voor alle y, a, b
- True Positive Rate verschil: [___]
- False Positive Rate verschil: [___]
- Drempel: verschil < 0.10 (10%)
- Resultaat: [Pass / Fail]

2c. Disparate Impact:
- Definitie: ratio van positieve uitkomsten tussen beschermde groep en referentie
- Gemeten waarde: [___]
- Drempel: 4/5 regel (0.80-1.25)
- Resultaat: [Pass / Fail]

2d. Individual Fairness:
- Definitie: vergelijkbare individuen krijgen vergelijkbare voorspellingen
- Gemeten waarde: [___]
- Drempel: [specificeer]
- Resultaat: [Pass / Fail]

2e. Intersectioneel (indien van toepassing):
- Beschermde combinaties: [bijv. vrouw + etniciteit]
- Gemeten waarde: [___]
- Resultaat: [Pass / Fail]
""",
            },
            "stap_3": {
                "titel": "Stap 3 — Bias-Bronanalyse",
                "instructie": "Identificeer de oorzaak van gevonden bias.",
                "content": """
3a. Historische bias:
[ ] Data weerspiegelt historische ongelijkheid
[ ] Data-collectie was bevooroordeeld
[ ] Andere: [beschrijf]

3b. Representatie-bias:
[ ] Ondervertegenwoordiging van bepaalde groepen
[ ] Steekproef-bias
[ ] Andere: [beschrijf]

3c. Meting-bias:
[ ] Features zijn proxy voor beschermde kenmerken
[ ] Labels zijn bevooroordeeld
[ ] Andere: [beschrijf]

3d. Aggregatie-bias:
[ ] Heterogene groepen worden samengevoegd
[ ] Context wordt genegeerd
[ ] Andere: [beschrijf]

3e. Confirmation:
[ ] Bias bevestigd door [test]
[ ] Geen bias gevonden
[ ] Onzeker — vereist verder onderzoek
""",
            },
            "stap_4": {
                "titel": "Stap 4 — Remediation",
                "instructie": "Definieer maatregelen om bias te mitigeren.",
                "content": """
4a. Pre-processing maatregelen:
[ ] Data-augmentatie voor ondervertegenwoordigde groepen
[ ] Herweging (reweighting) van samples
[ ] Resampling (over/under-sampling)
[ ] Feature-transformatie (debiasing)
[ ] Andere: [beschrijf]

4b. In-processing maatregelen:
[ ] Fairness constraints in loss function
[ ] Adversarial debiasing
[ ] Regularisatie voor fairness
[ ] Andere: [beschrijf]

4c. Post-processing maatregelen:
[ ] Threshold-adjustment per groep
[ ] Calibration van output
[ ] Andere: [beschrijf]

4d. Organisatorische maatregelen:
[ ] Menselijke review bij grensgevallen
[ ] Periodieke her-auditing (frequentie: [___])
[ ] Diverse ontwikkelteam
[ ] Externe validatie
[ ] Andere: [beschrijf]

4e. Gemeten verbetering na remediation:
- Metric voor: [___] → na: [___]
- Metric voor: [___] → na: [___]
- Alle drempels behaald? [Ja/Nee]
""",
            },
            "stap_5": {
                "titel": "Stap 5 — Documentatie en Monitoring",
                "content": """
5a. Audit-rapport:
- Datum audit: [datum]
- Uitgevoerd door: [naam, organisatie]
- Methodologie: [versie van dit protocol]
- Dataset: [versie + checksum]
- AI-model: [versie + checksum]

5b. Bevindingen samenvatting:
- Aantal geteste metrics: [___]
- Aantal Pass: [___]
- Aantal Fail: [___]
- Geconstateerde bias-bronnen: [lijst]
- Genomen remediation: [lijst]

5c. Monitoring:
- Frequentie her-audit: [elke 6 maanden / jaarlijks / bij wijziging]
- Automatische monitoring: [Ja/Nee — beschrijf]
- Alert-thresholds: [gedefinieerd]

5d. Goedkeuring:
- Auditor: [naam, functie, datum]
- AI-verantwoordelijke: [naam, functie, datum]
- FG: [naam, functie, datum]
""",
            },
        },
    }


def human_oversight_plan_template(org_naam: str, ai_systeem: str, **kwargs) -> dict:
    """Human Oversight Plan — EU AI Act Art. 14.

    Gebaseerd op:
    - EU AI Act Art. 14(1): high-risk AI systems designed to allow effective oversight
    - EU AI Act Art. 14(2): oversight measures indicated in instructions for use
    - EU AI Act Art. 14(3): oversight enables understanding, intervention, overruling, stopping
    - EU AI Act Art. 14(4): nature of oversight measures proportional to risk
    - EU AI Act Art. 14(5): effective human oversight ensured by deployer

    Deadline: 2 augustus 2026 — verplicht voor hoog-risico AI-systemen.
    """
    return {
        "document": "Human Oversight Plan",
        "wettelijke_basis": "EU AI Act Art. 14 (Verordening 2024/1689)",
        "model_versie": "1.0 (EU AI Act Art. 14 gebaseerd)",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "inleiding": {
                "titel": "Inleiding",
                "content": f"""
AI-systeem: [{ai_systeem}]

Art. 14(1): Hoog-risico AI-systemen worden zo ontworpen dat ze effectieve
menselijke tussenkomst mogelijk maken.

Art. 14(5): De deployer zorgt voor effectieve menselijke tussenkomst,
in overeenstemming met de instructies voor gebruik.

Deadline: 2 augustus 2026.
""",
            },
            "stap_1": {
                "titel": "Stap 1 — Oversight-Mechanismen",
                "instructie": "Beschrijf hoe menselijke tussenkomst is geimplementeerd.",
                "content": """
1a. Type oversight-mechanisme (Art. 14(4)):
[ ] Human-in-the-loop (HITL) — mens beslist vóór uitvoering
[ ] Human-on-the-loop (HOTL) — mens monitort en kan ingrijpen
[ ] Human-in-command (HIC) — mens geeft opdracht, AI voert uit
[ ] Human-override — mens kan output overrulen
[ ] Stop-kill-switch — mens kan systeem stoppen

1b. Implementatie-details:
- Waar in de workflow: [beschrijf]
- Hoeveel menselijke oversight-punten: [___]
- Responsetijd vereist: [seconden/minuten/uren]
- Escalatieprocedure: [beschrijf]

1c. Technische implementatie:
- Dashboard voor monitoring: [Ja/Nee]
- Alert-systemen: [beschrijf]
- Logging van menselijke ingrepen: [Ja/Nee]
- Audit trail: [Ja/Nee]
""",
            },
            "stap_2": {
                "titel": "Stap 2 — Oversight-Capaciteiten",
                "instructie": "Beschrijf wat de menselijke overseer moet kunnen.",
                "content": """
2a. Begrijpen (Art. 14(3)(a)):
[ ] Uitlegbaarheid (XAI) geïmplementeerd
[ ] Output is interpreteerbaar door mens
[ ] Besluitlogica is gedocumenteerd
[ ] Confidence-scores zijn zichtbaar

2b. Interveniëren (Art. 14(3)(b)):
[ ] Mens kan output wijzigen vóór gebruik
[ ] Mens kan parameters aanpassen
[ ] Mens kan systeem pauzeren
[ ] Mens kan alternatieve route kiezen

2c. Overrulen (Art. 14(3)(c)):
[ ] Mens kan AI-besluit negeren
[ ] Mens kan tegenbesluit nemen
[ ] Override wordt gelogd met reden
[ ] Override-frequentie wordt gemonitord

2d. Stoppen (Art. 14(3)(d)):
[ ] Kill-switch beschikbaar
[ ] Stop-procedure gedocumenteerd
[ ] Herstart-procedure gedocumenteerd
[ ] Fallback-procedure bij stopzetting
""",
            },
            "stap_3": {
                "titel": "Stap 3 — Rollen en Verantwoordelijkheden",
                "instructie": "Definieer wie oversight uitvoert.",
                "content": """
3a. Oversight-rollen:
- AI-verantwoordelijke: [naam, functie]
- Menselijke overseer(s): [naam, functie, kwalificaties]
- Escalatie-contact: [naam, functie]
- Technisch beheerder: [naam, functie]

3b. Kwalificaties overseer:
- Technisch begrip AI-systeem: [Ja/Nee]
- Training ontvangen: [Ja/Nee — datum: ___]
- Bevoegdheid tot overruling: [Ja/Nee]
- Beschikbaarheid: [24/7 / kantooruren / andere: ___]

3c. SLA voor menselijke oversight:
- Maximale responstijd: [___]
- Beschikbaarheid: [___%]
- Escalatietijd: [___]
- Rapportagefrequentie: [___]
""",
            },
            "stap_4": {
                "titel": "Stap 4 — Instructies voor Gebruik",
                "instructie": "Art. 14(2): oversight-maatregelen worden aangegeven in de gebruiksaanwijzing.",
                "content": """
4a. Gebruiksaanwijzing bevat:
[ ] Beschrijving van AI-systeem en beperkingen
[ ] Uitleg van besluitvormingslogica
[ ] Beschrijving van menselijke oversight-punten
[ ] Instructies voor overruling
[ ] Instructies voor stopzetting
[ ] Escalatieprocedure
[ ] Contactgegevens beheerder

4b. Toegankelijheid instructies:
[ ] Beschikbaar in Nederlands
[ ] Begrijpelijk voor eindgebruikers
[ ] Getest met gebruikers
[ ] Versie-beheer bijgehouden
""",
            },
            "stap_5": {
                "titel": "Stap 5 — Monitoring en Evaluatie",
                "content": """
5a. Effectiviteitsmetriken:
- Aantal menselijke interventies per [periode]: [___]
- Aantal overrides: [___]
- Responstijd (gemiddelde): [___]
- Escalaties: [___]
- Incidenten door gemiste oversight: [___]

5b. Evaluatie:
- Frequentie evaluatie: [elke 3 maanden / 6 maanden / jaarlijks]
- Laatste evaluatie: [datum]
- Bevindingen: [beschrijf]
- Verbeteracties: [beschrijf]

5c. Goedkeuring:
- AI-verantwoordelijke: [naam, datum]
- FG: [naam, datum]
- Management: [naam, datum]
""",
            },
        },
    }


def bewaarbeleid_template(org_naam: str, **kwargs) -> dict:
    """Bewaarbeleid / Retention Schedule — AVG Art. 5(1)(e) + Art. 30.

    Gebaseerd op:
    - AVG Art. 5(1)(e): bewaartermijn niet langer dan noodzakelijk
    - AVG Art. 30: verwerkingsregister met bewaartermijnen
    - Belastingdienst: 7 jaar administratieve verplichting
    - Archiefwet 1995: overbrengings- en vernietigingstermijnen
    - NEN-ISO 15489: records management

    Doel: Gestructureerd bewaarbeleid met per-categorie termijnen en vernietigingsproces.
    """
    return {
        "document": "Bewaarbeleid & Bewaarreglement",
        "wettelijke_basis": "AVG Art. 5(1)(e) + Art. 30 + Archiefwet 1995",
        "model_versie": "1.0 (AVG + Archiefwet gebaseerd)",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "inleiding": {
                "titel": "Inleiding",
                "content": f"""
Art. 5(1)(e) AVG: Persoonsgegevens worden bewaard in een vorm die
identificatie van betrokkenen slechts mogelijk zolang als noodzakelijk
voor de doeleinden waarvoor ze worden verwerkt.

Dit bewaarbied definieert:
- Bewaartermijnen per categorie
- Vernietigingsproces
- Uitzonderingen (wettelijke verplichtingen, lopende procedures)
- Verantwoordelijkheden
""",
            },
            "retention_schedule": {
                "titel": "Bewaartermijnen per Categorie",
                "instructie": "Pas de termijnen aan voor de context van de organisatie.",
                "content": """
| Categorie | Bewaartermijn | Wettelijke basis | Vernietiging |
|-----------|--------------|------------------|--------------|
| Personeelsadministratie | 7 jaar na eindiging | Belastingdienst + Arbeidsomstandighedenwet | Vernietigen |
| Salarisadministratie | 7 jaar | Belastingdienst | Vernietigen |
| Sollicitatiegegevens | 4 weken na afloop (of 1 jaar met toestemming) | AVG Art. 5(1)(e) | Vernietigen |
| Contractgegevens | 7 jaar na beëindiging | Verjaringstermijn | Vernietigen |
| Financiële administratie | 7 jaar | Belastingdienst | Vernietigen |
| Klantgegevens | 2 jaar na laatste contact | AVG Art. 5(1)(e) | Vernietigen |
| Website-statistieken | 26 maanden | AVG (Cookierichtlijn) | Anonimiseren of vernietigen |
| Camera-beeldmateriaal | Max. 72 uur | Tenzij incident | Vernietigen |
| Toestemmingen | Tot intrekking + 1 jaar | AVG Art. 7 | Vernietigen |
| Datalek-documentatie | 5 jaar na afhandeling | AVG Art. 33 | Archiveren |
| DPIA-documentatie | 5 jaar na beëindiging verwerking | AVG Art. 35 | Archiveren |
| Verzoeken betrokkenen | 2 jaar na afhandeling | AVG Art. 12-22 | Vernietigen |
| Correspondentie | 3 jaar | Organisatorisch | Vernietigen |
| Vergaderingstukken | 10 jaar | Bestuursrecht | Archiveren |
| Andere: [specificeer] | [termijn] | [basis] | [actie]
""",
            },
            "uitzonderingen": {
                "titel": "Uitzonderingen op Vernietiging",
                "content": """
Bewaartermijnen kunnen worden verlengd bij:

[ ] Wettelijke bewaarplicht (bijv. Belastingdienst: 7 jaar)
[ ] Lopende gerechtelijke procedure
[ ] Lopende bezwaar- of klachtprocedure
[ ] Openbaar belang (archiefwaarde)
[ ] Toestemming betrokkene voor langere bewaring
[ ] Anonimisering in plaats van vernietiging (voor statistiek/onderzoek)

Documenteer elke uitzondering:
- Reden: [beschrijf]
- Verlengde termijn: [___]
- Goedkeuring: [naam, functie, datum]
""",
            },
            "vernietigingsproces": {
                "titel": "Vernietigingsproces",
                "content": """
1. Trigger: bewaartermijn verstreken
2. Review: FG controleert op uitzonderingen
3. Goedkeuring: FG autoriseert vernietiging
4. Uitvoering: IT voert vernietiging uit
5. Certificaat: bewijs van vernietiging wordt bewaard
6. Registratie: vermelding in verwerkingsregister

Vernietigingsmethoden:
- Electronische data: secure wipe (NIST SP 800-88)
- Fysiek: vernietigingsdienst (certificaat)
- Back-ups: volgende cyclus of expliciete verwijdering
""",
            },
            "verantwoordelijkheden": {
                "titel": "Verantwoordelijkheden",
                "content": """
- FG: eigenaar bewaarbeleid, jaarlijkse review
- IT: technische uitvoering vernietiging
- Data-eigenaren: signalering verstreken termijnen
- Management: goedkeuring uitzonderingen
""",
            },
            "monitoring": {
                "titel": "Monitoring en Handhaving",
                "content": """
- Jaarlijkse review bewaarbeleid
- Kwartaalrapportage vernietigingen
- Alert-system voor verstreken termijnen
- Audit-trail van vernietigingen
- Handhaving: overtredingen melden aan FG
""",
            },
        },
    }
