import pytest
import os
from app import create_app, setup_database
import json


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


# TODO:
# - add tests for update_author, assign_author_to_joke and get_author
# - rewrite this test so I don't test on the actual db (maybe use pytest-postgresql for that)
def test_add_author_and_delete_author(client):
    res = client.post(
        "/author",
        data=json.dumps({"firstname": "Bob", "lastname": "Fischer"}),
        headers={"Content-Type": "application/json"}
    )
    assert res.status_code == 201
    assert res.json["firstname"] == "Bob"
    assert res.json["lastname"] == "Fischer"

    author_id = res.json["id"]
    res = client.delete(f"/author/{author_id}")
    assert res.status_code == 200
    assert res.json["firstname"] == "Bob"
    assert res.json["lastname"] == "Fischer"


def test_get_all_authors(client):
    res = client.get("/author")
    assert res.status_code == 200
