# Gegevensdelingsbeleid Use Case — JENV Model

**Als** data steward bij JenV **wil ik** automatisch valideren of een gegevensdeling conform het JENV gegevensdelingsbeleid is **zodat** ik doelbinding, BIV-classificatie en GLP compliance kan bewijzen.

| Rol | Probleem | Oplossing |
|---|---|---|
| Data steward | Gegevensdeling niet conform beleid | Rule API checkt 20 regels met bronverwijzingen |
| Privacy officer | Doelbinding niet aantoonbaar | GET /v1/gdb/check-doelbinding |
| Security officer | BIV-classificatie ontbreekt | GET /v1/gdb/biv-classify |

20 regels (anonimisering, BIV, bijzondere persoonsgegevens, doelbinding, GLP, GLS, datamaskering, crisis, audit). Bron: modellen.jenvgegevens.nl/gegevensdelingsbeleid v1.1.2. Port 8506.
