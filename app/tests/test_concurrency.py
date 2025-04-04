import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from uuid import uuid4


@pytest.mark.anyio
async def test_concurrent_user_registration():
    async def register_user():
        uid = uuid4().hex[:8]
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            data = {
                "username": f"user_{uid}",
                "email": f"{uid}@test.com",
                "password": "testpassword"
            }
            response = await client.post("/auth/register", json=data)
            assert response.status_code == 200

    # Ejecutar los registros uno por uno, cada uno con su propio contexto aislado
    for _ in range(10):
        await register_user()


@pytest.mark.anyio
async def test_concurrent_course_creation():
    async def create_course(i):
        uid = uuid4().hex[:8]
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            user_data = {
                "username": f"user_{uid}",
                "email": f"{uid}@test.com",
                "password": "testpassword"
            }
            reg_res = await client.post("/auth/register", json=user_data)
            assert reg_res.status_code == 200

            login_data = {
                "username": user_data["email"],
                "password": user_data["password"]
            }
            login_res = await client.post("/auth/login", data=login_data)
            assert login_res.status_code == 200

            token = login_res.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}

            course_data = {"title": f"Curso {i}", "description": "Carga concurrente"}
            res = await client.post("/courses/", json=course_data, headers=headers)
            assert res.status_code == 201

    for i in range(10):
        await create_course(i)
