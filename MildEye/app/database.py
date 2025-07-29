# app/database.py
from typing import AsyncGenerator
from datetime import datetime # Needed for scraped_at default factory
from sqlmodel import Field, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import os # For environment variables, if you plan to use them for DB_URL

# Database URL
# For development, we'll use a local SQLite database.
# You can later change this to PostgreSQL, MySQL, etc., using environment variables.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./database.db")

# Create an async engine for SQLModel
engine = create_async_engine(DATABASE_URL, echo=True)

# Define the ScrapedContent model
class ScrapedContent(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    url: str
    title: str | None = None
    content: str | None = None
    scraped_at: datetime = Field(default_factory=datetime.utcnow) # Automatically sets current UTC time

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