"""Uitgebreide assessment templates — Fase 3: Academisch diep.

Templates gebaseerd op:
- IEEE 7000-2021: Model Process for Addressing Ethical Concerns
- Value Sensitive Design (Friedman & Kahn, 2003; Friedman et al., 2017)
- NIST AI RMF 1.0 (NIST AI 100-1) + Generative AI Profile (NIST AI 600-1)
- EDPB WP29: DPIA iterative process (test, improve, check)
- AVG Art. 35(2): stakeholder consultation
"""

from datetime import date
from typing import Any


def ethics_by_design_framework_template(org_naam: str, systeem: str, **kwargs) -> dict:
    """Ethics by Design Framework — IEEE 7000-2021 Value-Based Engineering.

    Gebaseerd op:
    - IEEE 7000-2021: Model Process for Addressing Ethical Concerns
    - IEEE/ISO/IEC 24748-7000:2022 (international variant)
    - Value-Based Engineering (VBE) methodology

    4 kernprocessen:
    1. Value Elicitation — ethische waarden identificeren
    2. Value Prioritization — conflicten oplossen
    3. Ethical Risk Assessment — risico's op waarden beoordelen
    4. Values Traceability — waarden door ontwerp heen traceren
    """
    return {
        "document": "Ethics by Design Framework",
        "wettelijke_basis": "IEEE 7000-2021 + IEEE/ISO/IEC 24748-7000:2022",
        "model_versie": "1.0 (IEEE 7000-2021 gebaseerd)",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "inleiding": {
                "titel": "Inleiding",
                "content": f"""
Systeem: [{systeem}]

IEEE 7000-2021 is het eerste IEEE-standaard voor ethisch systeemontwerp.
Het biedt een Value-Based Engineering (VBE) proces om ethische waarden
(fairness, transparantie, privacy, autonomie, menselijke waardigheid)
als engineering-requirements te behandelen — niet als afterthought.

4 kernprocessen:
1. Value Elicitation — welke ethische waarden zijn relevant?
2. Value Prioritization — hoe los je conflicten tussen waarden op?
3. Ethical Risk Assessment — welke risico's bestaan er voor deze waarden?
4. Values Traceability — hoe traceer je waarden door het ontwerp heen?
""",
            },
            "proces_1": {
                "titel": "Proces 1 — Value Elicitation",
                "instructie": "Identificeer ethische waarden die relevant zijn voor het systeem en stakeholders.",
                "content": """
1a. Stakeholder-identificatie:
[ ] Directe gebruikers: [wie]
[ ] Indirecte betrokkenen: [wie]
[ ] Maatschappij: [welke groepen]
[ ] Toekomstige generaties: [relevant?]

1b. Ethische waarden (selecteer relevante):
[ ] Menselijke waardigheid (Human Dignity)
[ ] Autonomie (self-determination, informed consent)
[ ] Privacy (data protection, informational self-determination)
[ ] Fairness (non-discrimination, equal treatment)
[ ] Transparantie (explainability, openness)
[ ] Accountability (responsibility, auditability)
[ ] Veiligheid (safety, non-maleficence)
[ ] Duurzaamheid (environmental impact, long-term effects)
[ ] Inclusie (accessibility, digital divide)
[ ] Vertrouwenswaardigheid (trustworthiness)
[ ] Andere: [specificeer]

1c. Waarden uit elke stakeholder-perspectief:
Stakeholder: [naam]
- Belangrijkste waarde: [waarde]
- Reden: [waarom]
- Potentieel conflict met: [waarde]

Stakeholder: [naam]
- Belangrijkste waarde: [waarde]
- Reden: [waarom]
- Potentieel conflict met: [waarde]

1d. Conceptueel model:
[beschrijf hoe de geïdentificeerde waarden zich verhouden tot het systeem]
""",
            },
            "proces_2": {
                "titel": "Proces 2 — Value Prioritization",
                "instructie": "Los conflicten tussen waarden op via gestructureerde dialoog.",
                "content": """
2a. Identificeer waarde-conflicten:
Conflict 1: [waarde A] vs [waarde B]
- Context: [wanneer treedt dit op?]
- Impact: [wat zijn de gevolgen?]
- Stakeholders: [wie zijn betrokken?]

Conflict 2: [waarde A] vs [waarde B]
- Context: [wanneer treedt dit op?]
- Impact: [wat zijn de gevolgen?]
- Stakeholders: [wie zijn betrokken?]

2b. Prioriteringsmethode:
[ ] Stakeholder-dialoog (consensus)
[ ] Expert-panel (Delphi-methode)
[ ] Maatschappelijke impact-analyse
[ ] Rechten-based approach (mensenrechten als floor)
[ ] Andere: [specificeer]

2c. Resolutie per conflict:
Conflict 1 resolutie:
- Keuze: [waarde A krijgt prioriteit / balans / context-afhankelijk]
- Onderbouwing: [waarom]
- Acceptabel voor stakeholders? [Ja/Nee — motiveer]

Conflict 2 resolutie:
- Keuze: [waarde A krijgt prioriteit / balans / context-afhankelijk]
- Onderbouwing: [waarom]
- Acceptabel voor stakeholders? [Ja/Nee — motiveer]

2d. Geprioriteerde waarden-lijst:
1. [hoogste prioriteit]
2. [___]
3. [___]
4. [___]
5. [___]
""",
            },
            "proces_3": {
                "titel": "Proces 3 — Ethical Risk Assessment",
                "instructie": "Beoordeel risico's op de geïdentificeerde ethische waarden.",
                "content": """
3a. Risico-identificatie per waarde:

Waarde: [naam]
- Risico: [beschrijving]
- Bron: [waarom kan dit gebeuren?]
- Impact op waarde: [G1-G4 risicoschaal]
- Waarschijnlijkheid: [G1-G4]
- Risicoscore: [G1-G4]

Waarde: [naam]
- Risico: [beschrijving]
- Bron: [waarom kan dit gebeuren?]
- Impact op waarde: [G1-G4]
- Waarschijnlijkheid: [G1-G4]
- Risicoscore: [G1-G4]

3b. Risico-behandeling:
[ ] Verminderen (mitigeren)
[ ] Accepteren (documenteren)
[ ] Vermijden (stoppen)
[ ] Oververzekeren (transfereren)

3c. Ethische "red lines":
[definieer absolute grenzen die niet overschreden mogen worden]
- [red line 1]
- [red line 2]
""",
            },
            "proces_4": {
                "titel": "Proces 4 — Values Traceability",
                "instructie": "Traceer ethische waarden door het ontwerp en de implementatie.",
                "content": """
4a. Traceability matrix:

| Waarde | Requirement | Design Decision | Implementatie | Test | Status |
|--------|-------------|-----------------|---------------|------|--------|
| [waarde] | [req-id] | [besluit] | [code/config] | [test] | [✅/❌] |
| [waarde] | [req-id] | [besluit] | [code/config] | [test] | [✅/❌] |

4b. Value-to-Requirement mapping:
- Waarde: [naam] → Requirement: [req-id] → Rationale: [waarom deze mapping]

4c. Design-ethiek review:
[ ] Design-review met ethiek-perspectief gepland
[ ] Ethiek-lens toegepast op architectuur-besluiten
[ ] Trade-offs gedocumenteerd en gecommuniceerd
[ ] Stakeholders geïnformeerd over waarde-keuzes

4d. Monitoring:
[ ] Ethiek-KPIs gedefinieerd
[ ] Periodieke ethiek-audit gepland
[ ] Feedback-mechanisme voor stakeholders
[ ] Escalatieprocedure voor ethische incidenten
""",
            },
            "goedkeuring": {
                "titel": "Goedkeuring",
                "content": """
Goedkeuring Ethics by Design:
- Ethiek-auditor: [naam, functie, datum]
- AI-verantwoordelijke: [naam, functie, datum]
- FG: [naam, functie, datum]
- Management: [naam, functie, datum]

Herziening: dit framework wordt jaarlijks herzien of bij wijziging van het systeem of de context.
""",
            },
        },
    }


def value_sensitive_design_protocol_template(
    org_naam: str, systeem: str, **kwargs
) -> dict:
    """Value Sensitive Design (VSD) Protocol — Friedman & Kahn methodology.

    Gebaseerd op:
    - Friedman, B. & Kahn, P.H. (2003). "Human values, ethics, and design."
    - Friedman, B. et al. (2017). "A value sensitive design approach to intelligent information systems."
    - Friedman, B. & Hendry, D. (2019). "Value Sensitive Design: Shaping Technology with Moral Imagination."

    VSD is een iteratieve methode met 3 fasen:
    1. Conceptual investigation — waarden en stakeholders
    2. Empirical investigation — context en gebruik
    3. Technological investigation — ontwerp en implementatie
    """
    return {
        "document": "Value Sensitive Design (VSD) Protocol",
        "wettelijke_basis": "Friedman & Kahn (2003) + Friedman et al. (2017) + Friedman & Hendry (2019)",
        "model_versie": "1.0 (VSD methodologie)",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "inleiding": {
                "titel": "Inleiding",
                "content": f"""
Systeem: [{systeem}]

Value Sensitive Design (VSD) is een geïtereerde, interdisciplinaire methode
voor het ontwerpen van technologie die menselijke waarden centraal stelt.

3 onderzoeksfasen (iteratief, niet-lineair):
1. Conceptual: Welke waarden zijn relevant? Wie zijn stakeholders?
2. Empirical: Hoe functioneert het systeem in de praktijk?
3. Technological: Hoe ondersteunt het ontwerp de waarden?
""",
            },
            "fase_1": {
                "titel": "Fase 1 — Conceptual Investigation",
                "instructie": "Identificeer waarden, stakeholders, en hun relaties.",
                "content": """
1a. Directe en indirecte stakeholders:
Directe stakeholders (gebruikers, ontwikkelaars):
- [stakeholder 1]: [rol]
- [stakeholder 2]: [rol]

Indirecte stakeholders (derden, maatschappij):
- [stakeholder 1]: [rol]
- [stakeholder 2]: [rol]

1b. Waarden-identificatie:
Primaire waarden:
- [waarde 1]: [definitie in context]
- [waarde 2]: [definitie in context]

Secundaire waarden:
- [waarde 3]: [definitie in context]

1c. Waarden-relaties:
[ ] Complementair (waarden versterken elkaar)
[ ] Conflicterend (waarden zijn tegengesteld)
[ ] Context-afhankelijk (relatie hangt af van situatie)

1d. Morele impact:
[ ] Wie baat bij het systeem?
[ ] Wie wordt erdoor getroffen?
[ ] Wie is uitgesloten?
[ ] Zijn er machtsverschuivingen?
""",
            },
            "fase_2": {
                "titel": "Fase 2 — Empirical Investigation",
                "instructie": "Onderzoek hoe het systeem functioneert in de praktiek.",
                "content": """
2a. Context-analyse:
- Organisatorische context: [beschrijf]
- Sociale context: [beschrijf]
- Technische context: [beschrijf]
- Wettelijke context: [beschrijf]

2b. Gebruikersonderzoek:
[ ] Interviews met [aantal] stakeholders
[ ] Enquêtes bij [aantal] gebruikers
[ ] Observatie in praktijk
[ ] Prototype-testing
[ ] Andere: [specificeer]

2c. Bevindingen:
- Waarde [naam]: [wordt ondersteund / wordt bedreigd door [factor]]
- Waarde [naam]: [wordt ondersteund / wordt bedreigd door [factor]]

2d. Tegenspraak en onverwachte effecten:
[beschrijf onverwachte bevindingen uit het empirisch onderzoek]
""",
            },
            "fase_3": {
                "titel": "Fase 3 — Technological Investigation",
                "instructie": "Ontwerp en implementeer met waarden als requirements.",
                "content": """
3a. Waarde-geïnspireerde requirements:
- Waarde [naam] → Requirement: [beschrijf]
- Waarde [naam] → Requirement: [beschrijf]

3b. Ontwerp-besluiten:
[ ] Architectuur keuze: [beschrijf] — ondersteunt waarde: [naam]
[ ] Algoritme keuze: [beschrijf] — ondersteunt waarde: [naam]
[ ] Interface keuze: [beschrijf] — ondersteunt waarde: [naam]

3c. Trade-offs:
[ ] Waarde [A] is opgeofferd ten gunste van waarde [B] — reden: [___]
[ ] Waarde [A] en [B] zijn gebalanceerd via: [mechanisme]

3d. Evaluatie:
[ ] Waarden-metrics gedefinieerd
[ ] Test-protocol voor waarden-implementatie
[ ] Stakeholder-validatie van ontwerp
[ ] Iteratie-loop terug naar Fase 1 of 2
""",
            },
            "iteratie": {
                "titel": "Iteratie en Documentatie",
                "content": """
VSD is iteratief — herhaal de fasen bij:
- Nieuwe stakeholders
- Nieuwe waarden
- Wijzigingen in context
- Onverwachte empirische bevindingen

Documentatie:
- Versie: [semver]
- Laatste iteratie: [datum]
- Bevindingen: [samenvatting]
- Volgende stappen: [acties]
""",
            },
        },
    }


def nist_ai_rmf_mapping_template(org_naam: str, ai_systeem: str, **kwargs) -> dict:
    """NIST AI RMF Mapping — AI Risk Management Framework 1.0.

    Gebaseerd op:
    - NIST AI 100-1: AI Risk Management Framework 1.0 (jan 2023)
    - NIST AI 600-1: Generative AI Profile (juli 2024)
    - NIST AI RMF Playbook

    4 kerntuncties: Govern, Map, Measure, Manage
    """
    return {
        "document": "NIST AI RMF Mapping",
        "wettelijke_basis": "NIST AI 100-1 (RMF 1.0) + NIST AI 600-1 (Generative AI Profile)",
        "model_versie": "1.0 (NIST AI RMF gebaseerd)",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "inleiding": {
                "titel": "Inleiding",
                "content": f"""
AI-systeem: [{ai_systeem}]

Het NIST AI Risk Management Framework (RMF 1.0) biedt een gestructureerde
aanpak voor AI-risicomanagement met 4 kerntuncties:

1. GOVERN — cultuur van risicomanagement
2. MAP — context en risico's identificeren
3. MEASURE — risico's analyseren en evalueren
4. MANAGE — risico's behandelen

Dit document mappt de JuraRegel templates op het NIST AI RMF.
""",
            },
            "govern": {
                "titel": "GOVERN — Risico-Cultuur",
                "instructie": "Beschrijf hoe risicomanagement is georganiseerd.",
                "content": """
G1. Organisatorisch kader:
[ ] AI-risico-beleid gedefinieerd
[ ] Verantwoordelijkheden toegewezen
[ ] Escalatieprocédures gedocumenteerd
[ ] Training en awareness aanwezig

G2. Accountability:
[ ] AI-verantwoordelijke aangesteld
[ ] FG betrokken bij AI-risico's
[ ] Management review gepland
[ ] Audit-trail aanwezig

G3. Stakeholder engagement:
[ ] Stakeholder-identificatie uitgevoerd
[ ] Communicatieprotocol gedefinieerd
[ ] Feedback-mechanismen aanwezig
[ ] Publieke transparantie waar van toepassing

G4. Compliance:
[ ] EU AI Act verplichtingen gemap
[ ] AVG verplichtingen gemap
[ ] Sector-specifieke regelgeving gemap
[ ] Certificering waar van toepassing
""",
            },
            "map": {
                "titel": "MAP — Context & Risico's",
                "instructie": "Identificeer context, stakeholders, en risico's.",
                "content": """
M1. Context-beschrijving:
- Doel van het AI-systeem: [beschrijf]
- Gecontext: [beschrijf]
- Technologie: [beschrijf]
- Stakeholders: [lijst]

M2. Risico-identificatie:
[ ] Privacy-risico's (zie DPIA)
[ ] Bias-risico's (zie Bias Audit)
[ ] Veiligheidsrisico's
[ ] Transparantie-risico's
[ ] Autonomie-risico's
[ ] Maatschappelijke risico's

M3. Risico-classificatie:
[ ] Waarschijnlijkheid × Impact matrix
[ ] Risico-niveaus gedefinieerd
[ ] Prioritering toegepast

M4. Kritiekeity-assessment:
[ ] Welke risico's zijn onacceptabel?
[ ] Welke risico's vereisen onmiddellijke actie?
[ ] Welke risico's zijn acceptabel met monitoring?
""",
            },
            "measure": {
                "titel": "MEASURE — Analyse & Evaluatie",
                "instructie": "Analyseer en evalueer de geïdentificeerde risico's.",
                "content": """
M1. Kwantitatieve metrics:
[ ] Nauwkeurigheid: [___]
[ ] Precision / Recall: [___]
[ ] F1-score: [___]
[ ] Bias-metrics: [zie Bias Audit Protocol]

M2. Kwalitatieve evaluatie:
[ ] Stakeholder-tevredenheid
[ ] Gebruikerservaring
[ ] Deskundigenbeoordeling
[ ] Ethische review

M3. Testmethoden:
[ ] A/B-testing
[ ] Adversarial testing
[ ] Stress testing
[ ] Edge-case testing
[ ] Human evaluation

M4. Documentatie:
[ ] Testresultaten gedocumenteerd
[ ] Methodologie reproduceerbaar
[ ] Bevindingen gevalideerd
[ ] Aanbevelingen geformuleerd
""",
            },
            "manage": {
                "titel": "MANAGE — Risico-Behandeling",
                "instructie": "Behandel de geïdentificeerde risico's.",
                "content": """
MA1. Behandelingsstrategie:
[ ] Mitigeren (maatregelen nemen)
[ ] Accepteren (met monitoring)
[ ] Vermijden (stoppen)
[ ] Oververzekeren (transfereren)

MA2. Maatregelen-implementatie:
[ ] Technische maatregelen: [lijst]
[ ] Organisatorische maatregelen: [lijst]
[ ] Procedurele maatregelen: [lijst]

MA3. Residual risk:
[ ] Geaccepteerd door management
[ ] Gedocumenteerd
[ ] Gecommuniceerd naar stakeholders

MA4. Monitoring:
[ ] Continue monitoring geïmplementeerd
[ ] Alert-thresholds gedefinieerd
[ ] Periodieke her-evaluatie gepland
[ ] Incident-response procedure aanwezig
""",
            },
            "nist_juraregel_mapping": {
                "titel": "NIST ↔ JuraRegel Mapping",
                "content": """
NIST Functie          → JuraRegel Template
─────────────────────────────────────────────
GOV-1 (Accountability) → Human Oversight Plan
GOV-2 (Culture)        → Ethics by Design Framework
MAP-1 (Context)        → AI Risicoclassificatie
MAP-2 (Risk ID)        → DPIA + FRIA
MEAS-1 (Metrics)       → Bias Audit Protocol
MEAS-2 (Testing)       → Kwantitatieve Risico-Methodiek
MANAGE-1 (Treatment)   → Privacy by Design Checklist
MANAGE-2 (Monitoring)  → DPIA Review Protocol
""",
            },
        },
    }


def stakeholder_consultatie_protocol_template(
    org_naam: str, verwerking: str, **kwargs
) -> dict:
    """Stakeholder Consultatie Protocol — AVG Art. 35(2).

    Gebaseerd op:
    - AVG Art. 35(2): "Where appropriate, the controller shall seek the views of data subjects"
    - EDPB WP29 Guidelines on DPIA (Section 3.4: Consultation)
    - CNIL: "Consultation des personnes concernées"
    - ISO 26000: Stakeholder engagement guidance
    """
    return {
        "document": "Stakeholder Consultatie Protocol",
        "wettelijke_basis": "AVG Art. 35(2) + EDPB WP29 Guidelines",
        "model_versie": "1.0 (EDPB WP29 gebaseerd)",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "inleiding": {
                "titel": "Inleiding",
                "content": f"""
Verwerking: [{verwerking}]

Art. 35(2) AVG: "Indien passend, de verwerkingsverantwoordelijke raadt
de betrokkenen of hun vertegenwoordigers aan over de voorgenomen verwerking."

Dit protocol definieert:
- Wanneer consultatie passend is
- Hoe consultatie wordt georganiseerd
- Hoe resultaten worden gedocumenteerd
- Hoe resultaten worden meegenomen in de DPIA
""",
            },
            "toetsing": {
                "titel": "Is Consultatie Passend?",
                "instructie": "Beoordeel of stakeholder-consultatie noodzakelijk is.",
                "content": """
De consultatie is PASSEND bij:
[ ] Hoog risico voor betrokkenen
[ ] Grootschalige verwerking
[ ] Innovatieve technologie
[ ] Kwetsbare betrokkenen
[ ] Systematische monitoring
[ ] Maatschappelijke discussie over de verwerking

De consultatie is NIET nodig bij:
[ ] Verwerking is reeds onderwerp van publieke consultatie
[ ] Consultatie is disproportioneel veel moeite
[ ] Consultatie in strijd met vertrouwelijkheid
[ ] Wettelijke uitzondering van toepassing

Conclusie:
[ ] Consultatie is PASSEND — ga naar Stap 2
[ ] Consultatie is NIET passend — documenteer waarom
""",
            },
            "stakeholders": {
                "titel": "Stakeholder-Identificatie",
                "instructie": "Wie moet worden geraadpleegd?",
                "content": """
Primaire stakeholders (direct betrokkenen):
- [groep 1]: [beschrijving, aantal]
- [groep 2]: [beschrijving, aantal]

Secundaire stakeholders (indirect betrokkenen):
- [groep 1]: [beschrijving]
- [groep 2]: [beschrijving]

Experts en belangenorganisaties:
- [organisatie 1]: [expertise]
- [organisatie 2]: [expertise]

Vertegenwoordigers:
- [organisatie]: [vertegenwoordigt welke groep]
""",
            },
            "methode": {
                "titel": "Consultatie-Methode",
                "instructie": "Kies de juiste methode voor consultatie.",
                "content": """
Methode (selecteer):
[ ] Publieke online consultatie (minimum 30 dagen)
[ ] Enquête / vragenlijst
[ ] Focusgroepen
[ ] Interviews met sleutelstakeholders
[ ] Workshop / dialoogsessie
[ ] Adviesraad / klankbordgroep
[ ] Andere: [specificeer]

Communicatie:
- Taal: [Nederlands / Engels / toegankelijk]
- Formaat: [schriftelijk / digitaal / mondeling]
- Toegankelijkheid: [WCAG 2.2 AA compliant]
- Antwoordtermijn: [minimum 30 dagen]

Documentatie:
[ ] Consultatieplan goedgekeurd door FG
[ ] Communicatie richting stakeholders voorbereid
[ ] Informatiemateriaal beschikbaar
[ ] Feedback-formulier voorbereid
""",
            },
            "vragen": {
                "titel": "Consultatie-Vragen",
                "instructie": "Definieer de vragen voor stakeholders.",
                "content": """
Kernvragen (EDPB WP29):
1. Wat vindt u van het doel van de verwerking?
2. Ziet u risico's voor uw privacy of rechten?
3. Ziet u maatregelen die genoemd zouden moeten worden?
4. Heeft u zorgen over de verwerking?
5. Heeft u suggesties voor verbetering?

Aanvullende vragen:
6. [specifieer]
7. [specificeer]
""",
            },
            "verwerking": {
                "titel": "Verwerking van Resultaten",
                "instructie": "Documenteer hoe de input is verwerkt.",
                "content": """
Samenvatting:
- Aantal respondenten: [___]
- Aantal organisaties: [___]
- Periode: [start] — [einde]

Belangrijkste bevindingen:
1. [bevinding] — frequentie: [___]
2. [bevinding] — frequentie: [___]
3. [bevinding] — frequentie: [___]

Verwerking in DPIA:
[ ] Bevindingen geïntegreerd in DPIA
[ ] Maatregelen aangepast op basis van input
[ ] Teruggave aan stakeholders over gebruikte input
[ ] Documentatie van niet-opgenomen input + reden

Teruggave:
[ ] Resultaten gepubliceerd
[ ] Stakeholders geïnformeerd over uitkomsten
[ ] DPIA aangepast en opnieuw gedeeld
""",
            },
        },
    }


def dpia_review_protocol_template(org_naam: str, verwerking: str, **kwargs) -> dict:
    """DPIA Review Protocol — Iteratief "living document" proces.

    Gebaseerd op:
    - EDPB WP29: "After a DPIA — test it, improve it, check it"
    - EDPB WP29: DPIA is not a one-off exercise
    - CNIL: DPIA must be updated throughout the lifecycle
    - ISO 27001: Management review principles
    """
    return {
        "document": "DPIA Review Protocol",
        "wettelijke_basis": "EDPB WP29 Guidelines on DPIA (Section 4) + CNIL PIA",
        "model_versie": "1.0 (EDPB/CNIL gebaseerd)",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "inleiding": {
                "titel": "Inleiding",
                "content": f"""
Verwerking: [{verwerking}]

EDPB WP29: "A DPIA is not a one-off exercise. It must be continually
reviewed and re-assessed."

Dit protocol definieerd:
- Wanneer een DPIA herzien moet worden
- Hoe herziening wordt uitgevoerd
- Hoe updates worden gedocumenteerd
""",
            },
            "triggers": {
                "titel": "Review-Triggers",
                "instructie": "Identificeer wanneer een DPIA herziening vereist is.",
                "content": """
VEREIST REVIEW bij:
[ ] Wijziging in de verwerking (doel, gegevens, technologie)
[ ] Wijziging in wetgeving of regelgeving
[ ] Datalek of incident
[ ] Nieuwe risico's geïdentificeerd
[ ] Klacht of bezwaar van betrokkene
[ ] Resultaat van audit of inspectie
[ ] Feedback van FG of AP
[ ] Wijziging in organisatie (fusie, herstructururing)
[ ] Externe factoren (technologische ontwikkelingen)

PERIODIEKE REVIEW:
[ ] Jaarlijkse review (minimaal)
[ ] Tussentijdse review (elke [___] maanden)
[ ] Post-implementatie review (na [___] maanden)
""",
            },
            "review_proces": {
                "titel": "Review-Proces",
                "instructie": "Voer de herziening uit volgens een gestructureerd proces.",
                "content": """
Stap 1: Identificeer de trigger
- Trigger: [beschrijf]
- Datum: [datum]
- Gemeld door: [naam]

Stap 2: Beoordeel impact
- Welke secties van de DPIA zijn aangedaan?
- Is een volledige hernieuwing nodig of een partiële update?
- Prioriteit: [Hoog / Middel / Laag]

Stap 3: Voer herziening uit
- Sectie [___]: [wijziging]
- Sectie [___]: [wijziging]
- Nieuwe risico's: [beschrijf]
- Nieuwe maatregelen: [beschrijf]

Stap 4: Valideer
- Zijn alle wijzigingen consistent?
- Zijn nieuwe risico's voldoende gemitigeerd?
- Is het residuaal risico acceptabel?

Stap 5: Goedkeuring
- FG: [naam, oordeel, datum]
- Projectleider: [naam, oordeel, datum]
- Management: [naam, oordeel, datum]

Stap 6: Communiceer
- Stakeholders geïnformeerd: [Ja/Nee]
- Documentatie bijgewerkt: [Ja/Nee]
- Versie-nummer verhoogd: [___]
""",
            },
            "documentatie": {
                "titel": "Documentatie en Versiebeheer",
                "content": """
Versiebeheer:
- Huidige versie: [semver]
- Laatste herziening: [datum]
- Volgende geplande review: [datum]
- Eigenaar: [naam]

Changelog:
| Versie | Datum | Wijziging | Uitgevoerd door |
|--------|-------|-----------|----------------|
| 1.0    | [datum] | Eerste versie | [naam] |
| [x.x]  | [datum] | [beschrijving] | [naam] |

Bewaartermijn:
- DPIA + review-historie: 5 jaar na beëindiging verwerking
- Conform AVG Art. 5(1)(e) en Archiefwet
""",
            },
            "checklist": {
                "titel": "Review-Checklist",
                "content": """
[ ] Zijn er wijzigingen in de verwerking sinds laatste review?
[ ] Zijn er wijzigingen in wetgeving of regelgeving?
[ ] Zijn er incidenten geweest?
[ ] Zijn er nieuwe risico's geïdentificeerd?
[ ] Zijn de maatregelen effectief gebleken?
[ ] Is het residuaal risico nog acceptabel?
[ ] Zijn stakeholders geraadpleegd bij significante wijzigingen?
[ ] Is de DPIA consistent met andere assessments (FRIA, IAMA)?
[ ] Is de versie bijgewerkt en gecommuniceerd?
""",
            },
        },
    }
