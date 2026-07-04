// TypeScript example — JuraRegel SDK
import { GriffierechtClient } from "@juraregel/sdk";

const client = new GriffierechtClient("http://127.0.0.1:8490");
const result = await client.calculate({
    calculationDate: "2026-07-03",
    zaak: { rechtsgebied: "civiel", zaakstroom: "handel", procedureType: "dagvaarding",
            vorderingWaarde: 125000, bijzondereCategorie: "geen" },
    partij: { rol: "eiser", partijType: "natuurlijk_persoon", onvermogend: false, verweerStatus: "n.v.t." }
});
console.log(`Griffierecht: €${result.result.griffierecht.amount}`);
console.log(`Redeneerstappen: ${result.explanation.reasoningSteps.join(" → ")}`);
