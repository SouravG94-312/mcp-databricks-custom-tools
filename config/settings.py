from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    catalog: str = os.getenv("CATALOG", "main")
    schema: str = os.getenv("SCHEMA", "aftermarket_agent_poc")

    # SQL connector settings.
    # Local: DATABRICKS_SERVER_HOSTNAME, DATABRICKS_HTTP_PATH, DATABRICKS_TOKEN.
    databricks_server_hostname: str | None = os.getenv("DATABRICKS_SERVER_HOSTNAME")
    databricks_http_path: str | None = os.getenv("DATABRICKS_HTTP_PATH")
    databricks_token: str | None = os.getenv("DATABRICKS_TOKEN")

    # MCP runtime.
    mcp_transport: str = os.getenv("MCP_TRANSPORT", "stdio")
    mcp_host: str = os.getenv("MCP_HOST", "0.0.0.0")
    mcp_port: int = int(os.getenv("MCP_PORT", os.getenv("DATABRICKS_APP_PORT", "8000")))

    @property
    def fq_schema(self) -> str:
        return f"{self.catalog}.{self.schema}"


settings = Settings()
