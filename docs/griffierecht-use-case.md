# Griffierecht Use Case — Eerste volledig uitgewerkte use case

**Als** griffier **wil ik** bij zaakintake automatisch het correcte griffierecht bepalen **zodat** ik niet handmatig tarieven hoef op te zoeken en fouten voorkom.

| Rol | Probleem | Oplossing |
|---|---|---|
| Griffier | Verschillende tarieven per zaakstroom/partijtype — foutgevoelig | Rule API berekent bedrag met bronverwijzing |
| Burger | Begrijpt niet waarom een bedrag geldt | API retourneert uitleg met wetsartikel |
| Advocaat | Moet griffie bellen voor tarief | Directe berekening via API of portaal |
| Financieel beheer | Geen audit trail | inputHash + rulesetHash + timestamp per berekening |

36 regels voor civiele dagvaardingszaken (kanton + handel). Rule API op port 8490. 57 tests. 14 CI gates. Production status.

## Functiehuis Rijksoverheid Rollen

| Rol | Probleem | Oplossing |
|---|---|---|
| Griffier | Tarieven handmatig opzoeken | Rule API berekent automatisch met uitleg |
| Burger | Geen transparantie over griffierecht | API geeft redeneerstappen + bronverwijzing |
| Financieel beheerder | Geen audit trail van berekeningen | Audit endpoint met hashes |
| Product owner portaal | Wil griffierecht in intakeportaal | Rule API integrateerbaar via SDK/OpenAPI |
