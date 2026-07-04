// Go example — JuraRegel API call
package main

import ("bytes"; "encoding/json"; "fmt"; "net/http")

func main() {
    body, _ := json.Marshal(map[string]interface{}{
        "calculationDate": "2026-07-03",
        "zaak": map[string]interface{}{"rechtsgebied": "civiel", "zaakstroom": "handel",
            "procedureType": "dagvaarding", "vorderingWaarde": 125000, "bijzondereCategorie": "geen"},
        "partij": map[string]interface{}{"rol": "eiser", "partijType": "natuurlijk_persoon",
            "onvermogend": false, "verweerStatus": "n.v.t."},
    })
    resp, _ := http.Post("http://127.0.0.1:8490/v1/griffierecht/calculate",
        "application/json", bytes.NewBuffer(body))
    defer resp.Body.Close()
    var result map[string]interface{}
    json.NewDecoder(resp.Body).Decode(&result)
    fmt.Printf("Griffierecht: €%.0f\n", result["result"].(map[string]interface{})["griffierecht"].(map[string]interface{})["amount"])
}
