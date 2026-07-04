# Procesreglement Use Case — Digitale indiening

**Als** griffier **wil ik** weten welke stukken digitaal ingediend kunnen worden **zodat** zaakintake efficiënter verloopt.

| Rol | Probleem | Oplossing |
|---|---|---|
| Griffier | Onbekend welke stukken digitaal mogen | Rule API checkt per documenttype |
| Burger | Wil digitaal indienen maar weet niet of het kan | API retourneert "digitaal verplicht ja/nee" |
| Ontwikkelaar portaal | Wil digitale indiening implementeren | API endpoint met duidelijke response |

4 regels (PoC). Rule API op port 8491. 16 tests. PoC status.

## Functiehuis Rijksoverheid Rollen

| Rol | Probleem | Oplossing |
|---|---|---|
| Griffier | Procesreglement regels handmatig | Rule API checkt per documenttype |
| Portaal ontwikkelaar | Wil digitale indiening bouwen | API met duidelijke compliant/niet-compliant |
| Burger | Wil weten of digitaal indienen kan | API response met uitleg |
