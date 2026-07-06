# Decentrale Regelcheck

## Doel

Vind de relevante lokale regeling, bestuurslaag en procedure voor een product of activiteit.

## Input

- postcode of bestuursorgaan
- productnaam of UPL-naam
- activiteit

## Bronnen

- Lokale wet- en regelgeving / CVDR
- SRU zoekdienst
- UPL
- TOOI/ROO

## Live read-only pad

- `https://lokaleregelgeving.overheid.nl/ZoekResultaat`
- Parameters: `locatie` voor 4 postcodecijfers, `tekst` voor product/activiteit en `count` voor resultaatlimiet.
- De connector normaliseert alleen zoekresultaten, regelingstitels en sourceRefs.

## Output

- bevoegd gezag
- relevante regeling en sourceRef
- proceduretype: aanvraag, melding, verplichting, subsidie of bezwaar
- `manualReviewRequired=true` bij open normen of lokale beleidsruimte

## Niet Doen

Geen bulk-ingest van alle lokale regelingen voordat de product- en organisatie-as werkt.
Geen automatische eindbeslissing bij open normen, meerdere overheden of ontbrekende lokale context.
