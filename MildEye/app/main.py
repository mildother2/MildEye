# MildEye/app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from typing import List, Dict
from datetime import datetime

# THIS IS THE CRITICAL CHANGE: Use a relative import for your database module
from .database import engine, create_db_and_tables, get_session, ScrapedContent

# NEW: Import FastMCPClient for interacting with tool servers
# Ensure this is the only FastMCPClient import to avoid conflicts
from fastmcp import Client # FastMCP 2.0 uses 'Client' for client-side operations

# Initialize the FastAPI application
app = FastAPI(
    title="MildEye Backend API",
    description="Backend for MildEye personal AI platform, managing data, agents, and tools.",
    version="0.1.0",
)

# FastAPI startup event: create database tables when the app starts
@app.on_event("startup")
async def on_startup():
    print("FastAPI app starting up. Creating database tables...")
    await create_db_and_tables()
    print("Database tables ensured.")

# --- FastMCP Client Setup for 2.0 ---
# Configure FastMCPClient to connect to your tools_server.py.
# The tools_server is running on port 8002 and serves as the FastMCP server.
# --- FastMCP Client Setup for 2.0 ---
# Initialize the FastMCP Client.
# We are making an educated guess here that the 'Client' class can take a URL
# for a remote HTTP FastMCP server. This is common practice in many libraries.
mcp_client = Client(
    "http://localhost:8002" # Directly pass the base URL of your FastMCP tool server
)
# --- END FastMCP Client Setup ---

# Root endpoint for the backend (optional, but good for health checks)
@app.get("/")
async def read_root():
    return {"message": "MildEye Backend is running!"}

# Simple API endpoint for fasthtml to test communication
@app.get("/api/hello")
async def hello_world():
    """
    A simple endpoint to test communication from the frontend.
    """
    return {"message": "Hello from FastAPI Backend!"}

# --- NEW: Endpoint to call the FastMCP tool ---
@app.get("/api/calculate/add/{a}/{b}")
async def call_add_tool(
    a: float,
    b: float,
) -> Dict[str, float]:
    """
    Calls the 'add_numbers' tool hosted on the FastMCP tool server using FastMCPClient.
    """
    try:
        # Call the tool directly by its name and pass arguments as a dictionary
        result = await mcp_client.call_tool("add_numbers", {"a": a, "b": b})
        return result
    except Exception as e:
        # Catch potential errors during tool call (e.g., server not running, bad arguments)
        raise HTTPException(status_code=500, detail=f"Error calling add_numbers tool: {e}")

# --- API Endpoints for Scraped Content ---
# (Assuming your existing ScrapedContent endpoints go here)

# Example endpoint for ScrapedContent (if you want to add this back)
# You might have more complex logic here based on your database.py and models.py
"""
# If you have ScrapedContent model and table, you can add endpoints like this:
@app.post("/scraped_content/", response_model=ScrapedContent)
async def create_scraped_content(content: ScrapedContent, session: Session = Depends(get_session)):
    session.add(content)
    session.commit()
    session.refresh(content)
    return content

@app.get("/scraped_content/", response_model=List[ScrapedContent])
async def read_scraped_content(session: Session = Depends(get_session)):
    contents = session.exec(select(ScrapedContent)).all()
    return contents
"""