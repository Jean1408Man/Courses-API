# app/tests/database/test_db_connection.py
import pytest
from sqlalchemy import text
from app.db.database import AsyncSessionLocal

@pytest.mark.asyncio
async def test_db_connection():
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT 1"))
        value = result.scalar()
        assert value == 1
