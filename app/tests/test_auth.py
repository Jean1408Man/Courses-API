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


@pytest.mark.anyio
async def test_register_with_duplicate_email(async_client, unique_user_data):
    await async_client.post("/auth/register", json=unique_user_data)
    response = await async_client.post("/auth/register", json=unique_user_data)
    assert response.status_code == 400


@pytest.mark.anyio
async def test_login_with_wrong_password(async_client, unique_user_data):
    await async_client.post("/auth/register", json=unique_user_data)

    login_data = {
        "username": unique_user_data["email"],
        "password": "wrongpassword"
    }
    response = await async_client.post("/auth/login", data=login_data)
    assert response.status_code == 401


@pytest.mark.anyio
async def test_login_with_nonexistent_user(async_client):
    login_data = {
        "username": "nonexistent@example.com",
        "password": "any-password"
    }
    response = await async_client.post("/auth/login", data=login_data)
    assert response.status_code == 401


@pytest.mark.anyio
async def test_login_with_missing_fields(async_client):
    response = await async_client.post("/auth/login", data={})
    assert response.status_code == 422
