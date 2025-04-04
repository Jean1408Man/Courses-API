import pytest


@pytest.mark.anyio
async def test_register_user(async_client, unique_user_data):
    response = await async_client.post("/auth/register", json=unique_user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == unique_user_data["email"]
    assert "id" in data


@pytest.mark.anyio
async def test_login_user(async_client, unique_user_data):
    # Registrar usuario primero
    await async_client.post("/auth/register", json=unique_user_data)

    # Login con email (requerido por OAuth2PasswordRequestForm)
    login_data = {
        "username": unique_user_data["email"],
        "password": unique_user_data["password"]
    }
    response = await async_client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
