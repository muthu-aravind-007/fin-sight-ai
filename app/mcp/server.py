from mcp.server.fastmcp import FastMCP

print("Starting MCP...")

mcp = FastMCP("FinSight AI")

from .tools import *

print("Loaded tools")

if __name__ == "__main__":
    print("Running MCP server...")
    mcp.run()