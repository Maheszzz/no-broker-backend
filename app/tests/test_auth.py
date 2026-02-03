from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.configs.db_config import MySQLBase, get_mysql_db
from app.main import app
from app.models.user import User
from app.core.security import get_password_hash

# Use SQLite for testing to avoid touching production MySQL
# Note: This might fail if models use MySQL specific types incompatible with SQLite
# But let's try. If it fails, we will mock the repo.
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_mysql_db] = override_get_db

client = TestClient(app)

def setup_module(module):
    MySQLBase.metadata.create_all(bind=engine)

def teardown_module(module):
    MySQLBase.metadata.drop_all(bind=engine)

def test_auth_workflow():
    # 1. Signup
    signup_data = {"email": "test@example.com", "password": "password123"}
    response = client.post("/api/v1/auth/signup", json=signup_data)
    # If 400, user might already exist (if using persistent DB, but we use memory SQLite)
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"

    # 2. Login
    login_data = {"username": "test@example.com", "password": "password123"}
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None

    # 3. Access Protected Route (Create Contact)
    headers = {"Authorization": f"Bearer {token}"}
    contact_data = {
        "name": "Test User",
        "phone": "1234567890",
        "email": "test@example.com",
        "message": "Hello World"
    }
    response = client.post("/api/v1/realty/contacts", json=contact_data, headers=headers)
    assert response.status_code == 201
    created_id = response.json()["id"]

    # 4. Access Protected Route (Delete Contact)
    response = client.delete(f"/api/v1/realty/contacts/{created_id}", headers=headers)
    assert response.status_code == 204

    # 5. Access Without Token (Should Fail)
    response = client.post("/api/v1/realty/contacts", json=contact_data)
    assert response.status_code == 401
