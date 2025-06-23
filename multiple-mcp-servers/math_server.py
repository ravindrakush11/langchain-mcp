# Creating an MCP server that can add and multiply numbers.

from mcp.server.fastmcp import FastMCP
import sys
print("Math server starting...", file=sys.stderr)

mcp = FastMCP("math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiplies two numbers."""
    return a * b

if __name__ == "__main__":
    mcp.run(transport = "stdio")