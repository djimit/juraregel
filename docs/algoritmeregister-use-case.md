# Algoritmeregister Use Case — algoritmes.overheid.nl

**Als** algoritme-eigenaar bij een overheidsorganisatie **wil ik** automatisch valideren of mijn algoritme-registratie compleet en conform is **zodat** ik EU AI Act en AVG compliance aantoonbaar heb.

| Rol | Probleem | Oplossing |
|---|---|---|
| Algoritme-eigenaar | Onbekend of registratie compleet is | Rule API checkt 20 regels |
| Compliance officer | AI Act classificatie onduidelijk | Check risico verboden/hoog/beperkt/minimaal |
| Privacy officer | DPIA voor algoritme niet uitgevoerd | Check DPIA vereiste + AVG art. 35 |
| CISO | Security van algoritme niet beoordeeld | Check BIO2 + NCSC security maatregelen |

20 regels (registratie, classificatie, transparantie, oversight, DPIA, security, bias, rechten). Bron: algoritmes.overheid.nl + EU AI Act. Port 8508.
