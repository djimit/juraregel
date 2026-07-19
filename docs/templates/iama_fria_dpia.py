"""Gedetailleerde templates voor DPIA, IAMA en FRIA.

Dit zijn de meest gevraagde verplichte assessments voor overheden:

- DPIA (Data Protection Impact Assessment) — AVG Art. 35
  Verplicht bij hoog risico voor privacy van betrokkenen
  Bron: Model DPIA Rijksdienst v3.0 (KCBR/CIP)

- IAMA (Impact Assessment Mensenrechten en Algoritmes) — Nationaal kader
  Verplicht gesteld door Tweede Kamer voor AI inzet door overheid
  Bron: Rijksoverheid.nl / Universiteit Utrecht (v2026)

- FRIA (Fundamental Rights Impact Assessment) — EU AI Act Art. 27
  Verplicht voor hoog-risico AI-systemen (publieke dienstverleners)
  Bron: EU AI Act + ICTRecht template
"""

from datetime import date


def dpia_rijksdienst_template(org_naam: str, verwerking: str, **kwargs) -> dict:
    """DPIA volgens Model DPIA Rijksdienst v3.0.

    Gebaseerd op het officiële model van KCBR/CIP-Overheid.
    Verplicht bij verwerking die waarschijnlijk hoog risico oplevert.

    Structuur (3 delen):
    - Deel A: Algemene inleiding en voorbereiding
    - Deel B: Toetsing op 9 criteria (de DPIA-toets)
    - Deel C: Uitwerking en maatregelen
    """
    return {
        "document": "DPIA — Model Rijksdienst v3.0",
        "wettelijke_basis": "AVG Art. 35 + Art. 36",
        "model_versie": "3.0 (september 2023)",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "deel_a": {
                "titel": "Deel A — Algemene inleiding",
                "secties": {
                    "a1": {
                        "titel": "A1. Projectbeschrijving",
                        "content": f"""
Projectnaam: [{verwerking}]
Projectleider: [naam, functie]
Functionaris Gegevensbescherming (FG): [naam, contact]
Datum: {date.today().isoformat()}

Beschrijving van het project:
[beschrijf het project, de context en de aanleiding]

Doel van de verwerking:
[beschrijf specifiek wat het doel is]

Rechtsgrond:
[ ] Toestemming (Art. 6(1)(a))
[ ] Contract (Art. 6(1)(b))
[ ] Wettelijke verplichting (Art. 6(1)(c))
[ ] Openbaar belang (Art. 6(1)(e))
[ ] Gerechtvaardigd belang (Art. 6(1)(f))
""",
                    },
                    "a2": {
                        "titel": "A2. Betrokkenen en gegevens",
                        "content": """
Categorieën betrokkenen:
[ ] Medewerkers
[ ] Burgers
[ ] Kinderen (< 16 jaar)
[ ] Kwetsbare personen
[ ] Andere: [specificeer]

Categorieën persoonsgegevens:
[ ] Naam, adres, contact
[ ] Identificatie (BSN, paspoort)
[ ] Financiële gegevens
[ ] Gezondheidsgegevens (bijzondere categorie Art. 9)
[ ] Biometrische gegevens
[ ] Strafrechtelijke gegevens
[ ] Locatie/gedragsdata
[ ] Profielen/score

Worden bijzondere categorieën verwerkt (Art. 9)?
[ ] Ja — motiveer waarom toegestaan (Art. 9(2))
[ ] Nee

Worden gegevens doorggeven aan derde landen?
[ ] Nee
[ ] Ja — met [adequaat besluit / SCC / BCR]
""",
                    },
                    "a3": {
                        "titel": "A3. Noodzaak en proportionaliteit",
                        "content": """
Is de verwerking noodzakelijk voor het doel?
[ ] Ja — motiveer
[ ] Nee — stop

Kunnen minder gegevens volstaan?
[ ] Ja — pas aan
[ ] Nee — motiveer

Is de bewaartermijn proportioneel?
[ ] Ja — [termijn]
[ ] Nee — verkort

Is er een minder ingrijpend alternatief?
[ ] Nee
[ ] Ja — [beschrijf waarom niet gekozen]
""",
                    },
                },
            },
            "deel_b": {
                "titel": "Deel B — DPIA-toets (9 criteria)",
                "instructie": "Toets voor elk criterium of het risico hoog is. Bij ≥1 criterium = DPIA verplicht.",
                "criteria": {
                    "c1": {
                        "criterium": "1. Evaluatie of profiling",
                        "toets": "[ ] Systematische evaluatie/profiling van personen? [Ja/Nee]",
                    },
                    "c2": {
                        "criterium": "2. Geautomatiseerde besluiten",
                        "toets": "[ ] Geautomatiseerde besluiten met juridische/financiële gevolgen? [Ja/Nee]",
                    },
                    "c3": {
                        "criterium": "3. Systematische monitoring",
                        "toets": "[ ] Systematische monitoring van gedrag? [Ja/Nee]",
                    },
                    "c4": {
                        "criterium": "4. Gevoelige gegevens op grote schaal",
                        "toets": "[ ] Bijzondere categorieën (Art. 9) op grote schaal? [Ja/Nee]",
                    },
                    "c5": {
                        "criterium": "5. Gegevensverwerking op grote schaal",
                        "toets": "[ ] Verwerking op grote schaal (>5000 personen)? [Ja/Nee]",
                    },
                    "c6": {
                        "criterium": "6. Koppeling van datasets",
                        "toets": "[ ] Koppeling/combining van verschillende datasets? [Ja/Nee]",
                    },
                    "c7": {
                        "criterium": "7. Kwetsbare betrokkenen",
                        "toets": "[ ] Betrokkenen: kinderen, medewerkers, kwetsbaren? [Ja/Nee]",
                    },
                    "c8": {
                        "criterium": "8. Innovatief gebruik",
                        "toets": "[ ] Innovatieve technologie (AI, biometrie, etc.)? [Ja/Nee]",
                    },
                    "c9": {
                        "criterium": "9. Uitsluiting van rechtsbescherming",
                        "toets": "[ ] Betrokkenen worden uitgesloten van dienst/recht? [Ja/Nee]",
                    },
                },
                "conclusie": "[ ] DPIA verplicht (≥1 criterium positief)\n[ ] DPIA niet verplicht (alle criteria negatief) — documenteer waarom",
            },
            "deel_c": {
                "titel": "Deel C — Uitwerking en maatregelen",
                "secties": {
                    "c1": {
                        "titel": "C1. Risico-analyse",
                        "content": """
Risico 1: [beschrijving]
- Waarschijnlijkheid: [1-5]
- Impact: [1-5]
- Score: [1-25]
- Maatregel: [beschrijf]

Risico 2: [beschrijving]
- Waarschijnlijkheid: [1-5]
- Impact: [1-5]
- Score: [1-25]
- Maatregel: [beschrijf]

Risico 3: [beschrijving]
- Waarschijnlijkheid: [1-5]
- Impact: [1-5]
- Score: [1-25]
- Maatregel: [beschrijf]
""",
                    },
                    "c2": {
                        "titel": "C2. Maatregelen",
                        "content": """
Technische maatregelen:
[ ] Encryptie (at rest + in transit)
[ ] Pseudonimisering / anonimisering
[ ] Toegangscontrole (RBAC, MFA)
[ ] Logging en monitoring
[ ] Back-up en herstel
[ ] Privacy by design toegepast

Organisatorische maatregelen:
[ ] Training medewerkers
[ ] Vertrouwelijkheidsverklaringen
[ ] Procedure uitoefening rechten
[ ] Datalek meldprocedure
[ ] Periodieke audits
[ ] Verwerkersovereenkomsten
""",
                    },
                    "c3": {
                        "titel": "C3. Residuaal risico",
                        "content": """
Na uitvoering van maatregelen:
- Residuaal risico: [Laag/Middel/Hoog]
- Acceptabel? [Ja/Nee]
- Indien niet acceptabel: [verdere maatregelen of stop verwerking]

Voorafgaand overleg met AP verplicht?
[ ] Ja — risico blijft hoog ondanks maatregelen
[ ] Nee — risico voldoende gemitigeerd
""",
                    },
                    "c4": {
                        "titel": "C4. Goedkeuring",
                        "content": f"""
FG (Functionaris Gegevensbescherming):
Naam: [naam]
Oordeel: [Positief / Negatief / Met voorwaarden]
Datum: [datum]
Handtekening: [tekening]

Projectleider:
Naam: [naam]
Datum: [datum]
Handtekening: [tekening]

Herziening: deze DPIA wordt jaarlijks herzien of bij wezenlijke wijziging.
""",
                    },
                },
            },
        },
    }


def iama_template(org_naam: str, algoritme: str, **kwargs) -> dict:
    """IAMA — Impact Assessment Mensenrechten en Algoritmes.

    Nationaal kader voor overheden die AI/algoritmes inzetten.
    Ontwikkeld door RijksUniversiteit Utrecht, geactualiseerd februari 2026.
    Gesteld verplicht door Tweede Kamer voor AI-inzet door overheid.

    Structuur (5 fasen):
    1. Oriëntatie
    2. Mensenrechtenanalyse
    3. Proportionaliteit
    4. Maatregelen
    5. Besluit en monitoring
    """
    return {
        "document": "IAMA — Impact Assessment Mensenrechten en Algoritmes",
        "wettelijke_basis": "Tweede Kamer motie (verplicht voor overheids-AI) + EU AI Act Art. 27",
        "model_versie": "2.0 (februari 2026)",
        "ontwikkelaar": "RijksUniversiteit Utrecht / Ministerie van BZK",
        "organisatie": org_naam,
        "algoritme": algoritme,
        "datum": date.today().isoformat(),
        "inhoud": {
            "fase_1": {
                "titel": "Fase 1 — Oriëntatie",
                "secties": {
                    "1.1": {
                        "titel": "1.1 Beschrijving algoritme",
                        "content": f"""
Naam: [{algoritme}]
Type: [ ] Machine learning / [ ] LLM / [ ] Regelgebaseerd / [ ] Statistisch
Doel: [beschrijf het primaire doel]
Gebruik: [beschrijf hoe het wordt ingezet]
Ontwikkelaar: [intern / extern: naam]
Versie: [versie]
""",
                    },
                    "1.2": {
                        "titel": "1.2 Stakeholderanalyse",
                        "content": """
Wie is betrokken bij de ontwikkeling?
[lijst: ontwikkelaars, beheerders, eindgebruikers]

Wie wordt erdoor beïnvloed?
[lijst: burgers, medewerkers, kwetsbare groepen]

Wie heeft inspraak gehad?
[ ] Geïnterviewde stakeholders
[ ] Publieke consultatie
[ ] Geen — motiveer waarom niet
""",
                    },
                    "1.3": {
                        "titel": "1.3 Mensenrechtenkader",
                        "content": """
Relevante mensenrechten (Handvest EU):
[ ] Recht op menselige waardigheid (Art. 1)
[ ] Vrijheid van meningsuiting (Art. 11)
[ ] Recht op privacy (Art. 7)
[ ] Bescherming persoonsgegevens (Art. 8)
[ ] Non-discriminatie (Art. 21)
[ ] Recht op effectieve voorziening (Art. 47)
[ ] Rechten van het kind (Art. 24)
[ ] Integratie personen met handicap (Art. 26)
""",
                    },
                },
            },
            "fase_2": {
                "titel": "Fase 2 — Mensenrechtenanalyse",
                "secties": {
                    "2.1": {
                        "titel": "2.1 Impact per recht",
                        "content": """
Recht op privacy (Art. 7-8):
- Impact: [Geen / Laag / Middel / Hoog]
- Toelichting: [beschrijf]
- Genoegzaam? [Ja/Nee]

Non-discriminatie (Art. 21):
- Impact: [Geen / Laag / Middel / Hoog]
- Toelichting: [beschrijf bias-risico's]
- Genoegzaam? [Ja/Nee]

Recht op effectieve voorziening (Art. 47):
- Impact: [Geen / Laag / Middel / Hoog]
- Toelichting: [beschrijf toetsbaarheid]
- Genoegzaam? [Ja/Nee]
""",
                    },
                    "2.2": {
                        "titel": "2.2 Kwetsbare groepen",
                        "content": """
Specifieke impact op:
[ ] Kinderen
[ ] Ouderen
[ ] Personen met handicap
[ ] Minderheden
[ ] Werkzoekenden
[ ] Burgers met beperkte digitale vaardigheden

Maatregelen voor bescherming:
[beschrijf]
""",
                    },
                    "2.3": {
                        "titel": "2.3 Bias en discriminatie",
                        "content": """
Is er risico op bias?
[ ] Ja — [beschrijf type bias]
[ ] Nee

Bias-test uitgevoerd?
[ ] Ja — [datum, resultaat]
[ ] Nee — [plan]

Maatregelen tegen bias:
[ ] Diverse trainingsdata
[ ] Bias-audits
[ ] Menselijke review
[ ] Andere: [beschrijf]
""",
                    },
                },
            },
            "fase_3": {
                "titel": "Fase 3 — Proportionaliteit",
                "secties": {
                    "3.1": {
                        "titel": "3.1 Noodzaak",
                        "content": """
Is het algoritme noodzakelijk voor het doel?
[ ] Ja — motiveer
[ ] Nee — stop

Is er een minder ingrijpend alternatief?
[ ] Nee
[ ] Ja — [beschrijf waarom niet gekozen]
""",
                    },
                    "3.2": {
                        "titel": "3.2 Evenredigheid",
                        "content": """
Weegt het voordeel op tegen de inbreuk op rechten?
[ ] Ja — [motiveer]
[ ] Nee — [pas aan of stop]

Is de inbreuk minimaal?
[ ] Ja
[ ] Nee — [reduceer impact]
""",
                    },
                },
            },
            "fase_4": {
                "titel": "Fase 4 — Maatregelen",
                "secties": {
                    "4.1": {
                        "titel": "4.1 Technische maatregelen",
                        "content": """
[ ] Uitlegbaarheid (explainability)
[ ] Menselijke tussenkomst (human-in-the-loop)
[ ] Stopknop / kill switch
[ ] Logging van besluiten
[ ] Encryptie van trainingsdata
[ ] Toegangscontrole
""",
                    },
                    "4.2": {
                        "titel": "4.2 Organisatorische maatregelen",
                        "content": """
[ ] Training gebruikers
[ ] Duidelijke communicatie naar burgers
[ ] Procedure voor bezwaar en herziening
[ ] Periodieke her-evaluatie
[ ] Toezicht door onafhankelijke commissie
""",
                    },
                },
            },
            "fase_5": {
                "titel": "Fase 5 — Besluit en monitoring",
                "secties": {
                    "5.1": {
                        "titel": "5.1 Besluit",
                        "content": """
Conclusie:
[ ] Algoritme kan worden ingezet
[ ] Algoritme kan worden ingezet met voorwaarden: [beschrijf]
[ ] Algoritme kan NIET worden ingezet

Goedkeuring:
Naam: [naam]
Functie: [functie]
Datum: [datum]
Handtekening: [tekening]
""",
                    },
                    "5.2": {
                        "titel": "5.2 Monitoring",
                        "content": """
Her-evaluatie frequentie: [elke 6 maanden / jaarlijks / bij wijziging]
Monitoring-indicatoren:
- [indicatoren voor bias, nauwkeurigheid, gebruik]

Publieke informatie:
[ ] Gepubliceerd in algoritmeregister
[ ] Beschikbaar op website
[ ] Op verzoek verkrijgbaar
""",
                    },
                },
            },
        },
    }


def fria_eu_template(org_naam: str, ai_systeem: str, **kwargs) -> dict:
    """FRIA — Fundamental Rights Impact Assessment (EU AI Act Art. 27).

    Verplicht voor:
    - Publieke dienstverleners die hoog-risico AI inzetten
    - Private deployers van hoog-risico AI voor publieke doeleinden

    Gebaseerd op EU AI Act Art. 27 + ICTRecht template v1.0.
    """
    return {
        "document": "FRIA — Fundamental Rights Impact Assessment",
        "wettelijke_basis": "EU AI Act Art. 27",
        "model_versie": "1.0 (EU AI Act gebaseerd)",
        "organisatie": org_naam,
        "ai_systeem": ai_systeem,
        "datum": date.today().isoformat(),
        "inhoud": {
            "sectie_1": {
                "titel": "1. Algemene informatie",
                "content": f"""
Organisatie: [{org_naam}]
AI-systeem: [{ai_systeem}]
Risicoclassificatie: [Hoog-risico (Art. 6) / Beperkt risico / Minimaal risico]
Rol: [ ] Aanbieder / [ ] Gebruiker (deployer) / [ ] Distributeur
Datum: {date.today().isoformat()}
Versie: [versie]
""",
            },
            "sectie_2": {
                "titel": "2. Beschrijving van het AI-systeem",
                "content": """
Doel en functie:
[beschrijf wat het systeem doet en waarom]

Technische specificaties:
- Type AI: [machine learning, LLM, regelgebaseerd, etc.]
- Trainingsdata: [beschrijf bron, omvang, kwaliteit]
- Output: [beschrijf wat het systeem produceert]

Gebruik en context:
- Gebruikers: [wie gebruikt het systeem?]
- Betrokkenen: [wie wordt erdoor beïnvloed?]
- Besluitvorming: [besluitvormingsondersteuning / geautomatiseerd besluit]
""",
            },
            "sectie_3": {
                "titel": "3. Grondrechtenimpactanalyse",
                "instructie": "Beoordeel de impact op elk grondrecht. Gebruik schaal: Geen / Laag / Middel / Hoog.",
                "rechten": [
                    {
                        "recht": "Menselige waardigheid (Handvest Art. 1)",
                        "impact": "[schaal]",
                        "toelichting": "[beschrijf]",
                    },
                    {
                        "recht": "Vrijheid en veiligheid (Art. 6-7)",
                        "impact": "[schaal]",
                        "toelichting": "[beschrijf]",
                    },
                    {
                        "recht": "Privacy (Art. 7)",
                        "impact": "[schaal]",
                        "toelichting": "[beschrijf]",
                    },
                    {
                        "recht": "Bescherming persoonsgegevens (Art. 8)",
                        "impact": "[schaal]",
                        "toelichting": "[beschrijf]",
                    },
                    {
                        "recht": "Vrijheid van meningsuiting (Art. 11)",
                        "impact": "[schaal]",
                        "toelichting": "[beschrijf]",
                    },
                    {
                        "recht": "Non-discriminatie (Art. 21)",
                        "impact": "[schaal]",
                        "toelichting": "[beschrijf]",
                    },
                    {
                        "recht": "Gelijkheid vrouwen en mannen (Art. 23)",
                        "impact": "[schaal]",
                        "toelichting": "[beschrijf]",
                    },
                    {
                        "recht": "Rechten van het kind (Art. 24)",
                        "impact": "[schaal]",
                        "toelichting": "[beschrijf]",
                    },
                    {
                        "recht": "Integratie personen met handicap (Art. 26)",
                        "impact": "[schaal]",
                        "toelichting": "[beschrijf]",
                    },
                    {
                        "recht": "Toegang tot het recht (Art. 47)",
                        "impact": "[schaal]",
                        "toelichting": "[beschrijf]",
                    },
                ],
            },
            "sectie_4": {
                "titel": "4. Kwetsbare groepen",
                "content": """
Specifieke impact op kwetsbare groepen:

Kinderen (< 16 jaar):
- Betrokken? [Ja/Nee]
- Specifieke risico's: [beschrijf]
- Maatregelen: [beschrijf]

Personen met een handicap:
- Betrokken? [Ja/Nee]
- Specifieke risico's: [beschrijf]
- Maatregelen: [beschrijf]

Andere kwetsbare groepen:
- [beschrijf]
""",
            },
            "sectie_5": {
                "titel": "5. Menselijke tussenkomst",
                "content": """
Is menselijke tussenkomst verplicht? [Ja/Nee]
Hoe is menselijke tussenkomst geïmplementeerd?
[ ] Review van AI-output door mens
[ ] Mogelijkheid tot overruling
[ ] Stopknop / kill switch
[ ] Andere: [beschrijf]

Is de menselijke tussenkomst effectief?
[ ] Ja — [motiveer]
[ ] Nee — [verbeter]
""",
            },
            "sectie_6": {
                "titel": "6. Mitigerende maatregelen",
                "content": """
Technische maatregelen:
[ ] Uitlegbaarheid (XAI)
[ ] Bias-mitigatie
[ ] Encryptie
[ ] Toegangscontrole
[ ] Logging

Organisatorische maatregelen:
[ ] Training
[ ] Communicatie
[ ] Bezwaarprocedure
[ ] Periodieke her-evaluatie
""",
            },
            "sectie_7": {
                "titel": "7. Conclusie en goedkeuring",
                "content": """
Conclusie:
[ ] AI-systeem voldoet aan grondrechtenvereisten
[ ] AI-systeem voldoet met voorwaarden: [beschrijf]
[ ] AI-systeem voldoet NIET — stop inzet

Goedkeuring:
Naam: [naam]
Functie: [functie]
Datum: [datum]
Handtekening: [tekening]

Herziening: deze FRIA wordt [jaarlijks / bij wijziging] herzien.
""",
            },
        },
    }
