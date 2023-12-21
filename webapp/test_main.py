from fastapi.testclient import TestClient
from fastapi import status
from main import app
import pytest


client = TestClient(app=app)


def test_create_user():
    response = client.get('/healthz')
    print(response.content)

    assert response.status_code == status.HTTP_200_OK
