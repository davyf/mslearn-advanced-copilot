from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_countries():
    response = client.get("/countries")
    assert response.status_code == 200
    assert sorted(response.json()) == ["England", "France", "Germany", "Italy", "Peru", "Portugal", "Spain"]


def test_region_cities_spain() -> None:
    """Return exactly the cities listed for Spain."""
    response = client.get("/regions/Spain")
    assert response.status_code == 200
    assert response.json() == ["Seville"]


def test_region_cities_unknown_region() -> None:
    """Return the agreed error for an unknown region."""
    response = client.get("/regions/Atlantis")
    assert response.status_code == 404
    assert response.json() == {"detail": "Region not found"}


def test_region_cities_post_not_allowed() -> None:
    """Reject POST requests to the GET-only city-list route."""
    response = client.post("/regions/Spain")
    assert response.status_code == 405


def test_region_cities_in_openapi() -> None:
    """Expose the city-list GET operation in the HTTP OpenAPI schema."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "get" in response.json()["paths"]["/regions/{region}"]


def test_monthly_weather_spain_january() -> None:
    """Return the exact January weather at the requested region URL."""
    response = client.get("/regions/Spain/Seville/January")
    assert response.status_code == 200
    assert response.json() == {"high": 61, "low": 41}