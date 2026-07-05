# Traceability Matrix — Law to Code

**Als** architect **wil ik** de volledige keten van wet tot database constraint traceerbaar hebben **zodat** ik bij een wetwijziging precies weet welke code, tests en database constraints zijn geraakt.

| Rol | Probleem | Oplossing |
|---|---|---|
| Architect | Geen zicht op wet→code keten | GET /v1/traceability/matrix |
| Developer | Database constraints handmatig | DB constraint generator in matrix |
| PO | Wet wijziging impact onbekend | GET /v1/impact/analyze?source=Wgbz |
| Auditor | Evidence handmatig verzamelen | Traceability matrix als audit evidence |
| Scrum master | Compliance debt onzichtbaar | GET /v1/traceability/matrix → onuitgevoerde regels |

15 regels + traceability_engine.py. Port 8511. Custom endpoints:
- `GET /v1/traceability/matrix` — full matrix: wet → regel → API → DB → test → audit
- `GET /v1/impact/analyze?source=Wgbz` — regulatory impact analysis
