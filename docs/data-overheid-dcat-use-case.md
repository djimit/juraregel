# DCAT-AP-NL Use Case — data.overheid.nl

**Als** data steward **wil ik** automatisch valideren of mijn dataset conform DCAT-AP-NL is **zodat** publicatie op data.overheid.nl foutloos verloopt.

| Rol | Probleem | Oplossing |
|---|---|---|
| Data steward | DCAT metadata handmatig checken | Rule API checkt 15 verplichte/aanbevolen velden |
| Open data coördinator | Licentie niet conform beleid | Check CC0/CC-BY compliance |
| Developer | Dataservice zonder OpenAPI | Check endpoint URL + OpenAPI spec |

15 regels (titel, beschrijving, uitgever, licentie, distributie, formaat, thema, contactpunt, machine-readable). Bron: DCAT-AP-NL, data.overheid.nl. Port 8509.
