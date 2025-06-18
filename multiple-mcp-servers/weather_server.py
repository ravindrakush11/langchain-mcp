from typing import List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get the weather for a location."""
    return "It's always sunny in New York" +location

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
