from __future__ import annotations

from contextlib import contextmanager
from typing import Any

from databricks import sql
from databricks.sdk.core import Config

from config.settings import settings
from db.json_utils import rows_to_json


class DatabricksSQLClient:
    """Small wrapper around Databricks SQL Connector."""

    def __init__(self):
        self.server_hostname = settings.databricks_server_hostname
        self.http_path = settings.databricks_http_path
        self.access_token = settings.databricks_token

    def _resolve_connection_args(self) -> dict[str, Any]:
        if self.server_hostname and self.http_path and self.access_token:
            return {
                "server_hostname": self.server_hostname.replace("https://", "").rstrip("/"),
                "http_path": self.http_path,
                "access_token": self.access_token,
            }

        cfg = Config()
        host = (cfg.host or "").replace("https://", "").rstrip("/")
        token = cfg.token

        if not host or not self.http_path:
            raise RuntimeError(
                "Databricks SQL connection is not configured. "
                "Set DATABRICKS_SERVER_HOSTNAME, DATABRICKS_HTTP_PATH and DATABRICKS_TOKEN "
                "for local testing, or provide DATABRICKS_HTTP_PATH in Databricks Apps."
            )

        if not token:
            raise RuntimeError(
                "No Databricks access token found for SQL connector. "
                "For local testing set DATABRICKS_TOKEN. "
                "For Databricks Apps configure appropriate app auth/secrets."
            )

        return {
            "server_hostname": host,
            "http_path": self.http_path,
            "access_token": token,
        }

    @contextmanager
    def connect(self):
        args = self._resolve_connection_args()
        conn = sql.connect(**args)
        try:
            yield conn
        finally:
            conn.close()

    def query(self, query: str, parameters: dict[str, Any] | None = None) -> list[dict]:
        with self.connect() as conn:
            with conn.cursor() as cur:
                if parameters:
                    cur.execute(query, parameters)
                else:
                    cur.execute(query)

                columns = [c[0] for c in cur.description] if cur.description else []
                rows = cur.fetchall()

        result = [dict(zip(columns, row)) for row in rows]
        return rows_to_json(result)

    def query_one(self, query: str, parameters: dict[str, Any] | None = None) -> dict | None:
        rows = self.query(query, parameters)
        return rows[0] if rows else None


sql_client = DatabricksSQLClient()
