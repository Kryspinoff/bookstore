from fastapi.testclient import TestClient


def test_health_check(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "ok"
