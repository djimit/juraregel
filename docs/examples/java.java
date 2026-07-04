// Java example — JuraRegel API call
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class JuraregelExample {
    public static void main(String[] args) throws Exception {
        var client = HttpClient.newHttpClient();
        var body = """
            {
              "calculationDate": "2026-07-03",
              "zaak": {"rechtsgebied": "civiel", "zaakstroom": "handel", "procedureType": "dagvaarding", "vorderingWaarde": 125000, "bijzondereCategorie": "geen"},
              "partij": {"rol": "eiser", "partijType": "natuurlijk_persoon", "onvermogend": false, "verweerStatus": "n.v.t."}
            }""";
        var request = HttpRequest.newBuilder()
            .uri(URI.create("http://127.0.0.1:8490/v1/griffierecht/calculate"))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(body))
            .build();
        var response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println(response.body());
    }
}
