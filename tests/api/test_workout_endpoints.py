from fastapi.testclient import TestClient
from uuid6 import uuid7

from main import app

client = TestClient(app=app)


class TestWorkoutEndpoints:
    def test_read_workout_not_found_error(self):
        response = client.get(f"/workouts/{str(uuid7())}")
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

    def test_remove_workout_set(self):
        # Create workout with workout set
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

        # Delete workout set
        response = client.get(f"/workouts/{workout_id}")
        workout: dict = response.json()
        sets: dict = workout.get("sets", [])

        workout_set_id = sets[0].get("id")

        response = client.delete(f"/workouts/{workout_id}/sets/{workout_set_id}")
        assert response.status_code == 204

        # Assert that workout set deleted
        response = client.get(f"/workouts/{workout_id}")
        workout: dict = response.json()
        sets = workout.get("sets", [])

        assert sets == []
