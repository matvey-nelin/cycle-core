from uuid6 import uuid7


class TestAgonistEndpoints:
    async def test_create_agonist(self, client):
        response = await client.post(
            "/agonists",
            json={"name": "Pectoralis major"},
        )
        assert response.status_code == 201

    async def test_create_agonist_with_incorrect_agonist_name_error(self, client):
        response = await client.post(
            "/agonists",
            json={"name": ""},
        )
        assert response.status_code == 422

    async def test_read_agonist(self, client):
        response = await client.post(
            "/agonists",
            json={"name": "Pectoralis major"},
        )
        assert response.status_code == 201

        agonist_id = response.json()["agonist_id"]
        response = await client.get(
            f"/agonists/{agonist_id}",
        )
        assert response.status_code == 200
        assert response.json()["id"] == agonist_id
        assert response.json()["name"] == "Pectoralis major"

    async def test_read_agonist_with_agonist_not_found_error(self, client):
        agonist_id = str(uuid7())
        response = await client.get(
            f"/agonists/{agonist_id}",
        )
        assert response.status_code == 404

    async def test_update_agonist(self, client):
        response = await client.post("/agonists", json={"name": "Pectoralis major"})
        assert response.status_code == 201

        agonist_id = response.json()["agonist_id"]
        response = await client.patch(f"/agonists/{agonist_id}", json={"name": "Pectoralis minor"})
        assert response.status_code == 204

        response = await client.get(
            f"/agonists/{agonist_id}",
        )
        assert response.status_code == 200
        assert response.json()["id"] == agonist_id
        assert response.json()["name"] == "Pectoralis minor"

    async def test_update_agonist_with_agonist_not_found_error(self, client):
        agonist_id = str(uuid7())
        response = await client.patch(f"/agonists/{agonist_id}", json={"name": "Pectoralis minor"})
        assert response.status_code == 404
