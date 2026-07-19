# Verplichte Documenten — JuraRegel Document Generator

## Overzicht

JuraRegel kan **23 verplichte documenten** genereren die wettelijk verplicht zijn
voor overheidsorganisaties in Nederland en de EU.

---

## PRIVACY & DATA PROTECTION (AVG/GDPR)

| # | Document | Wettelijke Basis | Verplicht Wanneer |
|---|----------|------------------|-------------------|
| 1 | **DPIA** (Data Protection Impact Assessment) | AVG Art. 35 | Hoog risico voor betrokkenen |
| 2 | **Privacyverklaring** | AVG Art. 13-14 | Altijd bij verzamelen PII |
| 3 | **Verwerkersovereenkomst (DPA)** | AVG Art. 28 | Bij gebruik van verwerkers |
| 4 | **ROVA** (Registratie VerwerkingsActiviteiten) | AVG Art. 30 | Altijd — elke organisatie |
| 5 | **Datalek Meldprocedure** | AVG Art. 33-34 | Altijd — procedure klaar hebben |
| 6 | **Toestemmingsregister** | AVG Art. 7 | Bij toestemming als rechtsgrond |

## INFORMATIEBEVEILIGING (ISO 27001 / BIO2)

| # | Document | Wettelijke Basis | Verplicht Wanneer |
|---|----------|------------------|-------------------|
| 7 | **Informatiebeveiligingsbeleid** | ISO 27001 5.2 + BIO2 A.5 | Altijd — management vaststelt |
| 8 | **Statement of Applicability (SoA)** | ISO 27001 6.1.3d | Altijd — ISO 27001 certificering |
| 9 | **Risicoanalyse** | ISO 27001 6.1.2 | Minimaal jaarlijks |
| 10 | **Risicobehandelingsplan** | ISO 27001 6.1.3 | Per geïdentificeerd risico |
| 11 | **Beleidsdoelstellingen IB** | ISO 27001 6.2 | Altijd — meetbare doelen |
| 12 | **Business Continuity Plan** | ISO 22301 8.4 | Voor kritieke processen |
| 13 | **Incident Response Plan** | NIS2 Art. 21 + ISO 27001 A.5.24 | Altijd |

## AI & ALGORITMES (EU AI Act)

| # | Document | Wettelijke Basis | Verplicht Wanneer |
|---|----------|------------------|-------------------|
| 14 | **Algoritmeregister Publicatie** | EU AI Act Art. 26 | Hoog-risico AI-systemen |
| 15 | **FRIA** (Fundamental Rights Impact Assessment) | EU AI Act Art. 27 | Hoog-risico AI-systemen |
| 16 | **Technische Documentatie AI** | EU AI Act Art. 11 + Bijlage IV | Hoog-risico AI-systemen |
| 17 | **Conformiteitsverklaring AI** | EU AI Act Art. 43 + 49 | Voor markttoegang |
| 18 | **AI-geletterdijkheidsbeleid** | EU AI Act Art. 4 | Altijd — alle werknemers |

## CYBERSECURITY (NIS2)

| # | Document | Wettelijke Basis | Verplicht Wanneer |
|---|----------|------------------|-------------------|
| 19 | **Cybersecurity Risicomanagement** | NIS2 Art. 21 | Essentiële/belangrijke diensten |
| 20 | **Incidentmeldprocedure** | NIS2 Art. 23 | 24h/72h/1mnd meldingstermijnen |
| 21 | **Supply Chain Security Beleid** | NIS2 Art. 21(2)(c) | Leveranciersmanagement |

## KWALITEIT & GOVERNANCE

| # | Document | Wettelijke Basis | Verplicht Wanneer |
|---|----------|------------------|-------------------|
| 22 | **Kwaliteitsbeleid** | ISO 9001 5.2 | ISO 9001 certificering |
| 23 | **Kwaliteitsdoelstellingen** | ISO 9001 6.2 | Meetbare doelen per proces |
| 24 | **IT Service Management Beleid** | ISO 20000-1 5.2 | ISO 20000 certificering |
| 25 | **IT Governance Framework** | COBIT 2019 EDM | Enterprise IT governance |

## ZORG (NEN 7510)

| # | Document | Wettelijke Basis | Verplicht Wanneer |
|---|----------|------------------|-------------------|
| 26 | **IB-beleid Zorg** | NEN 7510-1:2024 | Alle zorgaanbieders |
| 27 | **MedMij Compliantieverklaring** | NEN 7510-2 + MedMij | Uitwisseling patiëntgegevens |
| 28 | **BSN-k Verwerkingsprotocol** | NEN 7510-2 + BSN-k | Verwerking BSN in zorg |

## MILIEU & VEILIGHEID

| # | Document | Wettelijke Basis | Verplicht Wanneer |
|---|----------|------------------|-------------------|
| 29 | **Milieubeleid** | ISO 14001 5.2 | ISO 14001 certificering |
| 30 | **Arbobeleid** | ISO 45001 5.2 | ISO 45001 certificering |
| 31 | **RI&E** (Risico-Inventarisatie & Evaluatie) | ISO 45001 6.1.2 + Arbowet | Elke werkgever (Arbowet Art. 5) |

---

## Gebruik

```python
from docs.document_generator import DocumentGenerator

gen = DocumentGenerator("Gemeente Voorbeeld")

# Enkel document
dpia = gen.generate("dpia")

# Alle documenten
alle_documenten = gen.generate_all()

# Lijst beschikbare documenten
beschikbaar = gen.list_available()
```

## Generatie via API

```
POST /v1/documents/generate
{
  "organisatie": "Gemeente Voorbeeld",
  "document_type": "dpia"
}
```

## Wettelijke Referenties

- [AVG (GDPR)](https://eur-lex.europa.eu/eli/reg/2016/679)
- [EU AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689)
- [NIS2](https://eur-lex.europa.eu/eli/dir/2022/2555)
- [Arbowet](https://wetten.overheid.nl/BWBR0017416)
- [Autoriteit Persoonsgegevens — DPIA-lijst](https://www.autoriteitpersoonsgegevens.nl/documenten/lijst-verplichte-dpia)
- [KCBR — Model DPIA Rijksdienst](https://www.kcbr.nl/)
