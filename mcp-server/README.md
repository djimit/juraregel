# JuraRegel MCP Server

Exposes all JuraRegel Rule APIs as MCP (Model Context Protocol) tools for LLM agent integration.

## Quick Start

```bash
# Run the MCP server (stdio mode)
python3 mcp-server/juraregel_mcp.py
```

## MCP Client Configuration

### OpenCode
```jsonc
// ~/.config/opencode/opencode.jsonc
{
  "mcp": {
    "juraregel": {
      "command": "python3",
      "args": ["/path/to/juraregel/mcp-server/juraregel_mcp.py"],
      "cwd": "/path/to/juraregel"
    }
  }
}
```

### Claude Desktop
```json
{
  "mcpServers": {
    "juraregel": {
      "command": "python3",
      "args": ["/path/to/juraregel/mcp-server/juraregel_mcp.py"],
      "cwd": "/path/to/juraregel"
    }
  }
}
```

## Available Tools

| Tool | Description |
|------|-------------|
| `juraregel.list_domains` | List all 28 domains with metadata |
| `juraregel.get_rules` | Get rules for a domain (optionally by ruleId) |
| `juraregel.search_rules` | Search rules by keyword across all domains |
| `juraregel.calculate` | Match input against rules and return outcome |
| `juraregel.get_sources` | Get all legal source references for a domain |
| `juraregel.trace` | Full traceability: wet → code → JREM → test → audit |
| `juraregel.version_diff` | Compare two versions of a ruleset |

## Example Usage

```
Agent: "Heeft een alleenstaande met €30.000 inkomen recht op zorgtoeslag?"
  → juraregel.calculate(domain="toeslagen", input={toeslagType:"zorgtoeslag", alleenstaande:true, inkomen:30000, leeftijd:30})
  ← {recht: true, bedrag: €123/maand, bron: Toeslagenwet art. 8}

Agent: "Welke regels gaan over vergunningplichtig bouwen?"
  → juraregel.search_rules(query="vergunning bouwen")
  ← [OW-B-001, OW-U-001]

Agent: "Traceer regel TZ-2025-001"
  → juraregel.trace(domain="toeslagen", rule_id="TZ-2025-001")
  ← {wet: Toeslagenwet art. 8, code: app.py, jrem: exports/, tests: [...], review: review-request.md}
```

## Architecture

The MCP server reads JREM files directly from the filesystem — no API servers need to be running. This makes it ideal for local agent use and CI/CD pipelines.

For production multi-user scenarios, deploy the Rule APIs and point the MCP server at them via HTTP.
