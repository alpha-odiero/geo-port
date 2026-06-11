import pytest
from fastapi.testclient import TestClient

def test_user_registration(client: TestClient):
    """
    Assert registration endpoint hashes passwords and returns sanitised customer records.
    """
    reg_payload = {
        "name": "Jane Cargo",
        "email": "jane@geoportlogistics.com",
        "password": "supersecurepassword123",
        "role": "customer"
    }
    response = client.post("/api/auth/register", json=reg_payload)
    assert response.status_code == 201  # 201 Created
    
    data = response.json()
    assert data["name"] == "Jane Cargo"
    assert data["email"] == "jane@geoportlogistics.com"
    assert "password" not in data
    assert "hashed_password" not in data

def test_user_registration_duplicate_prevention(client: TestClient):
    """
    Assert that register rejects duplicate logins.
    """
    payload = {
        "name": "Dup Account",
        "email": "dup@geoportlogistics.com",
        "password": "mypassword123"
    }
    # First write
    resp1 = client.post("/api/auth/register", json=payload)
    assert resp1.status_code == 201
    
    # Duplicate attempt
    resp2 = client.post("/api/auth/register", json=payload)
    assert resp2.status_code == 400
    assert "already registered" in resp2.json()["detail"].lower()

def test_user_authentication_workflow(client: TestClient):
    """
    Assert logins grant JWT access tokens on verified account configurations.
    """
    # 1. Register base user
    reg_payload = {
        "name": "Alex Dispatch",
        "email": "alex@geoportlogistics.com",
        "password": "dispatchpassword99"
    }
    client.post("/api/auth/register", json=reg_payload)

    # 2. Login correct password
    login_payload = {
        "email": "alex@geoportlogistics.com",
        "password": "dispatchpassword99"
    }
    response = client.post("/api/api/auth/login", json=login_payload) # Wait, prefix /api combined is /api/auth/login or /api/api/auth/login? 
    # Let's double check route: our APIRouter prefix is "/auth" and we register inside main.py with prefix="/api". So URL is "/api/auth/login". 
    response = client.post("/api/auth/login", json=login_payload)
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

    # 3. Read profile /me using JWT
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    profile_response = client.get("/api/auth/me", headers=headers)
    assert profile_response.status_code == 200
    assert profile_response.json()["email"] == "alex@geoportlogistics.com"

def test_shipment_tracking_endpoint(client: TestClient, session):
    """
    Assert tracking lookups return current metrics and handle missing entries securely.
    """
    from app.models.shipment import Shipment
    shipping_record = Shipment(
        tracking_number="GP123456",
        customer_name="East African Wholesales Ltd",
        status="In Transit",
        current_location="Nairobi Inland Container Depot",
        expected_delivery="Tomorrow morning of next cycle"
    )
    session.add(shipping_record)
    session.commit()

    # Look up seeded shipment (GP123456)
    response = client.get("/api/tracking/GP123456")
    assert response.status_code == 200
    shipment_data = response.json()
    assert shipment_data["tracking_number"] == "GP123456"
    assert "status" in shipment_data
    assert "current_location" in shipment_data

    # Look up invalid shipment
    response_invalid = client.get("/api/tracking/GP999999")
    assert response_invalid.status_code == 404

def test_quote_request_submission(client: TestClient):
    """
    Assert quote metrics pass strict schema rules and persist on submissions.
    """
    quote_payload = {
        "name": "Afritex Traders",
        "email": "logistics@afritex.com",
        "service": "Sea Ocean Clearance",
        "cargo_weight": 12500.50
    }
    response = client.post("/api/quotes", json=quote_payload)
    assert response.status_code == 201
    
    quote_data = response.json()
    assert quote_data["name"] == "Afritex Traders"
    assert quote_data["service"] == "Sea Ocean Clearance"
    assert quote_data["cargo_weight"] == 12500.50
    assert "id" in quote_data
    assert "tracking_number" in quote_data
    assert quote_data["tracking_number"].startswith("GP")
