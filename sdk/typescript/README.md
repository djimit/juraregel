# @juraregel/sdk

TypeScript SDK for the JuraRegel Legal RuleOps Platform.

## Install

```bash
npm install @juraregel/sdk
```

## Usage

```typescript
import { GriffierechtClient } from "@juraregel/sdk";

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
| Bio2Client | bio2 | 8494 |
| ForumStandaardisatieClient | forumstandaardisatie | 8495 |
| OverheidsstandaardenClient | overheidsstandaarden | 8496 |
| NoraClient | nora | 8497 |
| EuAiActClient | eu-ai-act | 8498 |
| AvgGdprClient | avg-gdpr | 8499 |

## License

MIT
