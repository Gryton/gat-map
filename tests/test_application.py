import json
import pytest
from gat_map.application import application


@pytest.fixture
def client():
    return application.test_client()


def test_response(client):
    result = client.get()
    assert result.status_code == 200
