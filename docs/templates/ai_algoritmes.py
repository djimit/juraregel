"""AI & Algoritmes Document Templates — EU AI Act."""

from datetime import date


def fria_template(org_naam: str, ai_systeem: str, **kwargs) -> dict:
    """FRIA — Fundamental Rights Impact Assessment (EU AI Act Art. 27)."""
    return {
        "document": "Fundamental Rights Impact Assessment (FRIA)",
        "wettelijke_basis": "EU AI Act Art. 27",
        "organisatie": org_naam,
        "ai_systeem": ai_systeem,
        "datum": date.today().isoformat(),
        "inhoud": {
            "sectie_1": {
                "titel": "1. Beschrijving AI-systeem",
                "content": f"""
Naam: [{ai_systeem}]
Versie: [versie]
Doel: [beschrijf het primaire doel]
Functie: [classificatie, voorspelling, besluitondersteuning, etc.]
Technologie: [machine learning, LLM, regelgebaseerd, etc.]
Gebruikers: [wie gebruikt het systeem?]
Betrokkenen: [wie wordt erdoor beïnvloed?]""",
            },
            "sectie_2": {
                "titel": "2. Grondrechtenanalyse",
                "content": """
Beoordeel de impact op elk van de volgende grondrechten:

[ ] Recht op menselige waardigheid (Handvest Art. 1)
[ ] Recht op vrijheid (Handvest Art. 6)
[ ] Recht op privacy (Handvest Art. 7)
[ ] Bescherming persoonsgegevens (Handvest Art. 8)
[ ] Non-discriminatie (Handvest Art. 21)
[ ] Gelijkheid vrouwen en mannen (Handvest Art. 23)
[ ] Rechten van het kind (Handvest Art. 24)
[ ] Integratie personen met een handicap (Handvest Art. 26)
[ ] Toegang tot het recht (Handvest Art. 47)

Per relevant grondrecht:
- Is er een inbreuk? [Ja/Nee]
- Zo ja: is deze gerechtvaardigd? [Ja/Nee + motiveer]
- Welke maatregelen mitigeren de inbreuk?""",
            },
            "sectie_3": {
                "titel": "3. Kwetsbare groepen",
                "content": """
Specifieke impact op kwetsbare groepen:

[ ] Kinderen (< 16 jaar)
[ ] Ouderen (> 65 jaar)
[ ] Personen met een handicap
[ ] Minderheden
[ ] Werkzoekenden
[ ] Burgers met beperkte digitale vaardigheden

Maatregelen voor bescherming:
[beschrijf]""",
            },
            "sectie_4": {
                "titel": "4. Menselijke tussenkomst",
                "content": """
Is menselijke tussenkomst verplicht? [Ja/Nee]
Hoe is menselijke tussenkomst geïmplementeerd?
[ ] Review van AI-output door mens
[ ] Mogelijkheid om AI-besluit te overrulen
[ ] Stopknop / kill switch
[ ] Andere: [beschrijf]""",
            },
            "sectie_5": {
                "titel": "5. Proportionaliteit",
                "content": """
Is de inbreuk op grondrechten proportioneel?
[ ] Ja — het doel weegt zwaarder dan de inbreuk
[ ] Nee — stop het gebruik van dit AI-systeem

Alternatieven overwogen:
[beschrijf alternatieven die minder ingrijpend zijn]""",
            },
            "goedkeuring": {
                "titel": "Goedkeuring",
                "content": "Naam: [naam]\nFunctie: [functie]\nDatum: [datum]\nHandtekening: [tekening]",
            },
        },
    }


def algoritmeregister_template(org_naam: str, **kwargs) -> dict:
    """Algoritmeregister Publicatie — EU AI Act Art. 26."""
    return {
        "document": "Algoritmeregister Publicatie",
        "wettelijke_basis": "EU AI Act Art. 26",
        "organisatie": org_naam,
        "datum": date.today().isoformat(),
        "inhoud": {
            "template": [
                {"veld": "Naam algoritme", "waarde": "[naam]"},
                {"veld": "Versie", "waarde": "[versie]"},
                {"veld": "Doel en werking", "waarde": "[beschrijving]"},
                {
                    "veld": "Risicoclassificatie (EU AI Act)",
                    "waarde": "[Verboden / Hoog-risico / Beperkt risico / Minimaal risico]",
                },
                {
                    "veld": "Verwerkte gegevens",
                    "waarde": "[categorieën persoonsgegevens]",
                },
                {"veld": "Rechtsgrond verwerking", "waarde": "[AVG Art. 6]"},
                {"veld": "Menselijke tussenkomst", "waarde": "[Ja/Nee + beschrijving]"},
                {
                    "veld": "Prestatie-indicatoren",
                    "waarde": "[nauwkeurigheid, recall, F1]",
                },
                {"veld": "Bias-monitoring", "waarde": "[procedure]"},
                {"veld": "FRIA uitgevoerd", "waarde": "[Ja/Nee + datum]"},
                {"veld": "Conformiteitsbeoordeling", "waarde": "[Ja/Nee + datum]"},
                {"veld": "Goedkeuringsdatum", "waarde": "[datum]"},
                {"veld": "Contactpersoon", "waarde": "[naam, email]"},
            ],
        },
    }


def technische_documentatie_ai_template(
    org_naam: str, ai_systeem: str, **kwargs
) -> dict:
    """Technische Documentatie AI — EU AI Act Art. 11 + Bijlage IV."""
    return {
        "document": "Technische Documentatie AI-systeem",
        "wettelijke_basis": "EU AI Act Art. 11 + Bijlage IV",
        "organisatie": org_naam,
        "ai_systeem": ai_systeem,
        "datum": date.today().isoformat(),
        "inhoud": {
            "bijlage_iv": [
                {
                    "punt": "1",
                    "beschrijving": "Algemene beschrijving van het AI-systeem, inclusief beoogd doel, beperkingen en prestaties",
                },
                {
                    "punt": "2",
                    "beschrijving": "Beschrijving van de architectuur (algoritmen, data, modellen, training)",
                },
                {
                    "punt": "3",
                    "beschrijving": "Beschrijving van de verwerkte gegevens (bronnen, categorieën, kwaliteit)",
                },
                {
                    "punt": "4",
                    "beschrijving": "Beschrijving van menselijke tussenkomst (oversight, override)",
                },
                {
                    "punt": "5",
                    "beschrijving": "Nauwkeurigheid, robuustheid en cybersecurity",
                },
                {
                    "punt": "6",
                    "beschrijving": "Beoordeling van bias en non-discriminatie",
                },
                {
                    "punt": "7",
                    "beschrijving": "Risico's voor de gezondheid, veiligheid en grondrechten",
                },
                {"punt": "8", "beschrijving": "Gebruiksaanwijzing en beperkingen"},
                {"punt": "9", "beschrijving": "Lifecycle management en monitoring"},
                {
                    "punt": "10",
                    "beschrijving": "Conformiteitsinformatie en CE-markering",
                },
            ],
        },
    }
