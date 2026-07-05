# API Registratie Use Case — developer.overheid.nl

**Als** API developer bij de overheid **wil ik** in één check weten of mijn API klaar is voor publicatie op developer.overheid.nl **zodat** ik niet drie losse compliance checks hoef te doen.

| Rol | Probleem | Oplossing |
|---|---|---|
| API developer | Registratie + API Design Rules + OSS zijn losse stappen | Eén Rule API checkt alle 18 regels |
| Solution architect | API niet conform NORA | Check NORA API standaardisatie |
| Security engineer | Security scan ontbreekt in CI | Check SAST/dependency check in pipeline |
| DevOps engineer | Monitoring niet actief | Check rate limiting + monitoring + alerting |

18 regels (registratie, OpenAPI, API Design Rules, OAuth, OSS, CI/CD, security, toegankelijkheid, monitoring). Bron: developer.overheid.nl, Logius, Forum Standaardisatie, NCSC. Port 8510.
