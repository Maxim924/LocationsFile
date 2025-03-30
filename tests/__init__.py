from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import StaticPool
from database import get_session
from main import app
from database import Base


SQLALCHEMY_DATABASE_URL = "sqlite://"

TestingSessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False))

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal.configure(bind=engine)
Base.metadata.create_all(bind=engine)

def get_test_session():
    session = TestingSessionLocal()
    session.commit = session.flush
    try:
        yield session
    finally:
        session.rollback()
        session.close()
        TestingSessionLocal.remove()


app.dependency_overrides[get_session] = get_test_session
client = TestClient(app, base_url="http://127.0.0.1:8000")
