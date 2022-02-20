import pytest
import os
from app import create_app, setup_database


app = create_app()
if not os.path.isdir(os.getenv("DATABASE_LOCAL_PATH")):
    setup_database(app)


@pytest.fixture
def client():
    return app.test_client()


def test_joke_random(client):
    res = client.get("/joke")
    assert res.status_code == 200
    assert "id" in res.json.keys()
    assert "value" in res.json.keys()


def test_joke_random_reverse(client):
    res = client.get("/joke")
    assert res.status_code == 200
    assert "id" in res.json.keys()
    assert "value" in res.json.keys()


def test_joke_id(client):
    res = client.get("/joke/a7G4M0EuRXiGa79XllTcKA")
    assert res.status_code == 200
    assert res.json["id"] == "a7G4M0EuRXiGa79XllTcKA"
    assert res.json["value"] == "Chuck Norris can beat anybody in a staring contest... with his eyes closed"


def test_joke_id_reverse(client):
    res = client.get("/joke/a7G4M0EuRXiGa79XllTcKA/reverse")
    assert res.status_code == 200
    assert res.json["id"] == "a7G4M0EuRXiGa79XllTcKA"
    assert res.json["value"] == "kcuhC sirroN nac taeb ydobyna ni a gnirats tsetnoc... htiw sih seye desolc"

