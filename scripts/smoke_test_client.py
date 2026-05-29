import asyncio
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters


async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["app.py"],
        env={"MCP_TRANSPORT": "stdio"}
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Tools:")
            for tool in tools.tools:
                print("-", tool.name)

            result = await session.call_tool("health_check", arguments={})
            print("\nHealth check:")
            print(result)


if __name__ == "__main__":
    asyncio.run(main())
