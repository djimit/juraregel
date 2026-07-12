# @juraregel/sdk

TypeScript SDK for the JuraRegel Legal RuleOps Platform.

## Local build

```bash
npm install
npm run build
```

## Usage

```typescript
import { GriffierechtClient } from "./dist/index.js";

const client = new GriffierechtClient("http://127.0.0.1:8490");

// Check griffierecht
const result = await client.calculate({
  calculationDate: "2026-07-03",
  zaak: {
    rechtsgebied: "civiel",
    zaakstroom: "handel",
    procedureType: "dagvaarding",
    vorderingWaarde: 125000,
    bijzondereCategorie: "geen"
  },
  partij: {
    rol: "eiser",
    partijType: "natuurlijk_persoon",
    onvermogend: false,
    verweerStatus: "n.v.t."
  }
});

console.log(result.result.griffierecht.amount); // 2803
console.log(result.explanation.reasoningSteps); // ["Rechtsgebied is civiel...", ...]
```

## Available Clients

| Client | Domain | Port |
|---|---|---|
| GriffierechtClient | griffierecht | 8490 |

Andere domeinen zijn catalog-only of hebben geen stabiel, getypeerd calculate-contract.

## License

MIT
