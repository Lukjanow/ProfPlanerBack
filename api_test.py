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
                           {"roomNumber": "TestRoom", "capacity": 100, "roomType": "Labor"}
                        )
    assert response.status_code == 200


def test_update_room():
    global room_id
    response = client.post("/room/add", json=
                           {"roomNumber": "TestRoom", "capacity": 100, "roomType": "Vorlesung"}
                        )
    
    room_id = response.json()["_id"]
    
    print(response.text)
    assert response.status_code == 200

    response = client.put(f"/room/{room_id}",json={"roomNumber":"N43"})
    print(response.text)
    assert response.status_code == 200, "Name konnte nicht geupdatet werden"

    response = client.put(f"/room/{room_id}",json={"capacity":101})
    print(response.text)
    assert response.status_code == 200, "Kapazität konnte nicht geupdatet werden"

    response = client.put(f"/room/{room_id}",json={"roomType":"Labor"})
    print(response.text)
    assert response.status_code == 200, "RoomType konnte nicht geupdatet werden"


def test_delete_room():
    global room_id

    response = client.delete(f"/room/{room_id}")
    assert response.status_code == 200, "Raum konnte nicht gelöscht werden"

    
