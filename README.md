# MCP Aftermarket Custom Tools

## 1. Overview

This project is a **local MCP (Model Context Protocol) server** for an Automotive Aftermarket Agentic AI PoC.

The MCP server runs on your **local system** and connects to **Databricks SQL Warehouse** to retrieve data from curated Delta / Unity Catalog views.

It is designed to support role-based agents such as:

- Warranty Agent
- Service Agent
- Parts Agent
- Dealer Performance Agent
- Deep Reasoning / Supervisor Agent

This setup is useful when Databricks Apps deployment or OAuth configuration is difficult in a trial workspace, while still keeping the data foundation in Databricks.

---

## 2. Architecture

```text
Local Agent / MCP Client / VS Code
        |
        | MCP tool call
        v
Local FastMCP Server
        |
        | Databricks SQL Connector
        v
Databricks SQL Warehouse
        |
        v
Unity Catalog Views / Delta Tables
```
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/a170e0c6-38b4-40da-b005-f956cd311e09" />

### Current hosting mode

```text
MCP Server: Local system
Data Platform: Databricks
Data Access: Databricks SQL Warehouse
Authentication: PAT-based local connection
Transport for agents: stdio
Transport for MCP Inspector: streamable-http
```

---

## 3. Why this MCP server exists

Genie is already used for analytical and business-friendly Q&A over curated views.

This custom MCP server is focused on deterministic operational tools, such as:

- Claim-level warranty lookup
- VIN-level service history lookup
- Part availability lookup
- Structured context pack generation for deep reasoning
- Controlled business logic and repeatable JSON responses

Recommended separation:

| Capability | Recommended Tool |
|---|---|
| Business analytics and summaries | Databricks Genie |
| Structured operational lookup | Custom MCP |
| Policy / document Q&A | Vector Search |
| Deep reasoning and synthesis | LLM + context pack |
| Agent-to-agent collaboration | A2A Protocol |

---

## 4. MCP Tools Included

### 4.1 `health_check(include_sql_ping=False)`

Checks whether the MCP server is running.

If `include_sql_ping=true`, it also validates Databricks SQL Warehouse connectivity.

Example input:

```json
{
  "include_sql_ping": true
}
```

---

### 4.2 `get_warranty_claim_details(claim_id)`

Returns deterministic warranty claim details.

Example input:

```json
{
  "claim_id": "WC1001"
}
```

Expected output includes:

- Claim status
- Dealer details
- VIN
- Repair order ID
- Claim amount
- Rejection reason
- Missing documents
- Prior authorization flag
- Repeat repair flag
- Claim risk level
- Recommended claim action

Primary Databricks view:

```text
main.aftermarket_agent_poc.vw_warranty_claim_intelligence
```

Output Screenshot:
<img width="1831" height="1028" alt="image" src="https://github.com/user-attachments/assets/4f53331f-f29a-4dab-bac2-a3699bcb6a0b" />

---

### 4.3 `get_vehicle_service_history(vin, limit=10)`

Returns VIN-level service history and recent repair order events.

Example input:

```json
{
  "vin": "VINDEF000123",
  "limit": 5
}
```

Expected output includes:

- Total service events
- Fault codes observed
- Symptoms observed
- Latest service event
- Recent repair orders
- Repeat issue indicator
- Escalation recommendation

Primary Databricks views:

```text
main.aftermarket_agent_poc.vw_vehicle_service_history_summary
main.aftermarket_agent_poc.vw_service_repair_order_intelligence
```
Output Screenshot:
<img width="1827" height="1023" alt="image" src="https://github.com/user-attachments/assets/90727d05-b2a7-4ebc-9d1f-1febe0c7fe24" />


---

### 4.4 `check_part_availability(part_number, market_code=None, limit=10)`

Checks stock availability, backorder risk, alternate part, reman part, and end-of-chain replacement.

Example input:

```json
{
  "part_number": "P001",
  "market_code": "DE",
  "limit": 10
}
```

Expected output includes:

- Available quantity
- Backorder quantity
- Dealer location
- Alternate part number
- Reman part number
- End-of-chain part number
- Availability status
- Recommended parts action

Primary Databricks view:

```text
main.aftermarket_agent_poc.vw_parts_availability_intelligence
```
Output Screenshot:
<img width="1833" height="1025" alt="image" src="https://github.com/user-attachments/assets/0bdd6d17-e391-48b5-88bd-5aa16ae82d00" />

---

### 4.5 `generate_aftermarket_context_pack(entity_type, entity_id)`

Generates a compact evidence pack for deep reasoning.

Supported entity types:

```text
dealer
vin
claim
market
part
```

Example input:

```json
{
  "entity_type": "dealer",
  "entity_id": "DLR003"
}
```

Expected output includes:

- Entity summary
- Recent warranty performance
- Bonus records
- Service or sales context where applicable
- Recommended reasoning focus

Primary Databricks views:

```text
main.aftermarket_agent_poc.vw_dealer_360_summary
main.aftermarket_agent_poc.vw_warranty_performance_summary
main.aftermarket_agent_poc.vw_bonus_eligibility_intelligence
main.aftermarket_agent_poc.vw_sales_market_partgroup_trend
```

Output Screenshot
<img width="1817" height="1023" alt="image" src="https://github.com/user-attachments/assets/2a0073c4-f974-47a6-9ad5-3d831aa38932" />


---

## 5. Required Databricks Objects

The following curated views should exist in Databricks:

```text
main.aftermarket_agent_poc.vw_warranty_claim_intelligence
main.aftermarket_agent_poc.vw_service_repair_order_intelligence
main.aftermarket_agent_poc.vw_vehicle_service_history_summary
main.aftermarket_agent_poc.vw_parts_availability_intelligence
main.aftermarket_agent_poc.vw_dealer_360_summary
main.aftermarket_agent_poc.vw_warranty_performance_summary
main.aftermarket_agent_poc.vw_sales_market_partgroup_trend
main.aftermarket_agent_poc.vw_bonus_eligibility_intelligence
```

Default catalog and schema:

```text
CATALOG=main
SCHEMA=aftermarket_agent_poc
```

---

## 6. Project Structure

```text
mcp-databricks-custom-tools/
│
├── app.py
├── requirements.txt
├── .env.example
├── README.md
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── db/
│   ├── __init__.py
│   ├── sql_client.py
│   └── json_utils.py
│
├── tools/
│   ├── __init__.py
│   ├── warranty_tools.py
│   ├── service_tools.py
│   ├── parts_tools.py
│   └── context_pack_tools.py
│
├── tests/
│   ├── test_sql_connection.py
│   └── test_tools_local.py
│
├── scripts/
│   ├── smoke_test_stdio_client.py
│   └── run_http_server.ps1
│
└── docs/
    ├── local_testing_steps.md
    └── demo_questions.md
```

---

## 7. Environment Setup

### 7.1 Create and activate virtual environment

```powershell
python -m venv s24h_env
.\s24h_env\Scripts\activate
```

Or activate your existing environment.

### 7.2 Install dependencies

Run from the project root:

```powershell
python -m pip install -r requirements.txt
```

If the Databricks SQL connector import fails, reinstall it:

```powershell
python -m pip uninstall -y databricks databricks-sql-connector
python -m pip install --upgrade databricks-sql-connector databricks-sdk
```

Validate:

```powershell
python -c "from databricks import sql; print('Databricks SQL connector import successful')"
```

---

## 8. `.env` Configuration

Copy `.env.example` to `.env`:

```powershell
copy .env.example .env
```

Update `.env`:

```env
CATALOG=main
SCHEMA=aftermarket_agent_poc

DATABRICKS_SERVER_HOSTNAME=dbc-xxxx.cloud.databricks.com
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/xxxxxxxxxxxxxxxx
DATABRICKS_TOKEN=dapi...

MCP_TRANSPORT=stdio
MCP_HOST=127.0.0.1
MCP_PORT=8000
```

For this local version, use PAT-based authentication only.

Do not mix these OAuth variables with PAT in the same local environment:

```env
DATABRICKS_HOST=
DATABRICKS_CLIENT_ID=
DATABRICKS_CLIENT_SECRET=
```

If you previously set them in PowerShell, clear them:

```powershell
Remove-Item Env:\DATABRICKS_HOST -ErrorAction SilentlyContinue
Remove-Item Env:\DATABRICKS_CLIENT_ID -ErrorAction SilentlyContinue
Remove-Item Env:\DATABRICKS_CLIENT_SECRET -ErrorAction SilentlyContinue
```

---

## 9. Get Databricks SQL Warehouse Connection Details

In Databricks:

```text
SQL Warehouses
    -> Select your SQL Warehouse
    -> Connection details
```

Copy:

```text
Server hostname
HTTP path
```

Use those values in `.env`.

Example:

```env
DATABRICKS_SERVER_HOSTNAME=dbc-7754433f-ad29.cloud.databricks.com
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/abc123xyz456
```

---

## 10. Local Testing Sequence

Run all commands from the project root.

### 10.1 Set PYTHONPATH

```powershell
$env:PYTHONPATH="."
```

### 10.2 Test SQL connection

```powershell
python .\tests\test_sql_connection.py
```

Expected output:

```text
status: ok
current_date
current_user
```

### 10.3 Test direct tool functions

```powershell
python .\tests\test_tools_local.py
```

Expected tests:

```text
Warranty claim: WC1001
Service history: VINDEF000123
Part availability: P001 / DE
Context pack: Dealer DLR003
```

### 10.4 Test MCP client over stdio

```powershell
python .\scripts\smoke_test_stdio_client.py
```

Expected output:

```text
Available MCP tools:
- health_check
- get_warranty_claim_details
- get_vehicle_service_history
- check_part_availability
- generate_aftermarket_context_pack
```

---

## 11. How the Local stdio MCP Client Works

The stdio client starts the MCP server automatically.

You do not need to run `python app.py` separately for stdio testing.

The client uses this pattern:

```python
server_params = StdioServerParameters(
    command="python",
    args=["app.py"],
    env=child_env
)
```

Recommended for:

```text
Local LangGraph agents
Local CrewAI agents
Local A2A testing
Local development from VS Code
```

---

## 12. MCP Inspector / Browser-Style Testing

Use this only if you want a browser UI to test MCP tools.

### 12.1 Start the MCP server in HTTP mode

Open Terminal 1:

```powershell
$env:PYTHONPATH="."
$env:MCP_TRANSPORT="streamable-http"
$env:MCP_HOST="127.0.0.1"
$env:MCP_PORT="8000"

python app.py
```

Keep this terminal open.

You should see something similar to:

```text
Uvicorn running on http://127.0.0.1:8000
Application startup complete
```

### 12.2 Validate port

Open Terminal 2:

```powershell
Test-NetConnection 127.0.0.1 -Port 8000
```

Expected:

```text
TcpTestSucceeded : True
```

### 12.3 Open MCP Inspector

```powershell
npx @modelcontextprotocol/inspector
```

Configure:

```text
Transport: Streamable HTTP
URL: http://127.0.0.1:8000/mcp
Authentication: None
```

Then click:

```text
Connect
List Tools
```

---

## 13. Common Errors and Fixes

### 13.1 `ModuleNotFoundError: No module named 'db'`

Fix:

```powershell
$env:PYTHONPATH="."
python .\tests\test_sql_connection.py
```

---

### 13.2 `ImportError: cannot import name 'sql' from 'databricks'`

Fix:

```powershell
python -m pip uninstall -y databricks databricks-sql-connector
python -m pip install --upgrade databricks-sql-connector databricks-sdk
```

Validate:

```powershell
python -c "from databricks import sql; print(sql)"
```

---

### 13.3 `McpError: Connection closed`

Most likely the MCP server crashed before initialization.

Check:

```powershell
python .\tests\test_sql_connection.py
python .\tests\test_tools_local.py
```

Also ensure the stdio client passes the full environment to the child server process.

---

### 13.4 `ECONNREFUSED 127.0.0.1:8000`

This means no HTTP server is listening on port `8000`.

Fix:

```powershell
$env:PYTHONPATH="."
$env:MCP_TRANSPORT="streamable-http"
$env:MCP_HOST="127.0.0.1"
$env:MCP_PORT="8000"
python app.py
```

Keep the terminal open and retry MCP Inspector.

---

### 13.5 Databricks SDK error: `more than one authorization method configured`

You are mixing PAT and OAuth variables.

For this local MCP version, keep only:

```env
DATABRICKS_SERVER_HOSTNAME=
DATABRICKS_HTTP_PATH=
DATABRICKS_TOKEN=
```

Remove:

```env
DATABRICKS_HOST=
DATABRICKS_CLIENT_ID=
DATABRICKS_CLIENT_SECRET=
```

---

## 14. Demo Scenarios

### 14.1 Warranty Agent

User question:

```text
Why was claim WC1001 rejected?
```

MCP tool:

```text
get_warranty_claim_details
```

Input:

```json
{
  "claim_id": "WC1001"
}
```

---

### 14.2 Service Agent

User question:

```text
Has VINDEF000123 had the same issue before?
```

MCP tool:

```text
get_vehicle_service_history
```

Input:

```json
{
  "vin": "VINDEF000123",
  "limit": 5
}
```

---

### 14.3 Parts Agent

User question:

```text
Is part P001 available in Germany?
```

MCP tool:

```text
check_part_availability
```

Input:

```json
{
  "part_number": "P001",
  "market_code": "DE",
  "limit": 10
}
```

---

### 14.4 Deep Reasoning Agent

User question:

```text
Why is dealer DLR003 underperforming despite good sales?
```

MCP tool:

```text
generate_aftermarket_context_pack
```

Input:

```json
{
  "entity_type": "dealer",
  "entity_id": "DLR003"
}
```

---

## 15. Recommended Agent Integration

Use the local MCP server with your role-based agent cluster.

```text
User
  |
  v
Supervisor Agent
  |
  |-- Warranty Agent -> Custom MCP -> Warranty Views
  |
  |-- Service Agent -> Custom MCP -> Service Views
  |
  |-- Parts Agent -> Custom MCP -> Inventory Views
  |
  |-- Sales Agent -> Genie / SQL / Context Pack
  |
  v
Final Response
```

### Suggested routing

| User Intent | Agent | MCP Tool |
|---|---|---|
| Claim status / rejection / resubmission | Warranty Agent | `get_warranty_claim_details` |
| VIN repair history / repeat issue | Service Agent | `get_vehicle_service_history` |
| Stock / alternate / reman part | Parts Agent | `check_part_availability` |
| Deep reasoning / RCA | Supervisor or Deep Reasoning Agent | `generate_aftermarket_context_pack` |

---

## 16. Final PoC Positioning

You can describe the setup like this:

```text
For this PoC, the custom MCP server is hosted locally to avoid Databricks trial account OAuth and app hosting limitations. The MCP server still connects to Databricks SQL Warehouse and accesses curated Unity Catalog views backed by Delta tables. In production, the same MCP server can be containerized or deployed as a Databricks App with OAuth-based authentication.
```

---

## 17. Next Steps

Recommended next steps:

```text
1. Connect this MCP server to a Warranty Agent.
2. Connect Service Agent and Parts Agent.
3. Add Supervisor Agent with routing logic.
4. Add A2A protocol between Supervisor and specialist agents.
5. Add GPT-5.5 reasoning over the context pack.
6. Add conversation memory for multi-turn follow-up.
```
