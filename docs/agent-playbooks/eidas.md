# Agent Playbook: eIDAS 2.0 Compliance

## Wanneer
Gebruik dit playbook om te beoordelen of een organisatie voldoet aan eIDAS 2.0 verplichtingen, met name de EUDI-wallet deadline van december 2026.

## Benodigde informatie
- Organisatie type (overheid, semi-overheid, private sector)
- Huidige authenticatie-infrastructuur (DigiD, eHerkenning, PKIoverheid)
- EUDI-wallet implementatie status (niet gestart / in ontwikkeling / piloot / productie)
- Vertrouwensdiensten in gebruik (handtekening, zegel, tijdsstempel, ERD, website-auth)
- Grensoverschrijdende dienstverlening (ja/nee)
- TSP-kwalificatie status

## Stappen

### 1. Identificeer applicabele regels
```
Gebruik juraregel.get_rules("eidas") om alle 32 regels op te halen
Filter op organisatietype:
- Overheid: alle 32 regels
- Private sector: EID-028 (deadline 2027-12) + trust service regels
- Semi-overheid: afhankelijk van dienstverlening
```

### 2. Check wallet status
```
Belangrijkste check: walletStatus
- "niet_gestart" → CRITICAL (EID-011)
- "in_ontwikkeling" → actie vereist (EID-010)
- "piloot" → tijdelijk compliant (EID-009)
- "productie" → compliant (EID-008)
```

### 3. Check vertrouwensdiensten
```
Per vertrouwensdienst:
- elektronisch_handtekening → assuranceLevel moet "hoog" zijn
- elektronisch_zegel → PKIoverheid certificaat vereist
- elektronisch_tijdsstempel → TSP met EN 2100-1
- elektronisch_geregistreerde_zending → TSP met ERD-certificering
- website_authenticatie → QWAC + EV SSL
- attestatie_attributen → nieuw in eIDAS 2.0 (QAA)
- elektronisch_archief → nieuw in eIDAS 2.0
```

### 4. Check grensoverschrijdende compliance
```
Als crossBorder == "ja":
- eIDAS Node configuratie vereist
- Trust List synchronisatie met EUTL
- Wallet interoperabiliteit (Art. 6j)
- Niet-discriminatie beleid (Art. 4(4))
```

### 5. Genereer rapport
```
Gebruik GET /v1/eidas/rapport/{orgId} voor compliance percentage
Gebruik GET /v1/eidas/deadlines} voor deadline overzicht
Gebruik GET /v1/eidas/wallet-status} voor wallet countdown
```

## Human Escalation
- **CRITICAL** (EID-011): Wallet niet gestart → escalate naar CIO + BZK
- **HIGH** (EID-008/017): Wallet niet in productie → escalate naar enterprise architect
- **MEDIUM** (EID-006/007): Nieuwe vertrouwensdiensten → escalate naar security team
- **Regelgeving wijziging**: eIDAS implementing acts → escalate naar juridisch

## Voorbeeld

**User:** "We zijn een gemeente met 50.000 inwoners. We gebruiken DigiD voor authentificatie maar hebben nog nooit van de EUDI-wallet gehoord. Zijn we compliant?"

**Agent:**
1. `juraregel.get_rules("eidas")` → 32 regels
2. Wallet status = "niet_gestart" → **EID-011: CRITICAL**
3. DigiD is nationaal eID maar nog niet wallet-geïntegreerd → **EID-024: actie vereist**
4. Als gemeente moet je wallets accepteren → **EID-018: verplichte acceptatie**
5. Rapport: ~30% compliant (alleen trust services die via PKIoverheid lopen)

**Advies:**
- Start direct met wallet-implementatie (deadline 2026-12-01)
- Neem contact op met VNG voor gemeentelijke wallet-roadmap
- Plan DigiD-wallet integratie (EID-024)
- Budget voor conformiteitsbeoordeling (EID-030)

## NEDERUS Koppeling

| NEDERUS Control | eIDAS Regels | Relevantie |
|---|---|---|
| NED-01 AI Impact Assessment | EID-006, EID-013 | Wallet impact + PID dataset |
| NED-03 Human Oversight | EID-012, EID-023 | Sole control + eHerkenning |
| NED-04 Transparency | EID-015, EID-022 | RDI certificering + attributen |
| NED-05 Incident Response | EID-011, EID-017 | Wallet deadline + crossborder |
| NED-06 Secure Development | EID-029, EID-030 | Security levels + certificering |
| NED-08 AI Liability | EID-031 | DPIA verplicht |

## Bronnen
- [eIDAS Verordening (EU) 2014/910](https://eur-lex.europa.eu/eli/reg/2014/910)
- [eIDAS 2.0 Verordening (EU) 2024/1183](https://eur-lex.europa.eu/eli/reg/2024/1183)
- [EUDI Wallet — developer.overheid.nl](https://developer.overheid.nl/kennisbank/security/wetgeving-en-beleid/eudi-wallet)
- [RvIG — PID Provider](https://www.rvig.nl/)
- [Logius — eIDAS](https://www.logius.nl/onze-dienstverlening/toegang/eidas)
