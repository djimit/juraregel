# NEDERUS MCP Tools

Documentatie voor de NEDERUS tools in de JuraRegel MCP server.

## Overzicht

De JuraRegel MCP server exposeert 3 NEDERUS tools die multi-jurisdictionele
AI-compliance mapping serveren aan LLM-agents:

| Tool | Functie | Input |
|------|---------|-------|
| `nederus.list_controls` | Lijst alle 5 NEDERUS controls | `framework` (optioneel) |
| `nederus.get_control` | Detail van één control | `control_id` (vereist) |
| `nederus.crosswalk` | Crosswalk tussen twee frameworks | `source_framework`, `target_framework` (vereist) |

## Gebruik

### Lijst alle controls

```json
{
  "method": "tools/call",
  "params": {
    "name": "nederus.list_controls",
    "arguments": {}
  }
}
```

Response: 5 controls met framework mappings, severity, coverage.

### Filter op framework

```json
{
  "method": "tools/call",
  "params": {
    "name": "nederus.list_controls",
    "arguments": {"framework": "eu-ai-act"}
  }
}
```

Response: 4 controls die EU AI Act dekken (NED-01 t/m NED-05, alle behalve gap-only).

### Detail van één control

```json
{
  "method": "tools/call",
  "params": {
    "name": "nederus.get_control",
    "arguments": {"control_id": "NED-01"}
  }
}
```

Response: Volledige control met alle framework references.

### Crosswalk tussen frameworks

```json
{
  "method": "tools/call",
  "params": {
    "name": "nederus.crosswalk",
    "arguments": {
      "source_framework": "eu-ai-act",
      "target_framework": "bio2"
    }
  }
}
```

Response: Overlapping controls + per-control source/target references.

## Integratie met JuraRegel use cases

De NEDERUS tools complementen de bestaande JuraRegel tools:

| JuraRegel tool | NEDERUS tool | Relatie |
|---|---|---|
| `juraregel.calculate` (eu-ai-act) | `nederus.list_controls` | JuraRegel berekent, NEDERUS mapt |
| `juraregel.calculate` (bio2) | `nederus.crosswalk` | JuraRegel checkt, NEDERUS toont overlap |
| `juraregel.check_compliance` | `nederus.get_control` | JuraRegel rapporteert, NEDERUS definieert |

## Data source

De NEDERUS controls in deze MCP server zijn een lightweight copy. De authoritative
source is het [nederus-framework repository](https://github.com/djimit/nederus-framework)
met `controls.yaml`, crosswalks, en validation pipeline.

## Toekomstige uitbreiding

- `nederus.validate`: Valideer een AI-systeem tegen alle 5 controls
- `nederus.gap_analysis`: Toon ontbrekende compliance per framework
- `nederus.export_evidence`: Genereer evidence pack voor audit
