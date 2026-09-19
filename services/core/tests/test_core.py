import pytest

pytestmark = pytest.mark.asyncio(loop_scope="session")


async def test_health(client):
    r = await client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["plugins"]["aos-domain-sis"] == "active"


async def test_register_login_me(client):
    r = await client.post("/api/v1/auth/register", json={
        "email": "ana@gdesigner.school", "password": "Segredo123", "first_name": "Ana", "last_name": "Kianda",
        "role": "student"})
    assert r.status_code == 201, r.text
    r = await client.post("/api/v1/auth/login/json", json={"email": "ana@gdesigner.school", "password": "Segredo123"})
    assert r.status_code == 200
    tok = r.json()
    r = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {tok['access_token']}"})
    assert r.json()["email"] == "ana@gdesigner.school"
    # plugin notify reagiu ao evento auth.user.registered
    r = await client.get("/api/v1/notifications", headers={"Authorization": f"Bearer {tok['access_token']}"})
    assert r.json()["total"] == 1
    assert r.json()["items"][0]["title"] == "Bem-vindo ao AOS"
    # refresh com rotação
    r = await client.post("/api/v1/auth/refresh", json={"refresh_token": tok["refresh_token"]})
    assert r.status_code == 200
    r = await client.post("/api/v1/auth/refresh", json={"refresh_token": tok["refresh_token"]})
    assert r.status_code == 401


async def test_rbac_and_users(client, auth):
    r = await client.get("/api/v1/users", headers=auth)
    assert r.status_code == 200 and r.json()["total"] >= 2
    r = await client.get("/api/v1/users")
    assert r.status_code == 401


async def test_plugins_registry(client, auth):
    r = await client.get("/api/v1/plugins", headers=auth)
    slugs = {p["slug"] for p in r.json()}
    assert {"aos-core-notify", "aos-domain-sis"} <= slugs
    r = await client.get("/api/v1/plugins/registry", headers=auth)
    assert "sis.enrollment.validate" in r.json()["filters"]
    assert any(n["href"] == "/sis/courses" for n in r.json()["nav"])


async def test_sis_flow_with_events(client, auth):
    r = await client.post("/api/v1/sis/courses", headers=auth, json={
        "code": "UX101", "name": "Fundamentos de UX", "credits": 6, "capacity": 1})
    assert r.status_code == 201, r.text
    course_id = r.json()["id"]
    # aluna matricula-se
    r = await client.post("/api/v1/auth/login/json", json={"email": "ana@gdesigner.school", "password": "Segredo123"})
    stud = {"Authorization": f"Bearer {r.json()['access_token']}"}
    r = await client.post("/api/v1/sis/enrollments", headers=stud, json={"course_id": course_id})
    assert r.status_code == 201, r.text
    # notificação gerada pelo plugin notify via evento sis.student.enrolled
    r = await client.get("/api/v1/notifications", headers=stud)
    assert any(n["title"] == "Matrícula confirmada" for n in r.json()["items"])
    # capacidade 1 → segundo aluno bloqueado pelo filter
    await client.post("/api/v1/auth/register", json={"email": "b@gdesigner.school", "password": "Segredo123",
                                                     "first_name": "Bento", "last_name": "Sousa"})
    r = await client.post("/api/v1/sis/enrollments", headers=auth, json={"course_id": course_id, "student_id": (
        await client.get("/api/v1/users", headers=auth, params={"search": "b@"})).json()["items"][0]["id"]})
    assert r.status_code == 400 and "lotada" in r.json()["detail"]
    # eventos ficaram no event store
    r = await client.get("/api/v1/events/recent", headers=auth)
    types = [e["type"] for e in r.json()]
    assert "sis.student.enrolled" in types and "sis.course.created" in types
    # audit middleware registou mutações
    r = await client.get("/api/v1/audit-logs", headers=auth, params={"resource": "sis"})
    assert r.json()["total"] >= 1


async def test_settings(client, auth):
    r = await client.put("/api/v1/settings/academic.min_grade", headers=auth, json={"value": 10, "type": "int"})
    assert r.status_code == 200
    r = await client.get("/api/v1/settings/academic.min_grade", headers=auth)
    assert r.json()["value"] == 10
