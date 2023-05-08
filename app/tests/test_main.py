from fastapi import status
from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_health():
    res = client.get("/")
    assert res.status_code == status.HTTP_200_OK
