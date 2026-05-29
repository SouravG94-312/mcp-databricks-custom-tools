# Databricks App Deployment Notes

## 1. Create app

```bash
databricks apps create mcp-aftermarket-custom-tools
```

## 2. Sync source

```bash
databricks sync . /Workspace/Users/<your-user>/mcp-aftermarket-custom-tools
```

## 3. Deploy

```bash
databricks apps deploy mcp-aftermarket-custom-tools --source-code-path /Workspace/Users/<your-user>/mcp-aftermarket-custom-tools
```

## 4. Permissions

Give your user/service principal access to the app.

## 5. Test

Open MCP Inspector:

```bash
npx @modelcontextprotocol/inspector
```

Use:

```text
Transport: Streamable HTTP
URL: https://<databricks-app-url>/mcp
Authentication: OAuth
```

For Databricks-hosted custom MCP, use OAuth. Do not use PAT for the Databricks App MCP endpoint.
