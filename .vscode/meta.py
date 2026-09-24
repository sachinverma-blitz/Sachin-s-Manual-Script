import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

MCP_URL = "https://metabase.blitznow.in/api/mcp"

SQL = """
SELECT *
FROM application_db.ticket
LIMIT 10;
"""

async def main():
    async with streamablehttp_client(MCP_URL) as (
        read_stream,
        write_stream,
        _,
    ):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            # List available tools
            tools = await session.list_tools()

            print("Available tools:")
            for tool in tools.tools:
                print(f"- {tool.name}")

            # Replace "run_sql" with the actual tool name if different
            result = await session.call_tool(
                "run_sql",
                {
                    "query": SQL
                }
            )

            print("\nResult:")
            print(result)

asyncio.run(main())