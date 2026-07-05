# DPIA Model Use Case — Rijksmodel DPIA

**Als** privacy officer **wil ik** automatisch bepalen of een DPIA vereist is en de DPIA conform het Rijksmodel is opgebouwd **zodat** ik AVG art. 35 compliance kan bewijzen.

| Rol | Probleem | Oplossing |
|---|---|---|
| Privacy officer | Onbekend of DPIA vereist is | GET /v1/dpia/vereist beslisboom |
| FG | DPIA niet conform Rijksmodel | Rule API checkt 30 regels |
| CISO | Risico's niet systematisch | Check risicoanalyse + maatregelen regels |

30 regels (vereiste, criteria, grondslagen, akkoord, advies FG, risico, maatregelen, bewaartermijn, doorgifte, algoritme, big data, cloud, profilering). Bron: modellen.jenvgegevens.nl/dpia v1.0.0, Rijksmodel DPIA v3.0. Port 8507.
