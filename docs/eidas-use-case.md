# eIDAS 2.0 Use Case — European Digital Identity Framework

## User Story

**Als** CIO, security engineer of enterprise architect bij een overheidsorganisatie **wil ik** automatisch valideren of mijn organisatie voldoet aan eIDAS 1.0 + 2.0 verplichtingen **zodat** ik niet handmatig 32 regels hoef te checken, de EUDI-wallet deadline van december 2026 gehaald wordt, en grensoverschrijdende erkenning gegarandeerd is.

## Probleemstelling

De Nederlandse overheid staat voor een **vierdubbel eIDAS-probleem**:

1. **eIDAS 1.0** (2014) — Vertrouwensdiensten (handtekeningen, zegels, tijdsstempel, ERD, website-auth) zijn al verplicht maar worden nog niet systematisch gecontroleerd
2. **eIDAS 2.0** (2024) — De EUDI-wallet is **verplicht** met deadline **1 december 2026**. NL wallet waarschijnlijk pas 2027 klaar.
3. **Grensoverschrijdende erkenning** — Wederzijdse acceptatie van eID's én wallets vereist actieve eIDAS Node configuratie
4. **Nieuwe vertrouwensdiensten** — Qualified Attestation of Attributes (QAA) en Electronic Archival zijn nieuw in eIDAS 2.0

### Actuele situatie (juli 2026)

| Aspect | Status |
|--------|--------|
| EUDI-wallet productie | ❌ Niet beschikbaar in NL |
| NL wallet (op basis DigiD) | 🔴 Verwacht 2027-Q1 |
| Deadline | 2026-12-01 |
| Dagen resterend | ~150 |
| Risico | **CRITICAL** |

> "Eind 2026 moet je voldoen aan de eIDAS-wetgeving, maar Nederland is daar nog niet klaar voor: Er is nog geen Nederlandse nationale wallet beschikbaar, en deze zal waarschijnlijk pas in 2027 klaar zijn." — CARE Internet Services, maart 2026

| Rol | Probleem | Oplossing |
|-----|----------|-----------|
| CIO | EUDI-wallet deadline nadert, onduidelijk waar te starten | Compliance dashboard met deadline-tracking |
| Security engineer | TSP-kwalificatie onduidelijk, certificaten afgelopen | Automatische validatie van TSP-status en certificaatgeldigheid |
| Enterprise architect | eHerkenning → wallet migratie complex | Stappenplan + compatibiliteitschecks |
| Integratie architect | DigiD + wallet integratie onbekend | Architectuur-documentatie + test-scenario's |
| Jurist | Grensoverschrijdende erkenning juridisch complex | Per-land compliance matrix |
| Privacy officer | PID-provider verplichtingen, DPIA | RvIG-integratie + DPIA-template |

## De 32 eIDAS Regels

### Vertrouwensdiensten eIDAS 1.0 (5 regels)

| ID | Regel | Artikel | Deadline | Categorie |
|----|-------|---------|----------|-----------|
| EID-001 | Kwalificeerde elektronische handtekening | Art. 25(1) | 2026-01-01 | eidas_handtekening |
| EID-002 | Kwalificeerde elektronische zegel | Art. 35(2) | 2026-01-01 | eidas_zegel |
| EID-003 | Kwalificeerde elektronische tijdsstempel | Art. 42 | 2026-01-01 | eidas_tijdsstempel |
| EID-004 | Kwalificeerde ERD | Art. 43 | 2026-01-01 | eidas_erd |
| EID-005 | Kwalificeerde website-authenticatie | Art. 45 | 2026-01-01 | eidas_webauth |

### Nieuwe Vertrouwensdiensten eIDAS 2.0 (2 regels)

| ID | Regel | Artikel | Deadline | Categorie |
|----|-------|---------|----------|-----------|
| EID-006 | Qualified Attestation of Attributes (QAA) | Art. 3(16a) | 2026-12-01 | eidas_qaa |
| EID-007 | Electronic Archival | Art. 3(16b) | 2026-12-01 | eidas_archief |

### EUDI-wallet (7 regels)

| ID | Regel | Artikel | Deadline | Urgentie |
|----|-------|---------|----------|----------|
| EID-008 | Wallet productie | Art. 6a | 2026-12-01 | 🔴 |
| EID-009 | Wallet pilootfase | Art. 6a | 2026-12-01 | 🟡 |
| EID-010 | Wallet in ontwikkeling | Art. 6a | 2026-12-01 | 🟡 |
| EID-011 | Wallet niet gestart | Art. 6a | 2026-12-01 | 🔴 CRITICAL |
| EID-012 | Wallet sole control design | Art. 6a(3) | 2026-12-01 | 🔴 |
| EID-013 | PID minimum dataset | Art. 6a(4) | 2026-12-01 | 🔴 |
| EID-029 | Security levels (LoA) | Art. 6a(5) | 2026-12-01 | 🟡 |

### PID + Certificering (3 regels)

| ID | Regel | Artikel | Deadline |
|----|-------|---------|----------|
| EID-014 | RvIG als PID-provider | NL impl. | 2026-12-01 |
| EID-015 | RDI certificering | Art. 6d | 2026-12-01 |
| EID-030 | Conformiteitsbeoordeling | Art. 6d | 2026-12-01 |

### Grensoverschrijdende Erkenning (3 regels)

| ID | Regel | Artikel | Deadline |
|----|-------|---------|----------|
| EID-016 | Wederzijdse erkenning | Art. 13+25 | 2024-09-29 |
| EID-017 | Wallet interoperabiliteit | Art. 6j | 2026-12-01 |
| EID-018 | Verplichte overheidsacceptatie | Art. 6a(6) | 2026-12-01 |

### TSP-kwalificatie (2 regels)

| ID | Regel | Artikel | Deadline |
|----|-------|---------|----------|
| EID-019 | Kwalificeerde TSP certificering | Art. 21 | 2026-01-01 |
| EID-020 | Niet-gekwalificeerde → upgrade | Art. 25 | 2026-01-01 |

### Niet-discriminatie (1 regel)

| ID | Regel | Artikel | Deadline |
|----|-------|---------|----------|
| EID-021 | Gelijke toegang | Art. 4(4) | 2024-09-29 |

### Attribuut-uitwisseling (3 regels)

| ID | Regel | Artikel | Deadline |
|----|-------|---------|----------|
| EID-022 | Attributen via wallet | Art. 12d | 2026-12-01 |
| EID-023 | eHerkenning-wallet koppeling | Art. 6l | 2026-12-01 |
| EID-024 | DigiD-wallet integratie | Art. 6l | 2026-12-01 |

### Trust Lists (2 regels)

| ID | Regel | Artikel | Deadline |
|----|-------|---------|----------|
| EID-025 | EU Trusted List | Art. 22 | 2024-09-29 |
| EID-026 | Nationale trustlist sync | Art. 6p | 2026-12-01 |

### Kwaliteitskeurmerken (2 regels)

| ID | Regel | Artikel | Deadline |
|----|-------|---------|----------|
| EID-027 | Wallet keurmerk | Art. 6e | 2027-12-01 |
| EID-028 | Private sector acceptatie | Art. 6a(6) | 2027-12-01 |

### Privacy + Implementing (2 regels)

| ID | Regel | Artikel | Deadline |
|----|-------|---------|----------|
| EID-031 | DPIA verplicht | AVG Art. 35 | 2026-12-01 |
| EID-032 | Implementing Acts | Reg. 2024/2977 | 2026-12-01 |

## API Endpoints

| Endpoint | Functie | Voorbeeld |
|----------|---------|-----------|
| `POST /v1/eidas/calculate` | Compliance check per vertrouwensdienst | `{"vertrouwensdienst": "eudiwallet", "walletStatus": "piloot"}` |
| `GET /v1/eidas/wallet-status` | Wallet countdown + NL readiness | — |
| `GET /v1/eidas/deadlines` | Deadline overzicht met urgentie | — |
| `GET /v1/eidas/rapport/{orgId}` | Compliance rapport per organisatie | `/v1/eidas/rapport/gemeente-amsterdam` |
| `GET /v1/eidas/categorieen` | Alle 21 categorieën met regels | — |
| `GET /v1/eidas/standaarden` | Lijst alle 32 regels | — |
| `GET /v1/health` | Healthcheck | — |

## Voorbeelden

### Wallet compliance check

```bash
curl -X POST http://127.0.0.1:8523/v1/eidas/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "vertrouwensdienst": "eudiwallet",
    "walletStatus": "niet_gestart",
    "crossBorder": "ja"
  }'
```

Response:
```json
{
  "compliant": false,
  "category": "eidas_wallet",
  "deadline": "2026-12-01",
  "actionRequired": "START DIRECT — deadline december 2026",
  "risk": "CRITICAL"
}
```

### Wallet status met countdown

```bash
curl http://127.0.0.1:8523/v1/eidas/wallet-status
```

Response:
```json
{
  "deadline": "2026-12-01",
  "days_remaining": 150,
  "status": "critical",
  "nl_readiness": {
    "wallet_available": false,
    "expected_date": "2027-Q1",
    "pid_provider": "RvIG",
    "certification_authority": "RDI",
    "risk": "HIGH — NL wallet verwacht na EU deadline"
  }
}
```

### Deadline overzicht

```bash
curl http://127.0.0.1:8523/v1/eidas/deadlines
```

Response:
```json
{
  "deadlines": [
    {"date": "2024-09-29", "status": "passed", "urgency": "info"},
    {"date": "2026-01-01", "status": "pending", "urgency": "warning"},
    {"date": "2026-12-01", "status": "pending", "urgency": "critical"},
    {"date": "2027-12-01", "status": "future", "urgency": "info"}
  ]
}
```

## MCP Server Integratie

De eIDAS use case is beschikbaar via de JuraRegel MCP server:

| MCP Tool | Functie |
|----------|---------|
| `juraregel.get_rules("eidas")` | Haal alle 32 eIDAS regels op |
| `juraregel.calculate("eidas", input)` | Check compliance |
| `juraregel.check_compliance("eidas")` | Rapporteer dekkingsgraad |
| `juraregel.search_rules("wallet", "eidas")` | Zoek wallet-specifieke regels |

## Relatie tot NEDERUS

eIDAS raakt meerdere NEDERUS controls:

| NEDERUS Control | eIDAS Koppeling | Regels |
|-----------------|-----------------|--------|
| NED-01 AI Impact Assessment | Wallet impact + PID dataset | EID-006, EID-013 |
| NED-03 Human Oversight | Sole control + eHerkenning | EID-012, EID-023 |
| NED-04 Transparency | RDI certificering + attributen | EID-015, EID-022 |
| NED-05 Incident Response | Wallet deadline + crossborder | EID-011, EID-017 |
| NED-06 Secure Development | Security levels + certificering | EID-029, EID-030 |
| NED-08 AI Liability | DPIA verplicht | EID-031 |

## Relatie tot Andere Use Cases

| Use Case | Koppeling |
|----------|-----------|
| Forum Standaardisatie | eIDAS als verplichte standaard (EIDAS SAML, iGOV) |
| Overheidsstandaarden | eIDAS SAML in authenticatie-categorie |
| BIO2 | PKIoverheid certificaten voor vertrouwensdiensten |
| NORA | Identiteit + toegang principe |
| AVG/GDPR | DPIA voor wallet, PID data protection |

## Nederlandse Uitvoering

| Rol | Organisatie | Verantwoordelijkheid |
|-----|-------------|---------------------|
| PID Provider | RvIG | Person Identification Data |
| Certificering | RDI | Wallet conformiteitsbeoordeling |
| Toezicht | OPTA/ACM | TSP-kwalificatie |
| Infrastructuur | Logius | DigiD, eHerkenning, eIDAS Node |
| Beleid | BZK | eIDAS 2.0 implementatie |

## Bronverwijzingen

- [eIDAS Verordening (EU) 2014/910](https://eur-lex.europa.eu/eli/reg/2014/910)
- [eIDAS 2.0 Verordening (EU) 2024/1183](https://eur-lex.europa.eu/eli/reg/2024/1183)
- [Implementing Regulation (EU) 2024/2977](https://eur-lex.europa.eu/eli/reg_impl/2024/2977)
- [EU Trusted List (EUTL)](https://webgate.ec.europa.eu/tl-browser/)
- [EUDI Wallet — developer.overheid.nl](https://developer.overheid.nl/kennisbank/security/wetgeving-en-beleid/eudi-wallet)
- [RvIG — PID Provider](https://www.rvig.nl/)
- [RDI — Certificering](https://www.rijksoverheid.nl/ministeries/ministerie-van-binnenlandse-zaken-en-koninkrijksrelaties/organisaties/rijksinspectie-digitale-infrastructuur)
- [Logius — eIDAS](https://www.logius.nl/onze-dienstverlening/toegang/eidas)
- [VNG — eIDAS implementatie](https://vng.nl/artikelen/implementatie-eidas)
- [Forum Standaardisatie — eIDAS](https://www.forumstandaardisatie.nl/open-standaarden/identiteit)
- [Wet elektronische handtekeningen (Weh)](https://wetten.overheid.nl/BWBR0025165/)
