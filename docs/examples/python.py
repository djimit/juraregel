# Python example — JuraRegel API call
import httpx

response = httpx.post("http://127.0.0.1:8490/v1/griffierecht/calculate", json={
    "calculationDate": "2026-07-03",
    "zaak": {"rechtsgebied": "civiel", "zaakstroom": "handel", "procedureType": "dagvaarding",
             "vorderingWaarde": 125000, "bijzondereCategorie": "geen"},
    "partij": {"rol": "eiser", "partijType": "natuurlijk_persoon", "onvermogend": False, "verweerStatus": "n.v.t."}
})
result = response.json()
print(f"Griffierecht: €{result['result']['griffierecht']['amount']}")
print(f"Categorie: {result['result']['category']}")
print(f"Redeneerstappen: {result['explanation']['reasoningSteps']}")
print(f"Bron: {result['explanation']['sourceRefs'][0]['title']}")
