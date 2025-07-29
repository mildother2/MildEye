# app/database.py
from typing import AsyncGenerator, List, Optional
from datetime import datetime # Needed for scraped_at default factory
from sqlmodel import Field, SQLModel, Relationship, create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import os # For environment variables, if you plan to use them for DB_URL

# Database URL
# For development, we'll use a local SQLite database.
# You can later change this to PostgreSQL, MySQL, etc., using environment variables.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./database.db")

# Create an async engine for SQLModel
engine = create_async_engine(DATABASE_URL, echo=True)

# Define the ScrapedContent model
# --- Existing: ScrapedContent Model ---
class ScrapedContent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(index=True)
    title: Optional[str] = None
    content: str
    scraped_at: datetime = Field(default_factory=datetime.utcnow)

# --- NEW: AgentMemory Model ---
class AgentMemory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Allows associating memory with a specific agent instance or type
    agent_id: Optional[str] = Field(default=None, index=True)
    # For conversational context, links related memory entries
    session_id: str = Field(index=True)
    # Who generated this memory entry (e.g., "user", "agent", "tool", "system")
    role: str
    # The actual content of the memory (e.g., user query, agent response, tool output)
    content: str
    # Timestamp for chronological ordering
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    # Optional: To store the name of a tool if this memory relates to a tool call/output
    tool_name: Optional[str] = None
    # Optional: To store specific metadata or structured output as JSON string
    metadata: Optional[str] = None # Will store JSON string if needed

# --- Existing: Database Engine and Session functions ---
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

async def create_db_and_tables():
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Database tables created.")

def get_session():
    with Session(engine) as session:
        yield session

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://example.com/article",
                "title": "Example Article Title",
                "content": "This is the scraped content of the example article.",
            }
        }

# Function to create tables in the database
async def create_db_and_tables():
    """
    Creates all defined SQLModel tables in the database.
    This should be called at application startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Dependency to get an async database session
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides an async session for database operations.
    This is used as a FastAPI dependency.
    """
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session