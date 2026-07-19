"""JuraRegel Document Generator — Genereert alle verplichte compliance-documenten.

Ondersteunde documenten (wettelijk verplicht):

PRIVACY & DATA PROTECTION (AVG):
  1. DPIA (Data Protection Impact Assessment) — AVG Art. 35
  2. Privacyverklaring / Informatiebeleid — AVG Art. 13-14
  3. Verwerkersovereenkomst (DPA) — AVG Art. 28
  4. Registratie van verwerkingsactiviteiten (ROVA) — AVG Art. 30
  5. Datalek meldprocedure — AVG Art. 33-34
  6. Toestemmingsregister — AVG Art. 7

INFORMATIEBEVEILIGING (ISO 27001 / BIO2):
  7. Informatiebeveiligingsbeleid (IB-beleid) — ISO 27001 5.2
  8. Statement of Applicability (SoA) — ISO 27001 6.1.3d
  9. Risicoanalyse & -beoordeling — ISO 27001 6.1.2
  10. Risicobehandelingsplan — ISO 27001 6.1.3
  11. Beleidsdoelstellingen informatiebeveiliging — ISO 27001 6.2
  12. Business Continuity Plan — ISO 22301 8.4
  13. Incident Response Plan — NIS2 Art. 21 + ISO 27001 A.5.24

AI & ALGORITMES (EU AI Act):
  14. Algoritmeregister publicatie — EU AI Act Art. 26
  15. FRIA (Fundamental Rights Impact Assessment) — EU AI Act Art. 27
  16. Technische documentatie AI-systeem — EU AI Act Art. 11
  17. Conformiteitsverklaring AI — EU AI Act Art. 43
  18. AI-geletterdijkheidsbeleid — EU AI Act Art. 4

CYBERSECURITY (NIS2):
  19. Cybersecurity risicomanagement — NIS2 Art. 21
  20. Incidentmeldprocedure (24h/72h/1mnd) — NIS2 Art. 23
  21. Supply chain security beleid — NIS2 Art. 21(2)(c)

KWALITEIT & GOVERNANCE:
  22. Kwaliteitsbeleid — ISO 9001 5.2
  23. Kwaliteitsdoelstellingen — ISO 9001 6.2
  24. IT Service Management beleid — ISO 20000-1 5.2
  25. IT Governance Framework — COBIT 2019 EDM

ZORG (NEN 7510):
  26. Informatiebeveiligingsbeleid Zorg — NEN 7510-1
  27. MedMij compliantieverklaring — NEN 7510-2 + MedMij
  28. BSN-k verwerkingsprotocol — NEN 7510-2 + BSN-k

MILIEU & VEILIGHEID:
  29. Milieubeleid — ISO 14001 5.2
  30. Arbeidsomstandighedenbeleid (Arbo) — ISO 45001 5.2
  31. Risico-inventarisatie - Evaluatie (RI&E) — ISO 45001 6.1.2
"""

from datetime import date
from pathlib import Path
from typing import Any


DOCUMENT_TEMPLATES = {
    "dpia": {
        "title": "Data Protection Impact Assessment (DPIA)",
        "legal_basis": "AVG Art. 35",
        "mandatory_when": "Verwerking levert waarschijnlijk hoog risico op voor betrokkenen",
        "sections": [
            "Beschrijving van de verwerking",
            "Beoordeling van noodzaak en proportionaliteit",
            "Risico-inschatting voor betrokkenen",
            "Maatregelen om risico's te mitigeren",
            "Goedkeuring en ondertekening",
        ],
    },
    "privacyverklaring": {
        "title": "Privacyverklaring / Informatiebeleid",
        "legal_basis": "AVG Art. 13-14",
        "mandatory_when": "Altijd — bij verzamelen persoonsgegevens",
        "sections": [
            "Verwerkingsverantwoordelijke",
            "Contactgegevens Functionaris Gegevensbescherming",
            "Doeleinden van verwerking",
            "Rechtsgrond voor verwerking",
            "Ontvangers van gegevens",
            "Bewaartermijnen",
            "Rechten van betrokkenen",
            "Recht op klacht bij Autoriteit Persoonsgegevens",
        ],
    },
    "verwerkersovereenkomst": {
        "title": "Verwerkersovereenkomst (DPA)",
        "legal_basis": "AVG Art. 28",
        "mandatory_when": "Bij gebruik van verwerkers",
        "sections": [
            "Onderwerp en duur",
            "Aard en doel van verwerking",
            "Type persoonsgegevens",
            "Rechten en plichten van partijen",
            "Beveiligingsmaatregelen",
            "Sub-processing voorwaarden",
            "Datalek meldprocedure",
            "Gegevens na beëindiging",
            "Auditrechten",
        ],
    },
    "rova": {
        "title": "Registratie van VerwerkingsActiviteiten (ROVA)",
        "legal_basis": "AVG Art. 30",
        "mandatory_when": "Altijd — elke organisatie die PII verwerkt",
        "sections": [
            "Naam en contactgegevens verwerkingsverantwoordelijke",
            "Doeleinden van de verwerking",
            "Categorieën betrokkenen",
            "Categorieën persoonsgegevens",
            "Categorieën ontvangers",
            "Doorgiften naar derde landen",
            "Bewaartermijnen",
            "Beveiligingsmaatregelen",
        ],
    },
    "statement_of_applicability": {
        "title": "Statement of Applicability (SoA)",
        "legal_basis": "ISO 27001:2022 6.1.3d",
        "mandatory_when": "Altijd — verplicht document voor ISO 27001 certificering",
        "sections": [
            "Scope van het ISMS",
            "Overzicht Annex A controls (93 controls)",
            "Applicable / Not applicable per control",
            "Justificatie voor uitsluitingen",
            "Verwijzing naar implementatie-documentatie",
            "Versiebeheer en goedkeuring",
        ],
    },
    "informatiebeveiligingsbeleid": {
        "title": "Informatiebeveiligingsbeleid (IB-beleid)",
        "legal_basis": "ISO 27001:2022 5.2 + BIO2 A.5",
        "mandatory_when": "Altijd — top-management vaststelt beleid",
        "sections": [
            "Doel en reikwijdte",
            "Visie op informatiebeveiliging",
            "Rollen en verantwoordelijkheden",
            "Acceptabel gebruiksbeleid",
            "Omgaan met incidenten",
            "Continuïteit van bedrijfsvoering",
            "Wettelijke en contractuele verplichtingen",
            "Goedkeuring door management",
        ],
    },
    "risicoanalyse": {
        "title": "Risicoanalyse & -beoordeling",
        "legal_basis": "ISO 27001:2022 6.1.2",
        "mandatory_when": "Altijd — minimaal jaarlijks herzien",
        "sections": [
            "Risicobeoordelingsmethodologie",
            "Risicocriteria (impact x waarschijnlijkheid)",
            "Geïdentificeerde risico's",
            "Risicoregister",
            "Risiconiveaus en acceptatiecriteria",
            "Resultaten en conclusies",
        ],
    },
    "risicobehandelingsplan": {
        "title": "Risicobehandelingsplan",
        "legal_basis": "ISO 27001:2022 6.1.3",
        "mandatory_when": "Altijd — per geïdentificeerd risico",
        "sections": [
            "Overzicht van te behandelen risico's",
            "Behandelingsopties (accepteeren, verminderen, vermijden, overdragen)",
            "Geselecteerde maatregelen",
            "Verantwoordelijke en deadlines",
            "Residuaal risico na maatregelen",
            "Acceptatie door management",
        ],
    },
    "business_continuity_plan": {
        "title": "Business Continuity Plan (BCP)",
        "legal_basis": "ISO 22301:2018 8.4",
        "mandatory_when": "Altijd — voor kritieke processen",
        "sections": [
            "Doel en reikwijdte",
            "BIA resultaten (RTO/RPO)",
            "Crisisorganisatie en rollen",
            "Communicatieprocedures",
            "Herstelprocedures per kritiek proces",
            "Alternatieve werkvoorzieningen",
            "Test- en oefenprogramma",
            "Contactlijsten",
        ],
    },
    "incident_response_plan": {
        "title": "Incident Response Plan",
        "legal_basis": "NIS2 Art. 21 + ISO 27001 A.5.24",
        "mandatory_when": "Altijd — verplicht voor essentiële/belangrijke diensten",
        "sections": [
            "Definities en classificatie",
            "Escalatieprocedure",
            "Meldingstermijnen (NIS2: 24h/72h/1mnd)",
            "Containment en eradication",
            "Herstel en lessons learned",
            "Communicatie (intern/extern)",
            "Juridische verplichtingen",
            "Contactlijsten CSIRT",
        ],
    },
    "fria": {
        "title": "Fundamental Rights Impact Assessment (FRIA)",
        "legal_basis": "EU AI Act Art. 27",
        "mandatory_when": "Verplicht voor hoog-risico AI-systemen",
        "sections": [
            "Beschrijving AI-systeem en doel",
            "Grondrechtenanalyse",
            "Impact op kwetsbare groepen",
            "Mitigerende maatregelen",
            "Proportionaliteitstoets",
            "Publieke consultatie (indien van toepassing)",
            "Goedkeuring en monitoring",
        ],
    },
    "algoritmeregister": {
        "title": "Algoritmeregister Publicatie",
        "legal_basis": "EU AI Act Art. 26",
        "mandatory_when": "Verplicht voor hoog-risico AI-systemen",
        "sections": [
            "Naam en versie algoritme",
            "Doel en werking",
            "Verwerkte gegevenscategorieën",
            "Risicoclassificatie (EU AI Act)",
            "Menselijke tussenkomst",
            "Prestatie-indicatoren",
            "Goedkeuringsdatum",
        ],
    },
    "technische_documentatie_ai": {
        "title": "Technische Documentatie AI-systeem",
        "legal_basis": "EU AI Act Art. 11 + Bijlage IV",
        "mandatory_when": "Verplicht voor hoog-risico AI-systemen",
        "sections": [
            "Algemene beschrijving AI-systeem",
            "Capaciteiten en beperkingen",
            "Data requirements (training, validatie, test)",
            "Menselijke tussenkomst (human oversight)",
            "Nauwkeurigheid en robuustheid",
            "Cybersecurity maatregelen",
            "CE-markering en conformiteit",
        ],
    },
    "conformiteitsverklaring_ai": {
        "title": "EU Conformiteitsverklaring AI",
        "legal_basis": "EU AI Act Art. 43 + 49",
        "mandatory_when": "Verificatie voor op de markt brengen hoog-risico AI",
        "sections": [
            "Productnaam en type",
            "Naam en adres fabrikant",
            "Verantwoordelijke persoon",
            "Verwijzen naar harmoniseerde normen",
            "Gecontroleerde conformiteitsprocedure",
            "Ondertekening en datum",
        ],
    },
    "nis2_cybersecurity_risico": {
        "title": "Cybersecurity Risicomanagement Document",
        "legal_basis": "NIS2 Art. 21",
        "mandatory_when": "Verplicht voor essentiële en belangrijke diensten",
        "sections": [
            "Risicomanagement raamwerk",
            "Technische beveiligingsmaatregelen",
            "Organisatorische maatregelen",
            "Incident preventie en detectie",
            "Supply chain beveiliging",
            "Human resources beveiliging",
            "Cryptografiebeleid",
            "Periodieke evaluatie",
        ],
    },
    "kwaliteitsbeleid": {
        "title": "Kwaliteitsbeleid",
        "legal_basis": "ISO 9001:2015 5.2",
        "mandatory_when": "Verplicht voor ISO 9001 certificering",
        "sections": [
            "Organisatiecontext",
            "Kwaliteitsvisie en -missie",
            "Kwaliteitsdoelstellingen",
            "Klantgericht beleid",
            "Continuïteitsverbetering",
            "Goedkeuring management",
        ],
    },
    "milieubeleid": {
        "title": "Milieubeleid",
        "legal_basis": "ISO 14001:2015 5.2",
        "mandatory_when": "Verplicht voor ISO 14001 certificering",
        "sections": [
            "Milieubeleidsverklaring",
            "Significante milieueffecten",
            "Compliance verplichtingen",
            "Milieudoelstellingen",
            "Preventie van vervuiling",
            "Continuïteitsverbetering",
        ],
    },
    "arbobeleid": {
        "title": "Arbobeleid (Arbeidsomstandigheden)",
        "legal_basis": "ISO 45001:2018 5.2",
        "mandatory_when": "Verplicht voor ISO 45001 certificering",
        "sections": [
            "Arbobeleidsverklaring",
            "Hazard identificatie",
            "Worker participation",
            "OH&S doelstellingen",
            "Compliance verplichtingen",
            "Preventie van ongevallen",
        ],
    },
    "rie": {
        "title": "Risico-Inventarisatie & Evaluatie (RI&E)",
        "legal_basis": "ISO 45001:2018 6.1.2 + Arbowet",
        "mandatory_when": "Verplicht voor elke werkgever (Arbowet Art. 5)",
        "sections": [
            "Organisatiegegevens",
            "Procesbeschrijving",
            "Geïdentificeerde gevaren",
            "Risicobeoordeling",
            "Te nemen maatregelen",
            "Actieprioritering",
            "Goedkeuring preventiemedewerker",
        ],
    },
    "itsm_beleid": {
        "title": "IT Service Management Beleid",
        "legal_basis": "ISO 20000-1:2018 5.2",
        "mandatory_when": "Verplicht voor ISO 20000 certificering",
        "sections": [
            "Service management visie",
            "Service portfolio",
            "SLA-raamwerk",
            "Incident management proces",
            "Change management proces",
            "Continual service improvement",
        ],
    },
    "it_governance_framework": {
        "title": "IT Governance Framework",
        "legal_basis": "COBIT 2019 EDM",
        "mandatory_when": "Aangewezen voor enterprise IT governance",
        "sections": [
            "IT governance structuur",
            "Rollen en verantwoordelijkheden (RACI)",
            "IT risicomanagement",
            "IT resource management",
            "Performance measurement",
            "Compliance monitoring",
        ],
    },
    "zorg_ib_beleid": {
        "title": "Informatiebeveiligingsbeleid Zorg",
        "legal_basis": "NEN 7510-1:2024",
        "mandatory_when": "Verplicht voor zorgaanbieders",
        "sections": [
            "Scope zorgorganisatie",
            "Patiëntgegevensbescherming",
            "MedMij-compliantie",
            "BSN-k verwerking",
            "Toegangscontrole medische gegevens",
            "IGJ-inspectie voorbereiding",
        ],
    },
}


class DocumentGenerator:
    """Genereert verplichte compliance-documenten."""

    def __init__(self, org_naam: str, **kwargs):
        self.org_naam = org_naam
        self.metadata = kwargs
        self.datum = date.today().isoformat()

    def generate(self, doc_type: str) -> dict:
        """Genereer een specifiek document."""
        template = DOCUMENT_TEMPLATES.get(doc_type)
        if not template:
            return {"error": f"Onbekend documenttype: {doc_type}"}

        return {
            "document": template["title"],
            "organisatie": self.org_naam,
            "datum": self.datum,
            "wettelijke_basis": template["legal_basis"],
            "verplicht_wanneer": template["mandatory_when"],
            "secties": {
                f"sectie_{i + 1}": section
                for i, section in enumerate(template["sections"])
            },
            "status": "concept",
            "versie": "1.0",
            "goedkeuring": "In behandeling",
        }

    def generate_all(self) -> dict:
        """Genereer alle beschikbare documenten."""
        return {doc_type: self.generate(doc_type) for doc_type in DOCUMENT_TEMPLATES}

    def list_available(self) -> list[dict]:
        """Lijst alle beschikbare documenten."""
        return [
            {"id": doc_id, "title": t["title"], "legal_basis": t["legal_basis"]}
            for doc_id, t in DOCUMENT_TEMPLATES.items()
        ]
