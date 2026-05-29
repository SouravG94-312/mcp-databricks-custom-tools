# MCP Aftermarket Custom Tools

Custom MCP server for the **Automotive Aftermarket Agent Cluster PoC**.

This server is designed to be hosted as a **Databricks App** and exposes deterministic business tools for agents:

1. `get_warranty_claim_details(claim_id)`
2. `get_vehicle_service_history(vin)`
3. `check_part_availability(part_number, market_code)`
4. `generate_aftermarket_context_pack(entity_type, entity_id)`

## Why custom MCP?

Use Genie for analytical Q&A, Vector Search for document intelligence, and this custom MCP server for deterministic operational lookups and deep-reasoning evidence packs.

## Expected Databricks objects

Catalog/schema:

```text
main.aftermarket_agent_poc
```

Required curated views:

```text
vw_warranty_claim_intelligence
vw_service_repair_order_intelligence
vw_vehicle_service_history_summary
vw_parts_availability_intelligence
vw_dealer_360_summary
vw_warranty_performance_summary
vw_sales_market_partgroup_trend
vw_bonus_eligibility_intelligence
```

## Local setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env`:

```env
DATABRICKS_SERVER_HOSTNAME=dbc-xxxx.cloud.databricks.com
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/xxxxxxxxxxxxxxxx
DATABRICKS_TOKEN=dapi...
CATALOG=main
SCHEMA=aftermarket_agent_poc
MCP_TRANSPORT=stdio
```

Run local stdio server:

```bash
python app.py
```

## Databricks App deployment

Use `app.yaml`.

The Databricks App should use OAuth/workspace identity. Do **not** hardcode PAT tokens in production.

```bash
databricks apps create mcp-aftermarket-custom-tools
databricks sync . /Workspace/Users/<your-user>/mcp-aftermarket-custom-tools
databricks apps deploy mcp-aftermarket-custom-tools --source-code-path /Workspace/Users/<your-user>/mcp-aftermarket-custom-tools
```

Your MCP endpoint should be:

```text
https://<your-databricks-app-url>/mcp
```

## Tool examples

### Warranty claim

```json
{
  "claim_id": "WC1001"
}
```

### Vehicle service history

```json
{
  "vin": "VINDEF000123"
}
```

### Part availability

```json
{
  "part_number": "P001",
  "market_code": "DE"
}
```

### Context pack

```json
{
  "entity_type": "dealer",
  "entity_id": "DLR003"
}
```

## Notes

- This code keeps all outputs JSON-safe for MCP clients.
- SQL is parameterized where supported by the Databricks SQL connector.
- The custom MCP server is intentionally focused on operational lookup tools, not duplicating Genie analytics.
