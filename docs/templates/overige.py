"""Overige Document Templates — NIS2, Kwaliteit, Zorg, Milieu, Arbo."""

from datetime import date


def nis2_cybersecurity_template(org_naam: str, **kwargs) -> dict:
    """Cybersecurity Risicomanagement — NIS2 Art. 21."""
    return {
        "document": "Cybersecurity Risicomanagement Document",
        "wettelijke_basis": "NIS2 Art. 21",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "sectie_1": {
                "titel": "1. Risicomanagement",
                "content": "- Risicobeoordeling uitgevoerd (frequentie: [jaarlijks/kwartaal)]\n- Risicoregister bijgehouden\n- Acceptatiecriteria gedefinieerd\n- Management review gepland",
            },
            "sectie_2": {
                "titel": "2. Technische maatregelen",
                "content": "- Netwerksegmentatie\n- Encryptie (at rest + in transit)\n- MFA voor alle bevoegde toegang\n- Logging en monitoring (min. 12 maanden)\n- Back-up en herstel (getest per kwartaal)\n- Patching (binnen 14 dagen na kritieke CVE)",
            },
            "sectie_3": {
                "titel": "3. Incident management",
                "content": "- CSIRT of externe meldlijn\n- Melding binnen 24u (voorlopig), 72u (uitgebreid), 1mnd (eindrapport)\n- Playbooks beschikbaar\n- Oefening minimaal jaarlijks",
            },
            "sectie_4": {
                "titel": "4. Supply chain",
                "content": "- Leveranciers risico-beoordeling\n- Cybersecurity-eisen in contracten\n- Auditrecht op leveranciers\n- SBOM (Software Bill of Materials) bijgehouden",
            },
            "sectie_5": {
                "titel": "5. Business continuity",
                "content": "- BCP beschikbaar en getest\n- RTO/RPO gedefinieerd per kritiek proces\n- Alternatieve communicatiemiddelen\n- Crisisgroep samengesteld",
            },
            "boetes": "NIS2 voorziet in boetes tot €10M of 2% van de wereldwijde jaaromzet (voor essentiële diensten) of €7M of 1,4% (voor belangrijke diensten).",
        },
    }


def kwaliteitsbeleid_template(org_naam: str, **kwargs) -> dict:
    """Kwaliteitsbeleid — ISO 9001 5.2."""
    return {
        "document": "Kwaliteitsbeleid",
        "wettelijke_basis": "ISO 9001:2015 5.2",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "visie": "[beschrijf kwaliteitsvisie]",
            "missie": "[beschrijf kwaliteitsmissie]",
            "doelstellingen": [
                "Klanttevredenheid: [X]%",
                "Proces-efficiëntie: [X]%",
                "Leverbetrouwbaarheid: [X]%",
                "Continuïteitsverbetering: [X] verbeteringen per jaar",
            ],
            "principes": [
                "Klantgerichtheid",
                "Leiderschap",
                "Betrokkenheid van mensen",
                "Proceraadpak",
                "Verbetering",
                "Evidence-based besluitvorming",
                "Relatiemanagement",
            ],
        },
    }


def milieubeleid_template(org_naam: str, **kwargs) -> dict:
    """Milieubeleid — ISO 14001 5.2."""
    return {
        "document": "Milieubeleid",
        "wettelijke_basis": "ISO 14001:2015 5.2",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "verklaring": f"{org_naam} zet zich in voor de bescherming van het milieu en het voorkomen van vervuiling.",
            "doelen": [
                "Verminderen energie- en waterverbruik",
                "Minimaliseren afvalstroom",
                "Voldoen aan milieuwetgeving",
                "Continuïteitsverbetering milieuprestaties",
            ],
            "aspecten": [
                {
                    "aspect": "Energieverbruik",
                    "impact": "CO2-uitstoot",
                    "maatregel": "Energiezuinig, LED, groene stroom",
                },
                {
                    "aspect": "Afval",
                    "impact": "Stortkosten",
                    "maatregel": "Scheiding, recycling",
                },
                {
                    "aspect": "Water",
                    "impact": "Verbruik",
                    "maatregel": "Besparende maatregelen",
                },
                {
                    "aspect": "Mobiliteit",
                    "impact": "Uitstoot",
                    "maatregel": "Elektrisch, OV, carpool",
                },
            ],
        },
    }


def arbobeleid_template(org_naam: str, **kwargs) -> dict:
    """Arbobeleid — ISO 45001 5.2 + Arbowet."""
    return {
        "document": "Arbobeleid",
        "wettelijke_basis": "ISO 45001:2018 5.2 + Arbowet",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "verklaring": f"{org_naam} zet zich in voor veilige en gezonde werkomstandigheden.",
            "doelen": [
                "Nul ongevallen",
                "Verminderen verzuim",
                "Voldoen aan Arbowet en NEN 4400",
                "Continuïteitsverbetering veiligheid",
            ],
            "hazard_categorieen": [
                {"categorie": "Fysiek", "voorbeeld": "Geluid, trilling, temperatuur"},
                {"categorie": "Chemisch", "voorbeeld": "Stoffen, gassen, stof"},
                {
                    "categorie": "Biologisch",
                    "voorbeeld": "Bacteriën, virussen, schimmels",
                },
                {
                    "categorie": "Ergonomisch",
                    "voorbeeld": "Tillen, herhaalbelasting, beeldscherm",
                },
                {"categorie": "Psychosociaal", "voorbeeld": "Stress, pesten, werkdruk"},
            ],
            "ri_e_verplicht": "Risico-Inventarisatie & Evaluatie (RI&E) is wettelijk verplicht (Arbowet Art. 5). Template beschikbaar.",
        },
    }


def zorg_ib_beleid_template(org_naam: str, **kwargs) -> dict:
    """Informatiebeveiligingsbeleid Zorg — NEN 7510-1."""
    return {
        "document": "Informatiebeveiligingsbeleid Zorg",
        "wettelijke_basis": "NEN 7510-1:2024",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "sectie_1": {
                "titel": "1. Scope zorg",
                "content": "Dit beleid geldt voor alle patiëntgegevens, medische systemen en ICT-infrastructuur binnen de zorgorganisatie.",
            },
            "sectie_2": {
                "titel": "2. Patiëntgegevensbescherming",
                "content": "- Minimale noodzaak (need-to-know)\n- Toestemming voor verwerking\n- Recht op inzage en correctie\n- Meldplicht datalek",
            },
            "sectie_3": {
                "titel": "3. MedMij compliantie",
                "content": "- Aansluiting MedMij-infrastructuur\n- Toestemming patiënt voor uitwisseling\n- Logging van toegang\n- Bewaartermijnen patiëntgegevens",
            },
            "sectie_4": {
                "titel": "4. BSN-k verwerking",
                "content": "- Alleen voor doeleinden als bepaald bij wet\n- Separatie van BSN en medische gegevens\n- Encryptie en toegangscontrole\n- Verwerkingregister bijhouden",
            },
            "sectie_5": {
                "titel": "5. IGJ-inspectie",
                "content": "- Documentatie beschikbaar voor IGJ\n- Beleidsdocumenten actueel\n- Incidenten gemeld\n- Verbeteracties bijgehouden",
            },
        },
    }
