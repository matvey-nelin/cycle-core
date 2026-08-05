from fastapi.testclient import TestClient
from uuid_extensions import uuid7

from main import app

client = TestClient(app=app)


class TestWorkoutEndpoints:
    def test_read_workout_not_found_error(self):
        id = str(uuid7())
        response = client.get(f"/workouts/{id}")
        assert response.status_code == 404

    def test_create_workout(self):
        response = client.post(
            "/workouts",
            json={
                "start_time": "2026-08-01T15:00:00+00:00",
                "end_time": "2026-08-01T16:00:00+00:00",
            },
        )
        assert response.status_code == 201

    def test_read_workout(self):
        response = client.post(
            "/workouts",
            json={
                "start_time": "2026-08-01T15:00:00+00:00",
                "end_time": "2026-08-01T16:00:00+00:00",
            },
        )
        assert response.status_code == 201

        workout_id = response.json()["workout_id"]
        response = client.get(f"/workouts/{workout_id}")
        assert response.status_code == 200

    def test_create_workout_set(self):
        response = client.post(
            "/workouts",
            json={
                "start_time": "2026-08-01T15:00:00+00:00",
                "end_time": "2026-08-01T16:00:00+00:00",
            },
        )

        workout_id = response.json()["workout_id"]
        response = client.post(
            f"/workouts/{workout_id}/sets",
            json={"exercise_id": str(uuid7()), "reps": 12, "weight": 60},
        )

        assert response.status_code == 201

        response = client.get(f"/workouts/{workout_id}")
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
