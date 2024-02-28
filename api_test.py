import re
import pytest
from fastapi.testclient import TestClient
from API import app  # import your FastAPI app

# Setup TestClient for FastAPI
client = TestClient(app)
room_id = ""

# Test for the index route
def test_index():
    response = client.get("/docs")
    assert response.status_code == 200
    #assert "items" in response.json()


#------------------------ Room Tests ---------------------------#

def test_create_room():
    response = client.post("/room/add", json=
                           {"name": "TestRoom", "capacity": 100, "equipment": 1}
                        )
    assert response.status_code == 200


def test_update_room():
    global room_id
    response = client.post("/room/add", json=
                           {"_id": "", "name": "TestRoom", "capacity": 100, "equipment": 1}
                        )
    
    object_id_pattern = re.compile(r"ObjectId\('(\w+)'\)")
    match = object_id_pattern.search(response.json()["message"])
    room_id = match.group(1)
    
    print(response.text)
    assert response.status_code == 200

    response = client.put(f"/room/{room_id}",json={"name":"N43"})
    print(response.text)
    assert response.status_code == 200, "Name konnte nicht geupdatet werden"

    response = client.put(f"/room/{room_id}",json={"capacity":101})
    print(response.text)
    assert response.status_code == 200, "Kapazität konnte nicht geupdatet werden"

    response = client.put(f"/room/{room_id}",json={"equipment":2})
    print(response.text)
    assert response.status_code == 200, "Equipment konnte nicht geupdatet werden"


def test_delete_room():
    global room_id

    response = client.delete(f"/room/{room_id}")
    assert response.status_code == 200, "Raum konnte nicht gelöscht werden"

    
