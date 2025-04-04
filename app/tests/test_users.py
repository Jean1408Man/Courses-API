import pytest
import uuid


@pytest.mark.anyio
async def test_get_own_profile(async_client, register_and_login_user):
    headers = register_and_login_user
    response = await async_client.get("/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    assert "id" in data


@pytest.mark.anyio
async def test_get_all_users(async_client, register_and_login_user):
    headers = register_and_login_user
    response = await async_client.get("/users/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.anyio
async def test_get_user_by_id(async_client, register_and_login_user):
    headers = register_and_login_user
    me_response = await async_client.get("/users/me", headers=headers)
    user_id = me_response.json()["id"]

    response = await async_client.get(f"/users/{user_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id


@pytest.mark.anyio
async def test_update_user(async_client, register_and_login_user):
    headers = register_and_login_user
    me_response = await async_client.get("/users/me", headers=headers)
    user_data = me_response.json()
    user_id = user_data["id"]

    update_data = {
        "username": user_data["username"],
        "email": user_data["email"],
        "password": "testpassword"
    }
    response = await async_client.put(f"/users/{user_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]


@pytest.mark.anyio
async def test_delete_user(async_client, register_and_login_user):
    headers = register_and_login_user
    me_response = await async_client.get("/users/me", headers=headers)
    user_id = me_response.json()["id"]

    response = await async_client.delete(f"/users/{user_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["detail"] == "Usuario eliminado"


@pytest.mark.anyio
async def test_update_other_user_forbidden(async_client, register_and_login_user):
    # Crear segundo usuario único
    uid = uuid.uuid4().hex[:8]
    second_user_data = {
        "username": f"user_{uid}",
        "email": f"{uid}@test.com",
        "password": "testpassword"
    }
    second_user_response = await async_client.post("/auth/register", json=second_user_data)
    assert second_user_response.status_code == 200
    second_user_id = second_user_response.json()["id"]

    headers = register_and_login_user
    update_data = {
        "username": second_user_data["username"],
        "email": second_user_data["email"],
        "password": "testpassword"
    }
    response = await async_client.put(f"/users/{second_user_id}", json=update_data, headers=headers)
    assert response.status_code == 403


@pytest.mark.anyio
async def test_delete_other_user_forbidden(async_client, register_and_login_user):
    # Crear segundo usuario único
    uid = uuid.uuid4().hex[:8]
    second_user_data = {
        "username": f"user_{uid}",
        "email": f"{uid}@test.com",
        "password": "testpassword"
    }
    second_user_response = await async_client.post("/auth/register", json=second_user_data)
    assert second_user_response.status_code == 200
    second_user_id = second_user_response.json()["id"]

    headers = register_and_login_user
    response = await async_client.delete(f"/users/{second_user_id}", headers=headers)
    assert response.status_code == 403