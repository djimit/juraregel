"""Informatiebeveiliging Document Templates — ISO 27001 / BIO2 / NIS2."""

from datetime import date


def ib_beleid_template(org_naam: str, **kwargs) -> dict:
    """Informatiebeveiligingsbeleid — ISO 27001 5.2 + BIO2 A.5."""
    return {
        "document": "Informatiebeveiligingsbeleid",
        "wettelijke_basis": "ISO 27001:2022 5.2 + BIO2 A.5",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "sectie_1": {
                "titel": "1. Doel en reikwijdte",
                "content": f"Het informatiebeveiligingsbeleid van {org_naam} beschrijft de kaders voor het beschermen van informatie tegen bedreigingen om continuïteit, integriteit en vertrouwelijkheid te garanderen.\n\nReikwijdte: alle systemen, processen en medewerkers binnen de organisatie.",
            },
            "sectie_2": {
                "titel": "2. Visie en principes",
                "content": """Informatiebeveiliging is een integraal onderdeel van onze bedrijfsvoering. Wij hanteren de volgende principes:

- Beschikbaarheid: Informatie is beschikbaar wanneer dat nodig is
- Integriteit: Informatie is volledig, juist en ongewijzigd
- Vertrouwelijkheid: Informatie is alleen toegankelijk voor geautoriseerden
- Compliance: Voldoen aan wettelijke en contractuele verplichtingen
- Continuïteit: Bedrijfsvoering blijft gegarandeerd bij incidenten""",
            },
            "sectie_3": {
                "titel": "3. Rollen en verantwoordelijkheden",
                "content": """Bestuurder:
- Goedkeuring beleid en doelstellingen
- Voldoende middelen beschikbaar stellen
- Eindverantwoordelijkheid dragen

Functionaris Informatiebeveiliging (FIC):
- Uitvoering en monitoring beleid
- Rapportage aan management
- Coördinatie incidenten

Functionaris Gegevensbescherming (FG):
- Privacy compliance
- DPIA-proces
- Contactpersoon AP

Alle medewerkers:
- Naleving beleid en procedures
- Melden van incidenten
- Deelnemen aan training""",
            },
            "sectie_4": {
                "titel": "4. Acceptabel gebruik",
                "content": """- Systemen uitsluitend gebruiken voor organisatiedoeleinden
- Geen ongeautoriseerde software installeren
- Wachtwoorden veilig beheren (min. 16 tekens, MFA)
- Vertrouwelijke gegevens niet delen zonder autorisatie
- Mobiele apparaten versleuteld en beveiligd
- Fysieke toegang respecteren (clean desk policy)""",
            },
            "sectie_5": {
                "titel": "5. Incidenten en melding",
                "content": """Alle medewerkers zijn verplicht incidenten direct te melden bij:
- FIC: [email/telefoon]
- Service Desk: [email/telefoon]

Incidenten worden geclassificeerd:
- Laag: geen directe dreiging, binnen 24u afgehandeld
- Middel: mogelijke impact, binnen 8u afgehandeld
- Hoog: actieve dreiging, direct escalatie naar FIC + management""",
            },
            "sectie_6": {
                "titel": "6. Continuïteit",
                "content": """- Business Continuity Plan (BCP) is beschikbaar en getest
- Recovery Time Objectives (RTO) zijn gedefinieerd per kritiek proces
- Recovery Point Objectives (RPO) zijn gedefinieerd per kritieke data
- Jaarlijkse BCP-oefening verplicht""",
            },
            "sectie_7": {
                "titel": "7. Compliance en handhaving",
                "content": """- Jaarlijkse interne audit verplicht
- Overtredingen worden gemeld aan management
- Herhaalde overtredingen leiden tot sancties
- Beleid wordt jaarlijks herzien en bijgewerkt""",
            },
            "goedkeuring": {
                "titel": "Goedkeuring",
                "content": f"Naam bestuurder: [naam]\nHandtekening: [tekening]\nDatum: {date.today().isoformat()}",
            },
        },
    }


def statement_of_applicability_template(org_naam: str, **kwargs) -> dict:
    """Statement of Applicability — ISO 27001 6.1.3d."""
    return {
        "document": "Statement of Applicability (SoA)",
        "wettelijke_basis": "ISO 27001:2022 6.1.3d",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "instructie": "Voor elk van de 93 Annex A controls aangeven: Toepaslijk (Ja/Nee), Implementatiestatus, en Verwijzing naar implementatie-documentatie.",
            "controls_categorieen": [
                {
                    "categorie": "A.5 Organizational controls (36)",
                    "voorbeelden": [
                        "A.5.1 Policies for information security",
                        "A.5.7 Threat intelligence",
                        "A.5.9 Inventory of information assets",
                        "A.5.12 Classification of information",
                    ],
                },
                {
                    "categorie": "A.6 People controls (8)",
                    "voorbeelden": [
                        "A.6.1 Screening",
                        "A.6.3 Information security awareness",
                        "A.6.6 Confidentiality agreements",
                    ],
                },
                {
                    "categorie": "A.7 Physical controls (14)",
                    "voorbeelden": [
                        "A.7.1 Physical security perimeters",
                        "A.7.4 Physical security monitoring",
                        "A.7.9 Security of assets off-premises",
                    ],
                },
                {
                    "categorie": "A.8 Technological controls (35)",
                    "voorbeelden": [
                        "A.8.1 User endpoint devices",
                        "A.8.2 Privileged access rights",
                        "A.8.5 Secure authentication",
                        "A.8.11 Data masking",
                        "A.8.15 Logging",
                        "A.8.24 Use of cryptography",
                    ],
                },
            ],
            "template": "Per control:\n| Control ID | Naam | Applicable? | Status | Justificatie | Verwijzing |\n|---|---|---|---|---|---|\n| A.5.1 | Policies | Ja | Geïmplementeerd | - | [link] |\n| A.5.7 | Threat intelligence | Nee | - | Geen threat intel programma | - |",
        },
    }


def risicoanalyse_template(org_naam: str, **kwargs) -> dict:
    """Risicoanalyse — ISO 27001 6.1.2."""
    return {
        "document": "Risicoanalyse & -beoordeling",
        "wettelijke_basis": "ISO 27001:2022 6.1.2",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "methodologie": "Risico = Impact x Waarschijnlijkheid (5x5 matrix)",
            "schaal": {
                "waarschijnlijkheid": "1 (Zeldzaam) → 5 (Zeker)",
                "impact": "1 (Verwaarloosbaar) → 5 (Catastrofaal)",
                "risico_niveau": "1-4 (Laag), 5-11 (Middel), 12-19 (Hoog), 20-25 (Kritiek)",
            },
            "template": [
                {
                    "id": "R-001",
                    "bedreiging": "[beschrijving]",
                    "zwakte": "[kwetsbaarheid]",
                    "impact": 4,
                    "waarschijnlijkheid": 3,
                    "score": 12,
                    "behandeling": "Verminderen",
                    "maatregel": "[maatregel]",
                    "eigenaar": "[naam]",
                    "deadline": "[datum]",
                },
            ],
            "voorbeelden": [
                {
                    "id": "R-001",
                    "bedreiging": "Ransomware-aanval",
                    "zwakte": "Verouderde systemen",
                    "impact": 5,
                    "waarschijnlijkheid": 3,
                    "score": 15,
                    "behandeling": "Verminderen",
                    "maatregel": "Patch management + backup + EDR",
                    "eigenaar": "CISO",
                    "deadline": "2026-10-01",
                },
                {
                    "id": "R-002",
                    "bedreiging": "Datalek via verwerker",
                    "zwakte": "Geen DPA of audit",
                    "impact": 4,
                    "waarschijnlijkheid": 3,
                    "score": 12,
                    "behandeling": "Verminderen",
                    "maatregel": "DPA afsluiten + jaarlijkse audit",
                    "eigenaar": "FG",
                    "deadline": "2026-09-01",
                },
                {
                    "id": "R-003",
                    "bedreiging": "Inwendig misbruik",
                    "zwakte": "Geen toegangscontrole",
                    "impact": 4,
                    "waarschijnlijkheid": 2,
                    "score": 8,
                    "behandeling": "Verminderen",
                    "maatregel": "RBAC + MFA + logging",
                    "eigenaar": "FIC",
                    "deadline": "2026-11-01",
                },
            ],
        },
    }


def bcp_template(org_naam: str, **kwargs) -> dict:
    """Business Continuity Plan — ISO 22301 8.4."""
    return {
        "document": "Business Continuity Plan (BCP)",
        "wettelijke_basis": "ISO 22301:2018 8.4",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "crisisorganisatie": {
                "crisismanager": "[naam, telefoon]",
                "communicatie": "[naam, telefoon]",
                "IT-coordinator": "[naam, telefoon]",
                "FG/FIC": "[naam, telefoon]",
            },
            "kritieke_processen": [
                {
                    "proces": "[naam]",
                    "impact": "Kritiek",
                    "RTO": "4u",
                    "RPO": "1u",
                    "alternatief": "[beschrijving]",
                },
            ],
            "procedures": {
                "activatie": "1. Crisis vaststellen 2. Crisisgroep bijeenroepen 3. Impact beoordelen 4. BCP activeren",
                "communicatie": "1. Intern informeren 2. Stakeholders informeren 3. Media-berichtgeving (indien nodig)",
                "herstel": "1. Tijdelijke werkvoorziening 2. Data-herstel vanuit backup 3. Systemen herstarten 4. Validatie 5. Normalisatie",
            },
            "testen": "Minimaal jaarlijks een tabletop-oefening + elke 2 jaar een full-scale test.",
        },
    }


def incident_response_template(org_naam: str, **kwargs) -> dict:
    """Incident Response Plan — NIS2 Art. 21 + ISO 27001 A.5.24."""
    return {
        "document": "Incident Response Plan",
        "wettelijke_basis": "NIS2 Art. 21 + ISO 27001 A.5.24",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "fasen": [
                {
                    "fase": "Voorbereiding",
                    "acties": [
                        "Team samenstellen",
                        "Tools beschikbaar",
                        "Playbooks schrijven",
                        "Oefeningen plannen",
                    ],
                },
                {
                    "fase": "Detectie",
                    "acties": [
                        "Monitoring",
                        "Alert analyse",
                        "Classificatie",
                        "Escalatie",
                    ],
                },
                {
                    "fase": "Containment",
                    "acties": [
                        "Isolatie",
                        "Bewaring bewijs",
                        "Tijdelijke maatregelen",
                        "Communicatie",
                    ],
                },
                {
                    "fase": "Eradicatie",
                    "acties": [
                        "Oorzaak verwijderen",
                        "Systemen herstellen",
                        "Beveiliging verbeteren",
                    ],
                },
                {
                    "fase": "Herstel",
                    "acties": [
                        "Normalisatie",
                        "Validatie",
                        "Monitoring",
                        "Lessons learned",
                    ],
                },
            ],
            "meldingstermijnen": {
                "vroegtijdig_signaal": "Binnen 24 uur (NIS2 Art. 23(1))",
                "uitgebreide_melding": "Binnen 72 uur (NIS2 Art. 23(2))",
                "eindrapport": "Binnen 1 maand (NIS2 Art. 23(3))",
                "AP_datalek": "Binnen 72 uur (AVG Art. 33)",
            },
            "playbooks": [
                "Ransomware",
                "Datalek",
                "DDoS",
                "Insider threat",
                "Phishing",
                "Supply chain",
            ],
        },
    }
