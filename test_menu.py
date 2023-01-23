import pytest
from main import app
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    client = TestClient(app)
    yield client


def test_get_menus(client):
    response = client.get("/api/v1/menus")
    assert response.status_code == 200
    print(response)


def test_one_menu(client):
    response = client.get("/api/v1/menus/0")
    if response.status_code == 404:
        assert response.json() == {'detail': 'menu not found'}
    else:
        assert response.status_code == 200
    print(response)


def test_create_menu(client):
    response = client.post("/api/v1/menus", json={"title": "My menu 1", "description": "My menu description 1"})
    if response.status_code == 404:
        assert response.json() == {"detail": "menu already exists"}
    print(response)

def test_update_menu(client):
    response = client.patch("/api/v1/menus/0",
                            json={"title": "My updated menu 1", "description": "My updated menu description 1"})
    if response.status_code == 404:
        assert response.json() == {"detail": "menu not found"}
    print(response)


def test_delete_menu(client):
    response = client.delete("/api/v1/menus/0")
    if response.status_code == 404:
        assert response.json() == {"detail": "menu not found"}
    if response.status_code == 200:
        assert response.json() == {"status": True, "message": "The menu has been deleted"}
    print(response)

def test_get_submenus(client):
    response = client.get("/api/v1/menus/0/submenus")
    assert response.status_code == 200
    print(response)

def test_one_submenu(client):
    response = client.get("/api/v1/menus/0/submenus/0")
    if response.status_code == 404:
        assert response.json() == {'detail': 'submenu not found'}
    else:
        assert response.status_code == 200
    print(response)

def test_create_submenu(client):
    test_create_menu(client)
    response = client.post("/api/v1/menus/0/submenus",json={"title": "My submenu 1","description": "My submenu description 1"})
    if response.status_code == 404:
        assert response.json() == {"detail": "submenu already exists"}
    print(response)

def test_update_submenu(client):
    response = client.patch("/api/v1/menus/0/submenus/0",
                            json={"title": "My updated submenu 1", "description": "My updated submenu description 1"})
    if response.status_code == 404:
        assert response.json() == {"detail": "submenu not found"}
    print(response)

def test_delete_submenu(client):
    response = client.delete("/api/v1/menus/0/submenus/0")
    if response.status_code == 404:
        assert response.json() == {"detail": "submenu not found"}
    if response.status_code == 200:
        assert response.json() == {"status": True, "message": "The submenu has been deleted"}
    print(response)

def test_get_dish(client):
    response = client.get("/api/v1/menus/0/submenus/0/dishes")
    assert response.status_code == 200
    print(response)

def test_one_dish(client):
    response = client.get("/api/v1/menus/0/submenus/0/dishes/0")
    if response.status_code == 404:
        assert response.json() == {'detail': 'dish not found'}
    else:
        assert response.status_code == 200
    print(response)

def test_create_dish(client):
    test_create_submenu(client)
    response = client.post("/api/v1/menus/0/submenus/0/dishes",json={"title": "My dish 1",
                                                                     "description": "My dish description 1",
                                                                     "price":"12.50"})
    if response.status_code == 404:
        assert response.json() == {"detail": "dish already exists"}
    print(response)

def test_update_dish(client):
    response = client.patch("/api/v1/menus/0/submenus/0/dishes/0",
                            json={"title": "My updated submenu 1",
                                  "description": "My updated submenu description 1",
                                  "price":"14.50"})
    if response.status_code == 404:
        assert response.json() == {"detail": "dish not found"}
    print(response)

def test_delete_dish(client):
    response = client.delete("/api/v1/menus/0/submenus/0/dishes/0")
    if response.status_code == 404:
        assert response.json() == {"detail": "dish not found"}
    if response.status_code == 200:
        assert response.json() == {"status": True, "message": "The dish has been deleted"}
    print(response)