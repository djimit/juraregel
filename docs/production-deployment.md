# JuraRegel production-candidate deployment contract

JuraRegel is niet zonder aanvullende bewijzen production-ready. De repository
levert een fail-closed container- en configuratiecontract; een specifieke
deployment wordt pas toegelaten nadat de externe poorten in het
[enterprise-grade plan](enterprise-grade-level3-plan.md) zijn geaccepteerd.

## Verplichte grensvoorwaarden

- PostgreSQL, Qdrant en Keycloak zijn goedgekeurde externe diensten.
- TLS en rate limiting worden door een vertrouwde ingress afgedwongen.
- CORS bevat uitsluitend expliciete origins.
- geheimen komen uit een goedgekeurde secret store, niet uit `.env` of Git;
- database-migraties worden vóór applicatiestart uitgevoerd. De API maakt in
  productie zelf geen tabellen aan.
- `/ready` moet database en Qdrant werkelijk kunnen bereiken.

Maak lokale configuratie vanuit `.env.example` en vervang alle placeholders:

```bash
cp .env.example .env
docker compose config --quiet
docker compose up --build
curl http://127.0.0.1:8096/health
curl http://127.0.0.1:8096/ready
```

`/health` bewijst alleen dat het proces leeft. Alleen `/ready` toetst de
geconfigureerde database- en vectorstore-afhankelijkheden; geen van beide
endpoints bewijst juridische juistheid of operationele productieacceptatie.

## Promotion record

Een productiepromotie moet ten minste verwijzen naar:

1. image digest, SBOM, kwetsbaarheidsscan en ondertekende provenance;
2. migratie-, backup/restore- en disaster-recoverybewijs;
3. SLO's, alerts, incidentrunbook en auditretentie;
4. Keycloak issuer/audience-, rol- en tenant-autorisatietests;
5. TLS-, ingress- en netwerksegmentatiebewijs;
6. onafhankelijke juridische acceptatie van de geactiveerde use cases;
7. de uitvoer van `python3 ci/enterprise_readiness.py --enforce`.

De laatste opdracht blijft falen zolang repository-onafhankelijke poorten nog
niet met goedgekeurde artifacts zijn ingevuld. Dat is opzettelijk.
