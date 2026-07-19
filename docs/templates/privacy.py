"""Privacy Document Templates — AVG/GDPR verplichte documenten.

Elke template is een werkbaar document met:
- Wettelijke verwijzingen
- Instructies per sectie
- Voorbeeldinhoud
- Invulvelden tussen [haken]
"""

from datetime import date
from typing import Any


def dpia_template(org_naam: str, verwerking: str, **kwargs) -> dict:
    """DPIA — Data Protection Impact Assessment (AVG Art. 35).

    Verplicht wanneer verwerking "waarschijnlijk een hoog risico oplevert
    voor de rechten en vrijheden van natuurlijke personen".
    """
    return {
        "document": "Data Protection Impact Assessment (DPIA)",
        "wettelijke_basis": "AVG Art. 35",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "versie": "1.0",
        "inhoud": {
            "sectie_1": {
                "titel": "1. Beschrijving van de verwerking",
                "content": f"""
Doel van de verwerking:
[{verwerking}]

Aard van de verwerking:
[ ] Systematische en grootschalige evaluatie van persoonsgegevens
[ ] Verwerking op grote schaal van bijzondere categorieën gegevens
[ ] Systematische monitoring van publiek toegankelijke ruimten
[ ] Innovatief gebruik van nieuwe technologie
[ ] Andere: [beschrijf]

Categorieën betrokkenen:
[ ] Medewerkers
[ ] Burgers/klanten
[ ] Kinderen (< 16 jaar)
[ ] Kwetsbare groepen
[ ] Andere: [beschrijf]

Categorieën persoonsgegevens:
[ ] Naam, adres, gegevens (contact)
[ ] Identificatienummers (BSN, paspoort)
[ ] Financiële gegevens
[ ] Biometrische gegevens
[ ] Gezondheidsgegevens
[ ] Strafrechtelijke gegevens
[ ] Locatiegegevens
[ ] Online identificatoren
[ ] Bijzondere categorieën (Art. 9 AVG)

Rechtsgrond voor de verwerking:
[ ] Toestemming (Art. 6(1)(a))
[ ] Contract (Art. 6(1)(b))
[ ] Wettelijke verplichting (Art. 6(1)(c))
[ ] Vitale belangen (Art. 6(1)(d))
[ ] Openbaar belang (Art. 6(1)(e))
[ ] Gerechtvaardigd belang (Art. 6(1)(f))
""",
            },
            "sectie_2": {
                "titel": "2. Beoordeling van noodzaak en proportionaliteit",
                "content": """
Is de verwerking noodzakelijk voor het genoemde doel?
[ ] Ja — motiveer waarom
[ ] Nee — stop de verwerking

Kunnen hetzelfde doel met minder gegevens worden bereikt?
[ ] Ja — beschrijf alternatief
[ ] Nee — motiveer waarom niet

Worden gegevens geminimaliseerd?
[ ] Ja — alleen noodzakelijke gegevens worden verwerkt
[ ] Nee — te veel gegevens worden verwerkt

Is de bewaartermijn proportioneel?
[ ] Ja — maximaal [X] maanden/jaren
[ ] Nee — bewaartermijn te lang
""",
            },
            "sectie_3": {
                "titel": "3. Risico-inschatting voor betrokkenen",
                "content": """
Risico 1: Ongeautoriseerde toegang tot persoonsgegevens
- Waarschijnlijkheid: [Laag/Middel/Hoog]
- Impact: [Laag/Middel/Hoog]
- Risicoscore: [1-25]

Risico 2: Verlies van vertrouwelijkheid
- Waarschijnlijkheid: [Laag/Middel/Hoog]
- Impact: [Laag/Middel/Hoog]
- Risicoscore: [1-25]

Risico 3: Onjuiste verwerking of bewerking
- Waarschijnlijkheid: [Laag/Middel/Hoog]
- Impact: [Laag/Middel/Hoog]
- Risicoscore: [1-25]

Risico 4: Discriminatie of profiling
- Waarschijnlijkheid: [Laag/Middel/Hoog]
- Impact: [Laag/Middel/Hoog]
- Risicoscore: [1-25]

Risico 5: Identiteitsdiefstal of fraude
- Waarschijnlijkheid: [Laag/Middel/Hoog]
- Impact: [Laag/Middel/Hoog]
- Risicoscore: [1-25]
""",
            },
            "sectie_4": {
                "titel": "4. Maatregelen om risico's te mitigeren",
                "content": """
Technische maatregelen:
[ ] Encryptie van gegevens (at rest en in transit)
[ ] Pseudonimisering / anonimisering
[ ] Toegangscontrole (RBAC, MFA)
[ ] Logging en monitoring
[ ] Back-up en herstelprocedures
[ ] Netwerksegmentatie

Organisatorische maatregelen:
[ ] Privacy training voor medewerkers
[ ] Vertrouwelijkheidsverklaringen
[ ] Functionaris Gegevensbescherming (FG) aangesteld
[ ] Procedure voor uitoefening rechten betrokkenen
[ ] Periodieke privacy-audits
[ ] Datalek meldprocedure

Overige maatregelen:
[ ] Privacy by design toegepast
[ ] Verwerkersovereenkomsten afgesloten
[ ] DPIA herhaling gepland (frequentie: [X] maanden)
""",
            },
            "sectie_5": {
                "titel": "5. Conclusie en goedkeuring",
                "content": """
Conclusie:
[ ] De verwerking kan doorgaan met de genoemde maatregelen
[ ] De verwerking kan NIET doorgaan — te hoog resterend risico
[ ] Voorafgaand overleg met Autoriteit Persoonsgegevens verplicht

Goedkeuring:
Naam functionaris: [naam]
Handtekening: [tekening]
Datum: [datum]

Herziening: deze DPIA wordt jaarlijks herzien of bij wijziging van de verwerking.
""",
            },
        },
    }


def privacyverklaring_template(org_naam: str, **kwargs) -> dict:
    """Privacyverklaring — AVG Art. 13-14."""
    return {
        "document": "Privacyverklaring",
        "wettelijke_basis": "AVG Art. 13-14",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "sectie_1": {"titel": "1. Wie zijn wij?", "content": f"[{org_naam}] is verwerkingsverantwoordelijke voor de verwerking van persoonsgegevens zoals beschreven in deze privacyverklaring.\n\nContactgegevens:\nOrganisatie: [{org_naam}]\nAdres: [adres]\nPostcode/plaats: [postcode]\nTelefoon: [telefoon]\nEmail: [email]\nKVN: [KvK-nummer]"},
            "sectie_2": {"titel": "2. Welke gegevens verzamelen wij?", "content": "[Beschrijf per doel welke gegevens worden verzameld]\n\nVoorbeelden:\n- Naam, adres, gegevens (voor contact)\n- E-mailadres (voor communicatie)\n- Telefoonnummer (voor afspraken)\n- BSN (alleen wettelijk verplicht)\n- Financiële gegevens (voor betaling)\n- IP-adres (voor website-statistieken)"},
            "sectie_3": {"titel": "3. Waarom verzamelen wij gegevens?", "content": "[Geef per verwerkingsdoel de rechtsgrond]\n\nDoel 1: [bijv. Leveren dienstverlening]\n- Rechtsgrond: Contract / Wettelijke verplichting\n\nDoel 2: [bijv. Vraagbaarheid]\n- Rechtsgrond: Gerechtvaardigd belang\n\nDoel 3: [bijv. Toestemming marketing]\n- Rechtsgrond: Toestemming"},
            "sectie_4": {"titel": "4. Met wie delen wij gegevens?", "content": "[Noem ontvangers of categorieën ontvangers]\n\n- Verwerkers (IT-hosting, salarisadministratie)\n- Overheidsinstanties (wettelijke verplichting)\n- [Andere partijen]\n\nWorden gegevens doorgegeven aan landen buiten de EU?\n[ ] Nee\n[ ] Ja — met passende waarborgen (BCR, SCC, adequaat besluit)"},
            "sectie_5": {"titel": "5. Hoe lang bewaren wij gegevens?", "content": "[Geef bewaartermijnen per categorie]\n\n- Administratieve gegevens: 7 jaar (Belastingdienst)\n- Contractgegevens: 7 jaar na beëindiging\n- Toestemmingen: tot intrekking\n- Website-statistieken: 26 maanden"},
            "sectie_6": {"titel": "6. Uw rechten", "content": "U heeft de volgende rechten:\n\n- Recht op inzage (Art. 15)\n- Recht op rectificatie (Art. 16)\n- Recht op verwijdering (Art. 17)\n- Recht op beperking van verwerking (Art. 18)\n- Recht op gegevensoverdraagbaarheid (Art. 20)\n- Recht op bezwaar (Art. 21)\n\nU kunt een verzoek indienen via: [email/adres]\n\nU heeft ook het recht een klacht in te dienen bij:\nAutoriteit Persoonsgegevens\nhttps://www.autoriteitpersoonsgegevens.nl"},
            "sectie_7": {"titel": "7. Cookies en tracking", "content": "[Beschrijf welke cookies worden gebruikt]\n\n- Functionele cookies (noodzakelijk)\n- Analytische cookies (met toestemming)\n- Marketing cookies (met toestemming)\n\nBeheer uw voorkeuren via: [cookie-instellingen]"},
            "sectie_8": {"titel": "8. Wijzigingen", "content": f"Deze privacyverklaring kan worden gewijzigd. De meest recente versie is altijd beschikbaar op [website].\n\nLaatst bijgewerkt: {date.today().isoformat()}"},
        },
    }


def verwerkersovereenkomst_template(org_naam: str, verwerker: str, **kwargs) -> dict:
    """Verwerkersovereenkomst (DPA) — AVG Art. 28."""
    return {
        "document": "Verwerkersovereenkomst (DPA)",
        "wettelijke_basis": "AVG Art. 28",
        "organisatie": org_naam,
        "verwerker": verwerker,
        "datum": date.today().isoformat(),
        "inhoud": {
            "artikel_1": {"titel": "Artikel 1 — Definities", "content": "Verwerkingsverantwoordelijke: [{org_naam}]\nVerwerker: [{verwerker}]\nPersoonsgegevens: zoals gedefinieerd in AVG Art. 4(1)\nVerwerking: zoals gedefinieerd in AVG Art. 4(2)\nDatalek: inbreuk op beveiliging als bedoeld in AVG Art. 4(12)"},
            "artikel_2": {"titel": "Artikel 2 — Doel en reikwijdte", "content": f"De verwerker verwerkt persoonsgegevens in opdracht van de verwerkingsverantwoordelijke voor het volgende doel:\n\n[beschrijf doel, bijv.:\n- Hosting van IT-systemen\n- Salarisadministratie\n- Klantenservice-ondersteuning]\n\nCategorieën persoonsgegevens: [lijst]\nCategorieën betrokkenen: [lijst]"},
            "artikel_3": {"titel": "Artikel 3 — Verplichtingen van de verwerker", "content": "De verwerker zorgt voor:\n\na) Verwerking alleen volgens gedocumenteerde instructies van de verwerkingsverantwoordelijke\nb) Vertrouwelijkheid door medewerkers gegarandeerd\nc) Passende technische en organisatorische maatregelen (Art. 32)\n)d) Melding van datalek binnen 24 uur\n)e) Medewerking bij verzoeken van betrokkenen\n)f) Medewerking bij audits door de verwerkingsverantwoordelijke"},
            "artikel_4": {"titel": "Artikel 4 — Sub-processing", "content": "[ ] Sub-processing is NIET toegestaan\n[ ] Sub-processing is toegestaan met voorafgaande schriftelige toestemming\n\nGoedgekeurde sub-verwerkers:\n1. [naam] — [dienst] — [locatie]\n2. [naam] — [dienst] — [locatie]"},
            "artikel_5": {"titel": "Artikel 5 — Internationale doorgiften", "content": "Persoonsgegevens worden alleen verwerkt binnen de EU/EER, tenzij:\n\n[ ] Adequaat besluit Europese Commissie\n[ ] Standaardcontractclausules (SCC)\n[ ] Bindende bedrijfsregels (BCR)\n[ ] Gevalideerde code of conduct"},
            "artikel_6": {"titel": "Artikel 6 — Beveiligingsmaatregelen", "content": "De verwerker implementeert minimaal:\n\n- Encryptie (AES-256 at rest, TLS 1.3 in transit)\n- Toegangscontrole (MFA, RBAC)\n- Logging en monitoring (min. 12 maanden)\n- Back-up (dagelijks, getest per kwartaal)\n- Fysieke beveiligingsmaatregelen\n- Periodieke penetratietesten"},
            "artikel_7": {"titel": "Artikel 7 — Datalekmelding", "content": "De verwerker meldt een datalek binnen 24 uur na ontdekking bij:\n\nContact: [naam, email, telefoon]\n\nDe melding bevat:\n- Aard van het datalek\n- Categorieën en aantallen betrokkenen\n- Waarschijnlijke gevolgen\n- Voorgenomen maatregelen"},
            "artikel_8": {"titel": "Artikel 8 — Gegevens na beëindiging", "content": "Bij beëindiging van deze overeenkomst:\n\n[ ] Gegevens worden teruggeleverd aan verwerkingsverantwoordelijke\n[ ] Gegevens worden vernietigd (met certificaat van vernietiging)\n\nTermijn: binnen 30 dagen na beëindiging"},
            "artikel_9": {"titel": "Artikel 9 — Auditrechten", "content": "De verwerkingsverantwoordelijke heeft het recht om:\n\n- Audits uit te voeren (jaarlijks of bij vermoeden van overtreding)\n- Informatie op te vragen over naleving\n- Inspectie op locatie (onder redelijke voorwaarden)\n\nDe verwerker verleent volledige medewerking."},
            "artikel_10": {"titel": "Artikel 10 — Duur en beëindiging", "content": f"Deze overeenkomst geldt vanaf {date.today().isoformat()} en loopt door tot:\n\n[ ] Vaste einddatum: [datum]\n[ ] Tot beëindiging door een der partijen (opzegtermijn: 3 maanden)\n\nBij beëindiging blijven de vertrouwelijkheids- en beveiligingsverplichtingen van kracht."},
        },
    }


def rova_template(org_naam: str, **kwargs) -> dict:
    """Registratie van VerwerkingsActiviteiten (ROVA) — AVG Art. 30."""
    return {
        "document": "Registratie van VerwerkingsActiviteiten (ROVA)",
        "wettelijke_basis": "AVG Art. 30",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "instructie": "Vul voor elke verwerkingsactiviteit onderstaande tabel in. Minimaal vereist: doel, categorieën gegevens, categorieën betrokkenen, ontvangers, bewaartermijn, beveiliging.",
            "template_tabel": [
                {"verwerking": "[naam]", "doel": "[doel]", "rechtsgrond": "[Art. 6]", "gegevens_categorieen": "[lijst]", "betrokkenen_categorieen": "[lijst]", "ontvangers": "[lijst]", "bewaartermijn": "[termijn]", "beveiliging": "[maatregelen]", "doorgifte_buiten_eu": "[Ja/Nee + waarborgen]"},
            ],
            "voorbeeld_verwerkingen": [
                {"verwerking": "Personeelsadministratie", "doel": "Salaris, verlof, ziekte", "rechtsgrond": "Art. 6(1)(b)/(c)", "gegevens": "Naam, adres, salaris, BSN", "betrokkenen": "Medewerkers", "ontvangers": "Salarisadministratie, Belastingdienst", "bewaartermijn": "7 jaar", "beveiliging": "Encryptie, toegangscontrole, logging"},
                {"verwerking": "Klantenservice", "doel": "Afhandelen vragen en klachten", "rechtsgrond": "Art. 6(1)(b)", "gegevens": "Naam, contact, geschiedenis", "betrokkenen": "Burgers", "ontvangers": "Geen", "bewaartermijn": "2 jaar na afhandeling", "beveiliging": "Toegangscontrole, encryptie"},
                {"verwerking": "Website-statistieken", "doel": "Inzicht gebruik website", "rechtsgrond": "Art. 6(1)(f) / toestemming", "gegevens": "IP-adres, cookies", "betrokkenen": "Websitebezoekers", "ontvangers": "Google Analytics (SCC)", "bewaartermijn": "26 maanden", "beveiliging": "Pseudonimisering"},
            ],
        },
    }


def datalek_procedure_template(org_naam: str, **kwargs) -> dict:
    """Datalek Meldprocedure — AVG Art. 33-34."""
    return {
        "document": "Datalek Meldprocedure",
        "wettelijke_basis": "AVG Art. 33-34",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "stap_1": {"titel": "Stap 1 — Herkenning en eerste reactie (0-4 uur)", "content": "- Direct na ontdekking: informeer Functionaris Gegevensbescherming (FG)\n- FG contact: [naam, telefoon, email]\n- Neem direct maatregelen om verdere schade te beperken\n- Documenteer: tijdstip ontdekking, aard van het lek, geschat aantal betrokkenen"},
            "stap_2": {"titel": "Stap 2 — Beoordeling (4-24 uur)", "content": "- Beoordeel risico voor betrokkenen:\n  [ ] Laag risico (geen gevolgen te verwachten)\n  [ ] Middel risico (mogelijke gevolgen)\n  [ ] Hoog risico (ernstige gevolgen)\n\n- Bepaal of melding aan AP verplicht is (Art. 33)\n- Bepaal of melding aan betrokkenen verplicht is (Art. 34)"},
            "stap_3": {"titel": "Stap 3 — Melding aan Autoriteit Persoonsgegevens (binnen 72 uur)", "content": "Meld via: https://www.autoriteitpersoonsgegevens.nl/nl/melding-doen\n\nVerplichte informatie (Art. 33(3)):\na) Aard van het datalek\nb) Naam en contactgegevens FG\nc) Waarschijnlijke gevolgen\nd) Voorgenomen maatregelen\n\nTemplate melding:\n[Gebruik het meldingsformulier van de AP]"},
            "stap_4": {"titel": "Stap 4 — Melding aan betrokkenen (bij hoog risico)", "content": "Verplicht bij hoog risico (Art. 34):\n\n- Beschrijving van het datalek\n- Naam en contactgegevens FG\n- Waarschijnlijke gevolgen\n- Genomen/voorgenomen maatregelen\n- Aanbevelingen voor bescherming betrokkenen\n\nCommunicatiekanaal: [email, brief, website, persbericht]"},
            "stap_5": {"titel": "Stap 5 — Lessen en verbetering (na afhandeling)", "content": "- Voer root cause analysis\n- Documenteer alle stappen en tijdstippen\n- Pas beveiligingsmaatregelen aan\n- Herzie DPIA indien van toepassing\n- Plan oefening voor toekomstig datalek\n- Bewaar documentatie minimaal 5 jaar"},
            "contactlijst": {
                "FG": "[naam, telefoon 24/7, email"],
                "AP melding": "https://www.autoriteitpersoonsgegevens.nl/nl/melding-doen",
                "CSIRT": "[naam, telefoon, email]",
                "Juridisch": "[naam, telefoon, email"],
                "Communicatie": "[naam, telefoon, email]",
            },
        },
    }


def toestemmingsregister_template(org_naam: str, **kwargs) -> dict:
    """Toestemmingsregister — AVG Art. 7."""
    return {
        "document": "Toestemmingsregister",
        "wettelijke_basis": "AVG Art. 7",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "instructie": "Documenteer elke verwerking gebaseerd op toestemming. Bewijs van toestemming moet kunnen worden geleverd (Art. 7(1)).",
            "template": [
                {"betrokkene": "[naam/initiaal]", "doel": "[doel]", "gegevens": "[categorieen]", "verkregen_op": "[datum]", "methode": "[online/formulier/mondeling]", "intrekking_mogelijk": "[Ja/Nee]", "introkken_op": "[datum of leeg]"},
            ],
            "vereisten": [
                "Toestemming moet vrijelijk zijn gegeven (geen druk)",
                "Toestemming moet specifiek zijn (geen blanket consent)",
                "Toestemming moet geïnformeerd zijn (privacyverklaring vooraf)",
                "Intrekking moet zo makkelijk zijn als verkrijging",
                "Bewijs van toestemming moet worden bewaard",
                "Toestemming van kinderen (<16) vereist toestemming ouder/verzorger",
            ],
        },
    }
