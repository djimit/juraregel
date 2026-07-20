# STTR Preflight

## Doel

Voorkom DSO/RTR-afkeur door toepasbare-regelbestanden vooraf te toetsen.

## Input

- toepasbare-regelbestand of metadata
- activiteit
- bevoegd gezag
- gewenste DSO/RTR versie

## Bronnen

- STTR 3.0.1, definitief op 1 augustus 2025
- IMTR 3.0.1, definitief op 4 december 2025
- RTR aansluitvoorwaarden
- STOP/TPOD

## Live read-only pad

- `https://iplo.nl/digitaal-stelsel/aansluiten/standaarden/sttr-imtr/`
- De connector leest het publieke blok met ondersteunde STTR/IMTR versies.
- Lokale package metadata kan als JSON of eenvoudige XML worden geparsed.

## Output

- STTR-versiefit
- veldlengte- en verificatieproblemen
- ontbrekende annotaties
- JREM sourceRef mapping

## Niet Doen

Geen inhoudelijke vergunningbeslissing nemen; alleen leveringsfit toetsen.
Geen DSO/RTR submission-client en geen volledige XSD/verificatiematrix-validatie in deze slice.

## Fail-closed grens

Een onbekend package, ontbrekende RTR-versie of ontbrekende JREM-mapping vereist handmatige controle.
