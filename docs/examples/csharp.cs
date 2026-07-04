// C# example — JuraRegel API call
using System.Net.Http.Json;

var client = new HttpClient();
var response = await client.PostAsJsonAsync("http://127.0.0.1:8490/v1/griffierecht/calculate", new {
    calculationDate = "2026-07-03",
    zaak = new { rechtsgebied = "civiel", zaakstroom = "handel", procedureType = "dagvaarding",
                vorderingWaarde = 125000, bijzondereCategorie = "geen" },
    partij = new { rol = "eiser", partijType = "natuurlijk_persoon", onvermogend = false, verweerStatus = "n.v.t." }
});
var result = await response.Content.ReadFromJsonAsync<dynamic>();
Console.WriteLine($"Griffierecht: {result.result.griffierecht.amount}");
