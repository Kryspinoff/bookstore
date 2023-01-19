from app.core.config import settings
from fastapi.testclient import TestClient


def test_get_orders(client: TestClient, admin_auth_header: dict[str, str]) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/orders",
        headers=admin_auth_header
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == []
