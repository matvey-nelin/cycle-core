from uuid6 import uuid7


class TestWorkoutEndpoints:
    async def test_create_workout(self, client):
        response = await client.post(
            "/workouts",
            json={
                "start_time": "2026-08-01T15:00:00+00:00",
                "end_time": "2026-08-01T16:00:00+00:00",
            },
        )
        assert response.status_code == 201

    async def test_create_workout_with_incorrect_workout_times_error(self, client):
        response = await client.post(
            "/workouts",
            json={"start_time": "2026-08-01T16:00:00+00:00", "end_time": "2026-08-01T15:00:00+00:00"},
        )
        assert response.status_code == 422

    async def test_read_workout(self, client):
        response = await client.post(
            "/workouts",
            json={
                "start_time": "2026-08-01T15:00:00+00:00",
                "end_time": "2026-08-01T16:00:00+00:00",
            },
        )
        assert response.status_code == 201

        workout_id = response.json()["workout_id"]
        response = await client.get(f"/workouts/{workout_id}")
        assert response.status_code == 200

    async def test_read_workout_with_workout_not_found_error(self, client):
        response = await client.get(f"/workouts/{str(uuid7())}")
        assert response.status_code == 404

    async def test_create_workout_set(self, client):
        workout_response = await client.post(
            "/workouts",
            json={
                "start_time": "2026-08-01T15:00:00+00:00",
                "end_time": "2026-08-01T16:00:00+00:00",
            },
        )
        assert workout_response.status_code == 201

        exercise_response = await client.post(
            "/exercises",
            json={"name": "Squat"},
        )
        assert exercise_response.status_code == 201

        workout_id = workout_response.json()["workout_id"]
        exercise_id = exercise_response.json()["exercise_id"]

        response = await client.post(
            f"/workouts/{workout_id}/sets",
            json={"exercise_id": exercise_id, "reps": 12, "weight": 60},
        )
        assert response.status_code == 201

        response = await client.get(f"/workouts/{workout_id}")
        workout: dict = response.json()
        sets: dict = workout.get("sets", [])

        assert response.status_code == 200

        assert workout.get("planned_start_time", None) == "2026-08-01T15:00:00Z"
        assert workout.get("planned_end_time", None) == "2026-08-01T16:00:00Z"
        assert workout.get("actual_start_time", None) == "2026-08-01T15:00:00Z"
        assert workout.get("actual_end_time", None) == "2026-08-01T16:00:00Z"

        assert sets[0].get("planned_tonnage", None) == 720.0
        assert sets[0].get("actual_tonnage", None) == 720.0
        assert sets[0].get("completion_percentage", None) == 100.00

    async def test_create_workout_set_with_workout_not_found_error(self, client):
        exercise_response = await client.post(
            "/exercises",
            json={"name": "Squat"},
        )
        assert exercise_response.status_code == 201

        workout_id = str(uuid7())
        exercise_id = exercise_response.json()["exercise_id"]

        response = await client.post(
            f"/workouts/{workout_id}/sets",
            json={"exercise_id": exercise_id, "reps": 12, "weight": 60},
        )
        assert response.status_code == 404

    async def test_create_workout_set_with_exercise_not_found_error(self, client):
        response = await client.post(
            "/workouts",
            json={
                "start_time": "2026-08-01T15:00:00+00:00",
                "end_time": "2026-08-01T16:00:00+00:00",
            },
        )
        assert response.status_code == 201

        workout_id = response.json()["workout_id"]
        response = await client.post(
            f"/workouts/{workout_id}/sets",
            json={"exercise_id": str(uuid7()), "reps": 12, "weight": 60},
        )
        assert response.status_code == 404

    async def test_remove_workout_set(self, client):
        # Create workout with workout set
        workout_response = await client.post(
            "/workouts",
            json={
                "start_time": "2026-08-01T15:00:00+00:00",
                "end_time": "2026-08-01T16:00:00+00:00",
            },
        )
        assert workout_response.status_code == 201

        exercise_response = await client.post(
            "/exercises",
            json={"name": "Squat"},
        )
        assert exercise_response.status_code == 201

        workout_id = workout_response.json()["workout_id"]
        exercise_id = exercise_response.json()["exercise_id"]

        response = await client.post(
            f"/workouts/{workout_id}/sets",
            json={"exercise_id": exercise_id, "reps": 12, "weight": 60},
        )
        assert response.status_code == 201

        workout_set_id = response.json()["workout_set_id"]
        response = await client.delete(f"/workouts/{workout_id}/sets/{workout_set_id}")
        assert response.status_code == 204

        # Assert that workout set deleted
        response = await client.get(f"/workouts/{workout_id}")
        workout: dict = response.json()
        sets = workout.get("sets", [])

        assert sets == []

    async def test_remove_workout_set_with_workout_not_found(self, client):
        workout_response = await client.post(
            "/workouts",
            json={
                "start_time": "2026-08-01T15:00:00+00:00",
                "end_time": "2026-08-01T16:00:00+00:00",
            },
        )
        assert workout_response.status_code == 201

        exercise_response = await client.post(
            "/exercises",
            json={"name": "Squat"},
        )
        assert exercise_response.status_code == 201

        workout_id = workout_response.json()["workout_id"]
        exercise_id = exercise_response.json()["exercise_id"]

        response = await client.post(
            f"/workouts/{workout_id}/sets",
            json={"exercise_id": exercise_id, "reps": 12, "weight": 60},
        )
        assert response.status_code == 201

        workout_set_id = response.json()["workout_set_id"]
        response = await client.delete(f"/workouts/{str(uuid7())}/sets/{workout_set_id}")
        assert response.status_code == 404

    async def test_remove_workout_set_with_incorrect_workout_set_id_error(self, client):
        workout_response = await client.post(
            "/workouts",
            json={
                "start_time": "2026-08-01T15:00:00+00:00",
                "end_time": "2026-08-01T16:00:00+00:00",
            },
        )
        assert workout_response.status_code == 201

        exercise_response = await client.post(
            "/exercises",
            json={"name": "Squat"},
        )
        assert exercise_response.status_code == 201

        workout_id = workout_response.json()["workout_id"]
        exercise_id = exercise_response.json()["exercise_id"]

        response = await client.post(
            f"/workouts/{workout_id}/sets",
            json={"exercise_id": exercise_id, "reps": 12, "weight": 60},
        )
        assert response.status_code == 201

        response = await client.delete(f"/workouts/{workout_id}/sets/{str(uuid7())}")
        assert response.status_code == 404
