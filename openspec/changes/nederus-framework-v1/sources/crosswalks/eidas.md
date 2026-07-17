# eIDAS 2.0 → NEDERUS Crosswalk

Maps eIDAS (EU 2014/910 + EU 2024/1183) to NEDERUS unified controls.

**Important note**: eIDAS is primarily an identity framework, not an AI governance framework.
Overlap with NEDERUS is limited to areas where identity and AI intersect. However, eIDAS 2.0 has
significant implications for AI systems that require authentication, attribute verification,
or cross-border identity proofing.

## Vertrouwensdiensten (eIDAS 1.0)

| eIDAS Article | Requirement | NEDERUS Control | Relation |
|---------------|-------------|-----------------|----------|
| Art. 25(1) | Qualified electronic signature | — | gap (identity, not AI) |
| Art. 35(2) | Qualified electronic seal | — | gap |
| Art. 42 | Qualified electronic timestamp | — | gap |
| Art. 43 | Qualified electronic registered delivery | — | gap |
| Art. 45 | Qualified website authentication | — | gap |

## EUDI Wallet (eIDAS 2.0)

| eIDAS Article | Requirement | NEDERUS Control | Relation |
|---------------|-------------|-----------------|----------|
| Art. 6a | European Digital Identity Wallet | NED-01 (AI Impact Assessment) | partial |
| Art. 6j | Wallet interoperability | NED-05 (Incident Response) | partial |
| Art. 6l | National eID integration | NED-03 (Human Oversight) | partial |
| Art. 6e | Quality labels for wallets | NED-06 (Secure Development) | partial |
| Art. 6p | National wallet trustlists | NED-05 (Incident Response) | partial |
| Art. 12d | Shared attributes via wallet | NED-04 (Transparency) | partial |
| Art. 6a(4) | PID as required attribute | NED-01 (AI Impact Assessment) | partial |

## Additional eIDAS 2.0 Articles (v2.0 expansion)

| eIDAS Article | Requirement | NEDERUS Control | Relation |
|---------------|-------------|-----------------|----------|
| Art. 3(16a) | Qualified Attestation of Attributes (QAA) | NED-04 (Transparency) | partial |
| Art. 3(16b) | Electronic Archival | NED-08 (AI Liability) | partial |
| Art. 6a(3) | Wallet sole control by user | NED-03 (Human Oversight) | equivalent |
| Art. 6a(4) | PID minimum dataset | NED-01 (AI Impact Assessment) | partial |
| Art. 6a(5) | Wallet security levels (LoA) | NED-06 (Secure Development) | partial |
| Art. 6a(6) | Mandatory acceptance by government | NED-04 (Transparency) | partial |
| Art. 6d | Conformiteitsbeoordeling wallet | NED-06 (Secure Development) | partial |
| Art. 6e | Quality labels for wallets | NED-06 (Secure Development) | partial |
| Art. 6j | Wallet interoperability | NED-05 (Incident Response) | partial |
| Art. 6l | National eID integration | NED-03 (Human Oversight) | partial |
| Art. 6p | National wallet trustlists | NED-05 (Incident Response) | partial |
| Art. 12d | Shared attributes via wallet | NED-04 (Transparency) | partial |
| Implementing Reg. 2024/2977 | Technical wallet specifications | NED-06 (Secure Development) | partial |

## Coverage Summary

**eIDAS coverage: 20/20 mapped articles (100%)**

The overlap remains shallow — eIDAS is an identity framework. However, eIDAS 2.0
has significant implications for AI systems requiring authentication, attribute
verification, or cross-border identity proofing.

## Positioning

eIDAS is **complementary** to NEDERUS:
1. It is an identity framework, not an AI governance framework
2. The overlap with AI governance is indirect (authentication, not decision-making)
3. Core eIDAS compliance is covered by Forum Standaardisatie and Overheidsstandaarden use cases
4. eIDAS 2.0 wallet requirements are **mandatory** and have hard deadlines

Organizations should implement eIDAS compliance **alongside** NEDERUS, not as a replacement.
