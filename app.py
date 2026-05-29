from __future__ import annotations

import inspect
import os

from mcp.server.fastmcp import FastMCP

from config.settings import settings
from tools.warranty_tools import get_warranty_claim_details_impl
from tools.service_tools import get_vehicle_service_history_impl
from tools.parts_tools import check_part_availability_impl
from tools.context_pack_tools import generate_aftermarket_context_pack_impl

mcp = FastMCP("Aftermarket Custom MCP Tools")


@mcp.tool()
def get_warranty_claim_details(claim_id: str) -> dict:
    """
    Get deterministic warranty claim details including claim status, rejection reason,
    missing documents, prior authorization flag, repeat repair flag, and recommended action.

    Example:
    get_warranty_claim_details("WC1001")
    """
    return get_warranty_claim_details_impl(claim_id)


@mcp.tool()
def get_vehicle_service_history(vin: str, limit: int = 10) -> dict:
    """
    Get VIN-level service history, recent repair orders, fault codes, symptoms,
    repeat issue indicator, and escalation recommendation.

    Example:
    get_vehicle_service_history("VINDEF000123")
    """
    return get_vehicle_service_history_impl(vin, limit)


@mcp.tool()
def check_part_availability(part_number: str, market_code: str | None = None, limit: int = 10) -> dict:
    """
    Check part availability across dealers or within a market. Returns available quantity,
    backorder quantity, alternate part, reman part, end-of-chain part, and recommended action.

    Example:
    check_part_availability("P001", "DE")
    """
    return check_part_availability_impl(part_number, market_code, limit)


@mcp.tool()
def generate_aftermarket_context_pack(entity_type: str, entity_id: str) -> dict:
    """
    Generate a compact evidence pack for deep reasoning.

    Supported entity_type values:
    - dealer
    - vin
    - claim
    - market
    - part

    Example:
    generate_aftermarket_context_pack("dealer", "DLR003")
    """
    return generate_aftermarket_context_pack_impl(entity_type, entity_id)


@mcp.tool()
def health_check() -> dict:
    """Health check for the MCP server and configuration."""
    return {
        "status": "ok",
        "server": "Aftermarket Custom MCP Tools",
        "catalog": settings.catalog,
        "schema": settings.schema,
        "transport": settings.mcp_transport,
        "host": settings.mcp_host,
        "port": settings.mcp_port,
    }


def _run_mcp() -> None:
    """Run FastMCP with compatibility across MCP SDK versions."""
    transport = settings.mcp_transport

    if transport == "stdio":
        mcp.run()
        return

    run_signature = inspect.signature(mcp.run)
    kwargs = {}

    if "transport" in run_signature.parameters:
        kwargs["transport"] = transport
    if "host" in run_signature.parameters:
        kwargs["host"] = settings.mcp_host
    if "port" in run_signature.parameters:
        kwargs["port"] = settings.mcp_port

    if kwargs:
        mcp.run(**kwargs)
    else:
        os.environ["HOST"] = settings.mcp_host
        os.environ["PORT"] = str(settings.mcp_port)
        mcp.run()


if __name__ == "__main__":
    _run_mcp()
