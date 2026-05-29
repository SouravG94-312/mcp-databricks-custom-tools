import asyncio
import os
from pathlib import Path

from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters


PROJECT_ROOT = Path(__file__).resolve().parents[1]


async def main():
    # Important:
    # Copy the full current environment, otherwise the MCP server process
    # may not get PATH, Python env, or Databricks-related variables.
    child_env = os.environ.copy()
    child_env["MCP_TRANSPORT"] = "stdio"

    server_params = StdioServerParameters(
        command="python",
        args=["app.py"],
        env=child_env,
        cwd=str(PROJECT_ROOT),
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()

            print("\nAvailable MCP tools:")
            for tool in tools.tools:
                print("-", tool.name)

            print("\nCalling health_check...")
            health = await session.call_tool(
                "health_check",
                arguments={"include_sql_ping": False},
            )
            print(health)

            print("\nCalling get_warranty_claim_details...")
            claim = await session.call_tool(
                "get_warranty_claim_details",
                arguments={"claim_id": "WC1001"},
            )
            print(claim)

            print("\nCalling get_vehicle_service_history...")
            service = await session.call_tool(
                "get_vehicle_service_history",
                arguments={
                    "vin": "VINDEF000123",
                    "limit": 5,
                },
            )
            print(service)

            print("\nCalling check_part_availability...")
            parts = await session.call_tool(
                "check_part_availability",
                arguments={
                    "part_number": "P001",
                    "market_code": "DE",
                    "limit": 10,
                },
            )
            print(parts)

            print("\nCalling generate_aftermarket_context_pack...")
            context = await session.call_tool(
                "generate_aftermarket_context_pack",
                arguments={
                    "entity_type": "dealer",
                    "entity_id": "DLR003",
                },
            )
            print(context)


if __name__ == "__main__":
    asyncio.run(main())