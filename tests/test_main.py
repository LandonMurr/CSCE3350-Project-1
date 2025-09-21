import jwt
from fastapi.testclient import TestClient
from app.main import app
from app.settings import ALGORITHM, ISSUER
import time

client = TestClient(app)


def test_jwks_endpoint():
    """
    Tests the JWKS endpoint
    """
    response = client.get(
        "/.well-known/jwks.json"
    )  # GET request to /.well-known/jwks.json
    assert response.status_code == 200  # Check that status is 200 OK
    data = response.json()
    assert "keys" in data  # Check that "keys" was included in the response data
    assert len(data["keys"]) > 0  # Check that key(s) actually exist


def test_auth_endpoint_valid():
    """
    Tests the auth endpoint under valid condition
    """
    response = client.post("/auth")  # POST request to /auth
    assert response.status_code == 200  # Check that status is 200 OK
    token = response.text  # Store token data
    headers = jwt.get_unverified_header(token)  # Store header data
    assert "kid" in headers  # Check that key ID was included in header
    payload = jwt.decode(
        token, options={"verify_signature": False}
    )  # Store payload data
    assert payload["iss"] == ISSUER  # Check that payload has correct issuer
    assert payload["exp"] > int(time.time())  # Check that token is unexpired


def test_auth_endpoint_expired():
    """
    Tests the auth endpoint under expired condition
    """
    response = client.post("/auth?expired")  # POST request to /auth?expired
    assert response.status_code == 200  # Check that status is 200 OK
    token = response.text  # Store token data
    payload = jwt.decode(
        token, options={"verify_signature": False}
    )  # Store payload data
    assert payload["exp"] <= int(time.time())  # Confirm that token is expired


def test_no_unexpired_keys(monkeypatch):
    """
    Tests get_unexpired_keys when no such keys exist
    """

    # returns empty list (to aritificially replace list of unexpired keys)
    def mock_empty():
        return []

    monkeypatch.setattr(
        "app.main.get_unexpired_keys", mock_empty
    )  # Empties list of unexpired keys
    response = client.post("/auth")  # POST request to /auth
    assert response.status_code == 500  # Confirm server error


def test_no_expired_key(monkeypatch):
    """
    Tests get_expired_key when no such keys exist
    """

    # Returns none
    def mock_none():
        return None

    monkeypatch.setattr(
        "app.main.get_expired_key", mock_none
    )  # Clears expired key data
    response = client.post("/auth?expired")  # POST request to /auth?expired
    assert response.status_code == 500  # Confirm server error
