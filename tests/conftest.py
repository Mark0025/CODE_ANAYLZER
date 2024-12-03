import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from code_analyzer.models.base import Base

@pytest.fixture
async def db_session():
    """Provide test database session."""
    engine = create_engine('sqlite:///test.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
    yield session
    session.close()
    Base.metadata.drop_all(engine)
