from main import app


def test_all_routers_registered():
    paths = set(app.openapi()["paths"].keys())
    for prefix in ["/workouts", "/exercises", "/agonists"]:
        assert any(path.startswith(prefix) for path in paths), prefix
