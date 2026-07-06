# Woo Publicatieplicht Preflight

## Doel

Controleer of Woo-publicatie metadata en vindbaarheid klaar zijn voor publicatieketens.

## Input

- bestuursorgaan
- documenttype
- sitemap of publicatie-URL
- Woo-informatiecategorie

## Bronnen

- Woo-index
- DiWoo metadata
- Woo-harvester publicatievoorwaarden
- TOOI/ROO waardelijsten

## Live read-only pad

- `https://organisaties.overheid.nl/woo/zoeken`
- Parameters: `keyword`, `maximumRecords`, `pageNumber`, `sortOrder`.
- Detailpad: publieke Woo-index organisatiepagina's, sectie `Locaties Woo-documenten`.
- De connector leest publicatielocaties en informatiecategorieen, geen documentbody's.

## Output

- ontbrekende metadata
- geldige TOOI waarden
- harvester-ready indicatie
- sourceRefs naar Woo-index, DiWoo en TOOI

## Niet Doen

Geen documenten publiceren of muteren; dit is alleen preflight.
Geen private documentinhoud ophalen of opslaan.
