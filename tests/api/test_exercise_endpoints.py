from uuid6 import uuid7


class TestExerciseEndpoints:
    async def test_create_exercise(self, client):
        response = await client.post(
            "/exercises",
            json={"name": "Squat"},
        )
        assert response.status_code == 201

    async def test_create_exercise_with_incorrect_exercise_name_error(self, client):
        response = await client.post(
            "/exercises",
            json={"name": ""},
        )
        assert response.status_code == 422

    async def test_read_exercise(self, client):
        response = await client.post(
            "/exercises",
            json={"name": "Squat"},
        )
        assert response.status_code == 201

        exercise_id = response.json()["exercise_id"]
        response = await client.get(
            f"/exercises/{exercise_id}",
        )
        assert response.status_code == 200
        assert response.json()["id"] == exercise_id
        assert response.json()["name"] == "Squat"
        assert response.json()["agonist_ids"] == []

    async def test_read_exercise_with_exercise_not_found_error(self, client):
        exercise_id = str(uuid7())
        response = await client.get(
            f"/exercises/{exercise_id}",
        )
        assert response.status_code == 404

    async def test_update_exercise(self, client):
        response = await client.post("/exercises", json={"name": "Squat"})
        assert response.status_code == 201

        exercise_id = response.json()["exercise_id"]
        response = await client.patch(f"/exercises/{exercise_id}", json={"name": "Bench press"})
        assert response.status_code == 204

        response = await client.get(
            f"/exercises/{exercise_id}",
        )
        assert response.status_code == 200
        assert response.json()["id"] == exercise_id
        assert response.json()["name"] == "Bench press"

    async def test_update_exercise_with_exercise_not_found_error(self, client):
        exercise_id = str(uuid7())
        response = await client.patch(f"/exercises/{exercise_id}", json={"name": "Squat"})
        assert response.status_code == 404

    async def test_add_agonist(self, client):
        exercise_response = await client.post("/exercises", json={"name": "Bench press"})
        assert exercise_response.status_code == 201

        agonist_response = await client.post(
            "/agonists",
            json={"name": "Pectoralis major"},
        )
        assert agonist_response.status_code == 201

        exercise_id = exercise_response.json()["exercise_id"]
        agonist_id = agonist_response.json()["agonist_id"]

        response = await client.post(
            f"/exercises/{exercise_id}/agonists/{agonist_id}",
        )
        assert response.status_code == 204

        exercise = (await client.get(f"/exercises/{exercise_id}")).json()
        assert exercise["agonist_ids"] == [agonist_id]

    async def test_add_agonist_with_exercise_not_found_error(self, client):
        agonist_response = await client.post(
            "/agonists",
            json={"name": "Pectoralis major"},
        )
        assert agonist_response.status_code == 201

        exercise_id = str(uuid7())
        agonist_id = agonist_response.json()["agonist_id"]

        response = await client.post(
            f"/exercises/{exercise_id}/agonists/{agonist_id}",
        )
        assert response.status_code == 404

    async def test_add_agonist_with_agonist_not_found_error(self, client):
        exercise_response = await client.post("/exercises", json={"name": "Bench press"})
        assert exercise_response.status_code == 201

        exercise_id = exercise_response.json()["exercise_id"]
        agonist_id = str(uuid7())

        response = await client.post(
            f"/exercises/{exercise_id}/agonists/{agonist_id}",
        )
        assert response.status_code == 404

    async def test_add_agonist_with_duplicate_agonist_id_error(self, client):
        exercise_response = await client.post("/exercises", json={"name": "Bench press"})
        assert exercise_response.status_code == 201

        agonist_response = await client.post(
            "/agonists",
            json={"name": "Pectoralis major"},
        )
        assert agonist_response.status_code == 201

        exercise_id = exercise_response.json()["exercise_id"]
        agonist_id = agonist_response.json()["agonist_id"]

        response = await client.post(
            f"/exercises/{exercise_id}/agonists/{agonist_id}",
        )
        assert response.status_code == 204

        response = await client.post(
            f"/exercises/{exercise_id}/agonists/{agonist_id}",
        )
        assert response.status_code == 409

    async def test_remove_agonist(self, client):
        exercise_response = await client.post("/exercises", json={"name": "Bench press"})
        assert exercise_response.status_code == 201

        agonist_response = await client.post(
            "/agonists",
            json={"name": "Pectoralis major"},
        )
        assert agonist_response.status_code == 201

        exercise_id = exercise_response.json()["exercise_id"]
        agonist_id = agonist_response.json()["agonist_id"]

        response = await client.post(
            f"/exercises/{exercise_id}/agonists/{agonist_id}",
        )
        assert response.status_code == 204

        response = await client.delete(f"/exercises/{exercise_id}/agonists/{agonist_id}")
        assert response.status_code == 204

        exercise = (await client.get(f"/exercises/{exercise_id}")).json()
        assert exercise["agonist_ids"] == []

    async def test_remove_agonist_with_exercise_not_found_error(self, client):
        exercise_response = await client.post("/exercises", json={"name": "Bench press"})
        assert exercise_response.status_code == 201

        agonist_response = await client.post(
            "/agonists",
            json={"name": "Pectoralis major"},
        )
        assert agonist_response.status_code == 201

        exercise_id = exercise_response.json()["exercise_id"]
        agonist_id = agonist_response.json()["agonist_id"]

        response = await client.post(
            f"/exercises/{exercise_id}/agonists/{agonist_id}",
        )
        assert response.status_code == 204

        response = await client.delete(f"/exercises/{str(uuid7())}/agonists/{agonist_id}")
        assert response.status_code == 404

    async def test_remove_agonist_with_non_existent_agonist_id_error(self, client):
        exercise_response = await client.post("/exercises", json={"name": "Bench press"})
        assert exercise_response.status_code == 201

        agonist_response = await client.post(
            "/agonists",
            json={"name": "Pectoralis major"},
        )
        assert agonist_response.status_code == 201

        exercise_id = exercise_response.json()["exercise_id"]
        agonist_id = agonist_response.json()["agonist_id"]

        response = await client.post(
            f"/exercises/{exercise_id}/agonists/{agonist_id}",
        )
        assert response.status_code == 204

        response = await client.delete(f"/exercises/{exercise_id}/agonists/{str(uuid7())}")
        assert response.status_code == 404

    async def test_read_exercise_full_graph(self, client):
        exercise_response = await client.post("/exercises", json={"name": "Bench press"})
        assert exercise_response.status_code == 201

        agonist_response2 = await client.post(
            "/agonists",
            json={"name": "Pectoralis minor"},
        )
        assert agonist_response2.status_code == 201

        agonist_response1 = await client.post(
            "/agonists",
            json={"name": "Pectoralis major"},
        )
        assert agonist_response1.status_code == 201

        exercise_id = exercise_response.json()["exercise_id"]
        agonist_id2 = agonist_response2.json()["agonist_id"]
        agonist_id1 = agonist_response1.json()["agonist_id"]

        response = await client.post(
            f"/exercises/{exercise_id}/agonists/{agonist_id2}",
        )
        assert response.status_code == 204

        response = await client.post(
            f"/exercises/{exercise_id}/agonists/{agonist_id1}",
        )
        assert response.status_code == 204

        response = await client.get(
            f"/exercises/{exercise_id}",
        )
        assert response.status_code == 200
        assert response.json()["id"] == exercise_id
        assert response.json()["name"] == "Bench press"
        assert response.json()["agonist_ids"] == [agonist_id1, agonist_id2]
