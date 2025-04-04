import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_create_course(async_client, register_and_login_user):
    headers = register_and_login_user
    payload = {"title": "Curso de Python", "description": "Aprende FastAPI"}

    response = await async_client.post("/courses/", json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json()["title"] == "Curso de Python"


@pytest.mark.anyio
async def test_get_all_courses(async_client, register_and_login_user):
    headers = register_and_login_user
    response = await async_client.get("/courses/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.anyio
async def test_get_course_by_id(async_client, register_and_login_user):
    headers = register_and_login_user
    # Crear curso
    create = await async_client.post("/courses/", json={"title": "X", "description": "Y"}, headers=headers)
    course_id = create.json()["id"]

    response = await async_client.get(f"/courses/{course_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == course_id


@pytest.mark.anyio
async def test_update_course(async_client, register_and_login_user):
    headers = register_and_login_user
    create = await async_client.post("/courses/", json={"title": "X", "description": "Y"}, headers=headers)
    course_id = create.json()["id"]

    updated_data = {"title": "Nuevo Titulo"}
    response = await async_client.put(f"/courses/{course_id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Nuevo Titulo"


@pytest.mark.anyio
async def test_delete_course(async_client, register_and_login_user):
    headers = register_and_login_user
    create = await async_client.post("/courses/", json={"title": "X", "description": "Y"}, headers=headers)
    course_id = create.json()["id"]

    response = await async_client.delete(f"/courses/{course_id}", headers=headers)
    assert response.status_code == 200


@pytest.mark.anyio
async def test_enroll_in_course(async_client, register_and_login_user):
    headers = register_and_login_user
    create = await async_client.post("/courses/", json={"title": "X", "description": "Y"}, headers=headers)
    course_id = create.json()["id"]

    response = await async_client.post(f"/courses/{course_id}/enroll", headers=headers)
    assert response.status_code == 200
    assert "Inscrito en el curso" in response.json()["message"]


@pytest.mark.anyio
async def test_get_my_courses(async_client, register_and_login_user):
    headers = register_and_login_user
    # Crear y enrolar curso
    create = await async_client.post("/courses/", json={"title": "Curso MIO", "description": "Propio"}, headers=headers)
    course_id = create.json()["id"]
    await async_client.post(f"/courses/{course_id}/enroll", headers=headers)

    response = await async_client.get("/courses/me", headers=headers)
    assert response.status_code == 200
    assert any(c["id"] == course_id for c in response.json())
