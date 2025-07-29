# app/tools_server.py
# Removed: from fastapi import FastAPI
from fastmcp import FastMCP
from typing import Dict

# Initialize FastMCP directly. FastMCP 2.0 takes a name string.
# This 'mcp' object itself will be our ASGI application.
mcp = FastMCP("MildEye Tool Server")

# --- Define a simple 'Tool' directly with @mcp.tool ---
# The tool function is decorated directly. The client will call it by the name "add_numbers".
@mcp.tool("add_numbers") # Registering the tool with the name "add_numbers"
async def add(a: float, b: float) -> Dict[str, float]:
    """
    Adds two numbers. This is a simple example of a tool.
    """
    result = a + b
    print(f"Tool 'add_numbers' executed: {a} + {b} = {result}")
    return {"result": result}

# This block allows you to run this FastMCP server directly via Uvicorn.
# We are using Uvicorn here to ensure it runs as an HTTP server,
# allowing your main FastAPI app to connect to it.
if __name__ == "__main__":
    import uvicorn
    # Pass the 'mcp' object (which is our FastMCP server) directly to Uvicorn.
    # We'll run it on port 8002 as before.
    uvicorn.run(
        mcp, # Pass the FastMCP object itself as the ASGI app
        host="0.0.0.0",
        port=8002, # This server will run on port 8002
        reload=True,
    )