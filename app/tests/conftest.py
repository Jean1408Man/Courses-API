import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from app.main import app
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db.database import get_db, Base

# Config DB para testing
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/mydb"


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="function")
async def db_session():
    test_engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)
    TestingSessionLocal = sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture(autouse=True, scope="function")
async def override_get_db(db_session):
    async def _override():
        yield db_session
    app.dependency_overrides[get_db] = _override
    yield
    app.dependency_overrides.clear()


@pytest.fixture()
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture()
def unique_user_data():
    """Genera datos únicos para usuario"""
    uid = uuid.uuid4().hex[:8]
    return {
        "username": f"user_{uid}",
        "email": f"{uid}@test.com",
        "password": "testpassword"
    }


@pytest.fixture()
async def register_and_login_user(async_client, unique_user_data):
    """
    Crea un usuario y devuelve headers con token listo para autenticación.
    """
    # Registro
    response = await async_client.post("/auth/register", json=unique_user_data)
    assert response.status_code == 200, response.text

    # Login
    login_data = {
        "username": unique_user_data["email"],  # 👈 este cambio
        "password": unique_user_data["password"]
    }

    response = await async_client.post("/auth/login", data=login_data)
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    return headers
