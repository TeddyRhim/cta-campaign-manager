import os

os.environ["DATABASE_URL"] = "sqlite://"
os.environ["JWT_SECRET_KEY"] = "test-secret-key"
os.environ["JWT_ALGORITHM"] = "HS256"
os.environ["JWT_ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.models  # noqa: F401  (enregistre les tables)
from app.core.dependencies import get_db
from app.core.security import hash_password
from app.db.database import Base
from app.main import app
from app.models.enums import UserRole
from app.models.user import User

PASSWORD = "mot-de-passe-solide"


@pytest.fixture()
def db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine, autoflush=False)()
    yield session
    session.close()
    engine.dispose()


@pytest.fixture()
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def make_user(db, email, role=UserRole.OPERATOR):
    user = User(email=email, password_hash=hash_password(PASSWORD), role=role)
    db.add(user)
    db.commit()
    return user


def auth_headers(client, email):
    response = client.post(
        "/auth/login", json={"email": email, "password": PASSWORD}
    )
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest.fixture()
def admin_headers(client, db):
    make_user(db, "admin@example.com", UserRole.ADMIN)
    return auth_headers(client, "admin@example.com")


@pytest.fixture()
def operator_headers(client, db):
    make_user(db, "op@example.com")
    return auth_headers(client, "op@example.com")


@pytest.fixture()
def other_operator_headers(client, db):
    make_user(db, "other@example.com")
    return auth_headers(client, "other@example.com")
