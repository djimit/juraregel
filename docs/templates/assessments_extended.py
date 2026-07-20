"""Uitgebreide assessment templates — Fase 1: Wettelijk kritiek.

Templates gebaseerd op:
- Handreiking Pre-scan DPIA v2.0 (KCBR/JenV, aug 2024)
- EDPB Guidelines on DPIA (WP29, 2017) + EDPB DPIA Template (2026)
- EDPB Recommendations 01/2020 on transfers (Schrems II)
- EU AI Act Art. 6 + Bijlage III (risicoclassificatie)
- EDPB Guidelines Art. 25 (Privacy by Design and by Default)
"""

from datetime import date
from typing import Any


def dpia_pre_scan_template(org_naam: str, verwerking: str, **kwargs) -> dict:
    """Pre-scan DPIA — Threshold assessment vóór volledige DPIA.

    Gebaseerd op Handreiking Pre-scan DPIA v2.0 (aug 2024).
    Bepaalt of een volledige DPIA verplicht is op basis van:
    - AP-lijst met verplichte DPIA-verwerkingen
    - 9 EDPB-criteria (≥2 = DPIA verplicht)
    - Proportionaliteitstoets

    Output: GO / NO-GO voor volledige DPIA + onderbouwing.
    """
    return {
        "document": "Pre-scan DPIA — Threshold Assessment",
        "wettelijke_basis": "AVG Art. 35(1) + Handreiking Pre-scan DPIA v2.0",
        "model_versie": "2.0 (augustus 2024)",
        "bron": "KCBR / Ministerie van JenV",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "stap_1": {
                "titel": "Stap 1 — AP Lijstcheck",
                "instructie": "Raadpleeg de AP-lijst met verplichte DPIA-verwerkingen. Indien de verwerking hierop staat, is een DPIA verplicht.",
                "content": f"""
Verwerking: [{verwerking}]
Raadpleeg: https://www.autoriteitpersoonsgegevens.nl/nl/onderwerpen/avg-privacyrecht/uitvoeren-dpia

Staat deze verwerking op de AP-lijst "DPIA verplicht"?
[ ] Ja — DPIA is verplicht, ga naar Stap 3
[ ] Nee — ga naar Stap 2
[ ] Onbekend — raadpleeg AP-lijst of FG

Toelichting: [beschrijf]
""",
            },
            "stap_2": {
                "titel": "Stap 2 — 9 EDPB-Criteria",
                "instructie": "Toets elk criterium. Bij ≥2 positieve criteria is een DPIA verplicht (EDPB WP29).",
                "criteria": {
                    "c1": {
                        "criterium": "1. Evaluatie of scoring (incl. profiling)",
                        "vraag": "Worden persoonsgegevens gebruikt voor evaluatie, scoring of profiling van personen?",
                        "toets": "[ ] Ja — [beschrijf type evaluatie]\n[ ] Nee",
                    },
                    "c2": {
                        "criterium": "2. Geautomatiseerde besluiten met juridige/financiële gevolgen",
                        "vraag": "Worden besluiten genomen op basis van geautomatiseerde verwerking die juridische of significante gevolgen hebben?",
                        "toets": "[ ] Ja — [beschrijf besluitvorming]\n[ ] Nee",
                    },
                    "c3": {
                        "criterium": "3. Systematische monitoring van gedrag",
                        "vraag": "Wordt het gedrag van personen systematisch gemonitord?",
                        "toets": "[ ] Ja — [beschrijf monitoring]\n[ ] Nee",
                    },
                    "c4": {
                        "criterium": "4. Gevoelige gegevens op grote schaal (Art. 9)",
                        "vraag": "Worden bijzondere categorieën persoonsgegevens verwerkt op grote schaal?",
                        "toets": "[ ] Ja — [specificeer categorieën]\n[ ] Nee",
                    },
                    "c5": {
                        "criterium": "5. Verwerking op grote schaal",
                        "vraag": "Worden persoonsgegevens verwerkt van meer dan 5000 betrokkenen?",
                        "toets": "[ ] Ja — [geschat aantal: ___]\n[ ] Nee",
                    },
                    "c6": {
                        "criterium": "6. Koppeling van datasets",
                        "vraag": "Worden twee of meer datasets gekoppeld die voor verschillende doeleinden zijn verzameld?",
                        "toets": "[ ] Ja — [beschrijf koppeling]\n[ ] Nee",
                    },
                    "c7": {
                        "criterium": "7. Kwetsbare betrokkenen",
                        "vraag": "Worden gegevens verwerkt van kinderen, medewerkers, patiënten of andere kwetsbare groepen?",
                        "toets": "[ ] Ja — [specificeer groep]\n[ ] Nee",
                    },
                    "c8": {
                        "criterium": "8. Innovatief gebruik van technologie",
                        "vraag": "Wordt innovatieve technologie ingezet (AI, biometrie, IoT) waarvan de gevolgen nog niet volledig inzichtelijk zijn?",
                        "toets": "[ ] Ja — [beschrijf technologie]\n[ ] Nee",
                    },
                    "c9": {
                        "criterium": "9. Uitsluiting van dienst of recht",
                        "vraag": "Kan de verwerking ertoe leiden dat personen worden uitgesloten van een dienst, contract of recht?",
                        "toets": "[ ] Ja — [beschrijf consequenties]\n[ ] Nee",
                    },
                },
                "scoring": """
Totaal positieve criteria: [0-9]

[ ] 0-1 criteria → DPIA niet verplicht (documenteer deze pre-scan)
[ ] ≥2 criteria → DPIA verplicht (ga naar Stap 3)
""",
            },
            "stap_3": {
                "titel": "Stap 3 — Conclusie en vervolg",
                "content": """
Conclusie:
[ ] GO — Volledige DPIA is verplicht
[ ] NO-GO — Volledige DPIA is niet verplicht (documenteer reden)
[ ] GO met voorwaarden — DPIA verplicht, maar beperkte scope: [beschrijf]

Reden (indien NO-GO):
[ ] Geen criteria positief
[ ] Verwerking vergelijkbaar met eerdere DPIA (ref: [link])
[ ] Verwerking op AP-lijst "niet verplicht"
[ ] Andere: [beschrijf]

Vervolgactie:
[ ] Start volledige DPIA (Model DPIA Rijksdienst v3.0)
[ ] Documenteer deze pre-scan als onderbouwing
[ ] Raadpleeg FG voor tweede oordeel

FG-beoordeling:
Naam: [naam]
Oordeel: [Akkoord / Niet akkoord — motiveer]
Datum: [datum]
""",
            },
        },
    }


def legitimate_interest_assessment_template(
    org_naam: str, verwerking: str, belang: str, **kwargs
) -> dict:
    """Legitimate Interest Assessment (LIA) — 3-staps proportionaliteitstoets.

    Verplicht bij verwerking gebaseerd op "gerechtvaardigd belang" (Art. 6(1)(f) AVG).
    Gebaseerd op:
    - EDPB Guidelines 8/2022 on identifying legitimate interest
    - ICO LIA template (UK)
    - CNIL LIA methodology

    De 3-staps test:
    1. Purpose test — Is het doel legitiem?
    2. Necessity test — Is de verwerking noodzakelijk?
    3. Balancing test — Weegt het belang zwaarder dan de rechten van betrokkenen?
    """
    return {
        "document": "Legitimate Interest Assessment (LIA)",
        "wettelijke_basis": "AVG Art. 6(1)(f) + EDPB Guidelines 8/2022",
        "model_versie": "1.0 (EDPB gebaseerd)",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "inleiding": {
                "titel": "Inleiding",
                "content": f"""
Verwerking: [{verwerking}]
Belegde rechtsgrond: Gerechtvaardigd belang (Art. 6(1)(f) AVG)
Omschrijving van het belang: [{belang}]

Doel van deze LIA:
Bewijzen dat het gerechtvaardigd belang zwaarder weegt dan de rechten en vrijheden van betrokkenen.
""",
            },
            "stap_1": {
                "titel": "Stap 1 — Purpose Test",
                "instructie": "Is het doel legitiem, wettig en ethisch verantwoord?",
                "content": """
1a. Wat is het precieze doel?
[beschrijf het doel in specifieke, meetbare termen]

1b. Is het doel legitiem?
[ ] Ja — het doel is wettig en duidelijk gedefinieerd
[ ] Nee — pas het doel aan of kies een andere rechtsgrond

1c. Wie heeft er baat bij dit doel?
[ ] De organisatie zelf
[ ] Derden (specificeer: [naam])
[ ] De maatschappij (publieke taak)
[ ] De betrokkenen zelf

1d. Is het doel ethisch verantwoord?
[ ] Ja — het doel is transparant en aanvaardbaar
[ ] Nee — heroverweeg het doel

1e. Zijn er negatieve effecten op betrokkenen te verwachten?
[ ] Nee
[ ] Ja — [beschrijf: emotionele stress, discriminatie, uitsluiting, etc.]

Conclusie Purpose Test:
[ ] Geslaagd — ga naar Stap 2
[ ] Niet geslaagd — stop, kies andere rechtsgrond
""",
            },
            "stap_2": {
                "titel": "Stap 2 — Necessity Test",
                "instructie": "Is de verwerking noodzakelijk voor het gestelde doel?",
                "content": """
2a. Is de verwerking daadwerkelijk noodzakelijk?
[ ] Ja — er is geen minder ingrijpend alternatief
[ ] Nee — er is een alternatief: [beschrijf]

2b. Kunnen hetzelfde doel bereikt worden met minder gegevens?
[ ] Nee
[ ] Ja — [pas de gegevensverwerking aan]

2c. Kunnen de gegevens gepseudonimiseerd of geanonimiseerd worden?
[ ] Nee — noodzakelijk om identificeerbaar te blijven
[ ] Ja — [pas aan: pseudonimiseer waar mogelijk]

2d. Is de bewaartermijn minimaal?
[ ] Ja — [termijn: ___]
[ ] Nee — verkort

2e. Is de ververking evenredig met het doel?
[ ] Ja
[ ] Nee — [pas aan]

Conclusie Necessity Test:
[ ] Geslaagd — ga naar Stap 3
[ ] Niet geslaagd — pas de verwerking aan en herhaal Stap 2
""",
            },
            "stap_3": {
                "titel": "Stap 3 — Balancing Test",
                "instructie": "Weegt het belang van de organisatie zwaarder dan de rechten van betrokkenen?",
                "content": """
3a. Aard en impact van de verwerking op betrokkenen:
- Type gegevens: [gewoon / gevoelig / bijzonder (Art. 9)]
- Omvant van verwerking: [aantal betrokkenen]
- Frequentie: [eenmalig / periodiek / continu]
- Mogelijke gevolgen voor betrokkenen: [beschrijf]

3b. Redelijke verwachtingen van betrokkenen:
- Konden betrokkenen deze verwerking verwachten? [Ja/Nee]
- Is de verwerking transparant gecommuniceerd? [Ja/Nee]
- Is er een bestaande relatie met de betrokkenen? [Ja/Nee — specificeer]

3c. Beschermende maatregelen:
[ ] Opt-in / toestemming geïnformeerd
[ ] Makkelijke intrekking mogelijk
[ ] Data minimalisatie toegepast
[ ] Pseudonimisering / anonimisering
[ ] Encryptie en toegangscontrole
[ ] Transparante privacyverklaring
[ ] Recht op bezwaar geïmplementeerd
[ ] Periodieke her-evaluatie

3d. Afweging:
Het belang van de organisatie: [beschrijf — bijv. fraudebestrijding, efficiëntie]
De impact op betrokkenen: [beschrijf — bijv. inbreuk privacy, risico discriminatie]

Weegt het belang zwaarder?
[ ] Ja — gerechtvaardigd belang is aangetoond
[ ] Nee — stop de verwerking of kies een andere rechtsgrond
[ ] Onzeker — raadpleeg de FG of AP

Conclusie Balancing Test:
[ ] Geslaagd — gerechtvaardigd belang is gerechtvaardigd
[ ] Niet geslaagd — kies een andere rechtsgrond

3e. Compenserende maatregelen (indien twijfel):
[beschrijf extra maatregelen om de balance te verbeteren]
""",
            },
            "eindoordeel": {
                "titel": "Eindoordeel LIA",
                "content": """
[ ] Gerechtvaardigd belang is AANGETOOND — verwerking kan doorgaan
[ ] Gerechtvaardigd belang is NIET aangetoond — kies andere rechtsgrond
[ ] Voorwaardelijk — alleen met extra maatregelen: [beschrijf]

Toetsing door FG:
Naam: [naam]
Oordeel: [Positief / Negatief / Met voorwaarden]
Datum: [datum]
Opmerkingen: [beschrijf]

Herziening: deze LIA wordt jaarlijks herzien of bij weziging van de verwerking.
""",
            },
        },
    }


def transfer_impact_assessment_template(
    org_naam: str,
    verwerking: str,
    ontvanger_land: str,
    ontvanger_naam: str,
    **kwargs,
) -> dict:
    """Transfer Impact Assessment (TIA) — Schrems II compliance.

    Verplicht bij doorgiften van persoonsgegevens naar landen buiten de EER.
    Gebaseerd op:
    - EDPB Recommendations 01/2020 on measures that supplement transfer tools (Schrems II)
    - EDPB Recommendations 02/2020 on European Essential Guarantees
    - Standard Contractual Clauses (SCC) 2021/914

    Structuur:
    1. Beschrijving van de doorgifte
    2. Identificatie van het transfer mechanisme
    3. Beoordeling van het derde land (rule of law, toezicht, rechten)
    4. Identificatie van risico's
    5. Supplementerende maatregelen
    6. Conclusie
    """
    return {
        "document": "Transfer Impact Assessment (TIA)",
        "wettelijke_basis": "AVG Art. 44-49 + EDPB Rec. 01/2020 + 02/2020",
        "model_versie": "1.0 (EDPB Schrems II gebaseerd)",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "stap_1": {
                "titel": "Stap 1 — Beschrijving van de doorgifte",
                "content": f"""
Verwerking: [{verwerking}]
Exporterende partij: [{org_naam}]
Importerende partij: [{ontvanger_naam}]
Land van ontvangst: [{ontvanger_land}]

1a. Welke gegevens worden doorgegeven?
- Categorieën persoonsgegevens: [lijst]
- Bijzondere categorieën (Art. 9)? [Ja/Nee — specificeer]
- Categorieën betrokkenen: [lijst]
- Volume: [aantal betrokkenen per jaar]

1b. Wat is het doel van de doorgifte?
[beschrijf het specifieke doel]

1c. Is de doorgifte periodiek of eenmalig?
[ ] Eenmalig
[ ] Periodiek — [frequentie: ___]
[ ] Continu

1d. Is er een adequaatheidsbesluit van de EU voor dit land?
[ ] Ja — [land staat op de adequaatheidslijst]
[ ] Nee — supplementerende maatregelen vereist
[ ] Onbekend — raadpleeg: https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/adequacy-decisions_en
""",
            },
            "stap_2": {
                "titel": "Stap 2 — Transfer Mechanisme",
                "instructie": "Identificeer het juridische mechanisme voor de doorgifte (Art. 46 AVG).",
                "content": """
2a. Gebruikt transfer mechanisme:
[ ] Adequaatheidsbesluit (Art. 45)
[ ] Standard Contractual Clauses (SCC) 2021/914 (Art. 46(2)(c))
[ ] Bindende bedrijfsregels (BCR) (Art. 47)
[ ] Gedragscode met verbintenis (Art. 46(2)(d))
[ ] Certificeringsmechanisme (Art. 46(2)(f))
[ ] Uitzondering Art. 49 (specificeer: [___])

2b. SCC-module (indien SCC):
[ ] Module 1: Controller → Controller
[ ] Module 2: Controller → Processor
[ ] Module 3: Processor → Processor
[ ] Module 4: Processor → Controller

2c. Zijn de SCC ondertekend?
[ ] Ja — datum: [datum]
[ ] Nee — [plan]
""",
            },
            "stap_3": {
                "titel": "Stap 3 — Beoordeling van het Derde Land",
                "instructie": "Beoordeel of het derde land een equivalent beschermingsniveau biedt (EDPB Rec. 01/2020 Stap 3).",
                "content": """
3a. Rule of Law beoordeling:
- Bestaan er wettelijke beperkingen op overheidstoegang? [Ja/Nee]
- Kunnen autoriteiten gegevens opvragen zonder rechterlijke machtiging? [Ja/Nee]
- Is er een onafhankelijke toezichthouder? [Ja/Nee]
- Zijn er effectieve rechtsmiddelen voor betrokkenen? [Ja/Nee]

3b. European Essential Guarantees (EDPB Rec. 02/2020):
[ ] A. Verwerking moet duidelijk omschreven hebben doel en uitgebreidheid
[ ] B. Onafhankelijke toezichthouder bestaat
[ ] C. Constitutionele en procedurele waarborgen bestaan
[ ] D. Effectieve rechten van betrokkenen (toegang, rectificatie, verwijdering)

3c. Risico-indicatoren:
- Massa-surveillance wetgeving? [Ja/Nee]
- Geen equivalente bescherming? [Ja/Nee]
- Geen effectieve rechtsmiddelen? [Ja/Nee]

3d. Conclusie landenbeoordeling:
[ ] Derde land biedt equivalent beschermingsniveau
[ ] Derde land biedt GEEN equivalent beschermingsniveau — supplementerende maatregelen vereist
""",
            },
            "stap_4": {
                "titel": "Stap 4 — Supplementerende Maatregelen",
                "instructie": "Indien het derde land geen equivalent bescherming biedt: welke extra maatregelen voer je in?",
                "content": """
4a. Technische maatregelen:
[ ] End-to-end encryptie (alleen betrokkene heeft sleutel)
[ ] Pseudonimisering vóór doorgifte
[ ] Splitting: gegevens worden gespreid over meerdere landen
[ ] Zero-knowledge architecture
[ ] Geografische data residency (data blijft in EU, alleen verwerking extern)

4b. Contractuele maatregelen:
[ ] Aanvullende clausules in SCC
[ ] Transparantieplicht: melding bij overheidsverzoeken
[ ] Auditrecht op importerende partij
[ ] Meldplicht bij wijziging derde-landswetgeving
[ ] Verbod op doorgeleiding aan derden

4c. Organisatorische maatregelen:
[ ] Interne transferbeleid
[ ] FG-toetsing vóór doorgifte
[ ] Periodieke her-evaluatie (frequentie: [___])
[ ] Training betrokken medewerkers
[ ] Procedure voor reactie op overheidsverzoeken

4d. Zijn de supplementerende maatregelen voldoende?
[ ] Ja — doorgifte kan doorgaan
[ ] Nee — stop de doorgifte of zoek alternatief
[ ] Onzeker — raadpleeg FG of AP
""",
            },
            "stap_5": {
                "titel": "Stap 5 — Documentatie en Goedkeuring",
                "content": """
Conclusie TIA:
[ ] Doorgifte is VERANTWOORDBAAR met de genomen maatregelen
[ ] Doorgifte is NIET verantwoordbaar — stop of zoek alternatief
[ ] Voorwaardelijk — alleen met extra maatregelen: [beschrijf]

FG-beoordeling:
Naam: [naam]
Oordeel: [Positief / Negatief / Met voorwaarden]
Datum: [datum]

Documentatie:
- SCC bijlage: [ja/nee]
- Technische maatregelen document: [ja/nee]
- Laatste herziening: [datum]
- Volgende herziening: [datum + 1 jaar]

Herziening: deze TIA wordt jaarlijks herzien of bij wijziging van wetgeving in het derde land.
""",
            },
        },
    }


def ai_risicoclassificatie_template(org_naam: str, ai_systeem: str, **kwargs) -> dict:
    """AI Risicoclassificatie — EU AI Act Art. 6 + Bijlage III.

    Verplicht vóór inzet van elk AI-systeem.
    Bepaalt of het systeem:
    - Verboden is (Art. 5)
    - Hoog-risico is (Art. 6 + Bijlage III)
    - Beperkt risico is (Art. 50 — transparantieplicht)
    - Minimaal risico is (geen verplichtingen)

    Gebaseerd op:
    - EU AI Act Verordening (EU) 2024/1689
    - Bijlage III: Hoog-risico toepassingsgebieden
    - Art. 6: Hoog-risico classificatieregels
    """
    return {
        "document": "AI Risicoclassificatie",
        "wettelijke_basis": "EU AI Act Art. 5-6 + Bijlage III (Verordening 2024/1689)",
        "model_versie": "1.0 (EU AI Act gebaseerd)",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "stap_1": {
                "titel": "Stap 1 — Is dit een AI-systeem?",
                "instructie": "Controleer of het systeem valt onder de AI-definitie (Art. 3(1)).",
                "content": f"""
AI-systeem: [{ai_systeem}]

1a. Voldoet aan Art. 3(1) definitie?
[ ] Ja — systeem ontwikkeld met technieken uit Bijlage I
[ ] Nee — geen AI-systeem, EU AI Act niet van toepassing

1b. Technische aanpak (Bijlage I):
[ ] Machine learning (supervised, unsupervised, reinforcement)
[ ] Logica- en kennisgebaseerde systemen (knowledge-based)
[ ] Statistische benaderingen
[ ] Bayesiaanse optimalisatie
[ ] Zoek- en optimalisatiemethoden
[ ] Regelgebaseerd / expert systemen

1c. Is het een bestaand of nieuw AI-systeem?
[ ] Bestaand (op de markt voor [datum])
[ ] Nieuw (ontwikkeld sinds [datum])
""",
            },
            "stap_2": {
                "titel": "Stap 2 — Verboden AI (Art. 5)",
                "instructie": "Controleer of het systeem onder een verbod valt.",
                "content": """
2a. Val het systeem onder een verbod?
[ ] a) Subliminale technieken die gedrag beïnvloeden (Art. 5(1)(a))
[ ] b) Uitbuiting van kwetsbaarheden (Art. 5(1)(b))
[ ] c) Social scoring door overheid (Art. 5(1)(c))
[ ] d) Real-time biometrie in openbare ruimten (Art. 5(1)(d)) — tenzij uitzondering
[ ] e) Gezichtsherkenning databases via internet (Art. 5(1)(e))
[ ] f) Emotie-herkenning op werk/onderwijs (Art. 5(1)(f))
[ ] g) Biometrische categorisering (Art. 5(1)(g))
[ ] h) Risicoprofielering voor misdrijven (Art. 5(1)(h))

[ ] Geen van bovenstaande — ga naar Stap 3

Indien verboden: STOP — het systeem mag niet worden ingezet.
""",
            },
            "stap_3": {
                "titel": "Stap 3 — Hoog-risico Classificatie (Art. 6 + Bijlage III)",
                "instructie": "Controleer of het systeem hoog-risico is.",
                "content": """
3a. Is het een product met CE-markering waarvan het AI-systeem onderdeel is?
(Zie Bijlage I producten — machines, medische hulpmiddelen, speelgoed, etc.)
[ ] Ja — [specificeer product]
[ ] Nee

3b. Val het systeem onder Bijlage III toepassingen?

BIJAGLE III — Hoog-risico toepassingen:

1. Biometrie:
[ ] 1.1 Biometrische identificatie (real-time of post)
[ ] 1.2 Biometrische categorisering
[ ] 1.3 Gezichtsherkenning

2. Kritieke infrastructuur:
[ ] 2.1 Beheer van kritieke infrastructuur

3. Onderwijs en beroep:
[ ] 3.1 Toelatingsexamens
[ ] 3.2 Beoordeling in onderwijs
[ ] 3.3 Beroepskeuze- en -examen

4. Werkgelegenheid en personeel:
[ ] 4.1 CV-sorting
[ ] 4.2 Evaluatie van prestaties
[ ] 4.3 Promotiebesluiten

5. Krediet en verzekering:
[ ] 5.1 Kredietscoring (geen financiële diensten)
[ ] 5.2 Verzekering risicobeoordeling en prijsstelling

6. Wetshandhaving:
[ ] 6.1 Risicobeoordeling van verdachten
[ ] 6.2 Polygraaf
[ ] 6.3 Evaluatie van bewijsmateriaal

7. Migratie en grensbeheer:
[ ] 7.1 Polygraaf
[ ] 7.2 Documentverificatie
[ ] 7.3 Risicobeoordeling van reizigers

8. Rechtspraak en democratie:
[ ] 8.1 Ondersteuning rechters
[ ] 8.2 Democratische procesvoering

[ ] Geen van bovenstaande — ga naar Stap 4

Indien ≥1 positief: SYSTEEM IS HOOG-RISICO
""",
            },
            "stap_4": {
                "titel": "Stap 4 — Uitzonderingen en Verfijning",
                "instructie": "Controleer uitzonderingen op hoog-risico classificatie.",
                "content": """
4a. Geldt een uitzondering (Art. 6(2)-(3))?
[ ] Systeem uitsluitend voor militaire/verdedigingsdoeleinden
[ ] Systeem uitsluitend voor onderzoek
[ ] Systeem vergelijkbaar met reeds geconformiteitsbeoordeeld product

4b. Is het een "gesloten" of "open" AI-systeem?
[ ] Gesloten (alleen intern gebruik)
[ ] Open (beschikbaar voor derden)

4c. Is er sprake van "significant beïnvloeding" van besluitvorming?
[ ] Ja — AI-systeem beïnvloedt substantiële besluiten
[ ] Nee — AI-systeem ondersteunt alleen, mens neemt besluit
""",
            },
            "stap_5": {
                "titel": "Stap 5 — Conclusie en Vervolg",
                "content": """
Classificatie:
[ ] VERBODEN (Art. 5) — STOP
[ ] HOOG-RISICO (Art. 6 + Bijlage III) — verplichtingen van toepassing
[ ] BEPERKT RISICO (Art. 50) — transparantieplicht
[ ] MINIMAAL RISICO — geen verplichtingen

Indien HOOG-RISICO, verplichtingen:
[ ] Risicobeheersysteem (Art. 9)
[ ] Data governance (Art. 10)
[ ] Technische documentatie (Art. 11)
[ ] Logging (Art. 12)
[ ] Transparantie (Art. 13)
[ ] Menselijke tussenkomst (Art. 14)
[ ] Nauwkeurigheid, robuustheid, cybersecurity (Art. 15)
[ ] Kwaliteitsbeheersysteem (Art. 16)
[ ] Conformiteitsbeoordeling (Art. 43)
[ ] FRIA verplicht (Art. 27)

Vervolgactie:
[ ] Start FRIA (Fundamental Rights Impact Assessment)
[ ] Stel technische documentatie op
[ ] Implementeer menselijke tussenkomst
[ ] Plan conformity assessment

Goedkeuring:
Naam: [naam]
Functie: [functie]
Datum: [datum]
""",
            },
        },
    }


def privacy_by_design_checklist_template(
    org_naam: str, verwerking: str, **kwargs
) -> dict:
    """Privacy by Design & Default (PbD) Checklist — AVG Art. 25.

    Gebaseerd op:
    - EDPB Guidelines 4/2019 on Article 25
    - ISO 27701:2019 (Privacy Information Management)
    - CNIL PbD principles
    - OWASP Privacy by Design Framework

    7 fundamentele principes + implementatie-checklist.
    """
    return {
        "document": "Privacy by Design & Default Checklist",
        "wettelijke_basis": "AVG Art. 25 + EDPB Guidelines 4/2019",
        "model_versie": "1.0 (EDPB gebaseerd)",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "inleiding": {
                "titel": "Inleiding",
                "content": f"""
Verwerking: [{verwerking}]

Privacy by Design (Art. 25(1)): Implementeer passende technische en organisatorische maatregelen om databeschermingseffectief toe te passen.

Privacy by Default (Art. 25(2)): Zorg dat standaard alleen persoonsgegevens worden verwerkt die noodzakelijk zijn voor elk specifiek doel.

Deze checklist dekt 7 principes + operationele checks.
""",
            },
            "principe_1": {
                "titel": "Principe 1 — Proactief niet Reactief",
                "instructie": "Voorkom privacy-incidenten in plaats van ze te herstellen.",
                "content": """
[ ] Privacy-risico's geïdentificeerd vóór ontwikkeling
[ ] Privacy Impact Assessment (DPIA) uitgevoerd
[ ] Privacy-risico's gedocumenteerd in risicoregister
[ ] Preventieve maatregelen geïmplementeerd
[ ] Geen "privacy als afterthought"

Status: [ ] Volledig [ ] Gedeeltelijk [ ] Niet
""",
            },
            "principe_2": {
                "titel": "Principe 2 — Privacy als Standaard (Default)",
                "instructie": "Privacy is de standaardinstelling, geen opt-in.",
                "content": """
[ ] Standaardinstellingen zijn privacy-vriendelijk
[ ] Betrokkenen hoeven niets te doen voor maximale privacy
[ ] Data minimalisatie is standaard (niet: alles verzamelen, later filteren)
[ ] Bewaartermijnen zijn standaard zo kort mogelijk
[ ] Toegang tot gegevens is standaard beperkt (need-to-know)
[ ] Profielen zijn standaard niet publiek toegankelijk

Status: [ ] Volledig [ ] Gedeeltelijk [ ] Niet
""",
            },
            "principe_3": {
                "titel": "Principe 3 — Privacy Ingebouwd in Ontwerp",
                "instructie": "Privacy is integraal onderdeel van de systeemarchitectuur.",
                "content": """
[ ] Privacy-vereisten in user stories / requirements opgenomen
[ ] Privacy-review onderdeel van SDLC (Software Development Life Cycle)
[ ] Architectuur-documentatie bevat privacy-sectie
[ ] Privacy-patterns toegepast (pseudonimisering, encryptie, etc.)
[ ] Privacy-testen onderdeel van QA-proces

Status: [ ] Volledig [ ] Gedeeltelijk [ ] Niet
""",
            },
            "principe_4": {
                "titel": "Principe 4 — Volledige Functionaliteit (Win-Win)",
                "instructie": "Privacy en functionaliteit sluiten elkaar niet uit.",
                "content": """
[ ] Privacy-maatregelen beperken functionaliteit niet onnodig
[ ] Geen vals dilemma "privacy vs. security"
[ ] Privacy-verhogende technieken onderzocht (PETs)
[ ] Functionele doelen behouden met privacy-maatregelen

Status: [ ] Volledig [ ] Gedeeltelijk [ ] Niet
""",
            },
            "principe_5": {
                "titel": "Principe 5 — End-to-End Beveiliging",
                "instructie": "Privacy door de gehele levenscyclus van de data.",
                "content": """
[ ] Encryptie bij verzamelen
[ ] Encryptie bij opslag (at rest)
[ ] Encryptie bij overdracht (in transit)
[ ] Veilige vernietiging na bewaartermijn
[ ] Geen plaintext logging van persoonsgegevens
[ ] Backup-encryptie

Status: [ ] Volledig [ ] Gedeeltelijk [ ] Niet
""",
            },
            "principe_6": {
                "titel": "Principe 6 — Transparantie en Zichtbaarheid",
                "instructie": "Voor betrokkenen moet duidelijk zijn wat er met hun gegevens gebeurt.",
                "content": """
[ ] Privacyverklaring beschikbaar en begrijpelijk
[ ] Verwerkingsdoelen expliciet gecommuniceerd
[ ] Contactgegevens FG zichtbaar
[ ] Betrokkenen kunnen inzien welke gegevens worden verwerkt
[ ] Wijzigingen in verwerking worden gecommuniceerd

Status: [ ] Volledig [ ] Gedeeltelijk [ ] Niet
""",
            },
            "principe_7": {
                "titel": "Principe 7 — Respect voor Privacy van Betrokkenen",
                "instructie": "De belangen van betrokkenen staan centraal.",
                "content": """
[ ] Recht op inzage geïmplementeerd
[ ] Recht op rectificatie geïmplementeerd
[ ] Recht op verwijdering geïmplementeerd
[ ] Recht op dataportabiliteit geïmplementeerd
[ ] Recht op bezwaar geïmplementeerd
[ ] Toestemmingsbeheer (waar van toepassing)
[ ] Makkelijke uitoefening rechten (self-service waar mogelijk)

Status: [ ] Volledig [ ] Gedeeltelijk [ ] Niet
""",
            },
            "operationele_checks": {
                "titel": "Operationele Checks",
                "content": """
Data Minimalisatie:
[ ] Alleen noodzakelijke gegevens worden verzameld
[ ] Geen "nice to have" data collection
[ ] Periodieke review van verzamelde gegevens

Toegangscontrole:
[ ] Role-Based Access Control (RBAC)
[ ] Multi-Factor Authentication (MFA)
[ ] Principle of Least Privilege
[ ] Periodieke toegangsreview

Logging en Monitoring:
[ ] Toegang tot persoonsgegevens wordt gelogd
[ ] Anomalie-detectie voor ongeautoriseerde toegang
[ ] Log-retentie voldoet aan AVG-vereisten

Verwerkersmanagement:
[ ] Verwerkersovereenkomsten (DPA) afgesloten
[ ] Sub-verwerkers geïdentificeerd en goedgekeurd
[ ] Periodieke verwerkersaudits

Incident Response:
[ ] Datalek-procedure beschikbaar
[ ] Meldprocedure AP (72u) en betrokkenen (hoog risico)
[ ] Root cause analysis na incident

Training:
[ ] Privacy-training voor alle medewerkers
[ ] Specifieke training voor medewerkers met datatoegang
[ ] Awareness programma actueel
""",
            },
            "eindoordeel": {
                "titel": "Eindoordeel",
                "content": """
Privacy by Design & Default status:
[ ] Volledig geïmplementeerd
[ ] Gedeeltelijk geïmplementeerd — actiepunten: [beschrijf]
[ ] Niet geïmplementeerd — urgentie: [Hoog/Middel/Laag]

Verbeteracties:
1. [actie] — eigenaar: [naam] — deadline: [datum]
2. [actie] — eigenaar: [naam] — deadline: [datum]
3. [actie] — eigenaar: [naam] — deadline: [datum]

Goedkeuring:
Naam: [naam]
Functie: [functie]
Datum: [datum]

Herziening: deze checklist wordt jaarlijks herzien of bij wijziging van de verwerking.
""",
            },
        },
    }
