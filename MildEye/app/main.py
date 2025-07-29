# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from datetime import datetime # Make sure datetime is imported here

# THIS IS THE CRITICAL CHANGE: Use a relative import
from .database import engine, create_db_and_tables, get_session, ScrapedContent

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

# Root endpoint for the backend (optional, but good for health checks)
@app.get("/")
async def read_root():
    return {"message": "MildEye Backend is running!"}

# --- NEW: Simple API endpoint for fasthtml to test communication ---
@app.get("/api/hello")
async def hello_world():
    """
    A simple endpoint to test communication from the frontend.
    """
    return {"message": "Hello from FastAPI Backend!"}

# Endpoint to create a new scraped content entry
@app.post("/api/scraped_content/", response_model=ScrapedContent)
async def create_scraped_content(content: ScrapedContent, session: Session = Depends(get_session)):
    """
    Creates a new scraped content entry in the database.
    """
    session.add(content)
    await session.commit()
    await session.refresh(content)
    return content

# Endpoint to get all scraped content entries
@app.get("/api/scraped_content/", response_model=List[ScrapedContent])
async def get_all_scraped_content(session: Session = Depends(get_session)):
    """
    Retrieves all scraped content entries from the database.
    """
    results = await session.exec(select(ScrapedContent))
    contents = results.all()
    return contents

# Endpoint to get a single scraped content entry by ID
@app.get("/api/scraped_content/{content_id}", response_model=ScrapedContent)
async def get_scraped_content_by_id(content_id: int, session: Session = Depends(get_session)):
    """
    Retrieves a single scraped content entry by its ID.
    """
    content = await session.get(ScrapedContent, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content

# This block allows you to run the app directly
if __name__ == "__main__":
    import uvicorn
    # When running directly with 'python app/main.py' from MildEye/
    # Python adds MildEye/ to sys.path, so 'app.main:app' will work.
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
    )